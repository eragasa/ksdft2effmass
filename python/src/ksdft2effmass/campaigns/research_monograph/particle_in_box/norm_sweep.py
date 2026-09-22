"""Multi-norm residual Workflow for the research-monograph particle in a box."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import (
    MatrixQuantity,
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    RepresentedMatrixNormAnalyzer,
    RepresentedMatrixNormResult,
    SparseMatrixQuantity,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ParticleInBoxNormSweepWorkflow:
    """Decode, evaluate, and serialize the version-one multi-norm campaign."""

    __slots__ = ("compression", "grid_evaluator", "norm_analyzer", "selector")

    def __init__(self) -> None:
        """Construct the campaign from reusable public operator actions."""
        self.grid_evaluator = ParticleInBoxGridEvaluator()
        self.selector = OrthogonalSpectralSubspaceSelector()
        self.compression = OperatorCompression()
        self.norm_analyzer = RepresentedMatrixNormAnalyzer()

    def execute(
        self, input_path: Path, script_path: Path, repository_root: Path
    ) -> bytes:
        """Return canonical JSON bytes for the declared multi-norm sweep."""
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        script_file = self.contained_file(script_path, root, "script_path")
        payload = self.mapping(
            cast(JsonValue, json.loads(input_file.read_text(encoding="utf-8"))),
            "input",
        )
        if self.integer(payload.get("schema_version"), "schema_version") != 1:
            raise ValueError("unsupported norm-sweep input schema version")
        if payload.get("evidence_status") != "illustrative numerical experiment":
            raise ValueError("incorrect evidence status")
        if payload.get("norms") != ["frobenius", "spectral", "maximum_entry"]:
            raise ValueError("unsupported norm declaration")
        values = self.mapping(
            payload.get("dimensionless_parameters"), "dimensionless_parameters"
        )
        parameters = ParticleInBoxParameters(
            ScalarQuantity(
                self.positive_real(values.get("length"), "length"), Unitless()
            ),
            ScalarQuantity(self.positive_real(values.get("mass"), "mass"), Unitless()),
            ScalarQuantity(self.positive_real(values.get("hbar"), "hbar"), Unitless()),
        )
        series = self.mapping(payload.get("grid_series"), "grid_series")
        point_counts = self.integer_sequence(
            series.get("interior_points"), "interior_points"
        )
        retained = self.positive_integer(
            series.get("retained_dimension"), "retained_dimension"
        )
        if retained > min(point_counts):
            raise ValueError("retained_dimension must exist on every grid")

        grids: list[JsonValue] = []
        for points in point_counts:
            evaluation = self.grid_evaluator.execute(parameters, points)
            eigenpairs = evaluation.eigenpairs
            if not isinstance(eigenpairs.operator, SparseMatrixQuantity):
                raise TypeError("grid evaluator must retain a sparse Hamiltonian")
            hamiltonian = eigenpairs.operator
            dense_hamiltonian = hamiltonian.to_dense().magnitude
            eigenvalues = eigenpairs.eigenvalues.magnitude
            eigenvectors = eigenpairs.eigenvectors.magnitude
            subspace = self.selector.execute(eigenpairs, retained)
            compression = self.compression.execute(hamiltonian, subspace)
            projector = subspace.projector().magnitude
            embedded = compression.embedded.magnitude
            consistent = embedded - projector @ dense_hamiltonian.copy() @ projector
            unmatched = embedded - dense_hamiltonian
            cyclic = dense_hamiltonian.copy()
            if points > 1:
                cyclic[0, -1] = dense_hamiltonian[0, 1]
                cyclic[-1, 0] = dense_hamiltonian[1, 0]
            boundary = dense_hamiltonian - cyclic
            algebraic = (
                dense_hamiltonian @ eigenvectors
                - eigenvectors * eigenvalues[np.newaxis, :]
            )
            reference_norms = self.norm_analyzer.execute(hamiltonian)
            residuals: dict[str, JsonValue] = {}
            for name, matrix in (
                ("consistent_compression", consistent),
                ("unmatched_compression", unmatched),
                ("boundary_realization", boundary),
            ):
                norms = self.norm_analyzer.execute(
                    MatrixQuantity(matrix, hamiltonian.unit)
                )
                residuals[name] = {
                    "raw": self.norms(norms),
                    "relative_to_hamiltonian": self.norms(
                        norms.normalized_by(reference_norms)
                    ),
                }
            algebraic_norms = self.norm_analyzer.execute(
                MatrixQuantity(algebraic, hamiltonian.unit)
            )
            grids.append(
                {
                    "interior_points": points,
                    "spacing": evaluation.finite_difference.grid_spacing.magnitude,
                    "hamiltonian_norms": self.norms(reference_norms),
                    "operator_residuals": residuals,
                    "full_eigenpair_algebraic_residual": {
                        "raw": self.norms(algebraic_norms),
                        "relative_to_hamiltonian": self.norms(
                            algebraic_norms.normalized_by(reference_norms)
                        ),
                    },
                }
            )
        result_payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": payload["experiment_id"],
            "evidence_status": payload["evidence_status"],
            "calculation_status": "calculated illustrative result",
            "input": payload,
            "grids": grids,
            "provenance": self.provenance(input_file, script_file, root),
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
        return (
            json.dumps(result_payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    @staticmethod
    def norms(result: RepresentedMatrixNormResult) -> dict[str, JsonValue]:
        """Represent one norm result in the retained version-one wire shape."""
        return {
            "frobenius": result.frobenius.magnitude,
            "spectral": result.spectral.magnitude,
            "maximum_entry": result.maximum_entry.magnitude,
        }

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
            package_root / "operators" / "matrix_norms.py",
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
