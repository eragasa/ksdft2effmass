"""Multi-norm residual Workflow for the research-monograph particle in a box."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np
from ksdft2effmass.analysis.operators import (
    OrthogonalCompressionResidualAnalyzer,
    RealSymmetricEigenpairDiagnosticAnalyzer,
)
from ksdft2effmass.linalg import (
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    RealSymmetricEigenpairResult,
    RepresentedMatrixNormAnalyzer,
    RepresentedMatrixNormResult,
)
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.units import UnitSystem

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Piab1dNormSweepWorkflow:
    """Decode, evaluate, and serialize the version-one multi-norm campaign."""

    __slots__ = (
        "compression",
        "eigenpair_analyzer",
        "finite_difference_solver",
        "norm_analyzer",
        "residual_analyzer",
        "selector",
    )

    def __init__(self) -> None:
        """Construct the campaign from reusable public operator actions."""
        self.finite_difference_solver = Piab1dTiseFdSolver()
        self.selector = OrthogonalSpectralSubspaceSelector()
        self.compression = OperatorCompression()
        self.norm_analyzer = RepresentedMatrixNormAnalyzer()
        self.residual_analyzer = OrthogonalCompressionResidualAnalyzer()
        self.eigenpair_analyzer = RealSymmetricEigenpairDiagnosticAnalyzer()

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
        if set(values) != {"length", "mass"}:
            raise ValueError("dimensionless_parameters fields do not match schema one")
        length = self.positive_real(values.get("length"), "length")
        mass = self.positive_real(values.get("mass"), "mass")
        model = Piab1D(
            length=length,
            mass=mass,
            unit_system=UnitSystem.NONDIMENSIONAL,
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
            solution = self.finite_difference_solver.solve(
                model=model,
                interior_points=points,
            )
            hamiltonian = CsrRealMatrixQuantity.from_csr(
                solution.hamiltonian.to_csr(),
                Unitless(),
            )
            eigenpairs = RealSymmetricEigenpairResult(
                operator=hamiltonian,
                eigenvalues=VectorQuantity(
                    solution.eigenpairs.eigenvalues,
                    hamiltonian.unit,
                ),
                eigenvectors=RealMatrixQuantity(
                    solution.eigenpairs.eigenvectors,
                    Unitless(),
                ),
            )
            dense_hamiltonian = hamiltonian.to_dense().magnitude
            subspace = self.selector.execute(eigenpairs, retained)
            compression = self.compression.execute(hamiltonian, subspace)
            eigenvalues = eigenpairs.eigenvalues.magnitude
            eigenvectors = eigenpairs.eigenvectors.magnitude
            retained_vectors = subspace.basis_vectors.magnitude
            projector = subspace.projector().magnitude
            retained_coordinates = compression.coordinates.magnitude
            retained_embedded = compression.embedded.magnitude
            exact_discrete = solution.closed_form_discrete_energies().magnitude
            expected_retained = np.diag(exact_discrete[:retained])
            complement = np.eye(points) - projector
            finite_identity_diagnostics: dict[str, JsonValue] = {
                "discrete_spectrum_maximum_absolute_error": float(
                    np.max(np.abs(eigenvalues - exact_discrete))
                ),
                "spectral_reconstruction_frobenius_error": float(
                    np.linalg.norm(
                        dense_hamiltonian
                        - eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T,
                        ord="fro",
                    )
                ),
                "projector_idempotency_frobenius_error": float(
                    np.linalg.norm(projector @ projector - projector, ord="fro")
                ),
                "retained_coordinate_frobenius_error": float(
                    np.linalg.norm(retained_coordinates - expected_retained, ord="fro")
                ),
                "retained_embedding_frobenius_error": float(
                    np.linalg.norm(
                        retained_embedded
                        - retained_vectors @ retained_coordinates @ retained_vectors.T,
                        ord="fro",
                    )
                ),
                "spectral_leakage_frobenius_norm": float(
                    np.linalg.norm(
                        complement @ dense_hamiltonian @ retained_vectors, ord="fro"
                    )
                ),
            }
            compression_residuals = self.residual_analyzer.execute(
                hamiltonian, subspace, compression
            )
            consistent = compression_residuals.consistent.magnitude
            unmatched = compression_residuals.unmatched.magnitude
            cyclic = dense_hamiltonian.copy()
            if points > 1:
                cyclic[0, -1] = dense_hamiltonian[0, 1]
                cyclic[-1, 0] = dense_hamiltonian[1, 0]
            boundary = dense_hamiltonian - cyclic
            algebraic = self.eigenpair_analyzer.execute(
                eigenpairs
            ).algebraic_residual.magnitude
            reference_norms = self.norm_analyzer.execute(hamiltonian)
            residuals: dict[str, JsonValue] = {}
            for name, matrix in (
                ("consistent_compression", consistent),
                ("unmatched_compression", unmatched),
                ("boundary_realization", boundary),
            ):
                norms = self.norm_analyzer.execute(
                    RealMatrixQuantity(matrix, hamiltonian.unit)
                )
                residuals[name] = {
                    "raw": self.norms(norms),
                    "relative_to_hamiltonian": self.norms(
                        norms.normalized_by(reference_norms)
                    ),
                }
            algebraic_norms = self.norm_analyzer.execute(
                RealMatrixQuantity(algebraic, hamiltonian.unit)
            )
            grids.append(
                {
                    "interior_points": points,
                    "spacing": solution.grid_spacing.magnitude,
                    "hamiltonian_norms": self.norms(reference_norms),
                    "finite_identity_diagnostics": finite_identity_diagnostics,
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
            "dependency_identities": self.dependency_identities(),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "floating_point": "IEEE-754 binary64 through numpy.float64",
            "eigensolver": "scipy.linalg.eigh_tridiagonal",
        }

    @staticmethod
    def dependency_identities() -> list[JsonValue]:
        """Return exact external owners used by PIAB1D production."""
        return [
            {
                "distribution": "projectkoios-optimization",
                "repository": "https://github.com/eragasa/projectkoios-optimization",
                "revision": "3cd32ea8985a855bcdbaffbf89af95e970b3bf14",
                "tree": "7596151740065d63e0bcfb61629ea3a57ae760bb",
            },
            {
                "distribution": "projectkoios-physkit",
                "repository": "https://github.com/eragasa/projectkoios-physkit",
                "revision": "2aaa4ba5ff4c51f5c5068ac895ef4ec5de293439",
                "tree": "a85740480be8ca397a9495c362771fa62de55c26",
            },
        ]

    @staticmethod
    def implementation_paths() -> tuple[Path, ...]:
        """Return exact public sources implementing the campaign."""
        source_root = (
            Path(__file__).resolve().parents[3] / "python" / "src" / "ksdft2effmass"
        )
        return (
            source_root / "analysis" / "operators" / "compression_residuals.py",
            source_root / "analysis" / "operators" / "eigenpair_diagnostics.py",
            source_root / "operators" / "eigenpairs.py",
            source_root / "operators" / "subspaces.py",
            source_root / "operators" / "matrix_norms.py",
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
