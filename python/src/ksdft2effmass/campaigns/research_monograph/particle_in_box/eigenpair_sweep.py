"""Higher-eigenpair sweep Workflow for the research-monograph particle in a box."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np

from ksdft2effmass.analysis import ObservedConvergenceOrderEstimator
from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import SparseMatrixQuantity

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ParticleInBoxEigenpairSweepWorkflow:
    """Decode, evaluate, and serialize the higher-index eigenpair campaign."""

    __slots__ = ("grid_evaluator", "order_estimator")

    def __init__(self) -> None:
        """Construct the campaign from reusable public analysis actions."""
        self.grid_evaluator = ParticleInBoxGridEvaluator()
        self.order_estimator = ObservedConvergenceOrderEstimator()

    def execute(
        self, input_path: Path, script_path: Path, repository_root: Path
    ) -> bytes:
        """Return canonical JSON bytes for full-spectrum and fixed-mode sweeps."""
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        script_file = self.contained_file(script_path, root, "script_path")
        payload = self.mapping(
            cast(JsonValue, json.loads(input_file.read_text(encoding="utf-8"))),
            "input",
        )
        if self.integer(payload.get("schema_version"), "schema_version") != 1:
            raise ValueError("unsupported eigenpair-sweep input schema version")
        if payload.get("evidence_status") != "illustrative numerical experiment":
            raise ValueError("incorrect evidence status")
        values = self.mapping(
            payload.get("dimensionless_parameters"), "dimensionless_parameters"
        )
        length = self.positive_real(values.get("length"), "length")
        mass = self.positive_real(values.get("mass"), "mass")
        hbar = self.positive_real(values.get("hbar"), "hbar")
        parameters = ParticleInBoxParameters(
            ScalarQuantity(length, Unitless()),
            ScalarQuantity(mass, Unitless()),
            ScalarQuantity(hbar, Unitless()),
        )
        series = self.mapping(payload.get("grid_series"), "grid_series")
        point_counts = self.integer_sequence(
            series.get("interior_points"), "interior_points"
        )
        fixed_modes = self.integer_sequence(
            series.get("fixed_higher_modes"), "fixed_higher_modes"
        )
        if max(fixed_modes) > max(point_counts):
            raise ValueError("fixed higher modes must exist on at least one grid")

        grids: list[JsonValue] = []
        fixed_errors: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_spacings: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_point_counts: dict[int, list[int]] = {mode: [] for mode in fixed_modes}
        for points in point_counts:
            evaluation = self.grid_evaluator.execute(parameters, points)
            eigenpairs = evaluation.eigenpairs
            if not isinstance(eigenpairs.operator, SparseMatrixQuantity):
                raise TypeError("grid evaluator must retain a sparse Hamiltonian")
            hamiltonian = eigenpairs.operator.to_dense().magnitude
            eigenvalues = eigenpairs.eigenvalues.magnitude
            eigenvectors = eigenpairs.eigenvectors.magnitude
            spacing = evaluation.finite_difference.grid_spacing.magnitude
            spectral_scale = float(np.max(np.abs(eigenvalues)))
            node_indices = np.arange(1, points + 1, dtype=np.float64)
            records: list[JsonValue] = []
            continuum_levels = evaluation.analytical.energy_levels(points).magnitude
            overlap_defects: list[float] = []
            scaled_residuals: list[float] = []
            for mode in range(1, points + 1):
                continuum_energy = float(continuum_levels[mode - 1])
                computed_energy = float(eigenvalues[mode - 1])
                relative_error = (
                    abs(computed_energy - continuum_energy) / continuum_energy
                )
                nodal_oracle = np.sqrt(2.0 / (points + 1)) * np.sin(
                    node_indices * mode * np.pi / (points + 1)
                )
                vector = eigenvectors[:, mode - 1]
                overlap_defect = max(0.0, 1.0 - abs(float(vector @ nodal_oracle)))
                scaled_residual = float(
                    np.linalg.norm(hamiltonian @ vector - computed_energy * vector)
                    / spectral_scale
                )
                overlap_defects.append(overlap_defect)
                scaled_residuals.append(scaled_residual)
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
                    "maximum_nodal_overlap_defect": max(overlap_defects),
                    "maximum_scaled_eigenpair_residual": max(scaled_residuals),
                }
            )
        fixed_mode_series: dict[str, JsonValue] = {}
        for mode in fixed_modes:
            orders = self.order_estimator.execute(
                VectorQuantity(np.asarray(fixed_spacings[mode]), Unitless()),
                VectorQuantity(np.asarray(fixed_errors[mode]), Unitless()),
            )
            fixed_mode_series[str(mode)] = {
                "interior_points": cast(list[JsonValue], fixed_point_counts[mode]),
                "spacings": cast(list[JsonValue], fixed_spacings[mode]),
                "relative_energy_errors": cast(list[JsonValue], fixed_errors[mode]),
                "observed_orders": list(orders.nullable_orders()),
            }
        result_payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": payload["experiment_id"],
            "evidence_status": payload["evidence_status"],
            "calculation_status": "calculated illustrative result",
            "input": payload,
            "grids": grids,
            "fixed_higher_mode_series": fixed_mode_series,
            "provenance": self.provenance(input_file, script_file, root),
            "limitations": [
                "Fixed-mode convergence does not imply uniform spectral convergence.",
                "Nodal overlap does not measure continuum interpolation error.",
                "High-index eigenvalues probe finite-difference dispersion.",
                "The result is not semiconductor evidence or scientific validation.",
            ],
        }
        return (
            json.dumps(result_payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    def provenance(
        self, input_path: Path, script_path: Path, root: Path
    ) -> dict[str, JsonValue]:
        """Return current source identities for one newly authored result."""
        return {
            "input_path": input_path.relative_to(root).as_posix(),
            "input_sha256": self.sha256(input_path),
            "script_path": script_path.relative_to(root).as_posix(),
            "script_sha256": self.sha256(script_path),
            "implementation_identities": [
                {"path": path.relative_to(root).as_posix(), "sha256": self.sha256(path)}
                for path in self.implementation_paths()
            ],
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
            "eigensolver": "scipy.linalg.eigh_tridiagonal",
        }

    @staticmethod
    def implementation_paths() -> tuple[Path, ...]:
        """Return exact public sources implementing the campaign."""
        package_root = Path(__file__).resolve().parents[3]
        return (
            package_root / "analysis" / "convergence.py",
            package_root
            / "analysis"
            / "model_systems"
            / "particle_in_box"
            / "model.py",
            package_root
            / "analysis"
            / "model_systems"
            / "particle_in_box"
            / "evaluation.py",
            package_root / "operators" / "eigenpairs.py",
            Path(__file__).resolve(),
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object with string keys."""
        if not isinstance(value, dict) or not all(type(key) is str for key in value):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one built-in JSON integer excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @classmethod
    def integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one strictly increasing sequence of positive integers."""
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty JSON array")
        result = tuple(cls.integer(item, name) for item in value)
        if any(item <= 0 for item in result):
            raise ValueError(f"{name} entries must be positive")
        if result != tuple(sorted(set(result))):
            raise ValueError(f"{name} must be strictly increasing")
        return result

    @staticmethod
    def positive_real(value: JsonValue, name: str) -> float:
        """Return one positive finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a positive JSON number")
        result = float(value)
        if not np.isfinite(result) or result <= 0.0:
            raise ValueError(f"{name} must be positive and finite")
        return result

    @staticmethod
    def contained_file(path: Path, root: Path, name: str) -> Path:
        """Return one existing source file beneath the explicit root."""
        resolved = path.resolve()
        if not resolved.is_file():
            raise ValueError(f"{name} must be an existing file")
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise ValueError(f"{name} must be beneath repository_root") from error
        return resolved

    @staticmethod
    def sha256(path: Path) -> str:
        """Return one file's lowercase SHA-256 identity."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
