#!/usr/bin/env python3
"""CLI adapter for the impurity-defect-1d-independent-route run experiment operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from independent_route_calculation.run_experiment import (
    BaselineLoader,
    ExperimentInputDeserializer,
    IndependentRouteExperiment,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt command-line paths into the owned experiment action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    specification = ExperimentInputDeserializer().execute(input_path.read_bytes())
    root = Path(__file__).resolve().parents[3]
    baseline = BaselineLoader().execute(specification, root)
    result = IndependentRouteExperiment().execute(
        specification, baseline, input_path, Path(__file__).resolve()
    )
    arguments.output.resolve().write_bytes(result)


if __name__ == "__main__":
    main()
