#!/usr/bin/env python3
"""Run the retained-space identifiability demonstration from Appendix D."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

RealMatrix = npt.NDArray[np.float64]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _matrix(value: object, name: str) -> RealMatrix:
    matrix = np.asarray(value, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must contain finite entries")
    return matrix


def _frobenius(matrix: RealMatrix) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def _build_shift(payload: dict[str, Any], dimension: int) -> RealMatrix:
    declaration = payload["alternative_decomposition_shift"]
    diagonal = np.asarray(declaration["diagonal"], dtype=np.float64)
    if diagonal.shape != (dimension,) or not np.all(np.isfinite(diagonal)):
        raise ValueError("shift diagonal must match the retained dimension")
    shift = np.diag(diagonal)
    for entry in declaration["upper_triangle"]:
        row = entry["row"]
        column = entry["column"]
        value = entry["value"]
        if (
            isinstance(row, bool)
            or not isinstance(row, int)
            or isinstance(column, bool)
            or not isinstance(column, int)
            or row < 0
            or row >= column
            or column >= dimension
            or isinstance(value, bool)
            or not isinstance(value, int | float)
            or not np.isfinite(float(value))
        ):
            raise ValueError("invalid upper-triangle shift entry")
        shift[row, column] = float(value)
        shift[column, row] = float(value)
    return shift


def _fit_model_classes(target: RealMatrix) -> dict[str, dict[str, Any]]:
    dimension = target.shape[0]
    scalar = np.eye(dimension) * float(np.trace(target) / dimension)
    diagonal = np.diag(np.diag(target))
    rows, columns = np.indices(target.shape)
    tridiagonal = np.where(np.abs(rows - columns) <= 1, target, 0.0)
    candidates = {
        "scalar_identity": scalar,
        "diagonal_in_retained_basis": diagonal,
        "real_symmetric_tridiagonal": tridiagonal,
        "arbitrary_real_symmetric": target.copy(),
    }
    return {
        name: {
            "best_fit": candidate.tolist(),
            "unexplained_residual": (target - candidate).tolist(),
            "unexplained_frobenius_norm": _frobenius(target - candidate),
        }
        for name, candidate in candidates.items()
    }


def run(
    input_path: Path, retained_result_path: Path, script_path: Path
) -> dict[str, Any]:
    """Execute the declared decomposition and model-class demonstration."""
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported identifiability input schema version")
    if payload.get("evidence_status") != "illustrative numerical experiment":
        raise ValueError("incorrect evidence status")
    expected_classes = [
        "scalar_identity",
        "diagonal_in_retained_basis",
        "real_symmetric_tridiagonal",
        "arbitrary_real_symmetric",
    ]
    if payload.get("admissible_model_classes") != expected_classes:
        raise ValueError("unsupported model-class declaration")

    retained_payload = json.loads(retained_result_path.read_text(encoding="utf-8"))
    reduced_hamiltonian = _matrix(
        retained_payload["matrices"]["retained_hamiltonian_coordinates"],
        "retained Hamiltonian",
    )
    dimension = reduced_hamiltonian.shape[0]
    shift = _build_shift(payload, dimension)

    physical_kinetic = reduced_hamiltonian.copy()
    physical_potential = np.zeros_like(reduced_hamiltonian)
    alternative_kinetic = reduced_hamiltonian - shift
    alternative_potential = shift.copy()

    decompositions = {
        "consistently_reduced_dirichlet": {
            "kinetic": physical_kinetic.tolist(),
            "potential": physical_potential.tolist(),
            "reconstruction_frobenius_error": _frobenius(
                reduced_hamiltonian - physical_kinetic - physical_potential
            ),
            "interpretation": (
                "physical box decomposition under the declared "
                "Dirichlet realization"
            ),
        },
        "illustratively_shifted": {
            "kinetic": alternative_kinetic.tolist(),
            "potential": alternative_potential.tolist(),
            "reconstruction_frobenius_error": _frobenius(
                reduced_hamiltonian - alternative_kinetic - alternative_potential
            ),
            "interpretation": (
                "algebraically valid alternative, not a physical assignment"
            ),
        },
    }

    repository_root = script_path.parents[3]
    return {
        "schema_version": 1,
        "experiment_id": payload["experiment_id"],
        "evidence_status": payload["evidence_status"],
        "calculation_status": "calculated illustrative result",
        "input": payload,
        "retained_space": {
            "identifier": "lowest discrete spectral coordinates",
            "dimension": dimension,
            "reduced_hamiltonian": reduced_hamiltonian.tolist(),
        },
        "decompositions": decompositions,
        "illustrative_shift": shift.tolist(),
        "model_class_fits": _fit_model_classes(shift),
        "provenance": {
            "input_path": input_path.relative_to(repository_root).as_posix(),
            "input_sha256": _sha256(input_path),
            "retained_result_path": retained_result_path.relative_to(
                repository_root
            ).as_posix(),
            "retained_result_sha256": _sha256(retained_result_path),
            "script_path": script_path.relative_to(repository_root).as_posix(),
            "script_sha256": _sha256(script_path),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
        },
        "limitations": [
            "The alternative shift is illustrative and has no physical assignment.",
            (
                "Model-class fits depend on the declared retained basis and "
                "Frobenius metric."
            ),
            "Algebraic reconstructability does not establish physical identifiability.",
            "The result is not semiconductor evidence or scientific validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--retained-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.input.resolve(),
        args.retained_result.resolve(),
        Path(__file__).resolve(),
    )
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
