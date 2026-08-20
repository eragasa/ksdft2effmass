#!/usr/bin/env python3
"""Run grid-refinement series for the particle-in-a-box experiment."""

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


def _frobenius(matrix: RealMatrix) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def _observed_orders(spacings: list[float], errors: list[float]) -> list[float | None]:
    orders: list[float | None] = [None]
    for previous_h, current_h, previous_error, current_error in zip(
        spacings[:-1], spacings[1:], errors[:-1], errors[1:], strict=True
    ):
        orders.append(
            float(
                np.log(previous_error / current_error) / np.log(previous_h / current_h)
            )
        )
    return orders


def run(input_path: Path, script_path: Path) -> dict[str, Any]:
    """Execute the declared grid-refinement series."""
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported convergence input schema version")
    if payload.get("evidence_status") != "illustrative numerical experiment":
        raise ValueError("incorrect evidence status")

    parameters = payload["dimensionless_parameters"]
    length = _positive_real(parameters.get("length"), "length")
    mass = _positive_real(parameters.get("mass"), "mass")
    hbar = _positive_real(parameters.get("hbar"), "hbar")
    series = payload["grid_series"]
    point_counts = _integer_list(series.get("interior_points"), "interior_points")
    reported_modes = _integer_list(series.get("reported_modes"), "reported_modes")
    order_modes = _integer_list(series.get("order_modes"), "order_modes")
    retained = series.get("retained_dimension")
    if isinstance(retained, bool) or not isinstance(retained, int) or retained <= 0:
        raise TypeError("retained_dimension must be a positive integer")
    if max(reported_modes) > min(point_counts):
        raise ValueError("reported modes must exist on every grid")
    if not set(order_modes).issubset(reported_modes):
        raise ValueError("order_modes must be a subset of reported_modes")
    if retained > min(point_counts):
        raise ValueError("retained_dimension must exist on every grid")

    spacings: list[float] = []
    refinements: list[dict[str, Any]] = []
    relative_errors: dict[int, list[float]] = {mode: [] for mode in order_modes}

    for points in point_counts:
        spacing = length / (points + 1)
        spacings.append(spacing)
        hamiltonian = _hamiltonian(points, length, mass, hbar)
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
        mode_indices = np.asarray(reported_modes, dtype=np.float64)
        continuum = (
            hbar
            * hbar
            * np.pi
            * np.pi
            * mode_indices
            * mode_indices
            / (2.0 * mass * length * length)
        )
        computed = eigenvalues[np.asarray(reported_modes) - 1]
        absolute = np.abs(computed - continuum)
        relative = absolute / continuum
        closed_discrete = (
            2.0
            * hbar
            * hbar
            / (mass * spacing * spacing)
            * np.sin(mode_indices * np.pi / (2.0 * (points + 1))) ** 2
        )

        retained_vectors = eigenvectors[:, :retained]
        projector = retained_vectors @ retained_vectors.T
        complement = np.eye(points) - projector
        embedded = projector @ hamiltonian @ projector
        consistent = embedded - projector @ hamiltonian.copy() @ projector
        unmatched = embedded - hamiltonian
        discarded = -(complement @ hamiltonian @ complement)

        modes = []
        for index, mode in enumerate(reported_modes):
            modes.append(
                {
                    "mode": mode,
                    "computed_energy": float(computed[index]),
                    "continuum_energy": float(continuum[index]),
                    "absolute_error": float(absolute[index]),
                    "relative_error": float(relative[index]),
                    "discrete_closed_form_error": float(
                        abs(computed[index] - closed_discrete[index])
                    ),
                }
            )
            if mode in relative_errors:
                relative_errors[mode].append(float(relative[index]))

        unmatched_norm = _frobenius(unmatched)
        unmatched_discarded_error = _frobenius(unmatched - discarded)
        refinements.append(
            {
                "interior_points": points,
                "spacing": spacing,
                "modes": modes,
                "diagnostic_residuals": {
                    "consistent_compression_frobenius_norm": _frobenius(consistent),
                    "unmatched_compression_frobenius_norm": unmatched_norm,
                    "unmatched_equals_discarded_frobenius_error": (
                        unmatched_discarded_error
                    ),
                    "unmatched_equals_discarded_relative_error": (
                        unmatched_discarded_error / unmatched_norm
                    ),
                    "interpretation": (
                        "identity diagnostics only; raw norms are not compared "
                        "as convergence quantities across changing spaces"
                    ),
                },
            }
        )

    observed_orders = {
        str(mode): _observed_orders(spacings, relative_errors[mode])
        for mode in order_modes
    }
    repository_root = script_path.parents[3]
    return {
        "schema_version": 1,
        "experiment_id": payload["experiment_id"],
        "evidence_status": payload["evidence_status"],
        "calculation_status": "calculated illustrative result",
        "input": payload,
        "refinements": refinements,
        "observed_relative_error_orders": observed_orders,
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
            "Observed order concerns fixed-index eigenvalues only.",
            "The series does not establish uniform spectral convergence.",
            "Residual norms on different matrix spaces are not convergence metrics.",
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
