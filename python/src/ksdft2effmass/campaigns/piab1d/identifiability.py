"""Retained-space identifiability Workflow for the research-monograph particle box."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np

from ksdft2effmass.operators import MatrixQuantity, ScalarQuantity, Unitless

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True, eq=False)
class RetainedModelClassFitResult:
    """Retain one best-fit model, residual, and Frobenius norm."""

    name: str
    best_fit: MatrixQuantity
    unexplained_residual: MatrixQuantity
    unexplained_frobenius_norm: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty string")
        if not isinstance(self.best_fit, MatrixQuantity):
            raise TypeError("best_fit must be MatrixQuantity")
        if not isinstance(self.unexplained_residual, MatrixQuantity):
            raise TypeError("unexplained_residual must be MatrixQuantity")
        if not isinstance(self.unexplained_frobenius_norm, ScalarQuantity):
            raise TypeError("unexplained_frobenius_norm must be ScalarQuantity")


class RetainedModelClassFitter:
    """Fit the four declared retained real-symmetric model classes."""

    __slots__ = ()

    def execute(
        self, target: MatrixQuantity
    ) -> tuple[RetainedModelClassFitResult, ...]:
        """Return ordered least-Frobenius fits for the declared nested classes."""
        if not isinstance(target, MatrixQuantity):
            raise TypeError("target must be MatrixQuantity")
        matrix = target.magnitude
        dimension = matrix.shape[0]
        if matrix.shape != (dimension, dimension):
            raise ValueError("target must be square")
        rows, columns = np.indices(matrix.shape)
        candidates = (
            (
                "scalar_identity",
                np.eye(dimension) * float(np.trace(matrix) / dimension),
            ),
            ("diagonal_in_retained_basis", np.diag(np.diag(matrix))),
            (
                "real_symmetric_tridiagonal",
                np.where(np.abs(rows - columns) <= 1, matrix, 0.0),
            ),
            ("arbitrary_real_symmetric", matrix.copy()),
        )
        return tuple(
            RetainedModelClassFitResult(
                name=name,
                best_fit=MatrixQuantity(candidate, target.unit),
                unexplained_residual=MatrixQuantity(matrix - candidate, target.unit),
                unexplained_frobenius_norm=ScalarQuantity(
                    float(np.linalg.norm(matrix - candidate, ord="fro")), target.unit
                ),
            )
            for name, candidate in candidates
        )


class ParticleInBoxIdentifiabilityWorkflow:
    """Decode, evaluate, and serialize the retained-space identifiability campaign."""

    __slots__ = ("model_fitter",)

    def __init__(self) -> None:
        """Construct with the declared retained model-class fitter."""
        self.model_fitter = RetainedModelClassFitter()

    def execute(
        self,
        input_path: Path,
        retained_result_path: Path,
        script_path: Path,
        repository_root: Path,
    ) -> bytes:
        """Return canonical JSON bytes for the declared identifiability study."""
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        retained_file = self.contained_file(
            retained_result_path, root, "retained_result_path"
        )
        script_file = self.contained_file(script_path, root, "script_path")
        payload = self.mapping(
            cast(JsonValue, json.loads(input_file.read_text(encoding="utf-8"))),
            "input",
        )
        if self.integer(payload.get("schema_version"), "schema_version") != 1:
            raise ValueError("unsupported identifiability input schema version")
        if payload.get("evidence_status") != "illustrative numerical experiment":
            raise ValueError("incorrect evidence status")
        expected_classes: list[JsonValue] = [
            "scalar_identity",
            "diagonal_in_retained_basis",
            "real_symmetric_tridiagonal",
            "arbitrary_real_symmetric",
        ]
        if payload.get("admissible_model_classes") != expected_classes:
            raise ValueError("unsupported model-class declaration")
        retained_payload = self.mapping(
            cast(JsonValue, json.loads(retained_file.read_text(encoding="utf-8"))),
            "retained result",
        )
        matrices = self.mapping(retained_payload.get("matrices"), "matrices")
        reduced_hamiltonian = self.matrix(
            matrices.get("retained_hamiltonian_coordinates"),
            "retained Hamiltonian",
        )
        dimension = reduced_hamiltonian.shape[0]
        shift = self.build_shift(payload, dimension)
        physical_kinetic = reduced_hamiltonian.copy()
        physical_potential = np.zeros_like(reduced_hamiltonian)
        alternative_kinetic = reduced_hamiltonian - shift
        alternative_potential = shift.copy()
        decompositions: dict[str, JsonValue] = {
            "consistently_reduced_dirichlet": {
                "kinetic": self.matrix_json(physical_kinetic),
                "potential": self.matrix_json(physical_potential),
                "reconstruction_frobenius_error": self.frobenius_norm(
                    reduced_hamiltonian - physical_kinetic - physical_potential
                ),
                "interpretation": (
                    "physical box decomposition under the declared "
                    "Dirichlet realization"
                ),
            },
            "illustratively_shifted": {
                "kinetic": self.matrix_json(alternative_kinetic),
                "potential": self.matrix_json(alternative_potential),
                "reconstruction_frobenius_error": self.frobenius_norm(
                    reduced_hamiltonian - alternative_kinetic - alternative_potential
                ),
                "interpretation": (
                    "algebraically valid alternative, not a physical assignment"
                ),
            },
        }
        fits = self.model_fitter.execute(MatrixQuantity(shift, Unitless()))
        model_class_fits: dict[str, JsonValue] = {
            fit.name: {
                "best_fit": self.matrix_json(fit.best_fit.magnitude),
                "unexplained_residual": self.matrix_json(
                    fit.unexplained_residual.magnitude
                ),
                "unexplained_frobenius_norm": (
                    fit.unexplained_frobenius_norm.magnitude
                ),
            }
            for fit in fits
        }
        result_payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": payload["experiment_id"],
            "evidence_status": payload["evidence_status"],
            "calculation_status": "calculated illustrative result",
            "input": payload,
            "retained_space": {
                "identifier": "lowest discrete spectral coordinates",
                "dimension": dimension,
                "reduced_hamiltonian": self.matrix_json(reduced_hamiltonian),
            },
            "decompositions": decompositions,
            "illustrative_shift": self.matrix_json(shift),
            "model_class_fits": model_class_fits,
            "provenance": self.provenance(input_file, retained_file, script_file, root),
            "limitations": [
                "The alternative shift is illustrative and has no physical assignment.",
                (
                    "Model-class fits depend on the declared retained basis and "
                    "Frobenius metric."
                ),
                (
                    "Algebraic reconstructability does not establish physical "
                    "identifiability."
                ),
                "The result is not semiconductor evidence or scientific validation.",
            ],
        }
        return (
            json.dumps(result_payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    def build_shift(
        self, payload: dict[str, JsonValue], dimension: int
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Return the validated declared symmetric decomposition shift."""
        declaration = self.mapping(
            payload.get("alternative_decomposition_shift"),
            "alternative_decomposition_shift",
        )
        diagonal_value = declaration.get("diagonal")
        if not isinstance(diagonal_value, list):
            raise TypeError("shift diagonal must be a JSON array")
        diagonal = np.asarray(diagonal_value, dtype=np.float64)
        if diagonal.shape != (dimension,) or not np.all(np.isfinite(diagonal)):
            raise ValueError("shift diagonal must match the retained dimension")
        shift = np.diag(diagonal)
        upper = declaration.get("upper_triangle")
        if not isinstance(upper, list):
            raise TypeError("upper_triangle must be a JSON array")
        for value in upper:
            entry = self.mapping(value, "upper-triangle shift entry")
            row = self.integer(entry.get("row"), "row")
            column = self.integer(entry.get("column"), "column")
            entry_value = self.real(entry.get("value"), "value")
            if row < 0 or row >= column or column >= dimension:
                raise ValueError("invalid upper-triangle shift entry")
            shift[row, column] = entry_value
            shift[column, row] = entry_value
        return shift

    def provenance(
        self,
        input_path: Path,
        retained_path: Path,
        script_path: Path,
        root: Path,
    ) -> dict[str, JsonValue]:
        """Return current source identities for one newly authored result."""
        return {
            "input_path": input_path.relative_to(root).as_posix(),
            "input_sha256": self.sha256(input_path),
            "retained_result_path": retained_path.relative_to(root).as_posix(),
            "retained_result_sha256": self.sha256(retained_path),
            "script_path": script_path.relative_to(root).as_posix(),
            "script_sha256": self.sha256(script_path),
            "implementation_identities": [
                {"path": path.relative_to(root).as_posix(), "sha256": self.sha256(path)}
                for path in self.implementation_paths()
            ],
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
        }

    @staticmethod
    def implementation_paths() -> tuple[Path, ...]:
        """Return exact public sources implementing the campaign."""
        return (Path(__file__).resolve(),)

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

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def matrix(
        value: JsonValue, name: str
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Return one finite square binary64 matrix."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        matrix = np.asarray(value, dtype=np.float64)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError(f"{name} must be a square matrix")
        if not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must contain finite entries")
        return matrix

    @staticmethod
    def matrix_json(
        matrix: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> list[JsonValue]:
        """Return one matrix in the closed recursive JSON representation."""
        return cast(list[JsonValue], matrix.tolist())

    @staticmethod
    def frobenius_norm(
        matrix: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> float:
        """Return the historical NumPy Frobenius norm."""
        return float(np.linalg.norm(matrix, ord="fro"))

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
