"""Report-based independent verification of PIAB1D grid convergence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import numpy as np

from .decoder import JsonValue, ParticleInBoxCampaignResultDecoder
from .source import (
    ParticleInBoxSourceAuthenticationRequest,
    ParticleInBoxSourceAuthenticationResult,
    ParticleInBoxSourceAuthenticator,
    ParticleInBoxSourceIdentity,
    ParticleInBoxSourceIdentityRole,
)


class ParticleInBoxConvergenceVerificationChannel(StrEnum):
    """Identify independently reconstructed convergence-result channels."""

    GRID_SPACING = "grid_spacing"
    RELATIVE_ENERGY_ERROR = "relative_energy_error"
    DISCRETE_CLOSED_FORM_ERROR = "discrete_closed_form_error"
    CONSISTENT_COMPRESSION = "consistent_compression"
    DISCARDED_SECTOR_IDENTITY = "discarded_sector_identity"
    FIXED_MODE_MONOTONICITY = "fixed_mode_monotonicity"
    OBSERVED_ORDER_RECONSTRUCTION = "observed_order_reconstruction"
    ASYMPTOTIC_SECOND_ORDER = "asymptotic_second_order"


@dataclass(frozen=True, slots=True)
class ParticleInBoxConvergenceVerificationCheckResult:
    """Retain one aggregate convergence-channel defect and tolerance.

    Parameters
    ----------
    channel
        Reconstructed convergence channel.
    maximum_defect
        Maximum absolute or normalized defect across the channel's reconstructed
        collection. Boolean conditions use zero for satisfaction and one for failure.
    inclusive_tolerance
        Inclusive acceptance threshold in the same channel convention.
    """

    channel: ParticleInBoxConvergenceVerificationChannel
    maximum_defect: float
    inclusive_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact channel typing and finite nonnegative values."""
        if type(self.channel) is not ParticleInBoxConvergenceVerificationChannel:
            raise TypeError(
                "channel must be ParticleInBoxConvergenceVerificationChannel"
            )
        for name, value in (
            ("maximum_defect", self.maximum_defect),
            ("inclusive_tolerance", self.inclusive_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def passes(self) -> bool:
        """Return whether the channel defect satisfies its inclusive tolerance."""
        return self.maximum_defect <= self.inclusive_tolerance


@dataclass(frozen=True, slots=True)
class ParticleInBoxConvergenceNumericalVerificationResult:
    """Retain the complete convergence-channel verification report.

    Parameters
    ----------
    checks
        Exactly one check for every convergence verification channel.
    refinement_count
        Count derived from the decoded refinement collection.
    reconstructed_mode_observation_count
        Count derived from all decoded refinement-mode records.
    """

    checks: tuple[ParticleInBoxConvergenceVerificationCheckResult, ...]
    refinement_count: int
    reconstructed_mode_observation_count: int

    def __post_init__(self) -> None:
        """Validate complete checks and collection-derived nonnegative counts."""
        if not isinstance(self.checks, tuple) or any(
            type(check) is not ParticleInBoxConvergenceVerificationCheckResult
            for check in self.checks
        ):
            raise TypeError("checks must contain convergence check results")
        channels = tuple(check.channel for check in self.checks)
        if len(set(channels)) != len(channels):
            raise ValueError("convergence verification channels must be unique")
        if set(channels) != set(ParticleInBoxConvergenceVerificationChannel):
            raise ValueError("convergence verification channels must be complete")
        for name, value in (
            ("refinement_count", self.refinement_count),
            (
                "reconstructed_mode_observation_count",
                self.reconstructed_mode_observation_count,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")

    @property
    def passes(self) -> bool:
        """Return whether every reconstructed convergence channel passes."""
        return all(check.passes for check in self.checks)

    @property
    def check_count(self) -> int:
        """Return the count derived from the immutable check collection."""
        return len(self.checks)


@dataclass(frozen=True, slots=True)
class ParticleInBoxConvergenceVerificationResult:
    """Retain separate source and numerical convergence verification outcomes.

    Parameters
    ----------
    source_authentication
        Input, runner, and current implementation identity report.
    numerical_reconstruction
        Independent fixed-mode convergence reconstruction report.
    """

    source_authentication: ParticleInBoxSourceAuthenticationResult
    numerical_reconstruction: ParticleInBoxConvergenceNumericalVerificationResult

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
            is not ParticleInBoxConvergenceNumericalVerificationResult
        ):
            raise TypeError(
                "numerical_reconstruction must be the convergence numerical result"
            )

    @property
    def passes(self) -> bool:
        """Return true only when source and numerical outcomes both pass."""
        return (
            self.source_authentication.passes and self.numerical_reconstruction.passes
        )


class ParticleInBoxConvergenceVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently authenticate and verify the grid-convergence campaign."""

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

    historical_runner_sha256 = (
        "4a470df61db42903ee32e849c203075174a41c736c006b58da4ecff0fb413768"
    )
    expected_implementation_paths = (
        "python/src/ksdft2effmass/analysis/convergence.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/model.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/evaluation.py",
        "python/src/ksdft2effmass/operators/eigenpairs.py",
        "python/src/ksdft2effmass/operators/subspaces.py",
        "python/src/ksdft2effmass/campaigns/piab1d/convergence.py",
    )

    def execute(
        self, path: Path, repository_root: Path
    ) -> ParticleInBoxConvergenceVerificationResult:
        """Return separate source and numerical convergence verification reports.

        Parameters
        ----------
        path
            Existing UTF-8 JSON convergence-result path.
        repository_root
            Existing repository directory used to resolve declared source paths.

        Returns
        -------
        ParticleInBoxConvergenceVerificationResult
            Source authentication, independent reconstruction, and aggregate
            disposition.

        Raises
        ------
        TypeError
            If paths or represented values have incorrect semantic types.
        ValueError
            If a path, structural version-one invariant, collection shape, or
            limitation contract is invalid.
        """
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        root = repository_root.resolve()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        payload = self.decode(path)
        self.validate_document_contract(payload)
        source = self.authenticate_sources(payload, root)
        numerical = self.reconstruct_numerics(payload)
        return ParticleInBoxConvergenceVerificationResult(source, numerical)

    def validate_document_contract(self, payload: dict[str, JsonValue]) -> None:
        """Validate version, status, and limitation fields before reconstruction."""
        if self.integer(payload["schema_version"], "schema_version") != 1:
            raise ValueError("convergence schema_version must equal one")
        if payload["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("convergence evidence_status is unsupported")
        if payload["calculation_status"] != "calculated illustrative result":
            raise ValueError("convergence calculation_status is unsupported")
        if payload["limitations"] != [
            "Observed order concerns fixed-index eigenvalues only.",
            "The series does not establish uniform spectral convergence.",
            "Residual norms on different matrix spaces are not convergence metrics.",
            "The result is not semiconductor evidence or scientific validation.",
        ]:
            raise ValueError("convergence limitations do not match version one")

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
            ),
            ParticleInBoxSourceIdentity(
                ParticleInBoxSourceIdentityRole.RUNNER,
                self.string(provenance["script_path"], "script_path"),
                self.sha256_string(provenance["script_sha256"], "script_sha256"),
            ),
        ]
        encoded = provenance.get("implementation_identities")
        if encoded is None:
            expected_paths: tuple[str, ...] = ()
            historical_runner = self.historical_runner_sha256
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
    ) -> ParticleInBoxConvergenceNumericalVerificationResult:
        """Reconstruct fixed-mode errors, identities, and observed orders."""
        input_payload = self.mapping(payload["input"], "input")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.integer_sequence(
            series["interior_points"], "interior_points"
        )
        reported_modes = self.integer_sequence(
            series["reported_modes"], "reported_modes"
        )
        order_modes = self.integer_sequence(series["order_modes"], "order_modes")
        refinements = self.sequence(payload["refinements"], "refinements")
        if (
            not point_counts
            or not reported_modes
            or not order_modes
            or len(refinements) < 2
        ):
            raise ValueError(
                "convergence verification needs grids, modes, and two refinements"
            )
        if any(value <= 0 for value in (*point_counts, *reported_modes, *order_modes)):
            raise ValueError("grid and mode indices must be positive")
        if not set(order_modes).issubset(reported_modes):
            raise ValueError("order_modes must be a subset of reported_modes")
        observed_point_counts = tuple(
            self.integer(self.mapping(item, "refinement")["interior_points"], "points")
            for item in refinements
        )
        if observed_point_counts != point_counts:
            raise ValueError("refinement point inventory disagrees with the input")

        errors_by_mode: dict[int, list[float]] = {mode: [] for mode in reported_modes}
        spacings: list[float] = []
        spacing_defects: list[float] = []
        relative_error_ratios: list[float] = []
        closed_form_ratios: list[float] = []
        consistent_norms: list[float] = []
        discarded_relative_errors: list[float] = []
        mode_observation_count = 0
        for item in refinements:
            refinement = self.mapping(item, "refinement")
            points = self.integer(refinement["interior_points"], "interior_points")
            spacing = self.real(refinement["spacing"], "spacing")
            if spacing <= 0.0:
                raise ValueError("spacing must be positive")
            spacings.append(spacing)
            spacing_defects.append(abs(spacing - 1.0 / (points + 1)))
            modes = self.sequence(refinement["modes"], "modes")
            if len(modes) != len(reported_modes):
                raise ValueError("every refinement must contain every reported mode")
            mode_observation_count += len(modes)
            for value, mode in zip(modes, reported_modes, strict=True):
                record = self.mapping(value, "mode record")
                if self.integer(record["mode"], "mode") != mode:
                    raise ValueError("mode records must follow the input inventory")
                continuum = self.real(record["continuum_energy"], "continuum_energy")
                closed_error = self.real(
                    record["discrete_closed_form_error"], "closed-form error"
                )
                observed = self.real(record["relative_error"], "relative_error")
                if continuum <= 0.0 or closed_error < 0.0 or observed < 0.0:
                    raise ValueError("energy and reported error signs are invalid")
                z = mode * np.pi / (2.0 * (points + 1))
                expected = 1.0 - (np.sin(z) / z) ** 2
                allowance = (
                    2.0 * closed_error / continuum + 32.0 * np.finfo(np.float64).eps
                )
                relative_error_ratios.append(abs(observed - expected) / allowance)
                closed_allowance = (
                    128.0 * np.finfo(np.float64).eps / (spacing * spacing)
                )
                closed_form_ratios.append(closed_error / closed_allowance)
                errors_by_mode[mode].append(observed)
            diagnostics = self.mapping(
                refinement["diagnostic_residuals"], "diagnostic_residuals"
            )
            consistent_norm = self.real(
                diagnostics["consistent_compression_frobenius_norm"],
                "consistent norm",
            )
            discarded_relative_error = self.real(
                diagnostics["unmatched_equals_discarded_relative_error"],
                "discarded relative error",
            )
            if consistent_norm < 0.0 or discarded_relative_error < 0.0:
                raise ValueError("reported norm diagnostics must be nonnegative")
            consistent_norms.append(consistent_norm)
            discarded_relative_errors.append(discarded_relative_error)

        monotonic = all(
            fine < coarse
            for mode in reported_modes
            for coarse, fine in zip(
                errors_by_mode[mode][:-1], errors_by_mode[mode][1:], strict=True
            )
        )
        recorded_orders = self.mapping(
            payload["observed_relative_error_orders"], "observed orders"
        )
        order_ratios: list[float] = []
        asymptotic = True
        for mode in order_modes:
            recorded = self.sequence(recorded_orders[str(mode)], "mode orders")
            if len(recorded) != len(spacings) or recorded[0] is not None:
                raise ValueError("observed order records must align with refinements")
            independent = tuple(
                float(np.log(a / b) / np.log(h_a / h_b))
                for h_a, h_b, a, b in zip(
                    spacings[:-1],
                    spacings[1:],
                    errors_by_mode[mode][:-1],
                    errors_by_mode[mode][1:],
                    strict=True,
                )
            )
            observed_orders = self.real_sequence(recorded[1:], "orders")
            for observed, expected in zip(observed_orders, independent, strict=True):
                order_allowance = 2.0e-10 + 2.0e-10 * abs(expected)
                order_ratios.append(abs(observed - expected) / order_allowance)
            final_order = self.real(recorded[-1], "last order")
            asymptotic = asymptotic and 1.99 < final_order < 2.01

        strict_one = float(np.nextafter(1.0, 0.0))
        strict_discarded = float(np.nextafter(1.0e-13, 0.0))
        checks = (
            self.check(
                ParticleInBoxConvergenceVerificationChannel.GRID_SPACING,
                max(spacing_defects),
                0.0,
            ),
            self.check(
                ParticleInBoxConvergenceVerificationChannel.RELATIVE_ENERGY_ERROR,
                max(relative_error_ratios),
                strict_one,
            ),
            self.check(
                ParticleInBoxConvergenceVerificationChannel.DISCRETE_CLOSED_FORM_ERROR,
                max(closed_form_ratios),
                strict_one,
            ),
            self.check(
                ParticleInBoxConvergenceVerificationChannel.CONSISTENT_COMPRESSION,
                max(consistent_norms),
                0.0,
            ),
            self.check(
                ParticleInBoxConvergenceVerificationChannel.DISCARDED_SECTOR_IDENTITY,
                max(discarded_relative_errors),
                strict_discarded,
            ),
            self.condition_check(
                ParticleInBoxConvergenceVerificationChannel.FIXED_MODE_MONOTONICITY,
                monotonic,
            ),
            self.check(
                ParticleInBoxConvergenceVerificationChannel.OBSERVED_ORDER_RECONSTRUCTION,
                max(order_ratios),
                1.0,
            ),
            self.condition_check(
                ParticleInBoxConvergenceVerificationChannel.ASYMPTOTIC_SECOND_ORDER,
                asymptotic,
            ),
        )
        return ParticleInBoxConvergenceNumericalVerificationResult(
            checks, len(refinements), mode_observation_count
        )

    @staticmethod
    def check(
        channel: ParticleInBoxConvergenceVerificationChannel,
        maximum_defect: float,
        inclusive_tolerance: float,
    ) -> ParticleInBoxConvergenceVerificationCheckResult:
        """Construct one finite aggregate convergence check."""
        return ParticleInBoxConvergenceVerificationCheckResult(
            channel, float(maximum_defect), float(inclusive_tolerance)
        )

    @classmethod
    def condition_check(
        cls,
        channel: ParticleInBoxConvergenceVerificationChannel,
        condition: bool,
    ) -> ParticleInBoxConvergenceVerificationCheckResult:
        """Represent one exact Boolean convergence condition as a check."""
        return cls.check(channel, 0.0 if condition else 1.0, 0.0)
