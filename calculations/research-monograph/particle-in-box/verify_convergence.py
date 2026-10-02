#!/usr/bin/env python3
"""Verify a particle-in-a-box grid-convergence result."""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.piab1d import (
    Piab1dConvergenceResultsVerifier,
)


def main() -> int:
    """Adapt one result path to the independent public verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    report = Piab1dConvergenceResultsVerifier().execute(
        arguments.result.resolve(), repository_root
    )
    if not report.passes:
        print(
            "particle-in-box convergence series: FAIL "
            f"(source_authentication={report.source_authentication.passes}, "
            f"numerical_reconstruction={report.numerical_reconstruction.passes})"
        )
        return 1
    print("particle-in-box convergence series: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
