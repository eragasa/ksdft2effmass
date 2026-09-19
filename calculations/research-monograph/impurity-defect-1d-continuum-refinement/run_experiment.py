#!/usr/bin/env python3
"""CLI adapter for the continuum-refinement experiment."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from continuum_refinement_calculation.run_experiment import (
    ContinuumRefinementWorkflow,
)


def main() -> None:
    """Adapt command-line paths to the continuum-refinement Workflow."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    ContinuumRefinementWorkflow().execute(
        cast(Path, arguments.input).resolve(),
        cast(Path, arguments.output).resolve(),
    )


if __name__ == "__main__":
    main()
