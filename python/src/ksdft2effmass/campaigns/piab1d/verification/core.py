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

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import numpy as np
import numpy.typing as npt

from .decoder import JsonValue, ParticleInBoxCampaignResultDecoder
from .source import (
    ParticleInBoxSourceAuthenticationRequest,
    ParticleInBoxSourceAuthenticationResult,
    ParticleInBoxSourceAuthenticator,
    ParticleInBoxSourceIdentity,
    ParticleInBoxSourceIdentityRole,
)

type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]

HISTORICAL_RUNNER_SHA256 = (
    "e945c0a6320f84b3b32e938e5cf7cd6f779ecf3261846abd67a2ae192a08252d"
)


class ParticleInBoxNumericalVerificationChannel(StrEnum):
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


@dataclass(frozen=True, slots=True)
class ParticleInBoxNumericalCheckResult:
    """Retain one maximum absolute defect and its inclusive tolerance.

    Parameters
    ----------
    channel
        Independently reconstructed numerical identity.
    maximum_absolute_defect
        Maximum elementwise absolute retained-versus-reconstructed defect in the
        dimensionless convention of the result.
    absolute_tolerance
        Inclusive absolute acceptance threshold in the same represented convention.
    """

    channel: ParticleInBoxNumericalVerificationChannel
    maximum_absolute_defect: float
    absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact channel typing and finite nonnegative values."""
        if type(self.channel) is not ParticleInBoxNumericalVerificationChannel:
            raise TypeError("channel must be ParticleInBoxNumericalVerificationChannel")
        for name, value in (
            ("maximum_absolute_defect", self.maximum_absolute_defect),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def passes(self) -> bool:
        """Return whether the defect satisfies its inclusive tolerance."""
        return self.maximum_absolute_defect <= self.absolute_tolerance


@dataclass(frozen=True, slots=True)
class ParticleInBoxNumericalVerificationResult:
    """Retain every core reconstruction check and the discarded-sector condition.

    Parameters
    ----------
    checks
        Exactly one check for every
        :class:`ParticleInBoxNumericalVerificationChannel` member.
    discarded_sector_frobenius_norm
        Frobenius norm of the unmatched-compression residual.
    discarded_sector_absolute_tolerance
        Scale-aware threshold below which that residual does not resolve a discarded
        sector.
    discarded_sector_expected
        Whether the retained dimension is smaller than the full dimension and must
        therefore leave a nonzero discarded sector.
    """

    checks: tuple[ParticleInBoxNumericalCheckResult, ...]
    discarded_sector_frobenius_norm: float
    discarded_sector_absolute_tolerance: float
    discarded_sector_expected: bool

    def __post_init__(self) -> None:
        """Validate complete unique channels and finite discarded-sector values."""
        if not isinstance(self.checks, tuple) or any(
            type(check) is not ParticleInBoxNumericalCheckResult
            for check in self.checks
        ):
            raise TypeError("checks must be a tuple of numerical check results")
        channels = tuple(check.channel for check in self.checks)
        if len(set(channels)) != len(channels):
            raise ValueError("numerical verification channels must be unique")
        if set(channels) != set(ParticleInBoxNumericalVerificationChannel):
            raise ValueError("numerical verification channels must be complete")
        for name, value in (
            ("discarded_sector_frobenius_norm", self.discarded_sector_frobenius_norm),
            (
                "discarded_sector_absolute_tolerance",
                self.discarded_sector_absolute_tolerance,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.discarded_sector_expected) is not bool:
            raise TypeError("discarded_sector_expected must be a built-in bool")

    @property
    def discarded_sector_is_resolved(self) -> bool:
        """Return whether unmatched compression contains a nonzero discarded sector."""
        return (
            self.discarded_sector_frobenius_norm
            > self.discarded_sector_absolute_tolerance
        )

    @property
    def discarded_sector_condition_satisfied(self) -> bool:
        """Return whether the residual agrees with the declared truncation dimension."""
        return self.discarded_sector_is_resolved is self.discarded_sector_expected

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded numerical-reconstruction disposition."""
        return self.discarded_sector_condition_satisfied and all(
            check.passes for check in self.checks
        )

    @property
    def check_count(self) -> int:
        """Return the count derived from the reconstructed check collection."""
        return len(self.checks)


@dataclass(frozen=True, slots=True)
class ParticleInBoxVerificationResult:
    """Retain separate source and numerical verification outcomes.

    Parameters
    ----------
    source_authentication
        Result of checking retained input, runner, and current implementation
        identities without treating identity agreement as numerical verification.
    numerical_reconstruction
        Result of independently reconstructing the finite represented mathematics.
    """

    source_authentication: ParticleInBoxSourceAuthenticationResult
    numerical_reconstruction: ParticleInBoxNumericalVerificationResult

    def __post_init__(self) -> None:
        """Validate exact constituent ResultObject types."""
        if (
            type(self.source_authentication)
            is not ParticleInBoxSourceAuthenticationResult
        ):
            raise TypeError(
                "source_authentication must be ParticleInBoxSourceAuthenticationResult"
            )
        if (
            type(self.numerical_reconstruction)
            is not ParticleInBoxNumericalVerificationResult
        ):
            raise TypeError(
                "numerical_reconstruction must be "
                "ParticleInBoxNumericalVerificationResult"
            )

    @property
    def passes(self) -> bool:
        """Return true only when source and numerical channels both pass."""
        return (
            self.source_authentication.passes and self.numerical_reconstruction.passes
        )


class ParticleInBoxResultVerifier(ParticleInBoxCampaignResultDecoder):
    """Verify one core PIAB1D result without importing its producer.

    The stateless ActionObject rejects malformed version-one documents, but represents
    content-identity disagreement and numerical disagreement in the returned report.
    This distinction lets callers inspect independent source-authentication and
    numerical-reconstruction outcomes without converting either into the other.
    """

    __slots__ = ("source_authenticator",)

    def __init__(
        self, source_authenticator: ParticleInBoxSourceAuthenticator | None = None
    ) -> None:
        """Construct with an explicit or default source authenticator."""
        if source_authenticator is not None and not isinstance(
            source_authenticator, ParticleInBoxSourceAuthenticator
        ):
            raise TypeError(
                "source_authenticator must be ParticleInBoxSourceAuthenticator or None"
            )
        self.source_authenticator = (
            source_authenticator or ParticleInBoxSourceAuthenticator()
        )

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

    def execute(
        self, path: Path, repository_root: Path
    ) -> ParticleInBoxVerificationResult:
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
        ParticleInBoxVerificationResult
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
        return ParticleInBoxVerificationResult(
            source_authentication, numerical_reconstruction
        )

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
    ) -> ParticleInBoxSourceAuthenticationResult:
        """Decode a source-authentication request and execute its shared policy."""
        provenance = self.mapping(payload["provenance"], "provenance")
        identities = [
            ParticleInBoxSourceIdentity(
                ParticleInBoxSourceIdentityRole.INPUT,
                self.string(provenance["input_path"], "input_path"),
                self.sha256_string(provenance["input_sha256"], "input_sha256"),
            )
        ]
        identities.append(
            ParticleInBoxSourceIdentity(
                ParticleInBoxSourceIdentityRole.RUNNER,
                self.string(provenance["script_path"], "script_path"),
                self.sha256_string(provenance["script_sha256"], "script_sha256"),
            )
        )
        encoded = provenance.get("implementation_identities")
        if encoded is None:
            expected_paths: tuple[str, ...] = ()
            historical_runner = HISTORICAL_RUNNER_SHA256
        else:
            if not isinstance(encoded, list):
                raise TypeError("implementation_identities must be a JSON array")
            observed: list[str] = []
            for value in encoded:
                identity = self.mapping(value, "implementation identity")
                relative_path = self.string(identity["path"], "implementation path")
                if relative_path in observed:
                    raise ValueError("implementation identity paths must be unique")
                observed.append(relative_path)
                identities.append(
                    ParticleInBoxSourceIdentity(
                        ParticleInBoxSourceIdentityRole.IMPLEMENTATION,
                        relative_path,
                        self.sha256_string(identity["sha256"], "implementation sha256"),
                    )
                )
            expected_paths = self.expected_implementation_paths
            historical_runner = None
        request = ParticleInBoxSourceAuthenticationRequest(
            tuple(identities), expected_paths, historical_runner
        )
        return self.source_authenticator.execute(request, repository_root)

    def reconstruct_numerics(
        self, payload: dict[str, JsonValue]
    ) -> ParticleInBoxNumericalVerificationResult:
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
                ParticleInBoxNumericalVerificationChannel.DIRICHLET_HAMILTONIAN,
                hamiltonian,
                expected_hamiltonian,
                0.0,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.DISCRETE_CLOSED_FORM,
                recorded_discrete,
                expected_discrete,
                0.0,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.CONTINUUM_CLOSED_FORM,
                recorded_continuum,
                expected_continuum,
                0.0,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.DISCRETE_TO_CONTINUUM_RATIO,
                recorded_ratio,
                expected_ratio,
                float(16.0 * np.finfo(np.float64).eps * ratio_scale),
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.COMPUTED_DISCRETE_SPECTRUM,
                computed,
                expected_discrete,
                float(128.0 * np.finfo(np.float64).eps * spectrum_scale),
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.RETAINED_BASIS_ORTHONORMALITY,
                vectors.T @ vectors,
                np.eye(retained),
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.PROJECTOR_DEFINITION,
                projector,
                vectors @ vectors.T,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.PROJECTOR_IDEMPOTENCY,
                projector @ projector,
                projector,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.EMBEDDED_REDUCTION,
                embedded,
                projector @ hamiltonian @ projector,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.RETAINED_COORDINATE_REDUCTION,
                coordinates,
                vectors.T @ hamiltonian @ vectors,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.RETAINED_COORDINATE_DIAGONALIZATION,
                coordinates,
                np.diag(expected_discrete[:retained]),
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.CONSISTENT_COMPRESSION,
                compressed,
                np.zeros((points, points)),
                0.0,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.UNMATCHED_COMPRESSION,
                unmatched,
                embedded - hamiltonian,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.DISCARDED_SECTOR,
                discarded,
                unmatched,
                tolerance,
            ),
            self.numerical_check(
                ParticleInBoxNumericalVerificationChannel.BOUNDARY_REALIZATION,
                boundary,
                expected_boundary,
                0.0,
            ),
        )
        return ParticleInBoxNumericalVerificationResult(
            checks,
            float(np.linalg.norm(unmatched, ord="fro")),
            tolerance,
            retained < points,
        )

    @staticmethod
    def numerical_check(
        channel: ParticleInBoxNumericalVerificationChannel,
        observed: RealMatrix | RealVector,
        expected: RealMatrix | RealVector,
        absolute_tolerance: float,
    ) -> ParticleInBoxNumericalCheckResult:
        """Return one maximum elementwise absolute-defect result."""
        defect = float(np.max(np.abs(observed - expected), initial=0.0))
        return ParticleInBoxNumericalCheckResult(channel, defect, absolute_tolerance)

    @staticmethod
    def vector(value: JsonValue, name: str, length: int) -> RealVector:
        """Decode one finite binary64 vector of an exact length."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        vector = np.asarray(value, dtype=np.float64)
        if vector.shape != (length,) or not np.all(np.isfinite(vector)):
            raise ValueError(f"{name} must be a finite vector of length {length}")
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

    @staticmethod
    def matrix_value(value: JsonValue, name: str, shape: tuple[int, int]) -> RealMatrix:
        """Decode one finite binary64 matrix with an exact shape."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        matrix = np.asarray(value, dtype=np.float64)
        if matrix.shape != shape or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix with shape {shape}")
        return matrix
