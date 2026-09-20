"""Version-one serialization for the core particle-in-a-box residual study."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np

from ksdft2effmass.operators import SparseMatrixQuantity

from .records import ParticleInBoxResidualStudyResult

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ParticleInBoxStudyResultSerializer:
    """Serialize one result to the retained version-one JSON representation."""

    __slots__ = ()

    def execute(
        self,
        result: ParticleInBoxResidualStudyResult,
        input_path: Path,
        script_path: Path,
        repository_root: Path,
    ) -> bytes:
        """Return canonical JSON bytes with current source identities."""
        if not isinstance(result, ParticleInBoxResidualStudyResult):
            raise TypeError("result must be ParticleInBoxResidualStudyResult")
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        script_file = self.contained_file(script_path, root, "script_path")
        definition = result.definition
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": definition.experiment_id,
            "evidence_status": definition.evidence_status,
            "calculation_status": "calculated illustrative result",
            "input": {
                "schema_version": 1,
                "experiment_id": definition.experiment_id,
                "evidence_status": definition.evidence_status,
                "dimensionless_parameters": {
                    "length": definition.length,
                    "mass": definition.mass,
                    "hbar": definition.hbar,
                    "interior_points": definition.interior_points,
                    "retained_dimension": definition.retained_dimension,
                },
                "boundary_reference": {
                    "kind": definition.boundary_kind,
                    "interpretation": definition.boundary_interpretation,
                },
            },
            "state_spaces": {
                "full": {
                    "identifier": "interior Dirichlet grid coordinates",
                    "dimension": definition.interior_points,
                },
                "retained": {
                    "identifier": "lowest discrete spectral coordinates",
                    "dimension": definition.retained_dimension,
                    "embedding": "columns of retained_eigenvectors",
                },
            },
            "spectra": {
                "computed_discrete": self.vector(result.eigenvalues.magnitude),
                "discrete_closed_form": self.vector(
                    result.discrete_closed_form.magnitude
                ),
                "continuum_closed_form": self.vector(
                    result.continuum_closed_form.magnitude
                ),
                "discrete_to_continuum_ratio": self.vector(
                    result.discrete_closed_form.magnitude
                    / result.continuum_closed_form.magnitude
                ),
            },
            "matrices": {
                "dirichlet_hamiltonian_full": self.sparse_matrix(result.hamiltonian),
                "retained_eigenvectors": self.matrix(result.retained_vectors.magnitude),
                "spectral_projector_full": self.matrix(result.projector.magnitude),
                "retained_hamiltonian_embedded_full": self.matrix(
                    result.retained_embedded.magnitude
                ),
                "retained_hamiltonian_coordinates": self.matrix(
                    result.retained_coordinates.magnitude
                ),
                "cyclic_reference_full": self.matrix(result.cyclic_reference.magnitude),
            },
            "residuals": {
                "consistently_compressed_physical_potential": {
                    "matrix": self.matrix(result.consistently_compressed.magnitude),
                    "interpretation": "zero after applying the same retention map",
                },
                "projected_hamiltonian_minus_unprojected_kinetic": {
                    "matrix": self.matrix(result.unmatched_compression.magnitude),
                    "discarded_sector_reference": self.matrix(
                        result.discarded_sector.magnitude
                    ),
                    "interpretation": "negative discarded kinetic sector",
                },
                "dirichlet_minus_cyclic_reference": {
                    "matrix": self.matrix(result.boundary_realization.magnitude),
                    "interpretation": (
                        "boundary-closure difference on one declared numerical space"
                    ),
                },
            },
            "diagnostics": {
                name: value.magnitude for name, value in result.diagnostics
            },
            "provenance": {
                "input_path": input_file.relative_to(root).as_posix(),
                "input_sha256": self.sha256(input_file),
                "script_path": script_file.relative_to(root).as_posix(),
                "script_sha256": self.sha256(script_file),
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
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    @staticmethod
    def vector(
        value: np.ndarray[tuple[int], np.dtype[np.float64]],
    ) -> list[JsonValue]:
        """Convert one binary64 vector to a JSON array."""
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def matrix(
        value: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> list[JsonValue]:
        """Convert one binary64 matrix to nested JSON arrays."""
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def sparse_matrix(value: SparseMatrixQuantity) -> list[JsonValue]:
        """Convert CSR data to nested JSON arrays one row at a time."""
        if not isinstance(value, SparseMatrixQuantity):
            raise TypeError("value must be SparseMatrixQuantity")
        matrix = value.to_csr()
        rows: list[JsonValue] = []
        for row in range(value.shape[0]):
            dense_row = np.asarray(matrix[row : row + 1, :].toarray())[0]
            rows.append(cast(list[JsonValue], dense_row.tolist()))
        return rows

    @staticmethod
    def contained_file(path: Path, root: Path, name: str) -> Path:
        """Return one existing file resolved beneath ``root``."""
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
    def implementation_paths() -> tuple[Path, ...]:
        """Return exact public source files implementing newly authored results."""
        package_root = Path(__file__).resolve().parents[3]
        model_root = package_root / "analysis" / "model_systems"
        operator_root = package_root / "operators"
        return (
            model_root / "intervals.py",
            model_root / "particle_in_box" / "model.py",
            operator_root / "eigenpairs.py",
            operator_root / "finite_differences.py",
            operator_root / "quantities.py",
            Path(__file__).resolve().with_name("records.py"),
            Path(__file__).resolve().with_name("input.py"),
            Path(__file__).resolve().with_name("residual_study.py"),
            Path(__file__).resolve(),
        )

    @staticmethod
    def sha256(path: Path) -> str:
        """Return one file's lowercase SHA-256 identity."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
