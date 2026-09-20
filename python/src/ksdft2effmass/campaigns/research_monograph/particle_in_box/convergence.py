"""Grid-convergence Workflow for the research-monograph particle in a box."""

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
from ksdft2effmass.operators import (
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    SparseMatrixQuantity,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ParticleInBoxConvergenceWorkflow:
    """Decode, evaluate, and serialize the version-one grid-convergence campaign."""

    __slots__ = ("compression", "grid_evaluator", "order_estimator", "selector")

    def __init__(self) -> None:
        """Construct the campaign from reusable public analysis actions."""
        self.grid_evaluator = ParticleInBoxGridEvaluator()
        self.order_estimator = ObservedConvergenceOrderEstimator()
        self.selector = OrthogonalSpectralSubspaceSelector()
        self.compression = OperatorCompression()

    def execute(
        self, input_path: Path, script_path: Path, repository_root: Path
    ) -> bytes:
        """Return canonical version-one JSON bytes for the declared grid series."""
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        script_file = self.contained_file(script_path, root, "script_path")
        payload = self.mapping(
            cast(JsonValue, json.loads(input_file.read_text(encoding="utf-8"))),
            "input",
        )
        if self.integer(payload.get("schema_version"), "schema_version") != 1:
            raise ValueError("unsupported convergence input schema version")
        if payload.get("evidence_status") != "illustrative numerical experiment":
            raise ValueError("incorrect evidence status")
        parameters_value = self.mapping(
            payload.get("dimensionless_parameters"), "dimensionless_parameters"
        )
        length = self.positive_real(parameters_value.get("length"), "length")
        mass = self.positive_real(parameters_value.get("mass"), "mass")
        hbar = self.positive_real(parameters_value.get("hbar"), "hbar")
        parameters = ParticleInBoxParameters(
            ScalarQuantity(length, Unitless()),
            ScalarQuantity(mass, Unitless()),
            ScalarQuantity(hbar, Unitless()),
        )
        series = self.mapping(payload.get("grid_series"), "grid_series")
        point_counts = self.integer_sequence(
            series.get("interior_points"), "interior_points"
        )
        reported_modes = self.integer_sequence(
            series.get("reported_modes"), "reported_modes"
        )
        order_modes = self.integer_sequence(series.get("order_modes"), "order_modes")
        retained = self.positive_integer(
            series.get("retained_dimension"), "retained_dimension"
        )
        if max(reported_modes) > min(point_counts):
            raise ValueError("reported modes must exist on every grid")
        if not set(order_modes).issubset(reported_modes):
            raise ValueError("order_modes must be a subset of reported_modes")
        if retained > min(point_counts):
            raise ValueError("retained_dimension must exist on every grid")

        spacings: list[float] = []
        refinements: list[JsonValue] = []
        relative_errors: dict[int, list[float]] = {mode: [] for mode in order_modes}
        for points in point_counts:
            evaluation = self.grid_evaluator.execute(parameters, points)
            eigenpairs = evaluation.eigenpairs
            if not isinstance(eigenpairs.operator, SparseMatrixQuantity):
                raise TypeError("grid evaluator must retain a sparse Hamiltonian")
            hamiltonian = eigenpairs.operator
            dense_hamiltonian = hamiltonian.to_dense().magnitude
            eigenvalues = eigenpairs.eigenvalues.magnitude
            spacing = evaluation.finite_difference.grid_spacing.magnitude
            spacings.append(spacing)
            continuum = evaluation.analytical.energy_levels(points).magnitude[
                np.asarray(reported_modes) - 1
            ]
            computed = eigenvalues[np.asarray(reported_modes) - 1]
            absolute = np.abs(computed - continuum)
            relative = absolute / continuum
            discrete = evaluation.finite_difference.discrete_energy_levels().magnitude[
                np.asarray(reported_modes) - 1
            ]
            subspace = self.selector.execute(eigenpairs, retained)
            compression = self.compression.execute(hamiltonian, subspace)
            projector = subspace.projector().magnitude
            complement = subspace.complement_projector().magnitude
            embedded = compression.embedded.magnitude
            consistent = embedded - projector @ dense_hamiltonian.copy() @ projector
            unmatched = embedded - dense_hamiltonian
            discarded = -(complement @ dense_hamiltonian @ complement)
            modes: list[JsonValue] = []
            for index, mode in enumerate(reported_modes):
                modes.append(
                    {
                        "mode": mode,
                        "computed_energy": float(computed[index]),
                        "continuum_energy": float(continuum[index]),
                        "absolute_error": float(absolute[index]),
                        "relative_error": float(relative[index]),
                        "discrete_closed_form_error": float(
                            abs(computed[index] - discrete[index])
                        ),
                    }
                )
                if mode in relative_errors:
                    relative_errors[mode].append(float(relative[index]))
            unmatched_norm = self.frobenius_norm(unmatched)
            unmatched_discarded_error = self.frobenius_norm(unmatched - discarded)
            refinements.append(
                {
                    "interior_points": points,
                    "spacing": spacing,
                    "modes": modes,
                    "diagnostic_residuals": {
                        "consistent_compression_frobenius_norm": self.frobenius_norm(
                            consistent
                        ),
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
        observed_orders: dict[str, JsonValue] = {}
        spacing_quantity = VectorQuantity(np.asarray(spacings), Unitless())
        for mode in order_modes:
            result = self.order_estimator.execute(
                spacing_quantity,
                VectorQuantity(np.asarray(relative_errors[mode]), Unitless()),
            )
            observed_orders[str(mode)] = list(result.nullable_orders())
        result_payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": payload["experiment_id"],
            "evidence_status": payload["evidence_status"],
            "calculation_status": "calculated illustrative result",
            "input": payload,
            "refinements": refinements,
            "observed_relative_error_orders": observed_orders,
            "provenance": self.provenance(input_file, script_file, root),
            "limitations": [
                "Observed order concerns fixed-index eigenvalues only.",
                "The series does not establish uniform spectral convergence.",
                (
                    "Residual norms on different matrix spaces are not "
                    "convergence metrics."
                ),
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
                {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": self.sha256(path),
                }
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
            package_root / "operators" / "subspaces.py",
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
    def positive_integer(cls, value: JsonValue, name: str) -> int:
        """Return one positive built-in JSON integer."""
        result = cls.integer(value, name)
        if result <= 0:
            raise ValueError(f"{name} must be positive")
        return result

    @classmethod
    def integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one strictly increasing sequence of positive integers."""
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty JSON array")
        result = tuple(cls.positive_integer(item, name) for item in value)
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
    def frobenius_norm(
        matrix: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> float:
        """Return the historical NumPy Frobenius norm."""
        return float(np.linalg.norm(matrix, ord="fro"))

    @staticmethod
    def contained_file(path: Path, root: Path, name: str) -> Path:
        """Return one existing source file beneath the explicit root."""
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
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
