#!/usr/bin/env python3
"""Run the public particle-in-a-box identifiability Workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxIdentifiabilityWorkflow,
)


def main() -> int:
    """Adapt command-line paths to the public identifiability Workflow."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--retained-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    script_path = Path(__file__).resolve()
    arguments.output.write_bytes(
        ParticleInBoxIdentifiabilityWorkflow().execute(
            arguments.input.resolve(),
            arguments.retained_result.resolve(),
            script_path,
            script_path.parents[3],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
