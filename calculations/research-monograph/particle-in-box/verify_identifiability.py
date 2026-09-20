#!/usr/bin/env python3
"""Verify a particle-in-a-box retained-space identifiability result."""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxIdentifiabilityVerifier,
)


def main() -> int:
    """Adapt one result path to the independent public verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    ParticleInBoxIdentifiabilityVerifier().execute(arguments.result.resolve())
    print("particle-in-box identifiability demonstration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
