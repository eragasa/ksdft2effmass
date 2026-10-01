#!/usr/bin/env python3
"""Verify a particle-in-a-box retained-space identifiability result."""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.piab1d import Piab1dIdentifiabilityResultsVerifier


def main() -> int:
    """Adapt one result path to the independent public verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    report = Piab1dIdentifiabilityResultsVerifier().execute(
        arguments.result.resolve(), repository_root
    )
    source_status = "PASS" if report.source_authentication.passes else "FAIL"
    numerical_status = "PASS" if report.numerical_reconstruction.passes else "FAIL"
    print(f"source authentication: {source_status}")
    print(f"numerical reconstruction: {numerical_status}")
    return 0 if report.passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
