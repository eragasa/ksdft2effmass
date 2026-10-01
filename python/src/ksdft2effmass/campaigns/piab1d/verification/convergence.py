"""Authenticate and independently reconstruct PIAB1D grid convergence.

The module verifies version-one fixed-mode refinement records for the dimensionless
centered second-order Dirichlet discretization. It reconstructs grid spacing, analytical
dispersion error, compression identities, and represented pairwise observed orders
without importing the producing Workflow or convergence estimator. Passing reports do
not establish uniform spectral convergence, scientific validation, or uncertainty
quantification.
"""

from __future__ import annotations

import math
from enum import StrEnum
from pathlib import Path

from .decoder import JsonValue, Piab1dResultDecoder
from .records import (
    Piab1dNumericalVerificationResult,
    Piab1dVerificationCheck,
    Piab1dVerificationCount,
    Piab1dVerificationResult,
)
from .source import (
    Piab1dSourceAuthenticationResult,
    Piab1dSourceAuthenticator,
)


class Piab1dConvergenceVerificationChannel(StrEnum):
    """Identify independently reconstructed convergence-result channels."""

    GRID_SPACING = "grid_spacing"
    RELATIVE_ENERGY_ERROR = "relative_energy_error"
    DISCRETE_CLOSED_FORM_ERROR = "discrete_closed_form_error"
    CONSISTENT_COMPRESSION = "consistent_compression"
    DISCARDED_SECTOR_IDENTITY = "discarded_sector_identity"
    OBSERVED_ORDER_RECONSTRUCTION = "observed_order_reconstruction"


class Piab1dConvergenceResultsVerifier(Piab1dResultDecoder):
    """Independently authenticate and verify the grid-convergence campaign."""

    __slots__ = ()

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

    def execute(self, path: Path, repository_root: Path) -> Piab1dVerificationResult:
        """Return separate source and numerical convergence verification reports.

        Parameters
        ----------
        path
            Existing UTF-8 JSON convergence-result path.
        repository_root
            Existing repository directory used to resolve declared source paths.

        Returns
        -------
        Piab1dVerificationResult
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
        return Piab1dVerificationResult(source, numerical)

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
    ) -> Piab1dSourceAuthenticationResult:
        """Decode a source-authentication request and execute its shared policy."""
        provenance = self.mapping(payload["provenance"], "provenance")
        return Piab1dSourceAuthenticator().execute(
            provenance,
            repository_root,
            self.expected_implementation_paths,
            self.historical_runner_sha256,
        )

    def reconstruct_numerics(
        self, payload: dict[str, JsonValue]
    ) -> Piab1dNumericalVerificationResult:
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
                z = mode * math.pi / (2.0 * (points + 1))
                expected = 1.0 - (math.sin(z) / z) ** 2
                allowance = 2.0 * closed_error / continuum + 32.0 * math.ulp(1.0)
                relative_error_ratios.append(abs(observed - expected) / allowance)
                closed_allowance = 128.0 * math.ulp(1.0) / (spacing * spacing)
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

        recorded_orders = self.mapping(
            payload["observed_relative_error_orders"], "observed orders"
        )
        order_ratios: list[float] = []
        for mode in order_modes:
            recorded = self.sequence(recorded_orders[str(mode)], "mode orders")
            if len(recorded) != len(spacings) or recorded[0] is not None:
                raise ValueError("observed order records must align with refinements")
            independent = tuple(
                math.log(a / b) / math.log(h_a / h_b)
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

        strict_one = math.nextafter(1.0, 0.0)
        strict_discarded = math.nextafter(1.0e-13, 0.0)
        # These checks establish represented identities only. Whether the reconstructed
        # sequence has the expected monotonic or second-order trend is interpretation,
        # not a condition for accepting the arithmetic reconstruction.
        check = Piab1dVerificationCheck
        checks = (
            check(
                Piab1dConvergenceVerificationChannel.GRID_SPACING,
                max(spacing_defects),
                0.0,
            ),
            check(
                Piab1dConvergenceVerificationChannel.RELATIVE_ENERGY_ERROR,
                max(relative_error_ratios),
                strict_one,
            ),
            check(
                Piab1dConvergenceVerificationChannel.DISCRETE_CLOSED_FORM_ERROR,
                max(closed_form_ratios),
                strict_one,
            ),
            check(
                Piab1dConvergenceVerificationChannel.CONSISTENT_COMPRESSION,
                max(consistent_norms),
                0.0,
            ),
            check(
                Piab1dConvergenceVerificationChannel.DISCARDED_SECTOR_IDENTITY,
                max(discarded_relative_errors),
                strict_discarded,
            ),
            check(
                Piab1dConvergenceVerificationChannel.OBSERVED_ORDER_RECONSTRUCTION,
                max(order_ratios),
                1.0,
            ),
        )
        counts = (
            Piab1dVerificationCount("refinements", len(refinements)),
            Piab1dVerificationCount("mode_observations", mode_observation_count),
        )
        return Piab1dNumericalVerificationResult(
            checks, tuple(Piab1dConvergenceVerificationChannel), counts
        )
