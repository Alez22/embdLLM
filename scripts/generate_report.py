#!/usr/bin/env python3
"""Generate a standalone visual benchmark report from results/runs/.

Usage:
    python scripts/generate_report.py [--results results] [--out results/report.html]

Aggregates ALL runs per model (partial runs are unioned by case), then renders
an interactive single-file HTML report (Plotly inlined). The same rendering
lives in ``embedeval.report`` so the dashboard can embed it under /report.
"""

import argparse
from pathlib import Path

from embedeval.report import write_standalone_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results"),
                        help="results directory containing runs/ (default: results)")
    parser.add_argument("--out", type=Path, default=None,
                        help="output HTML path (default: <results>/report.html)")
    parser.add_argument("--cases", type=Path, default=Path("cases"),
                        help="case root used to count cases for coverage")
    parser.add_argument("--total-cases", type=int, default=None,
                        help="override coverage denominator "
                             "(default: all implemented cases)")
    args = parser.parse_args()

    out = args.out or (args.results / "report.html")
    path = write_standalone_report(args.results, out, args.total_cases, args.cases)
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
