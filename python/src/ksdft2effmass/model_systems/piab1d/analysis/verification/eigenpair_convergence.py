"""Independent verification of PIAB1D represented eigenpair sweeps."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..grid_sweep import Piab1dEigenpairSweepResult


@dataclass(frozen=True, slots=True)
class Piab1dEigenpairSweepReference:
    """Retain immutable independent comparisons for one eigenpair sweep."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("eigenpair-sweep comparisons must be nonempty")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


class Piab1dEigenpairSweepReferenceAnalyzer:
    """Reconstruct PIAB1D grid dispersion independently of the sweep analyzer."""

    __slots__ = ()

    def execute(
        self,
        result: Piab1dEigenpairSweepResult,
    ) -> Piab1dEigenpairSweepReference:
        """Reconstruct the complete represented-spectrum sweep.

        Parameters
        ----------
        result
            Typed flattened eigenpair observations for every declared grid.

        Returns
        -------
        Piab1dEigenpairSweepReference
            Independent comparisons for spacing, fractional mode index, analytical
            finite-difference dispersion, nodal overlap, and scaled residuals.

        Raises
        ------
        TypeError
            ``result`` is not a ``Piab1dEigenpairSweepResult``.
        ValueError
            The declared grid inventory or reconstructed comparison is invalid.

        Notes
        -----
        The expected dispersion uses the closed-form finite-difference spectrum and
        does not execute the production sweep analyzer.
        """
        if not isinstance(result, Piab1dEigenpairSweepResult):
            raise TypeError("result must be Piab1dEigenpairSweepResult")
        definition = result.definition
        expected_spacings = definition.length / (
            np.asarray(definition.interior_points, dtype=np.float64) + 1.0
        )
        dimensions = np.concatenate(
            tuple(
                np.full(dimension, dimension, dtype=np.float64)
                for dimension in definition.interior_points
            )
        )
        modes = np.asarray(result.mode_numbers, dtype=np.float64)
        expected_fractions = modes / (dimensions + 1.0)
        arguments = modes * np.pi / (2.0 * (dimensions + 1.0))
        expected_errors = 1.0 - (np.sin(arguments) / arguments) ** 2
        discrepancies = {
            "eigenpair_sweep_spacing_maximum_absolute_error": float(
                np.max(np.abs(result.spacings.magnitude - expected_spacings))
            ),
            "eigenpair_sweep_fractional_index_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        result.fractional_mode_indices.magnitude - expected_fractions
                    )
                )
            ),
            "eigenpair_sweep_dispersion_maximum_absolute_error": float(
                np.max(
                    np.abs(result.relative_energy_errors.magnitude - expected_errors)
                )
            ),
            "eigenpair_sweep_nodal_overlap_defect_maximum": float(
                np.max(result.nodal_overlap_defects.magnitude)
            ),
            "eigenpair_sweep_scaled_residual_maximum": float(
                np.max(result.scaled_eigenpair_residuals.magnitude)
            ),
        }
        unitless = Unitless()
        finest_spacing = float(np.min(expected_spacings))
        lowest_continuum_energy = np.pi**2 / (
            2.0 * definition.mass * definition.length**2
        )
        dispersion_tolerance = float(
            128.0
            * np.finfo(np.float64).eps
            / finest_spacing**2
            / lowest_continuum_energy
        )
        tolerances = {
            name: (
                dispersion_tolerance
                if name == "eigenpair_sweep_dispersion_maximum_absolute_error"
                else 1.0e-12
            )
            for name in discrepancies
        }
        return Piab1dEigenpairSweepReference(
            comparisons={
                name: MaximumAbsoluteErrorComparison(
                    observed=ScalarQuantity(value, unitless),
                    reference=ScalarQuantity(0.0, unitless),
                    tolerance=ScalarQuantity(tolerances[name], unitless),
                )
                for name, value in discrepancies.items()
            }
        )
