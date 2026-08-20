#!/usr/bin/env python3
"""Verify the retained particle-in-a-box result against independent identities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

RealMatrix = npt.NDArray[np.float64]


def _matrix(payload: dict[str, Any], name: str) -> RealMatrix:
    return np.asarray(payload["matrices"][name], dtype=np.float64)


def _residual(payload: dict[str, Any], name: str, field: str = "matrix") -> RealMatrix:
    return np.asarray(payload["residuals"][name][field], dtype=np.float64)


def verify(path: Path) -> None:
    """Raise ``AssertionError`` unless the retained result satisfies the protocol."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["evidence_status"] == "illustrative numerical experiment"
    assert payload["calculation_status"] == "calculated illustrative result"

    parameters = payload["input"]["dimensionless_parameters"]
    length = float(parameters["length"])
    mass = float(parameters["mass"])
    hbar = float(parameters["hbar"])
    points = int(parameters["interior_points"])
    retained = int(parameters["retained_dimension"])
    spacing = length / (points + 1)
    prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)

    expected_hamiltonian = np.diag(np.full(points, 2.0 * prefactor))
    expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), 1)
    expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), -1)
    hamiltonian = _matrix(payload, "dirichlet_hamiltonian_full")
    np.testing.assert_array_equal(hamiltonian, expected_hamiltonian)

    indices = np.arange(1, points + 1, dtype=np.float64)
    z = indices * np.pi / (2.0 * (points + 1))
    expected_discrete = 4.0 * prefactor * np.sin(z) ** 2
    expected_continuum = (
        hbar * hbar * np.pi * np.pi * indices * indices / (2.0 * mass * length * length)
    )
    computed = np.asarray(payload["spectra"]["computed_discrete"], dtype=np.float64)
    recorded_discrete = np.asarray(
        payload["spectra"]["discrete_closed_form"], dtype=np.float64
    )
    recorded_continuum = np.asarray(
        payload["spectra"]["continuum_closed_form"], dtype=np.float64
    )
    recorded_ratio = np.asarray(
        payload["spectra"]["discrete_to_continuum_ratio"], dtype=np.float64
    )
    np.testing.assert_array_equal(recorded_discrete, expected_discrete)
    np.testing.assert_array_equal(recorded_continuum, expected_continuum)
    np.testing.assert_allclose(
        recorded_ratio,
        (np.sin(z) / z) ** 2,
        rtol=16.0 * np.finfo(np.float64).eps,
        atol=0.0,
    )
    scale = float(np.max(expected_discrete))
    np.testing.assert_allclose(
        computed,
        expected_discrete,
        rtol=64.0 * np.finfo(np.float64).eps,
        atol=64.0 * np.finfo(np.float64).eps * scale,
    )

    vectors = _matrix(payload, "retained_eigenvectors")
    projector = _matrix(payload, "spectral_projector_full")
    embedded = _matrix(payload, "retained_hamiltonian_embedded_full")
    coordinates = _matrix(payload, "retained_hamiltonian_coordinates")
    tolerance = (
        256.0 * np.finfo(np.float64).eps * float(np.linalg.norm(hamiltonian, ord="fro"))
    )
    np.testing.assert_allclose(vectors.T @ vectors, np.eye(retained), atol=tolerance)
    np.testing.assert_allclose(projector, vectors @ vectors.T, atol=tolerance)
    np.testing.assert_allclose(projector @ projector, projector, atol=tolerance)
    np.testing.assert_allclose(
        embedded, projector @ hamiltonian @ projector, atol=tolerance
    )
    np.testing.assert_allclose(
        coordinates, vectors.T @ hamiltonian @ vectors, atol=tolerance
    )
    np.testing.assert_allclose(
        coordinates,
        np.diag(expected_discrete[:retained]),
        atol=tolerance,
    )

    compressed = _residual(payload, "consistently_compressed_physical_potential")
    np.testing.assert_array_equal(compressed, np.zeros((points, points)))

    unmatched = _residual(payload, "projected_hamiltonian_minus_unprojected_kinetic")
    discarded = _residual(
        payload,
        "projected_hamiltonian_minus_unprojected_kinetic",
        "discarded_sector_reference",
    )
    np.testing.assert_allclose(unmatched, embedded - hamiltonian, atol=tolerance)
    np.testing.assert_allclose(unmatched, discarded, atol=tolerance)
    assert float(np.linalg.norm(unmatched, ord="fro")) > tolerance

    boundary = _residual(payload, "dirichlet_minus_cyclic_reference")
    expected_boundary = np.zeros((points, points))
    expected_boundary[0, -1] = prefactor
    expected_boundary[-1, 0] = prefactor
    np.testing.assert_array_equal(boundary, expected_boundary)

    assert payload["limitations"] == [
        "The finite matrix is not the continuum differential operator.",
        "The cyclic-reference residual is not a representation-independent potential.",
        "The result is not semiconductor evidence or scientific validation.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    verify(args.result)
    print("particle-in-box retained result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
