#!/usr/bin/env python3
"""CLI adapter for the impurity-spin-spaces verify result operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from spin_spaces_calculation.verify_result import (
    SpinSpaceResultVerifier,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt one result path into the owned verification action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    result_path = arguments.result.resolve()
    repository_root = Path(__file__).resolve().parents[3]
    SpinSpaceResultVerifier().execute(result_path, repository_root)
    print("impurity spin-space embedding result: PASS")


if __name__ == "__main__":
    main()
