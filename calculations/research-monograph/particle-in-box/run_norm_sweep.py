#!/usr/bin/env python3
"""Run the public particle-in-a-box multi-norm Workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxNormSweepWorkflow,
)


def main() -> int:
    """Adapt command-line paths to the public multi-norm Workflow."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    script_path = Path(__file__).resolve()
    arguments.output.write_bytes(
        ParticleInBoxNormSweepWorkflow().execute(
            arguments.input.resolve(), script_path, script_path.parents[3]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
