#!/usr/bin/env python3
"""CLI adapter for the defect-1D verify result operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from impurity_defect_1d_calculation.verify_result import (
    DefectResultVerifier,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt one result path into the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    DefectResultVerifier().execute(arguments.result.resolve(), repository_root)
    print("independent verification: PASS")


if __name__ == "__main__":
    main()
