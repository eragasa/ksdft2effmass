r"""Independent report-based verification of core PIAB1D results.

The verifier decodes the retained version-one JSON representation directly and
reconstructs its finite-difference Hamiltonian, spectra, retained subspace, and three
operator residuals without importing the producing model, operator, evaluator,
serializer, or Workflow modules. Source-identity authentication and numerical
reconstruction are retained as separate ResultObjects.

A passing report establishes only the stated finite, dimensionless numerical
identities and admitted source identities. It does not establish continuum
convergence, semiconductor relevance, scientific validation, uncertainty
quantification, or human acceptance.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

import numpy as np
import numpy.typing as npt

from .decoder import JsonValue, Piab1dResultDecoder
from .records import (
    Piab1dNumericalVerificationResult,
    Piab1dVerificationCheck,
    Piab1dVerificationResult,
)
from .source import (
    Piab1dSourceAuthenticationResult,
    Piab1dSourceAuthenticator,
)

type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]

HISTORICAL_RUNNER_SHA256 = (
    "e945c0a6320f84b3b32e938e5cf7cd6f779ecf3261846abd67a2ae192a08252d"
)


class Piab1dNumericalVerificationChannel(StrEnum):
    """Identify each independently reconstructed core numerical channel."""

    DIRICHLET_HAMILTONIAN = "dirichlet_hamiltonian"
    DISCRETE_CLOSED_FORM = "discrete_closed_form"
    CONTINUUM_CLOSED_FORM = "continuum_closed_form"
    DISCRETE_TO_CONTINUUM_RATIO = "discrete_to_continuum_ratio"
    COMPUTED_DISCRETE_SPECTRUM = "computed_discrete_spectrum"
    RETAINED_BASIS_ORTHONORMALITY = "retained_basis_orthonormality"
    PROJECTOR_DEFINITION = "projector_definition"
    PROJECTOR_IDEMPOTENCY = "projector_idempotency"
    EMBEDDED_REDUCTION = "embedded_reduction"
    RETAINED_COORDINATE_REDUCTION = "retained_coordinate_reduction"
    RETAINED_COORDINATE_DIAGONALIZATION = "retained_coordinate_diagonalization"
    CONSISTENT_COMPRESSION = "consistent_compression"
    UNMATCHED_COMPRESSION = "unmatched_compression"
    DISCARDED_SECTOR = "discarded_sector"
    BOUNDARY_REALIZATION = "boundary_realization"


class Piab1dResultsVerifier(Piab1dResultDecoder):
    """Verify one core PIAB1D result without importing its producer.

    The stateless ActionObject rejects malformed version-one documents, but represents
    content-identity disagreement and numerical disagreement in the returned report.
    This distinction lets callers inspect independent source-authentication and
    numerical-reconstruction outcomes without converting either into the other.
    """

    __slots__ = ()

    expected_implementation_paths = (
        "python/src/ksdft2effmass/analysis/model_systems/intervals.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/model.py",
        "python/src/ksdft2effmass/operators/eigenpairs.py",
        "python/src/ksdft2effmass/operators/finite_differences.py",
        "python/src/ksdft2effmass/operators/quantities.py",
        "python/src/ksdft2effmass/campaigns/piab1d/records.py",
        "python/src/ksdft2effmass/campaigns/piab1d/input.py",
        "python/src/ksdft2effmass/campaigns/piab1d/residual_study.py",
        "python/src/ksdft2effmass/campaigns/piab1d/serialization.py",
    )

    def execute(self, path: Path, repository_root: Path) -> Piab1dVerificationResult:
        """Verify one retained or newly authored version-one result.

        Parameters
        ----------
        path
            Existing UTF-8 JSON result file.
        repository_root
            Existing repository directory used to resolve declared relative source
            paths. Resolved source paths must remain beneath this directory.

        Returns
        -------
        Piab1dVerificationResult
            Separate source-authentication and numerical-reconstruction ResultObjects
            plus their derived aggregate disposition.

        Raises
        ------
        TypeError
            If paths or represented JSON values have incorrect semantic types.
        ValueError
            If a path, wire invariant, shape, finite-value requirement, version-one
            status, or limitation contract is invalid.
        """
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        root = repository_root.resolve()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        payload = self.decode(path)
        self.validate_document_contract(payload)
        source_authentication = self.authenticate_sources(payload, root)
        numerical_reconstruction = self.reconstruct_numerics(payload)
        return Piab1dVerificationResult(source_authentication, numerical_reconstruction)

    def validate_document_contract(self, payload: dict[str, JsonValue]) -> None:
        """Validate structural and status fields required before reconstruction."""
        if self.integer(payload["schema_version"], "schema_version") != 1:
            raise ValueError("result schema_version must equal one")
        if payload["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("result has an unsupported evidence_status")
        if payload["calculation_status"] != "calculated illustrative result":
            raise ValueError("result has an unsupported calculation_status")
        input_payload = self.mapping(payload["input"], "input")
        if self.integer(input_payload["schema_version"], "input.schema_version") != 1:
            raise ValueError("input schema_version must equal one")
        if input_payload["evidence_status"] != payload["evidence_status"]:
            raise ValueError("input and result evidence_status values must agree")
        if input_payload["experiment_id"] != payload["experiment_id"]:
            raise ValueError("input and result experiment_id values must agree")
        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        for name in ("length", "mass", "hbar"):
            if self.real(parameters[name], name) <= 0.0:
                raise ValueError(f"{name} must be positive")
        points = self.integer(parameters["interior_points"], "interior_points")
        retained = self.integer(parameters["retained_dimension"], "retained_dimension")
        if points <= 0:
            raise ValueError("interior_points must be positive")
        if retained <= 0 or retained > points:
            raise ValueError(
                "retained_dimension must be positive and not exceed interior_points"
            )
        boundary = self.mapping(
            input_payload["boundary_reference"], "boundary_reference"
        )
        if boundary["kind"] != "cyclic closure on the same finite coordinate space":
            raise ValueError("boundary reference kind is unsupported")
        if boundary["interpretation"] != (
            "Declared comparison reference only; not a "
            "representation-independent continuum potential."
        ):
            raise ValueError("boundary reference interpretation is unsupported")
        if payload["limitations"] != [
            "The finite matrix is not the continuum differential operator.",
            (
                "The cyclic-reference residual is not a "
                "representation-independent potential."
            ),
            "The result is not semiconductor evidence or scientific validation.",
        ]:
            raise ValueError("result limitations do not match schema version one")

    def authenticate_sources(
        self, payload: dict[str, JsonValue], repository_root: Path
    ) -> Piab1dSourceAuthenticationResult:
        """Decode a source-authentication request and execute its shared policy."""
        provenance = self.mapping(payload["provenance"], "provenance")
        return Piab1dSourceAuthenticator().execute(
            provenance,
            repository_root,
            self.expected_implementation_paths,
            HISTORICAL_RUNNER_SHA256,
        )

    def reconstruct_numerics(
        self, payload: dict[str, JsonValue]
    ) -> Piab1dNumericalVerificationResult:
        """Independently reconstruct every supported finite numerical channel."""
        input_payload = self.mapping(payload["input"], "input")
        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        length = self.real(parameters["length"], "length")
        mass = self.real(parameters["mass"], "mass")
        hbar = self.real(parameters["hbar"], "hbar")
        points = self.integer(parameters["interior_points"], "interior_points")
        retained = self.integer(parameters["retained_dimension"], "retained_dimension")
        spacing = length / (points + 1)
        prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        expected_hamiltonian = np.diag(np.full(points, 2.0 * prefactor))
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), 1)
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), -1)
        hamiltonian = self.section_matrix(
            payload,
            "matrices",
            "dirichlet_hamiltonian_full",
            (points, points),
        )

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
        expected_ratio = (np.sin(z) / z) ** 2
        spectra = self.mapping(payload["spectra"], "spectra")
        computed = self.vector(
            spectra["computed_discrete"], "computed_discrete", points
        )
        recorded_discrete = self.vector(
            spectra["discrete_closed_form"], "discrete_closed_form", points
        )
        recorded_continuum = self.vector(
            spectra["continuum_closed_form"], "continuum_closed_form", points
        )
        recorded_ratio = self.vector(
            spectra["discrete_to_continuum_ratio"],
            "discrete_to_continuum_ratio",
            points,
        )

        vectors = self.section_matrix(
            payload,
            "matrices",
            "retained_eigenvectors",
            (points, retained),
        )
        projector = self.section_matrix(
            payload, "matrices", "spectral_projector_full", (points, points)
        )
        embedded = self.section_matrix(
            payload,
            "matrices",
            "retained_hamiltonian_embedded_full",
            (points, points),
        )
        coordinates = self.section_matrix(
            payload,
            "matrices",
            "retained_hamiltonian_coordinates",
            (retained, retained),
        )
        tolerance = float(
            256.0 * np.finfo(np.float64).eps * np.linalg.norm(hamiltonian, ord="fro")
        )
        spectrum_scale = float(np.max(np.abs(expected_discrete)))
        ratio_scale = float(np.max(np.abs(expected_ratio)))

        compressed = self.residual(
            payload,
            "consistently_compressed_physical_potential",
            "matrix",
            (points, points),
        )
        unmatched = self.residual(
            payload,
            "projected_hamiltonian_minus_unprojected_kinetic",
            "matrix",
            (points, points),
        )
        discarded = self.residual(
            payload,
            "projected_hamiltonian_minus_unprojected_kinetic",
            "discarded_sector_reference",
            (points, points),
        )
        boundary = self.residual(
            payload,
            "dirichlet_minus_cyclic_reference",
            "matrix",
            (points, points),
        )
        expected_boundary = np.zeros((points, points))
        if points > 1:
            expected_boundary[0, -1] = prefactor
            expected_boundary[-1, 0] = prefactor

        checks = (
            self.numerical_check(
                Piab1dNumericalVerificationChannel.DIRICHLET_HAMILTONIAN,
                hamiltonian,
                expected_hamiltonian,
                0.0,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.DISCRETE_CLOSED_FORM,
                recorded_discrete,
                expected_discrete,
                0.0,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.CONTINUUM_CLOSED_FORM,
                recorded_continuum,
                expected_continuum,
                0.0,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.DISCRETE_TO_CONTINUUM_RATIO,
                recorded_ratio,
                expected_ratio,
                float(16.0 * np.finfo(np.float64).eps * ratio_scale),
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.COMPUTED_DISCRETE_SPECTRUM,
                computed,
                expected_discrete,
                float(128.0 * np.finfo(np.float64).eps * spectrum_scale),
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.RETAINED_BASIS_ORTHONORMALITY,
                vectors.T @ vectors,
                np.eye(retained),
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.PROJECTOR_DEFINITION,
                projector,
                vectors @ vectors.T,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.PROJECTOR_IDEMPOTENCY,
                projector @ projector,
                projector,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.EMBEDDED_REDUCTION,
                embedded,
                projector @ hamiltonian @ projector,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.RETAINED_COORDINATE_REDUCTION,
                coordinates,
                vectors.T @ hamiltonian @ vectors,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.RETAINED_COORDINATE_DIAGONALIZATION,
                coordinates,
                np.diag(expected_discrete[:retained]),
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.CONSISTENT_COMPRESSION,
                compressed,
                np.zeros((points, points)),
                0.0,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.UNMATCHED_COMPRESSION,
                unmatched,
                embedded - hamiltonian,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.DISCARDED_SECTOR,
                discarded,
                unmatched,
                tolerance,
            ),
            self.numerical_check(
                Piab1dNumericalVerificationChannel.BOUNDARY_REALIZATION,
                boundary,
                expected_boundary,
                0.0,
            ),
        )
        discarded_norm = np.linalg.norm(unmatched, ord="fro").item()
        return Piab1dNumericalVerificationResult(
            checks,
            tuple(Piab1dNumericalVerificationChannel),
            discarded_sector_is_resolved=discarded_norm > tolerance,
            discarded_sector_expected=retained < points,
        )

    @staticmethod
    def numerical_check(
        channel: Piab1dNumericalVerificationChannel,
        observed: RealMatrix | RealVector,
        expected: RealMatrix | RealVector,
        absolute_tolerance: float,
    ) -> Piab1dVerificationCheck:
        """Return one maximum elementwise absolute-defect result."""
        defect = float(np.max(np.abs(observed - expected), initial=0.0))
        return Piab1dVerificationCheck(channel, defect, absolute_tolerance)

    @classmethod
    def vector(cls, value: JsonValue, name: str, length: int) -> RealVector:
        """Decode one finite binary64 vector of an exact length."""
        vector = np.asarray(cls.real_sequence(value, name), dtype=np.float64)
        if vector.shape != (length,):
            raise ValueError(f"{name} must have length {length}")
        return vector

    def section_matrix(
        self,
        payload: dict[str, JsonValue],
        section: str,
        name: str,
        shape: tuple[int, int],
    ) -> RealMatrix:
        """Decode one finite matrix with an exact shape from a result section."""
        values = self.mapping(payload[section], section)[name]
        return self.matrix_value(values, name, shape)

    def residual(
        self,
        payload: dict[str, JsonValue],
        name: str,
        field: str,
        shape: tuple[int, int],
    ) -> RealMatrix:
        """Decode one finite residual-matrix field with an exact shape."""
        residuals = self.mapping(payload["residuals"], "residuals")
        record = self.mapping(residuals[name], name)
        return self.matrix_value(record[field], f"{name}.{field}", shape)

    @classmethod
    def matrix_value(
        cls, value: JsonValue, name: str, shape: tuple[int, int]
    ) -> RealMatrix:
        """Decode one finite binary64 matrix with an exact shape."""
        matrix = cls.matrix(value, name)
        if matrix.shape != shape:
            raise ValueError(f"{name} must have shape {shape}")
        return matrix
