#!/usr/bin/env python3
"""Backfill token_usage in historical result details from the generation corpus.

Cached results written before the corpus-hit token fix reported 0 tokens even
though the generation corpus cell stored the real values. This script repairs
those details/*.json in-place by looking up the matching corpus cell on
(model, case_id, attempt) and copying input/output tokens (and cost, if the
detail also has 0 cost).

It is conservative: a detail is only touched when its output_tokens == 0, its
generated_code is non-empty, and a corpus cell with non-zero output_tokens
exists for the same (model, case_id, attempt). Mock results are skipped.

Usage:
    uv run python scripts/backfill_token_usage.py            # dry-run, report only
    uv run python scripts/backfill_token_usage.py --apply    # write changes
"""

import argparse
import json
from pathlib import Path

RESULTS_DIR = Path("results")
CORPUS_DIR = RESULTS_DIR / "corpus" / "generations"


def _cell_path(model: str, case_id: str, attempt: int) -> Path:
    """Mirror corpus._cell_path so we resolve the same file the runner wrote."""
    model_slug = model.replace("/", "_").replace(":", "_")
    return CORPUS_DIR / model_slug / case_id / f"{attempt}.json"


def _load_cell(model: str, case_id: str, attempt: int) -> dict | None:
    path = _cell_path(model, case_id, attempt)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes. Without it the script only reports what it would do.",
    )
    args = parser.parse_args()

    detail_files = sorted(RESULTS_DIR.glob("runs/*/details/*.json"))
    repaired = skipped_no_cell = scanned = permission_denied = 0

    for path in detail_files:
        try:
            detail = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        scanned += 1

        model = detail.get("model", "")
        if not model or model == "mock":
            continue
        if not detail.get("generated_code", "").strip():
            continue
        tu = detail.get("token_usage") or {}
        if tu.get("output_tokens", 0) != 0:
            continue  # already has tokens — leave it untouched

        cell = _load_cell(model, detail.get("case_id", ""), detail.get("attempt", 0))
        if cell is None or cell.get("output_tokens", 0) == 0:
            skipped_no_cell += 1
            continue

        in_tok = cell.get("input_tokens", 0)
        out_tok = cell.get("output_tokens", 0)
        detail["token_usage"] = {
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
        }
        # Only fill cost if the detail had none; never overwrite a real cost.
        if detail.get("cost_usd", 0.0) == 0.0 and cell.get("cost_usd", 0.0) > 0.0:
            detail["cost_usd"] = cell["cost_usd"]

        if args.apply:
            try:
                path.write_text(
                    json.dumps(detail, indent=2) + "\n", encoding="utf-8"
                )
            except PermissionError:
                # Some result files are owned by root (written by the Docker
                # container via sudo). Skip them; re-run this script with sudo.
                permission_denied += 1
                continue
        repaired += 1

    mode = "Applied" if args.apply else "Would repair (dry-run)"
    print(f"Scanned {scanned} detail files.")
    print(f"{mode}: {repaired} details backfilled from corpus.")
    print(f"Skipped (no matching corpus cell with tokens): {skipped_no_cell}.")
    if permission_denied:
        print(
            f"Skipped (permission denied, root-owned): {permission_denied}. "
            "Re-run with: sudo $(which uv) run python scripts/backfill_token_usage.py --apply"
        )
    if not args.apply and repaired:
        print("\nRe-run with --apply to write changes.")


if __name__ == "__main__":
    main()
