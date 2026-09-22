#!/usr/bin/env python3
"""CLI adapter for the impurity-defect-1d-analytical-oracle verify result operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from analytical_oracle_calculation.verify_result import (
    AnalyticalOracleResultVerifier,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt one retained result into the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    AnalyticalOracleResultVerifier().execute(arguments.result.resolve(), root)
    print("independent verification: PASS")


if __name__ == "__main__":
    main()
