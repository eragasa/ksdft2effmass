"""Version-two serialization for the core particle-in-a-box residual study."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    SparseMatrixQuantity,
)

from ksdft2effmass.hamiltonian import OrthogonalSpectralSubspace

from .records import Piab1dResidualStudyResult

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Piab1dStudyResultSerializer:
    """Serialize one result to the retained version-two JSON representation."""

    __slots__ = ()

    def execute(
        self,
        result: Piab1dResidualStudyResult,
        input_path: Path,
        script_path: Path,
        repository_root: Path,
    ) -> bytes:
        """Serialize one historical result with exact source identities.

        Parameters
        ----------
        result
            Typed retained study result.
        input_path, script_path
            Existing repository-contained producer inputs.
        repository_root
            Root used for containment and relative provenance paths.

        Returns
        -------
        bytes
            Canonical retained version-two JSON bytes.

        Raises
        ------
        TypeError
            A result or path has the wrong type.
        ValueError
            A path escapes the repository or a result invariant is invalid.
        RuntimeError
            Enabled quadrature data is incomplete.
        """
        if not isinstance(result, Piab1dResidualStudyResult):
            raise TypeError("result must be Piab1dResidualStudyResult")
        root = repository_root.resolve()
        input_file = self.contained_file(input_path, root, "input_path")
        script_file = self.contained_file(script_path, root, "script_path")
        definition = result.definition
        reduced_matrix = result.reduced_hamiltonian.matrix
        embedded_matrix = result.reduced_hamiltonian.embedded.matrix
        if not isinstance(reduced_matrix, MatrixQuantity) or not isinstance(
            embedded_matrix, MatrixQuantity
        ):
            raise TypeError("PIAB1D serialization requires real Hamiltonian matrices")
        subspace = result.reduced_hamiltonian.spectral_subspace
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("PIAB1D serialization requires OrthogonalSpectralSubspace")
        projector = subspace.projector
        quadrature: dict[str, JsonValue] = {"enabled": definition.quadrature}
        if definition.quadrature:
            rule = result.quadrature_rule
            quadrature_vectors = result.quadrature_normalized_eigenvectors
            if rule is None or quadrature_vectors is None:
                raise RuntimeError("enabled quadrature result is incomplete")
            retained_quadrature_vectors = quadrature_vectors.magnitude[
                :, : definition.N_retained_eigenpairs
            ]
            weighted_gram = retained_quadrature_vectors.T @ (
                rule.interior_weights[:, None] * retained_quadrature_vectors
            )
            weighted_projector = (
                retained_quadrature_vectors
                @ (rule.interior_weights[:, None] * retained_quadrature_vectors).T
            )
            quadrature = {
                "enabled": True,
                "rule_identifier": rule.rule_identifier,
                "rule_version": rule.rule_version,
                "node_convention": rule.definition.node_convention,
                "full_weight_convention": rule.definition.full_weight_convention,
                "interior_restriction_convention": (
                    rule.definition.interior_restriction_convention
                ),
                "mass_matrix_convention": rule.definition.mass_matrix_convention,
                "interval": list(rule.interval),
                "full_grid_point_count": rule.point_count,
                "interior_full_grid_indices": cast(
                    list[JsonValue], rule.full_grid_indices.tolist()
                ),
                "spacing": rule.spacing,
                "full_weights": cast(
                    list[JsonValue], rule.full_rule.full_weights.tolist()
                ),
                "interior_weights": cast(
                    list[JsonValue], rule.interior_weights.tolist()
                ),
                "diagonal_mass_matrix": {
                    "representation": "diagonal",
                    "diagonal": cast(
                        list[JsonValue], rule.mass_matrix.diagonal.tolist()
                    ),
                },
                "solver_eigenvector_normalization": "euclidean",
                "stored_nodal_amplitude_normalization": (
                    "homogeneous-Dirichlet interior quadrature"
                ),
                "weighted_gram_frobenius_error": float(
                    np.linalg.norm(
                        weighted_gram - np.eye(definition.N_retained_eigenpairs),
                        ord="fro",
                    )
                ),
                "projector_equivalence_frobenius_error": float(
                    np.linalg.norm(
                        weighted_projector - projector.magnitude,
                        ord="fro",
                    )
                ),
            }
        payload: dict[str, JsonValue] = {
            "schema_version": 2,
            "experiment_id": "research-monograph.particle-in-box.v2",
            "evidence_status": "illustrative numerical experiment",
            "calculation_status": "calculated illustrative result",
            "input": {
                "schema_version": 2,
                "experiment_id": "research-monograph.particle-in-box.v2",
                "evidence_status": "illustrative numerical experiment",
                "dimensionless_parameters": {
                    "length": definition.model.length,
                    "mass": definition.model.mass,
                    "interior_points": definition.Nx_pts_interior,
                    "retained_dimension": definition.N_retained_eigenpairs,
                },
                "finite_representation": {
                    "quadrature": definition.quadrature,
                },
                "boundary_reference": {
                    "kind": "cyclic closure on the same finite coordinate space",
                    "interpretation": (
                        "Declared comparison reference only; not a "
                        "representation-independent continuum potential."
                    ),
                },
            },
            "quadrature": quadrature,
            "state_spaces": {
                "full": {
                    "identifier": "interior Dirichlet grid coordinates",
                    "dimension": definition.Nx_pts_interior,
                },
                "retained": {
                    "identifier": "lowest discrete spectral coordinates",
                    "dimension": definition.N_retained_eigenpairs,
                    "embedding": "columns of retained_eigenvectors_euclidean",
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
                "retained_eigenvectors_euclidean": self.matrix(
                    subspace.basis_vectors.magnitude
                ),
                "retained_nodal_amplitudes_quadrature_normalized": (
                    self.matrix(
                        result.quadrature_normalized_eigenvectors.magnitude[
                            :, : definition.N_retained_eigenpairs
                        ]
                    )
                    if result.quadrature_normalized_eigenvectors is not None
                    else None
                ),
                "spectral_projector_full": self.matrix(projector.magnitude),
                "retained_hamiltonian_embedded_full": self.matrix(
                    embedded_matrix.magnitude
                ),
                "retained_hamiltonian_coordinates": self.matrix(
                    reduced_matrix.magnitude
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
                "dependency_identities": [
                    {
                        "distribution": "projectkoios-optimization",
                        "repository": (
                            "https://github.com/eragasa/projectkoios-optimization"
                        ),
                        "revision": ("2a18e485109e307b2f7928bd0418bcf796aeb0d5"),
                        "tree": "77262fed5d75e7ddf01334321f9fb24bf6d5961e",
                        "capabilities": [
                            "projectkoios.numerics.quadrature.uniform_1d",
                            "projectkoios.numerics.quadrature.numpy.uniform_1d",
                            "projectkoios.numerics.linalg.matrix_norm",
                        ],
                    },
                    {
                        "distribution": "projectkoios-physkit",
                        "repository": "https://github.com/eragasa/projectkoios-physkit",
                        "revision": ("9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5"),
                        "tree": "e95aacc3b67bb3718e1e1a49fe3f46f9e16b109f",
                        "capabilities": [
                            "projectkoios.physkit.qm.piab1d",
                            "projectkoios.physkit.qm.piab1d.tise_fd",
                            "projectkoios.physkit.qm.piab1d.tise_analytical",
                            "projectkoios.physkit.qm.sampled_states",
                            "projectkoios.physkit.linalg.eigen",
                            "projectkoios.physkit.linalg.matrix.norm",
                        ],
                    },
                ],
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "floating_point": "IEEE-754 binary64 through numpy.float64",
                "eigensolver": "scipy.linalg.eigh_tridiagonal",
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
        """Convert one historical binary64 vector to a JSON array.

        Parameters
        ----------
        value
            One-dimensional binary64 array.

        Returns
        -------
        list[JsonValue]
            Historical list representation.
        """
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def matrix(
        value: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> list[JsonValue]:
        """Convert one historical binary64 matrix to nested JSON arrays.

        Parameters
        ----------
        value
            Two-dimensional binary64 array.

        Returns
        -------
        list[JsonValue]
            Historical row-major nested-list representation.
        """
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def sparse_matrix(value: SparseMatrixQuantity) -> list[JsonValue]:
        """Convert historical CSR data to dense nested JSON rows.

        Parameters
        ----------
        value
            Real sparse matrix quantity.

        Returns
        -------
        list[JsonValue]
            Historical dense row-major list representation.

        Raises
        ------
        TypeError
            ``value`` is not a sparse matrix quantity.
        """
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
        """Resolve one existing file beneath a provenance root.

        Parameters
        ----------
        path
            Candidate file path.
        root
            Required containing directory.
        name
            Field name used in failure messages.

        Returns
        -------
        pathlib.Path
            Absolute resolved contained file.

        Raises
        ------
        TypeError
            ``path`` is not ``pathlib.Path``.
        ValueError
            The path is not a file or escapes ``root``.
        """
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
        """Return exact source files bound by the historical serializer.

        Returns
        -------
        tuple[pathlib.Path, ...]
            Ordered implementation-file inventory used for provenance hashes.
        """
        package_root = Path(__file__).resolve().parents[3]
        model_root = package_root / "model_systems"
        hamiltonian_root = package_root / "hamiltonian"
        return (
            package_root / "analysis" / "diagnostics.py",
            package_root / "analysis" / "operators" / "eigenpair_diagnostics.py",
            model_root / "analysis.py",
            model_root / "study" / "base.py",
            hamiltonian_root / "blocks.py",
            hamiltonian_root / "decomposition.py",
            hamiltonian_root / "records.py",
            hamiltonian_root / "reduction.py",
            hamiltonian_root / "subspaces.py",
            model_root / "piab1d" / "analysis" / "core.py",
            model_root / "piab1d" / "diagnostics.py",
            Path(__file__).resolve().with_name("records.py"),
            Path(__file__).resolve().with_name("input.py"),
            Path(__file__).resolve().with_name("evaluation.py"),
            Path(__file__).resolve(),
        )

    @staticmethod
    def sha256(path: Path) -> str:
        """Calculate one file's lowercase SHA-256 identity.

        Parameters
        ----------
        path
            Existing readable file.

        Returns
        -------
        str
            Lowercase hexadecimal SHA-256 digest.
        """
        return hashlib.sha256(path.read_bytes()).hexdigest()
