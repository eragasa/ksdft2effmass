#!/usr/bin/env python3
"""CLI adapter for the impurity-defect-1d-analytical-oracle run experiment operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from analytical_oracle_calculation.run_experiment import (
    AnalyticalOracleExperiment,
    ExperimentInputDeserializer,
    ParentDataLoader,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt command-line paths into the analytical-oracle experiment."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    specification = ExperimentInputDeserializer().execute(input_path.read_bytes())
    script_path = Path(__file__).resolve()
    repository_root = script_path.parents[3]
    parent = ParentDataLoader().execute(specification, repository_root)
    result = AnalyticalOracleExperiment().execute(
        specification, parent, input_path, script_path
    )
    arguments.output.resolve().write_bytes(result)


if __name__ == "__main__":
    main()
