#!/usr/bin/env python3
"""Verify a particle-in-a-box higher-eigenpair result."""

from __future__ import annotations

import argparse
from pathlib import Path

from analysis.verification import Piab1dEigenpairSweepVerifier


def main() -> int:
    """Adapt one result path to the independent public verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    Piab1dEigenpairSweepVerifier().execute(arguments.result.resolve())
    print("particle-in-box higher eigenpair sweep: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
