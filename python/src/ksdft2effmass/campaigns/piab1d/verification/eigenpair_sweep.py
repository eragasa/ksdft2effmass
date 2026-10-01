"""Authenticate and independently reconstruct the PIAB1D eigenpair sweep.

The module verifies a version-one retained JSON representation of full discrete
Dirichlet spectra and fixed-mode refinement series. It operates on dimensionless
binary64 values, does not import the calculation Workflow or eigensolver, and keeps
source authentication distinct from numerical reconstruction. Passing reports provide
software and numerical verification only for the represented finite calculations; they
do not establish uniform spectral convergence, scientific validation, or uncertainty
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


class Piab1dEigenpairSweepVerificationChannel(StrEnum):
    """Identify independently reconstructed eigenpair-sweep channels.

    Attributes
    ----------
    GRID_INVENTORY
        Agreement between requested and represented grid dimensions.
    GRID_SPACING
        Agreement with the Dirichlet spacing ``length / (N + 1)``.
    MODE_INVENTORY
        Ordered presence of every mode index from one through ``N``.
    FRACTIONAL_MODE_INDEX
        Agreement of the represented mode fraction with ``n / (N + 1)``.
    CONTINUUM_ENERGY
        Agreement with the analytical Dirichlet energy for fixed mode ``n``.
    REPORTED_ENERGY_RELATION
        Internal relation among computed energy, continuum energy, and relative error.
    RELATIVE_ENERGY_ERROR
        Agreement with the closed-form second-order finite-difference dispersion.
    NODAL_OVERLAP
        Maximum retained defect between numerical and sampled sine eigenvectors.
    EIGENPAIR_RESIDUAL
        Maximum retained scaled algebraic eigenpair residual.
    GRID_MAXIMUM_DIAGNOSTICS
        Agreement between per-mode diagnostics and represented grid maxima.
    FIXED_MODE_POINT_INVENTORY
        Agreement of fixed-mode grid dimensions with reconstructed observations.
    FIXED_MODE_SPACING_SERIES
        Agreement of fixed-mode spacing series with reconstructed grid spacings.
    FIXED_MODE_ERROR_SERIES
        Agreement of fixed-mode errors with reconstructed full-spectrum records.
    OBSERVED_ORDER_RECONSTRUCTION
        Agreement of represented and independently reconstructed convergence orders.
    """

    GRID_INVENTORY = "grid_inventory"
    GRID_SPACING = "grid_spacing"
    MODE_INVENTORY = "mode_inventory"
    FRACTIONAL_MODE_INDEX = "fractional_mode_index"
    CONTINUUM_ENERGY = "continuum_energy"
    REPORTED_ENERGY_RELATION = "reported_energy_relation"
    RELATIVE_ENERGY_ERROR = "relative_energy_error"
    NODAL_OVERLAP = "nodal_overlap"
    EIGENPAIR_RESIDUAL = "eigenpair_residual"
    GRID_MAXIMUM_DIAGNOSTICS = "grid_maximum_diagnostics"
    FIXED_MODE_POINT_INVENTORY = "fixed_mode_point_inventory"
    FIXED_MODE_SPACING_SERIES = "fixed_mode_spacing_series"
    FIXED_MODE_ERROR_SERIES = "fixed_mode_error_series"
    OBSERVED_ORDER_RECONSTRUCTION = "observed_order_reconstruction"


class Piab1dEigenpairSweepResultsVerifier(Piab1dResultDecoder):
    """Reconstruct a full-spectrum and fixed-mode PIAB1D sweep.

    The calculation Workflow and eigensolver are not imported. Computed energies are
    checked through the represented energy-error relation and the closed-form
    finite-difference dispersion relation. Expected spectral trends are left to
    analysis tools and do not affect verification success.
    """

    __slots__ = ()

    historical_runner_sha256 = (
        "1297318c938443d2bd729a47545d99f3819ef97e4bbf3f929bdcec9c6ca1fded"
    )
    relative_error_roundoff_multiplier = 128.0

    expected_implementation_paths = (
        "python/src/ksdft2effmass/analysis/convergence.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/model.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/evaluation.py",
        "python/src/ksdft2effmass/operators/eigenpairs.py",
        "python/src/ksdft2effmass/campaigns/piab1d/eigenpair_sweep.py",
    )

    def execute(self, path: Path, repository_root: Path) -> Piab1dVerificationResult:
        """Return source and numerical eigenpair-sweep verification reports.

        Parameters
        ----------
        path : pathlib.Path
            Existing UTF-8 version-one eigenpair-sweep JSON result.
        repository_root : pathlib.Path
            Existing repository directory against which declared relative source paths
            are resolved and contained.

        Returns
        -------
        Piab1dVerificationResult
            Separate source-authentication and numerical-reconstruction outcomes with a
            derived aggregate disposition.

        Raises
        ------
        TypeError
            If paths or represented JSON values have incorrect semantic types.
        ValueError
            If the repository root, version-one wire contract, source path containment,
            collection shape, finite-value rule, or numerical precondition is invalid.

        Notes
        -----
        Source-content or reconstructed-number disagreement is represented by a failed
        report. Malformed wire contracts and unsafe paths raise instead.
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
        """Validate version, status, identity, and limitation fields.

        Parameters
        ----------
        payload : dict[str, JsonValue]
            Decoded top-level result object.

        Raises
        ------
        TypeError
            If a required field has an incompatible JSON representation type.
        ValueError
            If a version, status, experiment identity, or limitation differs from the
            version-one contract.
        """
        if self.integer(payload["schema_version"], "schema_version") != 1:
            raise ValueError("eigenpair-sweep schema_version must equal one")
        if payload["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("eigenpair-sweep evidence_status is unsupported")
        if payload["calculation_status"] != "calculated illustrative result":
            raise ValueError("eigenpair-sweep calculation_status is unsupported")
        input_payload = self.mapping(payload["input"], "input")
        if self.integer(input_payload["schema_version"], "input schema_version") != 1:
            raise ValueError("eigenpair-sweep input schema_version must equal one")
        if input_payload["evidence_status"] != payload["evidence_status"]:
            raise ValueError("input and result evidence_status values must agree")
        if input_payload["experiment_id"] != payload["experiment_id"]:
            raise ValueError("input and result experiment_id values must agree")
        if payload["limitations"] != [
            "Fixed-mode convergence does not imply uniform spectral convergence.",
            "Nodal overlap does not measure continuum interpolation error.",
            "High-index eigenvalues probe finite-difference dispersion.",
            "The result is not semiconductor evidence or scientific validation.",
        ]:
            raise ValueError("eigenpair-sweep limitations do not match version one")

    def authenticate_sources(
        self, payload: dict[str, JsonValue], repository_root: Path
    ) -> Piab1dSourceAuthenticationResult:
        """Decode and authenticate source identities without numerical inference.

        Parameters
        ----------
        payload : dict[str, JsonValue]
            Validated result payload containing version-one provenance.
        repository_root : pathlib.Path
            Resolved repository root used by the shared authenticator.

        Returns
        -------
        Piab1dSourceAuthenticationResult
            Per-source dispositions and implementation-inventory agreement.

        Raises
        ------
        TypeError
            If provenance values have incompatible representation types.
        ValueError
            If identity digests, paths, inventories, or containment are invalid.
        """
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
        """Reconstruct spectra, nodal diagnostics, residuals, and mode orders.

        Parameters
        ----------
        payload : dict[str, JsonValue]
            Validated version-one eigenpair-sweep result object.

        Returns
        -------
        Piab1dNumericalVerificationResult
            Sixteen aggregate channel checks and counts derived from decoded
            collections.

        Raises
        ------
        TypeError
            If a represented value has an incompatible JSON semantic type.
        ValueError
            If a scalar is non-finite, a count or mode is invalid, collections do not
            align, a fixed mode has fewer than two observations, or channels cannot be
            reconstructed completely.

        Notes
        -----
        Energies are dimensionless. Arrays are not decoded; reconstruction operates on
        ordered immutable scalar collections and binary64 NumPy elementary functions.
        """
        input_payload = self.mapping(payload["input"], "input")
        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        length = self.positive_real(parameters["length"], "length")
        mass = self.positive_real(parameters["mass"], "mass")
        hbar = self.positive_real(parameters["hbar"], "hbar")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.positive_integer_sequence(
            series["interior_points"], "interior_points"
        )
        fixed_modes = self.positive_integer_sequence(
            series["fixed_higher_modes"], "fixed_higher_modes"
        )
        grids = self.sequence(payload["grids"], "grids")
        if len(grids) != len(point_counts):
            raise ValueError("grid collection must align with the input inventory")

        fixed_errors: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_spacings: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_points: dict[int, list[int]] = {mode: [] for mode in fixed_modes}
        grid_inventory_defects: list[float] = []
        spacing_defects: list[float] = []
        mode_inventory_defects: list[float] = []
        fractional_index_defects: list[float] = []
        continuum_energy_defects: list[float] = []
        energy_relation_defects: list[float] = []
        relative_error_ratios: list[float] = []
        overlap_defects: list[float] = []
        scaled_residuals: list[float] = []
        maximum_diagnostic_defects: list[float] = []
        eigenpair_count = 0
        epsilon = math.ulp(1.0)

        for value, expected_points in zip(grids, point_counts, strict=True):
            grid = self.mapping(value, "grid")
            points = self.integer(grid["interior_points"], "interior_points")
            if points <= 0:
                raise ValueError("interior_points must be positive")
            grid_inventory_defects.append(float(abs(points - expected_points)))
            spacing = self.positive_real(grid["spacing"], "spacing")
            expected_spacing = length / (points + 1)
            spacing_defects.append(abs(spacing - expected_spacing))
            records = self.sequence(grid["eigenpairs"], "eigenpairs")
            if len(records) != points:
                raise ValueError("each grid must contain one record per eigenpair")
            eigenpair_count += len(records)
            grid_overlaps: list[float] = []
            grid_residuals: list[float] = []
            for item, expected_mode in zip(records, range(1, points + 1), strict=True):
                record = self.mapping(item, "eigenpair")
                mode = self.integer(record["mode"], "mode")
                if mode <= 0:
                    raise ValueError("mode indices must be positive")
                mode_inventory_defects.append(float(abs(mode - expected_mode)))
                fractional = self.real(
                    record["fractional_mode_index"], "fractional_mode_index"
                )
                fractional_index_defects.append(
                    abs(fractional - expected_mode / (points + 1))
                )
                computed = self.positive_real(
                    record["computed_energy"], "computed_energy"
                )
                continuum = self.positive_real(
                    record["continuum_energy"], "continuum_energy"
                )
                observed_error = self.nonnegative_real(
                    record["relative_energy_error"], "relative_energy_error"
                )
                # The modal phase z converts the exact discrete spectrum into the
                # continuum-normalized dispersion ratio (sin(z) / z)^2.
                z = expected_mode * math.pi / (2.0 * (points + 1))
                expected_continuum = (
                    hbar
                    * hbar
                    * math.pi
                    * math.pi
                    * expected_mode
                    * expected_mode
                    / (2.0 * mass * length * length)
                )
                expected_error = 1.0 - (math.sin(z) / z) ** 2
                # This scale-aware envelope is the retained version-one
                # compatibility rule, not a general eigensolver forward-error bound.
                relative_allowance = (
                    self.relative_error_roundoff_multiplier
                    * epsilon
                    / (spacing * spacing * expected_continuum)
                )
                continuum_energy_defects.append(abs(continuum - expected_continuum))
                energy_relation_defects.append(
                    abs(observed_error - abs(computed - continuum) / continuum)
                )
                relative_error_ratios.append(
                    abs(observed_error - expected_error) / relative_allowance
                )
                overlap = self.nonnegative_real(
                    record["nodal_overlap_defect"], "nodal_overlap_defect"
                )
                residual = self.nonnegative_real(
                    record["scaled_eigenpair_residual"],
                    "scaled_eigenpair_residual",
                )
                overlap_defects.append(overlap)
                scaled_residuals.append(residual)
                grid_overlaps.append(overlap)
                grid_residuals.append(residual)
                if expected_mode in fixed_errors:
                    fixed_errors[expected_mode].append(observed_error)
                    fixed_spacings[expected_mode].append(spacing)
                    fixed_points[expected_mode].append(points)
            reported_overlap = self.nonnegative_real(
                grid["maximum_nodal_overlap_defect"],
                "maximum_nodal_overlap_defect",
            )
            reported_residual = self.nonnegative_real(
                grid["maximum_scaled_eigenpair_residual"],
                "maximum_scaled_eigenpair_residual",
            )
            maximum_diagnostic_defects.extend(
                (
                    abs(reported_overlap - max(grid_overlaps)),
                    abs(reported_residual - max(grid_residuals)),
                )
            )

        all_series = self.mapping(
            payload["fixed_higher_mode_series"], "fixed_higher_mode_series"
        )
        if set(all_series) != {str(mode) for mode in fixed_modes}:
            raise ValueError("fixed-mode series keys must match the input inventory")
        point_inventory_defects: list[float] = []
        spacing_series_defects: list[float] = []
        error_series_defects: list[float] = []
        order_ratios: list[float] = []
        for mode in fixed_modes:
            mode_series = self.mapping(all_series[str(mode)], "mode series")
            observed_points = self.integer_sequence(
                mode_series["interior_points"], "interior_points"
            )
            observed_spacings = self.real_sequence(mode_series["spacings"], "spacings")
            observed_errors = self.real_sequence(
                mode_series["relative_energy_errors"], "relative_energy_errors"
            )
            expected_series_points = tuple(fixed_points[mode])
            expected_spacings = tuple(fixed_spacings[mode])
            expected_errors = tuple(fixed_errors[mode])
            if not expected_series_points or len(expected_series_points) < 2:
                raise ValueError("each fixed mode must occur on at least two grids")
            if not (
                len(observed_points)
                == len(observed_spacings)
                == len(observed_errors)
                == len(expected_series_points)
            ):
                raise ValueError(
                    "fixed-mode series collections must have equal lengths"
                )
            point_inventory_defects.extend(
                float(abs(observed - expected))
                for observed, expected in zip(
                    observed_points, expected_series_points, strict=True
                )
            )
            spacing_series_defects.extend(
                abs(observed - expected)
                for observed, expected in zip(
                    observed_spacings, expected_spacings, strict=True
                )
            )
            error_series_defects.extend(
                abs(observed - expected)
                for observed, expected in zip(
                    observed_errors, expected_errors, strict=True
                )
            )
            recorded_orders = self.sequence(mode_series["observed_orders"], "orders")
            if (
                len(recorded_orders) != len(expected_series_points)
                or recorded_orders[0] is not None
            ):
                raise ValueError(
                    "observed orders must align with the fixed-mode series"
                )
            # Pairwise log-ratios reconstruct the observed order without importing
            # the producer's convergence estimator.
            independent_orders = tuple(
                math.log(a / b) / math.log(h_a / h_b)
                for h_a, h_b, a, b in zip(
                    expected_spacings[:-1],
                    expected_spacings[1:],
                    expected_errors[:-1],
                    expected_errors[1:],
                    strict=True,
                )
            )
            observed_orders = self.real_sequence(recorded_orders[1:], "orders")
            for observed, expected in zip(
                observed_orders, independent_orders, strict=True
            ):
                allowance = 2.0e-10 + 2.0e-10 * abs(expected)
                order_ratios.append(abs(observed - expected) / allowance)

        # nextafter converts strict version-one inequalities into inclusive ResultObject
        # thresholds while preserving their binary64 boundary.
        strict_one = math.nextafter(1.0, 0.0)
        strict_small = math.nextafter(1.0e-13, 0.0)
        # These checks establish retained numerical identities. Expected spectral
        # contrast and near-second-order fixed-mode behavior are intentionally left
        # for later analysis and do not influence verification success.
        check = Piab1dVerificationCheck
        checks = (
            check(
                Piab1dEigenpairSweepVerificationChannel.GRID_INVENTORY,
                max(grid_inventory_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.GRID_SPACING,
                max(spacing_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.MODE_INVENTORY,
                max(mode_inventory_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.FRACTIONAL_MODE_INDEX,
                max(fractional_index_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.CONTINUUM_ENERGY,
                max(continuum_energy_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.REPORTED_ENERGY_RELATION,
                max(energy_relation_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.RELATIVE_ENERGY_ERROR,
                max(relative_error_ratios),
                strict_one,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.NODAL_OVERLAP,
                max(overlap_defects),
                strict_small,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.EIGENPAIR_RESIDUAL,
                max(scaled_residuals),
                strict_small,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.GRID_MAXIMUM_DIAGNOSTICS,
                max(maximum_diagnostic_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.FIXED_MODE_POINT_INVENTORY,
                max(point_inventory_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.FIXED_MODE_SPACING_SERIES,
                max(spacing_series_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.FIXED_MODE_ERROR_SERIES,
                max(error_series_defects),
                0.0,
            ),
            check(
                Piab1dEigenpairSweepVerificationChannel.OBSERVED_ORDER_RECONSTRUCTION,
                max(order_ratios),
                1.0,
            ),
        )
        counts = (
            Piab1dVerificationCount("grids", len(grids)),
            Piab1dVerificationCount("eigenpairs", eigenpair_count),
            Piab1dVerificationCount("fixed_mode_series", len(all_series)),
        )
        return Piab1dNumericalVerificationResult(
            checks, tuple(Piab1dEigenpairSweepVerificationChannel), counts
        )
