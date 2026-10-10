"""Prospective controls for a one-dimensional multiband alignment calculation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic1d.model import Periodic1DBlockHamiltonianToyModel


def _nonnegative_increasing_integers(name: str, values: tuple[int, ...]) -> None:
    if not isinstance(values, tuple) or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{name} must contain built-in integers")
    if tuple(sorted(set(values))) != values:
        raise ValueError(f"{name} must be unique and strictly increasing")
    if values[0] < 0:
        raise ValueError(f"{name} must contain nonnegative values")


def _finite_nonnegative_float(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not np.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DMultibandAlignmentCalculationDefinition:
    """Freeze the M2 parent, frame, attack, locality, and sample controls.

    The retained group has rank two.  The attack family is the periodic
    rotation ``exp(-i theta(k) sigma_y)`` with a frozen constant angle and sine
    series.  A generic definition may select the identity; nonidentity is a
    property verified for the retained M2 instance, not guaranteed by this data
    type.  Pointwise unitary Procrustes alignment and one global unitary
    alignment are evaluated separately.  The staggered withheld mesh is
    evaluation-only and cannot alter frames, hoppings, ranges, or tolerances.
    """

    calculation_id: str
    parent_model: Periodic1DBlockHamiltonianToyModel
    retained_rank: int
    reciprocal_mesh_size: int
    withheld_mesh_size: int
    hopping_ranges: tuple[int, ...]
    attack_constant_angle: float
    attack_sine_coefficients: tuple[float, ...]
    external_gap_lower_bound: ScalarQuantity
    overlap_singular_value_threshold: float
    orthonormality_absolute_tolerance: float
    coordinate_absolute_tolerance: float
    reconstruction_absolute_tolerance: float
    hermiticity_absolute_tolerance: ScalarQuantity
    verification_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Reject ambiguous identities, ranks, sample roles, and tolerances."""
        if type(self.calculation_id) is not str:
            raise TypeError("calculation_id must be a built-in str")
        if not self.calculation_id:
            raise ValueError("calculation_id must be nonempty")
        if type(self.parent_model) is not Periodic1DBlockHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DBlockHamiltonianToyModel")
        for name, value in (
            ("retained_rank", self.retained_rank),
            ("reciprocal_mesh_size", self.reciprocal_mesh_size),
            ("withheld_mesh_size", self.withheld_mesh_size),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.retained_rank != 2:
            raise ValueError("the v1 rank-two rotation family requires retained_rank=2")
        if self.retained_rank >= self.parent_model.hopping_model.matrix_dimension:
            raise ValueError("retained rank must be smaller than the parent dimension")
        if self.reciprocal_mesh_size < 4 or self.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal_mesh_size must be even and at least four")
        if self.withheld_mesh_size < 3:
            raise ValueError("withheld_mesh_size must be at least three")
        _nonnegative_increasing_integers("hopping_ranges", self.hopping_ranges)
        if self.hopping_ranges[-1] >= self.reciprocal_mesh_size // 2:
            raise ValueError("hopping ranges must be smaller than half the mesh size")
        _finite_nonnegative_float("attack_constant_angle", self.attack_constant_angle)
        if (
            not isinstance(self.attack_sine_coefficients, tuple)
            or not self.attack_sine_coefficients
        ):
            raise TypeError("attack_sine_coefficients must be a nonempty tuple")
        if any(
            type(coefficient) is not float or not np.isfinite(coefficient)
            for coefficient in self.attack_sine_coefficients
        ):
            raise ValueError(
                "attack_sine_coefficients must contain finite built-in floats"
            )
        for name, numeric_value in (
            (
                "overlap_singular_value_threshold",
                self.overlap_singular_value_threshold,
            ),
            (
                "orthonormality_absolute_tolerance",
                self.orthonormality_absolute_tolerance,
            ),
            ("coordinate_absolute_tolerance", self.coordinate_absolute_tolerance),
            (
                "reconstruction_absolute_tolerance",
                self.reconstruction_absolute_tolerance,
            ),
            (
                "verification_absolute_tolerance",
                self.verification_absolute_tolerance,
            ),
        ):
            _finite_nonnegative_float(name, numeric_value)
        if self.overlap_singular_value_threshold >= 1.0:
            raise ValueError(
                "overlap singular-value threshold must be smaller than one"
            )
        energy_unit = self.parent_model.hopping_model.hopping_blocks[0].unit
        for name, quantity in (
            ("external_gap_lower_bound", self.external_gap_lower_bound),
            (
                "hermiticity_absolute_tolerance",
                self.hermiticity_absolute_tolerance,
            ),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(quantity.unit, energy_unit):
                raise ValueError(f"{name} must use energy dimensions")

    @property
    def withheld_reduced_momenta(self) -> tuple[float, ...]:
        """Return the frozen staggered uniform mesh disjoint from training."""
        offset = 1.0 / float(self.reciprocal_mesh_size + 1)
        return tuple(
            float(-0.5 + (float(index) + offset) / self.withheld_mesh_size)
            for index in range(self.withheld_mesh_size)
        )


__all__ = ["Periodic1DMultibandAlignmentCalculationDefinition"]
