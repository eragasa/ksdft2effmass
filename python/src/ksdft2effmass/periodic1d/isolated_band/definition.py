"""Prospective controls for a one-dimensional isolated-band calculation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.periodic1d.model import Periodic1DFourierHamiltonianToyModel


def _positive_increasing_integers(name: str, values: tuple[int, ...]) -> None:
    """Reject a non-tuple, empty, Boolean-contaminated, or unordered inventory."""
    if not isinstance(values, tuple) or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{name} must contain built-in integers")
    if tuple(sorted(set(values))) != values:
        raise ValueError(f"{name} must be unique and strictly increasing")
    if values[0] <= 0:
        raise ValueError(f"{name} must contain positive values")


def _nonnegative_increasing_integers(name: str, values: tuple[int, ...]) -> None:
    """Reject an invalid ordered inventory of nonnegative exact integers."""
    if not isinstance(values, tuple) or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{name} must contain built-in integers")
    if tuple(sorted(set(values))) != values:
        raise ValueError(f"{name} must be unique and strictly increasing")
    if values[0] < 0:
        raise ValueError(f"{name} must contain nonnegative values")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCalculationDefinition:
    """Freeze model, sampling, reduction, and numerical-diagnostic controls.

    Parameters
    ----------
    calculation_id
        Stable nonempty M1 calculation identity.
    parent_model
        Scalar Fourier toy parent with explicit direct/reciprocal and energy units.
    plane_wave_cutoffs, finite_difference_points
        Strictly increasing finite-discretization sweep inventories.
    plane_wave_reference_cutoff
        Finite reference cutoff, strictly larger than the plane-wave sweep.
    production_plane_wave_cutoff
        Declared sweep cutoff used for reduction samples.
    parent_sample_reduced_momenta
        Ordered dimensionless coordinates in ``[-0.5, 0.5]`` for parent comparison.
    compared_band_count
        Positive number of low parent bands compared across discretizations.
    reciprocal_mesh_size
        Even training-mesh extent used by the complete discrete Fourier transform.
    hopping_ranges
        Strictly increasing nonnegative finite ranges, each below half the mesh extent.
    withheld_mesh_size
        Extent of the disjoint staggered evaluation mesh.
    coordinate_absolute_tolerance, reconstruction_absolute_tolerance
        Finite nonnegative coordinate and transform tolerances.
    hermiticity_absolute_tolerance, imaginary_absolute_tolerance
        Nonnegative quantities with parent-energy dimensions.
    parseval_absolute_tolerance
        Nonnegative quantity with squared-parent-energy dimensions.

    Notes
    -----
    This definition owns no execution and no acceptance policy.  The training mesh
    supplies the complete finite Fourier transform.  The separately generated
    evaluation mesh cannot update the transform, direct fit, ranges, or tolerances.
    """

    calculation_id: str
    parent_model: Periodic1DFourierHamiltonianToyModel
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    production_plane_wave_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_reduced_momenta: tuple[float, ...]
    compared_band_count: int
    reciprocal_mesh_size: int
    hopping_ranges: tuple[int, ...]
    withheld_mesh_size: int
    coordinate_absolute_tolerance: float
    reconstruction_absolute_tolerance: float
    hermiticity_absolute_tolerance: ScalarQuantity
    parseval_absolute_tolerance: ScalarQuantity
    imaginary_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Reject ambiguous identities, inventories, units, and sample roles."""
        if type(self.calculation_id) is not str:
            raise TypeError("calculation_id must be a built-in str")
        if not self.calculation_id:
            raise ValueError("calculation_id must be nonempty")
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DFourierHamiltonianToyModel")
        _positive_increasing_integers("plane_wave_cutoffs", self.plane_wave_cutoffs)
        _positive_increasing_integers(
            "finite_difference_points", self.finite_difference_points
        )
        _nonnegative_increasing_integers("hopping_ranges", self.hopping_ranges)
        for name, value in (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("production_plane_wave_cutoff", self.production_plane_wave_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("reciprocal_mesh_size", self.reciprocal_mesh_size),
            ("withheld_mesh_size", self.withheld_mesh_size),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError(
                "plane_wave_reference_cutoff must exceed every sweep cutoff"
            )
        if self.production_plane_wave_cutoff not in self.plane_wave_cutoffs:
            raise ValueError(
                "production_plane_wave_cutoff must be one declared sweep cutoff"
            )
        if self.compared_band_count > 2 * self.plane_wave_cutoffs[0] + 1:
            raise ValueError("compared bands must fit every plane-wave basis")
        if any(
            points < max(3, self.compared_band_count + 1)
            for points in self.finite_difference_points
        ):
            raise ValueError(
                "finite-difference grids must fit the requested bands and contain "
                "at least three points"
            )
        if self.reciprocal_mesh_size < 2 or self.reciprocal_mesh_size % 2 != 0:
            raise ValueError(
                "reciprocal_mesh_size must be an even integer of at least two"
            )
        if self.hopping_ranges[-1] >= self.reciprocal_mesh_size // 2:
            raise ValueError(
                "hopping ranges must be smaller than half the reciprocal mesh size"
            )
        if self.withheld_mesh_size < 3:
            raise ValueError("withheld_mesh_size must be at least three")
        momenta = self.parent_sample_reduced_momenta
        if not isinstance(momenta, tuple) or not momenta:
            raise TypeError("parent_sample_reduced_momenta must be a nonempty tuple")
        if any(type(value) is not float for value in momenta):
            raise TypeError(
                "parent_sample_reduced_momenta must contain built-in floats"
            )
        if any(
            not np.isfinite(value) or value < -0.5 or value > 0.5 for value in momenta
        ):
            raise ValueError(
                "parent sample momenta must be finite and lie in [-0.5, 0.5]"
            )
        if tuple(sorted(set(momenta))) != momenta:
            raise ValueError(
                "parent sample momenta must be unique and strictly increasing"
            )
        for tolerance_name, tolerance_value in (
            ("coordinate_absolute_tolerance", self.coordinate_absolute_tolerance),
            (
                "reconstruction_absolute_tolerance",
                self.reconstruction_absolute_tolerance,
            ),
        ):
            if type(tolerance_value) is not float:
                raise TypeError(f"{tolerance_name} must be a built-in float")
            if not np.isfinite(tolerance_value) or tolerance_value < 0.0:
                raise ValueError(f"{tolerance_name} must be finite and nonnegative")
        energy_unit = self.parent_model.recoil_energy.unit
        for name, tolerance in (
            ("hermiticity_absolute_tolerance", self.hermiticity_absolute_tolerance),
            ("imaginary_absolute_tolerance", self.imaginary_absolute_tolerance),
        ):
            if type(tolerance) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if tolerance.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(tolerance.unit, energy_unit):
                raise ValueError(f"{name} must use energy dimensions")
        if type(self.parseval_absolute_tolerance) is not ScalarQuantity:
            raise TypeError("parseval_absolute_tolerance must be ScalarQuantity")
        if self.parseval_absolute_tolerance.magnitude < 0.0:
            raise ValueError("parseval_absolute_tolerance must be nonnegative")
        squared_energy_unit = (
            Unitless()
            if isinstance(energy_unit, Unitless)
            else PhysicalUnit(f"({energy_unit.expression}) ** 2")
        )
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.parseval_absolute_tolerance.unit, squared_energy_unit
        ):
            raise ValueError(
                "parseval_absolute_tolerance must use squared-energy dimensions"
            )

    @property
    def withheld_reduced_momenta(self) -> tuple[float, ...]:
        """Return the frozen staggered mesh, disjoint from the training mesh.

        For training extent ``N`` and withheld extent ``M``, point ``i`` is
        ``-1/2 + (i + 1/(N+1))/M``. Training points are rational multiples with
        denominator ``N``; the nonintegral ``N/(N+1)`` offset prevents equality while
        preserving a uniform withheld mesh over one reciprocal period.
        """
        offset = 1.0 / float(self.reciprocal_mesh_size + 1)
        return tuple(
            float(-0.5 + (float(index) + offset) / self.withheld_mesh_size)
            for index in range(self.withheld_mesh_size)
        )


__all__ = ["Periodic1DIsolatedBandCalculationDefinition"]
