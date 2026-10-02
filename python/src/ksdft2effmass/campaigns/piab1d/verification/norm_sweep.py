r"""Reconstruct the finite-matrix identities in the PIAB1D norm sweep."""

from __future__ import annotations

import math
from enum import StrEnum
from pathlib import Path

import numpy as np

from .decoder import Piab1dResultDecoder
from .records import (
    Piab1dNumericalVerificationResult,
    Piab1dVerificationCheck,
    Piab1dVerificationCount,
    Piab1dVerificationResult,
)
from .source import Piab1dSourceAuthenticator


class Piab1dNormSweepVerificationChannel(StrEnum):
    """Identify the norm-sweep quantities reconstructed from the retained document."""

    GRID_INVENTORY = "grid_inventory"
    GRID_SPACING = "grid_spacing"
    HAMILTONIAN_NORMS = "hamiltonian_norms"
    CONSISTENT_COMPRESSION = "consistent_compression"
    BOUNDARY_RESIDUAL_NORMS = "boundary_residual_norms"
    UNMATCHED_COMPRESSION_NORMS = "unmatched_compression_norms"


class Piab1dNormSweepResultsVerifier(Piab1dResultDecoder):
    r"""Check the analytical finite-matrix identities reported by the norm sweep.

    For an ``N``-point centered Dirichlet discretization with spacing ``h``, the
    Hamiltonian prefactor is ``a = 1 / (2 h**2)`` and its eigenvalues are

    .. math::

       E_n = 4a\sin^2\!\left(\frac{n\pi}{2(N+1)}\right).

    The verifier uses these values to reconstruct Hamiltonian norms, the endpoint-link
    boundary residual, and the discarded spectral sector. Trends across grid sizes are
    analysis questions and do not affect this report.
    """

    __slots__ = ()

    historical_runner_sha256 = (
        "22498c13d30c1334e023e9a4fcab58d8c226c90a51a29a82e2b4fc0621b57556"
    )
    expected_implementation_paths = (
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/model.py",
        "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/evaluation.py",
        "python/src/ksdft2effmass/operators/eigenpairs.py",
        "python/src/ksdft2effmass/operators/subspaces.py",
        "python/src/ksdft2effmass/operators/matrix_norms.py",
        "python/src/ksdft2effmass/campaigns/piab1d/norm_sweep.py",
    )

    def execute(self, path: Path, repository_root: Path) -> Piab1dVerificationResult:
        """Return source and numerical reports for one norm-sweep result."""
        payload = self.decode(path)
        if self.integer(payload["schema_version"], "schema_version") != 1:
            raise ValueError("norm-sweep schema_version must equal one")
        input_payload = self.mapping(payload["input"], "input")
        if self.integer(input_payload["schema_version"], "input.schema_version") != 1:
            raise ValueError("norm-sweep input schema_version must equal one")
        if input_payload["experiment_id"] != payload["experiment_id"]:
            raise ValueError("input and result experiment_id values must agree")
        if input_payload["evidence_status"] != payload["evidence_status"]:
            raise ValueError("input and result evidence_status values must agree")
        expected_limitations = [
            "Raw matrix norms are dimension- and discretization-scale-dependent.",
            (
                "Normalized norms compare each residual only with its same-grid "
                "Hamiltonian."
            ),
            "Maximum-entry norms are basis-dependent.",
            "Algebraic eigenpair residuals do not measure continuum error.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
        if payload["limitations"] != expected_limitations:
            raise ValueError("norm-sweep limitations must match version one")

        provenance = self.mapping(payload["provenance"], "provenance")
        source = Piab1dSourceAuthenticator().execute(
            provenance,
            repository_root,
            self.expected_implementation_paths,
            self.historical_runner_sha256,
        )

        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        length = self.positive_real(parameters["length"], "length")
        mass = self.positive_real(parameters["mass"], "mass")
        hbar = self.positive_real(parameters["hbar"], "hbar")
        norm_names = tuple(
            self.string(value, "norm")
            for value in self.sequence(input_payload["norms"], "norms")
        )
        expected_norm_names = ("frobenius", "spectral", "maximum_entry")
        if norm_names != expected_norm_names:
            raise ValueError("norms must match the version-one norm inventory")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.positive_integer_sequence(
            series["interior_points"], "interior_points"
        )
        retained = self.integer(series["retained_dimension"], "retained_dimension")
        if retained <= 0 or retained > min(point_counts):
            raise ValueError("retained_dimension must fit every grid")
        grids = self.sequence(payload["grids"], "grids")
        if len(grids) != len(point_counts):
            raise ValueError("grid collection must match the input inventory")

        grid_defects: list[float] = []
        spacing_defects: list[float] = []
        hamiltonian_ratios: list[float] = []
        consistent_defects: list[float] = []
        boundary_ratios: list[float] = []
        unmatched_ratios: list[float] = []

        # The retained JSON rounds binary64 values. Each reconstructed norm therefore
        # uses the same explicit relative-plus-absolute envelope as the original
        # independent verifier, but the report stores a dimensionless defect ratio.
        relative_tolerance = 2.0e-13
        raw_absolute_tolerance = 2.0e-12
        unmatched_absolute_tolerance = 2.0e-11

        for value, expected_points in zip(grids, point_counts, strict=True):
            grid = self.mapping(value, "grid")
            points = self.integer(grid["interior_points"], "interior_points")
            grid_defects.append(abs(points - expected_points) * 1.0)
            spacing = self.positive_real(grid["spacing"], "spacing")
            expected_spacing = length / (points + 1)
            spacing_defects.append(abs(spacing - expected_spacing))

            prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
            indices = np.arange(1, points + 1, dtype=np.float64)
            eigenvalues = (
                4.0 * prefactor * np.sin(indices * math.pi / (2.0 * (points + 1))) ** 2
            )
            expected_hamiltonian = {
                "frobenius": prefactor * math.sqrt(6.0 * points - 2.0),
                "spectral": eigenvalues[-1].item(),
                "maximum_entry": 2.0 * prefactor,
            }
            hamiltonian_norms = self.mapping(
                grid["hamiltonian_norms"], "hamiltonian_norms"
            )
            if set(hamiltonian_norms) != set(norm_names):
                raise ValueError("Hamiltonian norms must match the input inventory")
            for name, expected in expected_hamiltonian.items():
                observed = self.nonnegative_real(hamiltonian_norms[name], name)
                allowance = raw_absolute_tolerance + relative_tolerance * abs(expected)
                hamiltonian_ratios.append(abs(observed - expected) / allowance)

            residuals = self.mapping(grid["operator_residuals"], "operator_residuals")
            consistent = self.mapping(
                residuals["consistent_compression"], "consistent_compression"
            )
            for section in ("raw", "relative_to_hamiltonian"):
                values = self.mapping(consistent[section], section)
                if set(values) != set(norm_names):
                    raise ValueError(
                        "consistent-compression norms must match the input inventory"
                    )
                consistent_defects.extend(
                    self.nonnegative_real(values[name], name) for name in norm_names
                )

            boundary = self.mapping(
                residuals["boundary_realization"], "boundary_realization"
            )
            boundary_raw = self.mapping(boundary["raw"], "boundary.raw")
            boundary_relative = self.mapping(
                boundary["relative_to_hamiltonian"],
                "boundary.relative_to_hamiltonian",
            )
            if set(boundary_raw) != set(norm_names) or set(boundary_relative) != set(
                norm_names
            ):
                raise ValueError("boundary norms must match the input inventory")
            expected_boundary = {
                "frobenius": math.sqrt(2.0) * prefactor,
                "spectral": prefactor,
                "maximum_entry": prefactor,
            }
            for name, expected in expected_boundary.items():
                raw = self.nonnegative_real(boundary_raw[name], name)
                raw_allowance = raw_absolute_tolerance + relative_tolerance * abs(
                    expected
                )
                boundary_ratios.append(abs(raw - expected) / raw_allowance)
                expected_relative = expected / expected_hamiltonian[name]
                relative = self.nonnegative_real(boundary_relative[name], name)
                relative_allowance = 2.0e-13 + relative_tolerance * abs(
                    expected_relative
                )
                boundary_ratios.append(
                    abs(relative - expected_relative) / relative_allowance
                )

            unmatched = self.mapping(
                residuals["unmatched_compression"], "unmatched_compression"
            )
            unmatched_raw = self.mapping(unmatched["raw"], "unmatched.raw")
            unmatched_relative = self.mapping(
                unmatched["relative_to_hamiltonian"],
                "unmatched.relative_to_hamiltonian",
            )
            if set(unmatched_raw) != set(norm_names) or set(unmatched_relative) != set(
                norm_names
            ):
                raise ValueError(
                    "unmatched-compression norms must match the input inventory"
                )

            # Closed-form sine vectors reconstruct the discarded spectral operator in
            # the coordinate basis. This makes the basis-dependent maximum-entry norm
            # independently checkable rather than trusting the retained scalar.
            coordinates = indices[:, np.newaxis]
            modes = indices[np.newaxis, :]
            eigenvectors = math.sqrt(2.0 / (points + 1)) * np.sin(
                coordinates * modes * math.pi / (points + 1)
            )
            discarded = eigenvectors[:, retained:]
            discarded_operator = (discarded * eigenvalues[retained:]) @ discarded.T
            expected_unmatched = {
                "frobenius": np.linalg.norm(discarded_operator, ord="fro").item(),
                "spectral": eigenvalues[-1].item(),
                "maximum_entry": np.max(np.abs(discarded_operator)).item(),
            }
            for name, expected in expected_unmatched.items():
                observed = self.nonnegative_real(unmatched_raw[name], name)
                allowance = unmatched_absolute_tolerance + relative_tolerance * abs(
                    expected
                )
                unmatched_ratios.append(abs(observed - expected) / allowance)
                expected_relative = expected / expected_hamiltonian[name]
                relative = self.nonnegative_real(unmatched_relative[name], name)
                relative_allowance = unmatched_absolute_tolerance + (
                    relative_tolerance * abs(expected_relative)
                )
                unmatched_ratios.append(
                    abs(relative - expected_relative) / relative_allowance
                )

        check = Piab1dVerificationCheck
        checks = (
            check(
                Piab1dNormSweepVerificationChannel.GRID_INVENTORY,
                max(grid_defects),
                0.0,
            ),
            check(
                Piab1dNormSweepVerificationChannel.GRID_SPACING,
                max(spacing_defects),
                0.0,
            ),
            check(
                Piab1dNormSweepVerificationChannel.HAMILTONIAN_NORMS,
                max(hamiltonian_ratios),
                1.0,
            ),
            check(
                Piab1dNormSweepVerificationChannel.CONSISTENT_COMPRESSION,
                max(consistent_defects),
                0.0,
            ),
            check(
                Piab1dNormSweepVerificationChannel.BOUNDARY_RESIDUAL_NORMS,
                max(boundary_ratios),
                1.0,
            ),
            check(
                Piab1dNormSweepVerificationChannel.UNMATCHED_COMPRESSION_NORMS,
                max(unmatched_ratios),
                1.0,
            ),
        )
        numerical = Piab1dNumericalVerificationResult(
            checks,
            tuple(Piab1dNormSweepVerificationChannel),
            (Piab1dVerificationCount("grids", len(grids)),),
        )
        return Piab1dVerificationResult(source, numerical)
