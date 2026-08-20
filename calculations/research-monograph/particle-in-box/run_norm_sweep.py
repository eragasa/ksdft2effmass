#!/usr/bin/env python3
"""Run multi-norm residual diagnostics for the particle-in-a-box experiment."""

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


def _hamiltonian(points: int, length: float, mass: float, hbar: float) -> RealMatrix:
    spacing = length / (points + 1)
    prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
    matrix = np.diag(np.full(points, 2.0 * prefactor))
    matrix += np.diag(np.full(points - 1, -prefactor), 1)
    matrix += np.diag(np.full(points - 1, -prefactor), -1)
    return matrix


def _cyclic_reference(
    points: int, length: float, mass: float, hbar: float
) -> RealMatrix:
    matrix = _hamiltonian(points, length, mass, hbar)
    spacing = length / (points + 1)
    prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
    matrix[0, -1] = -prefactor
    matrix[-1, 0] = -prefactor
    return matrix


def _positive_real(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a positive JSON number")
    result = float(value)
    if not np.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _integer_list(value: object, name: str) -> list[int]:
    if not isinstance(value, list) or not value:
        raise TypeError(f"{name} must be a nonempty JSON array")
    if any(isinstance(item, bool) or not isinstance(item, int) for item in value):
        raise TypeError(f"{name} entries must be integers")
    result = list(value)
    if any(item <= 0 for item in result):
        raise ValueError(f"{name} entries must be positive")
    if result != sorted(set(result)):
        raise ValueError(f"{name} must be strictly increasing")
    return result


def _matrix_norms(matrix: RealMatrix) -> dict[str, float]:
    return {
        "frobenius": float(np.linalg.norm(matrix, ord="fro")),
        "spectral": float(np.linalg.norm(matrix, ord=2)),
        "maximum_entry": float(np.max(np.abs(matrix))),
    }


def _normalized(
    numerator: dict[str, float], denominator: dict[str, float]
) -> dict[str, float]:
    return {name: value / denominator[name] for name, value in numerator.items()}


def run(input_path: Path, script_path: Path) -> dict[str, Any]:
    """Execute the declared residual and algebraic multi-norm sweep."""
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported norm-sweep input schema version")
    if payload.get("evidence_status") != "illustrative numerical experiment":
        raise ValueError("incorrect evidence status")
    if payload.get("norms") != ["frobenius", "spectral", "maximum_entry"]:
        raise ValueError("unsupported norm declaration")

    parameters = payload["dimensionless_parameters"]
    length = _positive_real(parameters.get("length"), "length")
    mass = _positive_real(parameters.get("mass"), "mass")
    hbar = _positive_real(parameters.get("hbar"), "hbar")
    series = payload["grid_series"]
    point_counts = _integer_list(series.get("interior_points"), "interior_points")
    retained = series.get("retained_dimension")
    if isinstance(retained, bool) or not isinstance(retained, int) or retained <= 0:
        raise TypeError("retained_dimension must be a positive integer")
    if retained > min(point_counts):
        raise ValueError("retained_dimension must exist on every grid")

    grids: list[dict[str, Any]] = []
    for points in point_counts:
        spacing = length / (points + 1)
        hamiltonian = _hamiltonian(points, length, mass, hbar)
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
        retained_vectors = eigenvectors[:, :retained]
        projector = retained_vectors @ retained_vectors.T
        embedded = projector @ hamiltonian @ projector
        consistent = embedded - projector @ hamiltonian.copy() @ projector
        unmatched = embedded - hamiltonian
        boundary = hamiltonian - _cyclic_reference(points, length, mass, hbar)
        algebraic = (
            hamiltonian @ eigenvectors - eigenvectors * eigenvalues[np.newaxis, :]
        )

        reference_norms = _matrix_norms(hamiltonian)
        residuals: dict[str, dict[str, dict[str, float]]] = {}
        for name, matrix in {
            "consistent_compression": consistent,
            "unmatched_compression": unmatched,
            "boundary_realization": boundary,
        }.items():
            raw = _matrix_norms(matrix)
            residuals[name] = {
                "raw": raw,
                "relative_to_hamiltonian": _normalized(raw, reference_norms),
            }

        algebraic_raw = _matrix_norms(algebraic)
        grids.append(
            {
                "interior_points": points,
                "spacing": spacing,
                "hamiltonian_norms": reference_norms,
                "operator_residuals": residuals,
                "full_eigenpair_algebraic_residual": {
                    "raw": algebraic_raw,
                    "relative_to_hamiltonian": _normalized(
                        algebraic_raw, reference_norms
                    ),
                },
            }
        )

    repository_root = script_path.parents[3]
    return {
        "schema_version": 1,
        "experiment_id": payload["experiment_id"],
        "evidence_status": payload["evidence_status"],
        "calculation_status": "calculated illustrative result",
        "input": payload,
        "grids": grids,
        "provenance": {
            "input_path": input_path.relative_to(repository_root).as_posix(),
            "input_sha256": _sha256(input_path),
            "script_path": script_path.relative_to(repository_root).as_posix(),
            "script_sha256": _sha256(script_path),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
            "eigensolver": "numpy.linalg.eigh",
        },
        "limitations": [
            "Raw matrix norms are dimension- and discretization-scale-dependent.",
            (
                "Normalized norms compare each residual only with its "
                "same-grid Hamiltonian."
            ),
            "Maximum-entry norms are basis-dependent.",
            "Algebraic eigenpair residuals do not measure continuum error.",
            "The result is not semiconductor evidence or scientific validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.input.resolve(), Path(__file__).resolve())
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
