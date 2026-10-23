#!/usr/bin/env python3
"""Run the reusable Hamiltonian decomposition on the declared PIAB1D inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import numpy as np
from ksdft2effmass.hamiltonian import HamiltonianDecomposition
from ksdft2effmass.linalg import (
    RealMatrixQuantity,
    Unitless,
)
from ksdft2effmass.model_systems.piab1d import (
    Piab1dResidualStudyEvaluator,
    Piab1dStudyInputDeserializer,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
    """Return one JSON object with built-in string keys."""
    if not isinstance(value, dict) or not all(type(key) is str for key in value):
        raise TypeError(f"{name} must be a JSON object")
    return value


def real(value: JsonValue, name: str) -> float:
    """Return one finite JSON real excluding Booleans."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a JSON number")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def integer(value: JsonValue, name: str) -> int:
    """Return one built-in JSON integer excluding Booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be a JSON integer")
    return value


def declared_shift(
    value: JsonValue, dimension: int
) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
    """Construct the declared symmetric shift without PIAB1D dimension constants."""
    declaration = mapping(value, "alternative_decomposition_shift")
    diagonal_value = declaration.get("diagonal")
    if not isinstance(diagonal_value, list):
        raise TypeError("shift diagonal must be a JSON array")
    diagonal = np.asarray(diagonal_value, dtype=np.float64)
    if diagonal.shape != (dimension,) or not np.all(np.isfinite(diagonal)):
        raise ValueError("shift diagonal must match the retained dimension")
    result = np.diag(diagonal)
    upper = declaration.get("upper_triangle")
    if not isinstance(upper, list):
        raise TypeError("upper_triangle must be a JSON array")
    for raw_entry in upper:
        entry = mapping(raw_entry, "upper-triangle shift entry")
        row = integer(entry.get("row"), "row")
        column = integer(entry.get("column"), "column")
        entry_value = real(entry.get("value"), "value")
        if row < 0 or row >= column or column >= dimension:
            raise ValueError("invalid upper-triangle shift entry")
        result[row, column] = entry_value
        result[column, row] = entry_value
    return result


def main() -> int:
    """Evaluate PIAB1D and invoke the reusable decomposition directly."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--study-input", type=Path, required=True)
    parser.add_argument("--decomposition-input", type=Path, required=True)
    parser.add_argument("--figure-output", type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.figure_output.exists():
        raise FileExistsError(f"refusing to overwrite {arguments.figure_output}")

    definition = Piab1dStudyInputDeserializer().execute(
        arguments.study_input.read_bytes()
    )
    study_result = Piab1dResidualStudyEvaluator().execute(definition)
    input_payload = mapping(
        cast(
            JsonValue,
            json.loads(arguments.decomposition_input.read_text(encoding="utf-8")),
        ),
        "decomposition input",
    )
    shift = declared_shift(
        input_payload.get("alternative_decomposition_shift"),
        study_result.definition.N_retained_eigenpairs,
    )

    decomposition = HamiltonianDecomposition(
        study_result.reduced_hamiltonian,
        RealMatrixQuantity(shift, Unitless()),
    )
    calculation = decomposition.run()
    verification = decomposition.verify(calculation)
    if not verification.passed:
        raise ValueError("; ".join(verification.issues))
    visualization = decomposition.visualize(calculation, verification)
    arguments.figure_output.write_bytes(visualization.png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
