"""Independent verification of particle-in-a-box residual-study results."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]

HISTORICAL_RUNNER_SHA256 = (
    "e945c0a6320f84b3b32e938e5cf7cd6f779ecf3261846abd67a2ae192a08252d"
)
HISTORICAL_DEPENDENCY_IDENTITIES: list[JsonValue] = [
    {
        "distribution": "projectkoios-optimization",
        "repository": "https://github.com/eragasa/projectkoios-optimization",
        "revision": "3cd32ea8985a855bcdbaffbf89af95e970b3bf14",
        "tree": "7596151740065d63e0bcfb61629ea3a57ae760bb",
        "capabilities": [
            "projectkoios.numerics.quadrature.uniform_1d",
            "projectkoios.numerics.quadrature.numpy.uniform_1d",
        ],
    },
    {
        "distribution": "projectkoios-physkit",
        "repository": "https://github.com/eragasa/projectkoios-physkit",
        "revision": "2aaa4ba5ff4c51f5c5068ac895ef4ec5de293439",
        "tree": "a85740480be8ca397a9495c362771fa62de55c26",
        "capabilities": [
            "projectkoios.physkit.qm.piab1d",
            "projectkoios.physkit.qm.piab1d.tise_fd",
            "projectkoios.physkit.qm.piab1d.tise_analytical",
            "projectkoios.physkit.qm.sampled_states",
        ],
    },
]
CURRENT_DEPENDENCY_IDENTITIES: list[JsonValue] = [
    {
        "distribution": "projectkoios-optimization",
        "repository": "https://github.com/eragasa/projectkoios-optimization",
        "revision": "2a18e485109e307b2f7928bd0418bcf796aeb0d5",
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
        "revision": "9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5",
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
]


class Piab1dResultVerifier:
    """Verify retained or currently authored results without importing producers."""

    __slots__ = ()

    def execute(self, path: Path, repository_root: Path) -> None:
        """Verify one retained result and its exact provenance.

        Parameters
        ----------
        path
            Historical result JSON path.
        repository_root
            Repository root used to resolve recorded evidence paths.

        Returns
        -------
        None
            Completion without an exception signifies passing declared checks.

        Raises
        ------
        TypeError
            A path, document, or field has the wrong type.
        ValueError
            Schema, numerical identity, or provenance authentication fails.
        """
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        payload = self.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), "result"
        )
        schema_version = self.integer(payload["schema_version"], "schema_version")
        if schema_version not in {1, 2}:
            raise ValueError("result schema_version must equal one or two")
        if payload["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("result has an unsupported evidence_status")
        if payload["calculation_status"] != "calculated illustrative result":
            raise ValueError("result has an unsupported calculation_status")
        input_payload = self.mapping(payload["input"], "input")
        if schema_version == 2:
            if (
                self.integer(input_payload["schema_version"], "input schema_version")
                != 2
            ):
                raise ValueError("input schema_version must equal two")
            if input_payload["experiment_id"] != (
                "research-monograph.particle-in-box.v2"
            ):
                raise ValueError("input experiment_id is unsupported")
            if payload["experiment_id"] != input_payload["experiment_id"]:
                raise ValueError("result and input experiment identities must agree")
        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        length = self.real(parameters["length"], "length")
        mass = self.real(parameters["mass"], "mass")
        if length <= 0.0 or mass <= 0.0:
            raise ValueError("length and mass must be positive")
        if schema_version == 1:
            hbar = self.real(parameters["hbar"], "hbar")
        else:
            if set(parameters) != {
                "length",
                "mass",
                "interior_points",
                "retained_dimension",
            }:
                raise ValueError(
                    "dimensionless_parameters fields do not match schema version two"
                )
            hbar = 1.0
        points = self.integer(parameters["interior_points"], "interior_points")
        retained = self.integer(parameters["retained_dimension"], "retained_dimension")
        spacing = length / (points + 1)
        prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        expected_hamiltonian = np.diag(np.full(points, 2.0 * prefactor))
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), 1)
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), -1)
        hamiltonian = self.matrix(payload, "matrices", "dirichlet_hamiltonian_full")
        np.testing.assert_array_equal(hamiltonian, expected_hamiltonian)

        indices = np.arange(1, points + 1, dtype=np.float64)
        z = indices * np.pi / (2.0 * (points + 1))
        expected_discrete = 4.0 * prefactor * np.sin(z) ** 2
        expected_continuum = (
            hbar
            * hbar
            * np.pi
            * np.pi
            * indices
            * indices
            / (2.0 * mass * length * length)
        )
        spectra = self.mapping(payload["spectra"], "spectra")
        computed = self.vector(spectra["computed_discrete"], "computed_discrete")
        recorded_discrete = self.vector(
            spectra["discrete_closed_form"], "discrete_closed_form"
        )
        recorded_continuum = self.vector(
            spectra["continuum_closed_form"], "continuum_closed_form"
        )
        recorded_ratio = self.vector(
            spectra["discrete_to_continuum_ratio"], "discrete_to_continuum_ratio"
        )
        np.testing.assert_array_equal(recorded_discrete, expected_discrete)
        np.testing.assert_allclose(
            recorded_continuum,
            expected_continuum,
            rtol=16.0 * np.finfo(np.float64).eps,
            atol=0.0,
        )
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

        vector_field = (
            "retained_eigenvectors"
            if schema_version == 1
            else "retained_eigenvectors_euclidean"
        )
        vectors = self.matrix(payload, "matrices", vector_field)
        projector = self.matrix(payload, "matrices", "spectral_projector_full")
        embedded = self.matrix(
            payload, "matrices", "retained_hamiltonian_embedded_full"
        )
        coordinates = self.matrix(
            payload, "matrices", "retained_hamiltonian_coordinates"
        )
        tolerance = (
            256.0
            * np.finfo(np.float64).eps
            * float(np.linalg.norm(hamiltonian, ord="fro"))
        )
        np.testing.assert_allclose(
            vectors.T @ vectors, np.eye(retained), atol=tolerance
        )
        np.testing.assert_allclose(projector, vectors @ vectors.T, atol=tolerance)
        np.testing.assert_allclose(projector @ projector, projector, atol=tolerance)
        np.testing.assert_allclose(
            embedded, projector @ hamiltonian @ projector, atol=tolerance
        )
        np.testing.assert_allclose(
            coordinates, vectors.T @ hamiltonian @ vectors, atol=tolerance
        )
        np.testing.assert_allclose(
            coordinates, np.diag(expected_discrete[:retained]), atol=tolerance
        )
        if schema_version == 2:
            self.verify_quadrature(
                payload=payload,
                length=length,
                points=points,
                retained=retained,
                euclidean_vectors=vectors,
                projector=projector,
                tolerance=tolerance,
            )
        diagnostics = self.mapping(payload["diagnostics"], "diagnostics")
        expected_diagnostic_names = {
            "boundary_realization_frobenius_norm",
            "consistently_compressed_residual_frobenius_norm",
            "discrete_spectrum_maximum_absolute_error",
            "projector_complement_frobenius_error",
            "projector_idempotency_frobenius_error",
            "retained_coordinate_frobenius_error",
            "retained_embedding_frobenius_error",
            "spectral_leakage_frobenius_norm",
            "spectral_reconstruction_frobenius_error",
            "unmatched_compression_frobenius_norm",
            "unmatched_equals_discarded_frobenius_error",
        }
        if set(diagnostics) != expected_diagnostic_names:
            raise ValueError("result diagnostics do not match schema version one")
        leakage = float(
            np.linalg.norm(
                (np.eye(points) - projector) @ hamiltonian @ vectors, ord="fro"
            )
        )
        np.testing.assert_allclose(
            self.real(
                diagnostics["spectral_leakage_frobenius_norm"],
                "spectral_leakage_frobenius_norm",
            ),
            leakage,
            rtol=0.0,
            atol=tolerance,
        )

        compressed = self.residual(
            payload, "consistently_compressed_physical_potential", "matrix"
        )
        np.testing.assert_array_equal(compressed, np.zeros((points, points)))
        unmatched = self.residual(
            payload, "projected_hamiltonian_minus_unprojected_kinetic", "matrix"
        )
        discarded = self.residual(
            payload,
            "projected_hamiltonian_minus_unprojected_kinetic",
            "discarded_sector_reference",
        )
        np.testing.assert_allclose(unmatched, embedded - hamiltonian, atol=tolerance)
        np.testing.assert_allclose(unmatched, discarded, atol=tolerance)
        if float(np.linalg.norm(unmatched, ord="fro")) <= tolerance:
            raise ValueError("unmatched compression must retain a discarded sector")
        boundary = self.residual(payload, "dirichlet_minus_cyclic_reference", "matrix")
        expected_boundary = np.zeros((points, points))
        expected_boundary[0, -1] = prefactor
        expected_boundary[-1, 0] = prefactor
        np.testing.assert_array_equal(boundary, expected_boundary)
        if payload["limitations"] != [
            "The finite matrix is not the continuum differential operator.",
            (
                "The cyclic-reference residual is not a "
                "representation-independent potential."
            ),
            "The result is not semiconductor evidence or scientific validation.",
        ]:
            raise ValueError("result limitations do not match schema version one")
        self.verify_provenance(
            payload,
            repository_root.resolve(),
            schema_version,
        )

    def verify_quadrature(
        self,
        *,
        payload: dict[str, JsonValue],
        length: float,
        points: int,
        retained: int,
        euclidean_vectors: RealMatrix,
        projector: RealMatrix,
        tolerance: float,
    ) -> None:
        """Independently verify retained version-two quadrature evidence.

        Parameters
        ----------
        payload
            Decoded historical result document.
        length, points, retained
            Declared box length, interior dimension, and retained dimension.
        euclidean_vectors, projector
            Independently checked retained vectors and projector.
        tolerance
            Absolute numerical comparison tolerance.

        Returns
        -------
        None
            Completion signifies agreement with the retained quadrature contract.

        Raises
        ------
        TypeError
            A quadrature field has the wrong JSON type.
        ValueError
            Metadata, dimensions, or reconstructed identities disagree.
        """
        input_payload = self.mapping(payload["input"], "input")
        representation = self.mapping(
            input_payload["finite_representation"],
            "finite_representation",
        )
        if set(representation) != {"quadrature"}:
            raise ValueError("finite_representation fields do not match schema two")
        enabled = representation["quadrature"]
        if type(enabled) is not bool:
            raise TypeError("quadrature must be a JSON Boolean")
        quadrature = self.mapping(payload["quadrature"], "quadrature")
        matrices = self.mapping(payload["matrices"], "matrices")
        nodal_values = matrices["retained_nodal_amplitudes_quadrature_normalized"]
        if not enabled:
            if quadrature != {"enabled": False}:
                raise ValueError("disabled quadrature must retain only its status")
            if nodal_values is not None:
                raise ValueError("disabled quadrature must not retain nodal amplitudes")
            return
        if quadrature.get("enabled") is not True:
            raise ValueError("enabled quadrature status is inconsistent")
        expected_fields = {
            "enabled",
            "rule_identifier",
            "rule_version",
            "node_convention",
            "full_weight_convention",
            "interior_restriction_convention",
            "mass_matrix_convention",
            "interval",
            "full_grid_point_count",
            "interior_full_grid_indices",
            "spacing",
            "full_weights",
            "interior_weights",
            "diagonal_mass_matrix",
            "solver_eigenvector_normalization",
            "stored_nodal_amplitude_normalization",
            "weighted_gram_frobenius_error",
            "projector_equivalence_frobenius_error",
        }
        if set(quadrature) != expected_fields:
            raise ValueError("quadrature fields do not match schema version two")
        spacing = length / (points + 1)
        expected_full_weights = np.full(points + 2, spacing, dtype=np.float64)
        expected_full_weights[0] = 0.5 * spacing
        expected_full_weights[-1] = 0.5 * spacing
        expected_indices = np.arange(1, points + 1, dtype=np.int64)
        expected_interior_weights = np.full(points, spacing, dtype=np.float64)
        if quadrature.get("rule_identifier") != (
            "projectkoios.numerics.quadrature.uniform_closed_interval_trapezoidal"
        ):
            raise ValueError("quadrature rule_identifier is unsupported")
        if self.integer(quadrature["rule_version"], "rule_version") != 1:
            raise ValueError("quadrature rule_version is unsupported")
        expected_conventions = {
            "node_convention": "endpoint-inclusive-uniform-closed-interval",
            "full_weight_convention": "composite-trapezoidal",
            "interior_restriction_convention": ("homogeneous-dirichlet-interior-nodes"),
            "mass_matrix_convention": "diagonal-lumped-diag-weights",
            "solver_eigenvector_normalization": "euclidean",
            "stored_nodal_amplitude_normalization": (
                "homogeneous-Dirichlet interior quadrature"
            ),
        }
        for name, expected in expected_conventions.items():
            if quadrature.get(name) != expected:
                raise ValueError(f"quadrature {name} is unsupported")
        interval = self.vector(quadrature["interval"], "quadrature interval")
        np.testing.assert_array_equal(interval, np.array([0.0, length]))
        if (
            self.integer(quadrature["full_grid_point_count"], "full_grid_point_count")
            != points + 2
        ):
            raise ValueError("quadrature full_grid_point_count is inconsistent")
        np.testing.assert_array_equal(
            self.vector(
                quadrature["interior_full_grid_indices"],
                "interior_full_grid_indices",
            ),
            expected_indices,
        )
        np.testing.assert_array_equal(
            self.vector(quadrature["full_weights"], "full_weights"),
            expected_full_weights,
        )
        interior_weights = self.vector(
            quadrature["interior_weights"], "interior_weights"
        )
        np.testing.assert_array_equal(interior_weights, expected_interior_weights)
        np.testing.assert_array_equal(
            self.vector(
                self.mapping(
                    quadrature["diagonal_mass_matrix"],
                    "diagonal_mass_matrix",
                )["diagonal"],
                "diagonal_mass_matrix.diagonal",
            ),
            expected_interior_weights,
        )
        if (
            self.mapping(
                quadrature["diagonal_mass_matrix"], "diagonal_mass_matrix"
            ).get("representation")
            != "diagonal"
        ):
            raise ValueError("quadrature mass matrix representation is unsupported")
        recorded_spacing = self.real(quadrature["spacing"], "quadrature spacing")
        if recorded_spacing != spacing:
            raise ValueError("quadrature spacing is inconsistent")
        if not isinstance(nodal_values, list):
            raise TypeError("quadrature-normalized nodal amplitudes must be an array")
        nodal = np.asarray(nodal_values, dtype=np.float64)
        expected_nodal = euclidean_vectors / np.sqrt(spacing)
        np.testing.assert_allclose(
            nodal,
            expected_nodal,
            rtol=0.0,
            atol=tolerance,
        )
        weighted_gram_error = float(
            np.linalg.norm(
                nodal.T @ (interior_weights[:, None] * nodal) - np.eye(retained),
                ord="fro",
            )
        )
        weighted_projector_error = float(
            np.linalg.norm(
                nodal @ (interior_weights[:, None] * nodal).T - projector,
                ord="fro",
            )
        )
        np.testing.assert_allclose(
            self.real(
                quadrature["weighted_gram_frobenius_error"],
                "weighted_gram_frobenius_error",
            ),
            weighted_gram_error,
            rtol=0.0,
            atol=tolerance,
        )
        np.testing.assert_allclose(
            self.real(
                quadrature["projector_equivalence_frobenius_error"],
                "projector_equivalence_frobenius_error",
            ),
            weighted_projector_error,
            rtol=0.0,
            atol=tolerance,
        )

    def verify_provenance(
        self,
        payload: dict[str, JsonValue],
        repository_root: Path,
        schema_version: int,
    ) -> None:
        """Verify a supported historical implementation-identity profile.

        Parameters
        ----------
        payload
            Decoded historical result document.
        repository_root
            Root containing every recorded evidence path.
        schema_version
            Supported retained schema version.

        Returns
        -------
        None
            Completion signifies exact path and SHA-256 agreement.

        Raises
        ------
        TypeError
            A provenance field has the wrong JSON type.
        ValueError
            A path, dependency profile, source inventory, or digest differs.
        """
        provenance = self.mapping(payload["provenance"], "provenance")
        current_profile = False
        if schema_version == 2:
            dependency_identities = provenance.get("dependency_identities")
            if dependency_identities == CURRENT_DEPENDENCY_IDENTITIES:
                current_profile = True
            elif dependency_identities != HISTORICAL_DEPENDENCY_IDENTITIES:
                raise ValueError(
                    "dependency identities do not match a supported schema-two profile"
                )
        input_path = self.evidence_path(
            repository_root,
            self.string(provenance["input_path"], "input_path"),
        )
        if hashlib.sha256(input_path.read_bytes()).hexdigest() != self.string(
            provenance["input_sha256"], "input_sha256"
        ):
            raise ValueError("input_sha256 does not match input_path")
        recorded_runner = self.string(provenance["script_sha256"], "script_sha256")
        identities = provenance.get("implementation_identities")
        if identities is None:
            if recorded_runner != HISTORICAL_RUNNER_SHA256:
                raise ValueError("unrecognized historical runner identity")
            return
        if not isinstance(identities, list):
            raise TypeError("implementation_identities must be a JSON array")
        if schema_version == 1:
            expected = {
                "python/src/ksdft2effmass/model_systems/intervals.py",
                "python/src/ksdft2effmass/model_systems/piab1d/model.py",
                "python/src/ksdft2effmass/model_systems/study/base.py",
                "python/src/ksdft2effmass/operators/eigenpairs.py",
                "python/src/ksdft2effmass/operators/finite_differences.py",
                "python/src/ksdft2effmass/linalg/quantities.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/records.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/input.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/evaluation.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/serialization.py",
            }
        elif current_profile:
            expected = {
                "python/src/ksdft2effmass/analysis/diagnostics.py",
                "python/src/ksdft2effmass/analysis/operators/eigenpair_diagnostics.py",
                "python/src/ksdft2effmass/model_systems/analysis.py",
                "python/src/ksdft2effmass/model_systems/study/base.py",
                "python/src/ksdft2effmass/hamiltonian/blocks.py",
                "python/src/ksdft2effmass/hamiltonian/decomposition.py",
                "python/src/ksdft2effmass/hamiltonian/records.py",
                "python/src/ksdft2effmass/hamiltonian/reduction.py",
                "python/src/ksdft2effmass/hamiltonian/subspaces.py",
                "python/src/ksdft2effmass/model_systems/piab1d/analysis/core.py",
                "python/src/ksdft2effmass/model_systems/piab1d/diagnostics.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/records.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/input.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/evaluation.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/serialization.py",
            }
        else:
            expected = {
                "python/src/ksdft2effmass/model_systems/study/base.py",
                "python/src/ksdft2effmass/operators/eigenpairs.py",
                "python/src/ksdft2effmass/operators/quantities.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/records.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/input.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/evaluation.py",
                "python/src/ksdft2effmass/model_systems/piab1d/study/serialization.py",
            }
        observed: set[str] = set()
        for value in identities:
            identity = self.mapping(value, "implementation identity")
            relative = self.string(identity["path"], "implementation path")
            observed.add(relative)
            source = repository_root / relative
            if not source.is_file():
                raise ValueError("implementation source path is unavailable")
            if hashlib.sha256(source.read_bytes()).hexdigest() != self.string(
                identity["sha256"], "implementation sha256"
            ):
                raise ValueError("implementation sha256 does not match its path")
        if observed != expected:
            raise ValueError("implementation identity paths do not match")
        script_path = self.evidence_path(
            repository_root,
            self.string(provenance["script_path"], "script_path"),
        )
        if hashlib.sha256(script_path.read_bytes()).hexdigest() != recorded_runner:
            raise ValueError("script_sha256 does not match script_path")

    @staticmethod
    def evidence_path(repository_root: Path, relative: str) -> Path:
        """Resolve a current or relocated historical evidence path.

        Parameters
        ----------
        repository_root
            Current repository root.
        relative
            Recorded repository-relative path.

        Returns
        -------
        pathlib.Path
            Current filesystem locator preserving the explicit historical relocation.
        """
        historical_prefix = "calculations/research-monograph/particle-in-box/"
        if relative.startswith(historical_prefix):
            relative = "calculations/piab1d/" + relative.removeprefix(historical_prefix)
        return repository_root / relative

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Validate one JSON object with string keys.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        dict[str, JsonValue]
            Validated object.

        Raises
        ------
        TypeError
            The value is not a string-keyed object.
        """
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Validate one nonempty JSON string.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        str
            Nonempty string.

        Raises
        ------
        TypeError
            The value is not a nonempty string.
        """
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Validate one built-in integer excluding booleans.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        int
            Exact built-in integer.

        Raises
        ------
        TypeError
            The value is Boolean or not an integer.
        """
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Validate one finite JSON real excluding booleans.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        float
            Finite built-in floating-point value.

        Raises
        ------
        TypeError
            The value is Boolean or nonnumeric.
        ValueError
            The converted value is nonfinite.
        """
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def vector(value: JsonValue, name: str) -> npt.NDArray[np.float64]:
        """Decode one historical binary64 vector.

        Parameters
        ----------
        value
            JSON array.
        name
            Field name used in failure messages.

        Returns
        -------
        numpy.ndarray
            Binary64 array.

        Raises
        ------
        TypeError
            The value is not a JSON array.
        """
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return np.asarray(value, dtype=np.float64)

    def matrix(
        self, payload: dict[str, JsonValue], section: str, name: str
    ) -> RealMatrix:
        """Decode one matrix from a named result section.

        Parameters
        ----------
        payload
            Decoded result document.
        section
            Top-level matrix section name.
        name
            Matrix field name.

        Returns
        -------
        RealMatrix
            Binary64 matrix.

        Raises
        ------
        TypeError
            The section or matrix is not represented by a JSON object or array.
        """
        values = self.mapping(payload[section], section)[name]
        if not isinstance(values, list):
            raise TypeError(f"{name} must be a JSON array")
        return np.asarray(values, dtype=np.float64)

    def residual(
        self, payload: dict[str, JsonValue], name: str, field: str
    ) -> RealMatrix:
        """Decode one historical residual matrix field.

        Parameters
        ----------
        payload
            Decoded result document.
        name
            Residual-record name.
        field
            Matrix field within the residual record.

        Returns
        -------
        RealMatrix
            Binary64 residual matrix.

        Raises
        ------
        TypeError
            The residual record or matrix has the wrong JSON representation.
        """
        residuals = self.mapping(payload["residuals"], "residuals")
        record = self.mapping(residuals[name], name)
        values = record[field]
        if not isinstance(values, list):
            raise TypeError(f"{name}.{field} must be a JSON array")
        return np.asarray(values, dtype=np.float64)
