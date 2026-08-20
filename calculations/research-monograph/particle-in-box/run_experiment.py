#!/usr/bin/env python3
"""Reproduce the particle-in-a-box residual experiment from its JSON input."""

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


def _require_positive_real(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a positive JSON number")
    result = float(value)
    if not np.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _require_positive_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be a positive JSON integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _load_input(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("experiment input must be a JSON object")
    expected = {
        "schema_version",
        "experiment_id",
        "evidence_status",
        "dimensionless_parameters",
        "boundary_reference",
    }
    if set(payload) != expected:
        raise ValueError("experiment input fields do not match schema version 1")
    if payload["schema_version"] != 1:
        raise ValueError("unsupported experiment input schema version")
    if not isinstance(payload["experiment_id"], str) or not payload["experiment_id"]:
        raise TypeError("experiment_id must be a nonempty string")
    if payload["evidence_status"] != "illustrative numerical experiment":
        raise ValueError("evidence_status must identify an illustrative experiment")
    if not isinstance(payload["dimensionless_parameters"], dict):
        raise TypeError("dimensionless_parameters must be a JSON object")
    if not isinstance(payload["boundary_reference"], dict):
        raise TypeError("boundary_reference must be a JSON object")
    return payload


def _dirichlet_hamiltonian(
    interior_points: int, length: float, mass: float, hbar: float
) -> RealMatrix:
    spacing = length / (interior_points + 1)
    prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
    matrix = np.diag(np.full(interior_points, 2.0 * prefactor))
    if interior_points > 1:
        off_diagonal = np.full(interior_points - 1, -prefactor)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    return matrix


def _cyclic_reference(
    interior_points: int, length: float, mass: float, hbar: float
) -> RealMatrix:
    matrix = _dirichlet_hamiltonian(interior_points, length, mass, hbar)
    if interior_points > 1:
        spacing = length / (interior_points + 1)
        prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        matrix[0, -1] = -prefactor
        matrix[-1, 0] = -prefactor
    return matrix


def _frobenius(matrix: RealMatrix) -> float:
    return float(np.sqrt(np.sum(np.square(matrix))))


def _matrix(matrix: RealMatrix) -> list[list[float]]:
    return matrix.tolist()


def run(input_path: Path, script_path: Path) -> dict[str, Any]:
    """Execute the declared finite-dimensional experiment."""
    repository_root = script_path.parents[3]
    input_reference = input_path.relative_to(repository_root).as_posix()
    script_reference = script_path.relative_to(repository_root).as_posix()
    payload = _load_input(input_path)
    parameters = payload["dimensionless_parameters"]
    length = _require_positive_real(parameters.get("length"), "length")
    mass = _require_positive_real(parameters.get("mass"), "mass")
    hbar = _require_positive_real(parameters.get("hbar"), "hbar")
    interior_points = _require_positive_integer(
        parameters.get("interior_points"), "interior_points"
    )
    retained_dimension = _require_positive_integer(
        parameters.get("retained_dimension"), "retained_dimension"
    )
    if retained_dimension > interior_points:
        raise ValueError("retained_dimension must not exceed interior_points")

    hamiltonian = _dirichlet_hamiltonian(interior_points, length, mass, hbar)
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    retained_vectors = eigenvectors[:, :retained_dimension]
    projector = retained_vectors @ retained_vectors.T
    complement = np.eye(interior_points) - projector

    retained_embedded = projector @ hamiltonian @ projector
    retained_kinetic = projector @ hamiltonian.copy() @ projector
    retained_coordinates = retained_vectors.T @ hamiltonian @ retained_vectors

    consistently_compressed = retained_embedded - retained_kinetic
    unmatched_compression = retained_embedded - hamiltonian
    discarded_sector = -(complement @ hamiltonian @ complement)

    cyclic_reference = _cyclic_reference(interior_points, length, mass, hbar)
    boundary_realization = hamiltonian - cyclic_reference

    indices = np.arange(1, interior_points + 1, dtype=np.float64)
    spacing = length / (interior_points + 1)
    discrete_closed_form = (
        2.0
        * hbar
        * hbar
        / (mass * spacing * spacing)
        * np.sin(indices * np.pi / (2.0 * (interior_points + 1))) ** 2
    )
    continuum_closed_form = (
        hbar * hbar * np.pi * np.pi * indices * indices / (2.0 * mass * length * length)
    )
    expected_retained_coordinates = np.diag(discrete_closed_form[:retained_dimension])

    identity = np.eye(interior_points)
    diagnostics = {
        "discrete_spectrum_maximum_absolute_error": float(
            np.max(np.abs(eigenvalues - discrete_closed_form))
        ),
        "spectral_reconstruction_frobenius_error": _frobenius(
            hamiltonian - eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        ),
        "projector_idempotency_frobenius_error": _frobenius(
            projector @ projector - projector
        ),
        "projector_complement_frobenius_error": _frobenius(
            projector + complement - identity
        ),
        "retained_embedding_frobenius_error": _frobenius(
            retained_embedded
            - retained_vectors @ retained_coordinates @ retained_vectors.T
        ),
        "retained_coordinate_frobenius_error": _frobenius(
            retained_coordinates - expected_retained_coordinates
        ),
        "consistently_compressed_residual_frobenius_norm": _frobenius(
            consistently_compressed
        ),
        "unmatched_equals_discarded_frobenius_error": _frobenius(
            unmatched_compression - discarded_sector
        ),
        "unmatched_compression_frobenius_norm": _frobenius(unmatched_compression),
        "boundary_realization_frobenius_norm": _frobenius(boundary_realization),
    }

    return {
        "schema_version": 1,
        "experiment_id": payload["experiment_id"],
        "evidence_status": payload["evidence_status"],
        "calculation_status": "calculated illustrative result",
        "input": payload,
        "state_spaces": {
            "full": {
                "identifier": "interior Dirichlet grid coordinates",
                "dimension": interior_points,
            },
            "retained": {
                "identifier": "lowest discrete spectral coordinates",
                "dimension": retained_dimension,
                "embedding": "columns of retained_eigenvectors",
            },
        },
        "spectra": {
            "computed_discrete": eigenvalues.tolist(),
            "discrete_closed_form": discrete_closed_form.tolist(),
            "continuum_closed_form": continuum_closed_form.tolist(),
            "discrete_to_continuum_ratio": (
                discrete_closed_form / continuum_closed_form
            ).tolist(),
        },
        "matrices": {
            "dirichlet_hamiltonian_full": _matrix(hamiltonian),
            "retained_eigenvectors": _matrix(retained_vectors),
            "spectral_projector_full": _matrix(projector),
            "retained_hamiltonian_embedded_full": _matrix(retained_embedded),
            "retained_hamiltonian_coordinates": _matrix(retained_coordinates),
            "cyclic_reference_full": _matrix(cyclic_reference),
        },
        "residuals": {
            "consistently_compressed_physical_potential": {
                "matrix": _matrix(consistently_compressed),
                "interpretation": "zero after applying the same retention map",
            },
            "projected_hamiltonian_minus_unprojected_kinetic": {
                "matrix": _matrix(unmatched_compression),
                "discarded_sector_reference": _matrix(discarded_sector),
                "interpretation": "negative discarded kinetic sector",
            },
            "dirichlet_minus_cyclic_reference": {
                "matrix": _matrix(boundary_realization),
                "interpretation": (
                    "boundary-closure difference on one declared numerical space"
                ),
            },
        },
        "diagnostics": diagnostics,
        "provenance": {
            "input_path": input_reference,
            "input_sha256": _sha256(input_path),
            "script_path": script_reference,
            "script_sha256": _sha256(script_path),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
            "eigensolver": "numpy.linalg.eigh",
        },
        "limitations": [
            "The finite matrix is not the continuum differential operator.",
            (
                "The cyclic-reference residual is not a "
                "representation-independent potential."
            ),
            "The result is not semiconductor evidence or scientific validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    script_path = Path(__file__).resolve()
    result = run(args.input.resolve(), script_path)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
