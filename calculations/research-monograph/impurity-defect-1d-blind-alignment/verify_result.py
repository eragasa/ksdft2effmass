#!/usr/bin/env python3
"""CLI adapter for the impurity-defect-1d-blind-alignment verify result operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from blind_alignment_calculation.verify_result import (
    BlindAlignmentResultVerifier,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt one result path into the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    BlindAlignmentResultVerifier().execute(arguments.result.resolve(), repository_root)
    print("independent verification: PASS")


if __name__ == "__main__":
    main()
