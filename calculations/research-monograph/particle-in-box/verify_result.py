#!/usr/bin/env python3
"""CLI adapter for independent particle-in-a-box result verification."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph import ParticleInBoxResultVerifier


def main() -> None:
    """Adapt one retained-result path to the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result_path = cast(Path, args.result).resolve()
    repository_root = Path(__file__).resolve().parents[3]
    ParticleInBoxResultVerifier().execute(result_path, repository_root)
    print("particle-in-box retained result: PASS")


if __name__ == "__main__":
    main()
