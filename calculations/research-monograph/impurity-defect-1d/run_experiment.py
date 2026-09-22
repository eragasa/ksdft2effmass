#!/usr/bin/env python3
"""CLI adapter for the defect-1D run experiment operation."""

from __future__ import annotations

import argparse
from pathlib import Path

from impurity_defect_1d_calculation.records import (
    DefectExerciseInputDeserializer,
    ParentDataLoader,
)
from impurity_defect_1d_calculation.workflows import (
    MatchedDefectExtractionExperiment,
)


def main() -> None:
    """Adapt command-line paths into the owned experiment Workflow."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    output_path = arguments.output.resolve()
    specification = DefectExerciseInputDeserializer().execute(input_path.read_bytes())
    repository_root = Path(__file__).resolve().parents[3]
    parent = ParentDataLoader().execute(specification.parent, repository_root)
    output_path.write_bytes(
        MatchedDefectExtractionExperiment().execute(
            specification, parent, input_path, Path(__file__).resolve()
        )
    )


if __name__ == "__main__":
    main()
