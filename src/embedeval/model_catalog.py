"""Dynamic model catalog for the New Run TUI form.

Fetches the list of available models live from the provider APIs
(OpenRouter and Groq), caches the result on disk, and falls back to a
static preset list when the network or the API keys are unavailable.

Design notes / hidden costs:
- Network calls block. Callers in the TUI must run :func:`fetch_models`
  in a worker thread, never on the UI thread.
- The cache file lives under ``results/`` and is git-ignored.
- Groq does not expose pricing, so :attr:`ModelInfo.price_per_mtok` is
  ``None`` for Groq models; the free/paid filter treats them as unknown
  (shown in both views).
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import requests

# Cache lives next to the other results artifacts; git-ignored.
_CACHE_FILE = Path("results") / ".model_catalog_cache.json"
_CACHE_TTL_SECONDS = 24 * 60 * 60  # 24h

_OPENROUTER_URL = "https://openrouter.ai/api/v1/models"
_GROQ_URL = "https://api.groq.com/openai/v1/models"
_HTTP_TIMEOUT = 10  # seconds per request

# Static fallback used when the network or API keys are unavailable.
# Verified available via the provider APIs (2026-06-07).
_PRESET_MODELS: list[str] = [
    "groq/llama-3.3-70b-versatile",
    "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    "groq/qwen/qwen3-32b",
    "groq/openai/gpt-oss-20b",
    "groq/openai/gpt-oss-120b",
    "openrouter/deepseek/deepseek-r1-0528",
    "openrouter/deepseek/deepseek-chat-v3-0324",
    "openrouter/deepseek/deepseek-v4-flash",
    "openrouter/meta-llama/llama-4-maverick",
    "openrouter/meta-llama/llama-3.3-70b-instruct",
    "openrouter/qwen/qwen3-235b-a22b",
    "openrouter/qwen/qwen3-30b-a3b",
    "openrouter/google/gemini-2.5-flash",
    "openrouter/google/gemini-2.5-pro",
    "openrouter/mistralai/mistral-small-3.2-24b-instruct",
]


@dataclass(frozen=True)
class ModelInfo:
    """A single model offered by a provider.

    :param slug: Full model slug usable by the runner (e.g.
        ``openrouter/anthropic/claude-opus-4``).
    :param provider: Top-level provider name (e.g. ``openrouter``, ``groq``).
    :param sub_provider: Vendor inside the provider catalog (e.g.
        ``anthropic``, ``qwen``); used for the dynamic provider filter.
    :param price_per_mtok: Combined prompt+completion price per million
        tokens in USD, or ``None`` when unknown (Groq).
    :param price_in_per_mtok: Prompt price per million tokens (USD), or
        ``None`` when unknown. Used for real cost tracking of runs.
    :param price_out_per_mtok: Completion price per million tokens (USD),
        or ``None`` when unknown.
    """

    slug: str
    provider: str
    sub_provider: str
    price_per_mtok: float | None
    price_in_per_mtok: float | None = None
    price_out_per_mtok: float | None = None

    @property
    def is_free(self) -> bool:
        """True only when pricing is known and zero."""
        return self.price_per_mtok == 0.0


def _api_key(name: str) -> str | None:
    """Return an API key from the environment, falling back to .env.

    Mirrors the TUI's manual .env parsing so the catalog uses the same
    credentials as the run subprocess without importing python-dotenv.
    """
    value = os.environ.get(name)
    if value:
        return value
    dot_env = Path(".env")
    if not dot_env.is_file():
        return None
    for line in dot_env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        if key.strip() == name:
            return val.strip()
    return None


def _preset_catalog() -> list[ModelInfo]:
    """Build ModelInfo objects from the static preset slugs (no pricing)."""
    catalog: list[ModelInfo] = []
    for slug in _PRESET_MODELS:
        parts = slug.split("/")
        provider = parts[0]
        sub_provider = parts[1] if len(parts) > 2 else provider
        catalog.append(ModelInfo(slug, provider, sub_provider, None))
    return catalog


def _fetch_openrouter() -> list[ModelInfo]:
    """Fetch the OpenRouter model list. Returns [] on any failure."""
    key = _api_key("OPENROUTER_API_KEY")
    if not key:
        return []
    headers = {"Authorization": f"Bearer {key}"}
    try:
        resp = requests.get(_OPENROUTER_URL, headers=headers, timeout=_HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except (requests.RequestException, ValueError):
        return []

    catalog: list[ModelInfo] = []
    for entry in data:
        model_id = entry.get("id")
        if not model_id:
            continue
        # The benchmark only sends and receives text: drop music/image/video
        # and vision-input models (lyria, *-vl, ...) that clutter the picker.
        # Entries without modality info are kept (fail open).
        if not _is_text_to_text(entry.get("architecture")):
            continue
        # OpenRouter ids look like "anthropic/claude-opus-4".
        sub_provider = model_id.split("/")[0]
        price_in, price_out = _openrouter_price_split(entry.get("pricing"))
        catalog.append(
            ModelInfo(
                slug=f"openrouter/{model_id}",
                provider="openrouter",
                sub_provider=sub_provider,
                price_per_mtok=_openrouter_price(entry.get("pricing")),
                price_in_per_mtok=price_in,
                price_out_per_mtok=price_out,
            )
        )
    return catalog


def _is_text_to_text(architecture: dict | None) -> bool:
    """True when the model consumes and produces only text.

    OpenRouter reports ``architecture.modality`` as e.g. ``text->text`` or
    ``text+image->text``. Missing/unparsable info counts as text-to-text so
    an API change never empties the catalog.
    """
    if not architecture:
        return True
    modality = architecture.get("modality")
    if not isinstance(modality, str) or "->" not in modality:
        return True
    inputs, _, outputs = modality.partition("->")
    return inputs.strip() == "text" and outputs.strip() == "text"


def _openrouter_price(pricing: dict | None) -> float | None:
    """Combine prompt+completion per-token price into USD per million tokens.

    OpenRouter prices are strings in USD per token. Returns ``None`` when
    pricing is missing or unparsable.
    """
    if not pricing:
        return None
    try:
        prompt = float(pricing.get("prompt", 0) or 0)
        completion = float(pricing.get("completion", 0) or 0)
    except (TypeError, ValueError):
        return None
    # OpenRouter uses negative sentinels (e.g. -1) for variable-priced
    # entries like the "auto" router; treat those as unknown, not free.
    if prompt < 0 or completion < 0:
        return None
    return (prompt + completion) * 1_000_000


def _openrouter_price_split(pricing: dict | None) -> tuple[float | None, float | None]:
    """Return (prompt, completion) prices in USD per million tokens.

    Same parsing rules as :func:`_openrouter_price`; negative sentinels
    mean variable pricing and are treated as unknown.
    """
    if not pricing:
        return None, None
    try:
        prompt = float(pricing.get("prompt", 0) or 0)
        completion = float(pricing.get("completion", 0) or 0)
    except (TypeError, ValueError):
        return None, None
    if prompt < 0 or completion < 0:
        return None, None
    return prompt * 1_000_000, completion * 1_000_000


def estimate_cost_usd(model_slug: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate the USD cost of one call from catalog pricing.

    Fallback for providers litellm cannot price (e.g. ``openrouter/...``
    slugs). Returns 0.0 when the model or its pricing is unknown, so the
    caller can keep litellm's value when this fails.

    .. warning:: May perform blocking network I/O on a cold catalog cache.
    """
    for info in fetch_models():
        if info.slug == model_slug:
            if info.price_in_per_mtok is None or info.price_out_per_mtok is None:
                return 0.0
            return (
                input_tokens * info.price_in_per_mtok
                + output_tokens * info.price_out_per_mtok
            ) / 1_000_000
    return 0.0


def _fetch_groq() -> list[ModelInfo]:
    """Fetch the Groq model list. Returns [] on any failure.

    Groq exposes no pricing, so price_per_mtok stays None.
    """
    key = _api_key("GROQ_API_KEY")
    if not key:
        return []
    headers = {"Authorization": f"Bearer {key}"}
    try:
        resp = requests.get(_GROQ_URL, headers=headers, timeout=_HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except (requests.RequestException, ValueError):
        return []

    catalog: list[ModelInfo] = []
    for entry in data:
        model_id = entry.get("id")
        if not model_id:
            continue
        # Groq exposes no modality info, so filter the known non-chat
        # families by name (speech-to-text, TTS, moderation models).
        lowered = model_id.lower()
        if any(t in lowered for t in ("whisper", "tts", "guard")):
            continue
        # Groq ids may be flat ("llama-3.3-70b-versatile") or vendored
        # ("meta-llama/llama-4-scout"). Derive the sub-provider accordingly.
        sub_provider = model_id.split("/")[0] if "/" in model_id else "groq"
        catalog.append(
            ModelInfo(
                slug=f"groq/{model_id}",
                provider="groq",
                sub_provider=sub_provider,
                price_per_mtok=None,
            )
        )
    return catalog


def _read_cache() -> list[ModelInfo] | None:
    """Return cached catalog if present and fresh, else None."""
    if not _CACHE_FILE.is_file():
        return None
    try:
        raw = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if time.time() - raw.get("fetched_at", 0) > _CACHE_TTL_SECONDS:
        return None
    return [ModelInfo(**m) for m in raw.get("models", [])]


def _write_cache(models: list[ModelInfo]) -> None:
    """Persist the catalog to the cache file (best effort)."""
    payload = {
        "fetched_at": time.time(),
        "models": [asdict(m) for m in models],
    }
    try:
        _CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        pass  # Cache is an optimization; failure is non-fatal.


def fetch_models(force_refresh: bool = False) -> list[ModelInfo]:
    """Return the available model catalog, sorted by slug.

    Order of preference:
    1. Fresh on-disk cache (unless ``force_refresh``).
    2. Live API fetch (OpenRouter + Groq), then cached.
    3. Static preset fallback (never cached).

    :param force_refresh: Skip the cache and hit the APIs.
    :return: Models sorted by slug. Never empty (preset fallback).

    .. warning:: Performs blocking network I/O. Call from a worker thread.
    """
    if not force_refresh:
        cached = _read_cache()
        if cached:
            return sorted(cached, key=lambda m: m.slug)

    live = _fetch_openrouter() + _fetch_groq()
    if live:
        _write_cache(live)
        return sorted(live, key=lambda m: m.slug)

    # Network/keys unavailable — degrade gracefully, do not cache.
    return sorted(_preset_catalog(), key=lambda m: m.slug)
