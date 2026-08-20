#!/usr/bin/env python3
"""Run the particle-in-a-box higher-index eigenpair sweep."""

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


def _orders(spacings: list[float], errors: list[float]) -> list[float | None]:
    result: list[float | None] = [None]
    for previous_h, current_h, previous_error, current_error in zip(
        spacings[:-1], spacings[1:], errors[:-1], errors[1:], strict=True
    ):
        result.append(
            float(
                np.log(previous_error / current_error) / np.log(previous_h / current_h)
            )
        )
    return result


def run(input_path: Path, script_path: Path) -> dict[str, Any]:
    """Execute the declared full-spectrum and fixed-higher-mode sweeps."""
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported eigenpair-sweep input schema version")
    if payload.get("evidence_status") != "illustrative numerical experiment":
        raise ValueError("incorrect evidence status")

    parameters = payload["dimensionless_parameters"]
    length = _positive_real(parameters.get("length"), "length")
    mass = _positive_real(parameters.get("mass"), "mass")
    hbar = _positive_real(parameters.get("hbar"), "hbar")
    series = payload["grid_series"]
    point_counts = _integer_list(series.get("interior_points"), "interior_points")
    fixed_modes = _integer_list(series.get("fixed_higher_modes"), "fixed_higher_modes")
    if max(fixed_modes) > max(point_counts):
        raise ValueError("fixed higher modes must exist on at least one grid")

    grids: list[dict[str, Any]] = []
    fixed_errors: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
    fixed_spacings: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
    fixed_point_counts: dict[int, list[int]] = {mode: [] for mode in fixed_modes}

    for points in point_counts:
        spacing = length / (points + 1)
        hamiltonian = _hamiltonian(points, length, mass, hbar)
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
        spectral_scale = float(np.max(np.abs(eigenvalues)))
        node_indices = np.arange(1, points + 1, dtype=np.float64)
        records: list[dict[str, float | int]] = []

        for mode in range(1, points + 1):
            continuum_energy = (
                hbar
                * hbar
                * np.pi
                * np.pi
                * mode
                * mode
                / (2.0 * mass * length * length)
            )
            computed_energy = float(eigenvalues[mode - 1])
            relative_error = abs(computed_energy - continuum_energy) / continuum_energy
            nodal_oracle = np.sqrt(2.0 / (points + 1)) * np.sin(
                node_indices * mode * np.pi / (points + 1)
            )
            vector = eigenvectors[:, mode - 1]
            overlap_defect = max(0.0, 1.0 - abs(float(vector @ nodal_oracle)))
            scaled_residual = float(
                np.linalg.norm(hamiltonian @ vector - computed_energy * vector)
                / spectral_scale
            )
            records.append(
                {
                    "mode": mode,
                    "fractional_mode_index": mode / (points + 1),
                    "computed_energy": computed_energy,
                    "continuum_energy": continuum_energy,
                    "relative_energy_error": relative_error,
                    "nodal_overlap_defect": overlap_defect,
                    "scaled_eigenpair_residual": scaled_residual,
                }
            )
            if mode in fixed_errors:
                fixed_errors[mode].append(relative_error)
                fixed_spacings[mode].append(spacing)
                fixed_point_counts[mode].append(points)

        grids.append(
            {
                "interior_points": points,
                "spacing": spacing,
                "eigenpairs": records,
                "maximum_nodal_overlap_defect": max(
                    record["nodal_overlap_defect"] for record in records
                ),
                "maximum_scaled_eigenpair_residual": max(
                    record["scaled_eigenpair_residual"] for record in records
                ),
            }
        )

    fixed_mode_series = {}
    for mode in fixed_modes:
        fixed_mode_series[str(mode)] = {
            "interior_points": fixed_point_counts[mode],
            "spacings": fixed_spacings[mode],
            "relative_energy_errors": fixed_errors[mode],
            "observed_orders": _orders(fixed_spacings[mode], fixed_errors[mode]),
        }

    repository_root = script_path.parents[3]
    return {
        "schema_version": 1,
        "experiment_id": payload["experiment_id"],
        "evidence_status": payload["evidence_status"],
        "calculation_status": "calculated illustrative result",
        "input": payload,
        "grids": grids,
        "fixed_higher_mode_series": fixed_mode_series,
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
            "Fixed-mode convergence does not imply uniform spectral convergence.",
            "Nodal overlap does not measure continuum interpolation error.",
            "High-index eigenvalues probe finite-difference dispersion.",
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
