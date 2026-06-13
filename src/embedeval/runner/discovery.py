"""Case discovery and filtering."""

import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from embedeval.models import (
    CaseCategory,
    CaseMetadata,
    CaseTier,
    DifficultyTier,
    Sdk,
    Visibility,
)

# Directory names under cases/ that map to SDK buckets.
_SDK_BUCKET_DIRS: frozenset[str] = frozenset(sdk.value for sdk in Sdk)

logger = logging.getLogger(__name__)


@dataclass
class Filters:
    """Filtering criteria for benchmark case selection."""

    categories: list[CaseCategory] = field(default_factory=list)
    difficulties: list[DifficultyTier] = field(default_factory=list)
    tiers: list[CaseTier] = field(default_factory=list)
    sdks: list[Sdk] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    visibility: Visibility | None = None
    # ISO date string; only include cases created after this date
    after_date: str | None = None
    case_ids: list[str] | None = None  # explicit case ID whitelist (for retest-only)


def iter_case_dirs(cases_root: Path) -> list[Path]:
    """Yield every case directory under ``cases_root`` in sorted order.

    Understands both the 2-level SDK-bucket layout
    (``cases/<sdk>/<case-id>/``) and, transitionally, the 1-level flat
    layout. A directory counts as a case dir if it contains a
    ``metadata.yaml``. Used by migration/audit scripts that iterate raw
    paths rather than going through ``discover_cases`` (which parses
    metadata and would drop malformed entries).
    """
    if not cases_root.is_dir():
        return []
    out: list[Path] = []
    for entry in sorted(cases_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in _SDK_BUCKET_DIRS:
            for case_dir in sorted(entry.iterdir()):
                if case_dir.is_dir() and (case_dir / "metadata.yaml").is_file():
                    out.append(case_dir)
        elif (entry / "metadata.yaml").is_file():
            out.append(entry)
    return out


def load_case_metadata(case_dir: Path) -> CaseMetadata | None:
    """Load case metadata from a case directory's metadata.yaml.

    Args:
        case_dir: Path to the case directory.

    Returns:
        CaseMetadata if valid, None if metadata is missing or invalid.
    """
    metadata_file = case_dir / "metadata.yaml"
    if not metadata_file.is_file():
        logger.warning("No metadata.yaml in %s", case_dir)
        return None

    try:
        raw = yaml.safe_load(metadata_file.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            logger.warning("Invalid metadata format in %s", case_dir)
            return None
        return CaseMetadata(**raw)
    except Exception as exc:
        logger.warning("Failed to parse metadata in %s: %s", case_dir, exc)
        return None


def discover_cases(cases_dir: Path) -> list[tuple[Path, CaseMetadata]]:
    """Discover all valid case directories under cases_dir.

    Expected layout: ``cases/<sdk>/<case-id>/metadata.yaml`` (2 levels).
    During the SDK-bucket migration transition we also accept the legacy
    1-level layout ``cases/<case-id>/metadata.yaml`` and emit a warning so
    stragglers surface at runtime.

    Args:
        cases_dir: Root directory containing SDK bucket subdirectories.

    Returns:
        List of (case_dir, metadata) tuples for valid cases.
    """
    if not cases_dir.is_dir():
        logger.warning("Cases directory does not exist: %s", cases_dir)
        return []

    cases: list[tuple[Path, CaseMetadata]] = []
    for entry in sorted(cases_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in _SDK_BUCKET_DIRS:
            # SDK bucket — descend one level.
            for case_dir in sorted(entry.iterdir()):
                if not case_dir.is_dir():
                    continue
                metadata = load_case_metadata(case_dir)
                if metadata is not None:
                    cases.append((case_dir, metadata))
        elif (entry / "metadata.yaml").is_file():
            # Legacy flat layout — warn but still load.
            logger.warning(
                "Case %s found at legacy flat location; expected cases/<sdk>/%s/",
                entry,
                entry.name,
            )
            metadata = load_case_metadata(entry)
            if metadata is not None:
                cases.append((entry, metadata))

    logger.info("Discovered %d cases in %s", len(cases), cases_dir)
    return cases


def filter_cases(
    cases: list[tuple[Path, CaseMetadata]],
    filters: Filters,
) -> list[tuple[Path, CaseMetadata]]:
    """Filter cases by category, difficulty, and tags.

    Args:
        cases: List of (case_dir, metadata) tuples.
        filters: Filtering criteria.

    Returns:
        Filtered list of cases.
    """
    filtered: list[tuple[Path, CaseMetadata]] = []
    for case_dir, meta in cases:
        if filters.case_ids is not None and meta.id not in filters.case_ids:
            continue
        if filters.categories and meta.category not in filters.categories:
            continue
        if filters.difficulties and meta.difficulty not in filters.difficulties:
            continue
        if filters.tiers and meta.tier not in filters.tiers:
            continue
        if filters.sdks and meta.sdk not in filters.sdks:
            continue
        if filters.tags and not any(tag in meta.tags for tag in filters.tags):
            continue
        if filters.visibility is not None and meta.visibility != filters.visibility:
            continue
        if filters.after_date and meta.created_date:
            try:
                from datetime import date as _date

                _date.fromisoformat(filters.after_date)
                _date.fromisoformat(meta.created_date)
            except ValueError:
                pass  # skip filter on invalid format
            else:
                if meta.created_date <= filters.after_date:
                    continue
        filtered.append((case_dir, meta))

    logger.info(
        "Filtered %d -> %d cases",
        len(cases),
        len(filtered),
    )
    return filtered
