#!/usr/bin/env python3
"""CLI adapter for the impurity-spin-spaces run experiment operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from spin_spaces_calculation.run_experiment import (
    SpinSpaceEmbeddingExperiment,
    SpinSpaceInputDeserializer,
)


def main() -> None:
    """Adapt command-line values to calculation-owned objects."""

    """Adapt command-line paths into the owned experiment action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    output_path = arguments.output.resolve()
    specification = SpinSpaceInputDeserializer().execute(input_path.read_bytes())
    output_path.write_bytes(
        SpinSpaceEmbeddingExperiment().execute(
            specification, input_path, Path(__file__).resolve()
        )
    )


if __name__ == "__main__":
    main()
