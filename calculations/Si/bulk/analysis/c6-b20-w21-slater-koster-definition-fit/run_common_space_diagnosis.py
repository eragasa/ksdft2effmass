#!/usr/bin/env python3
"""Run the read-only CSD0/CSD1 common-space rank diagnosis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BULK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BULK))

from common_space.diagnostics import (  # noqa: E402
    DEFAULT_REQUEST,
    CommonSpaceRankDiagnosis,
    HumanReadableProgressReporter,
)


def main() -> None:
    """Parse explicit paths, run the diagnosis, and explain status on stdout."""
    parser = argparse.ArgumentParser(
        description=(
            "Authenticate the exact declared C6-B20-W21 evidence and reconstruct the "
            "blocked S110 common-space rank gate without importing its implementation. "
            "No fit or calculator is invoked."
        )
    )
    parser.add_argument(
        "--request",
        type=Path,
        default=DEFAULT_REQUEST,
        help=(
            "CSD0/CSD1 request JSON (default: exact calculation-owned unretained "
            "development request)"
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="fresh directory for result.json, the stdout transcript, and manifest.json",
    )
    arguments = parser.parse_args()
    reporter = HumanReadableProgressReporter(stream=sys.stdout)
    try:
        CommonSpaceRankDiagnosis().execute(
            request_path=arguments.request,
            output_root=arguments.output_root,
            reporter=reporter,
        )
    except Exception as error:
        reporter.line()
        reporter.line("Execution outcome: FAILED")
        reporter.line(f"Reason: {error}")
        raise


if __name__ == "__main__":
    main()
