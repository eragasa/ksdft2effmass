"""Rank-two pointwise and global gauge-alignment capability values."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.solidstate import ReciprocalBandFramePath1D


@dataclass(frozen=True, slots=True)
class Periodic1DRank2GaugeAlignmentResult:
    """Retain selected right actions and their aligned frame paths."""

    pointwise_aligned: ReciprocalBandFramePath1D
    globally_aligned: ReciprocalBandFramePath1D
    pointwise_rotations: tuple[ComplexMatrixQuantity, ...]
    global_rotation: ComplexMatrixQuantity
    pointwise_minimum_cross_singular_value: float
    global_minimum_cross_singular_value: float
    pointwise_maximum_rank_cutoff: float
    global_rank_cutoff: float

    def __post_init__(self) -> None:
        if type(self.pointwise_aligned) is not ReciprocalBandFramePath1D:
            raise TypeError("pointwise_aligned must be ReciprocalBandFramePath1D")
        if type(self.globally_aligned) is not ReciprocalBandFramePath1D:
            raise TypeError("globally_aligned must be ReciprocalBandFramePath1D")
        if not isinstance(self.pointwise_rotations, tuple) or any(
            type(value) is not ComplexMatrixQuantity
            or value.magnitude.shape != (2, 2)
            or not isinstance(value.unit, Unitless)
            for value in self.pointwise_rotations
        ):
            raise TypeError(
                "pointwise_rotations must contain unitless two-by-two matrices"
            )
        if (
            type(self.global_rotation) is not ComplexMatrixQuantity
            or self.global_rotation.magnitude.shape != (2, 2)
            or not isinstance(self.global_rotation.unit, Unitless)
        ):
            raise TypeError("global_rotation must be a unitless two-by-two matrix")
        for value, name in (
            (
                self.pointwise_minimum_cross_singular_value,
                "pointwise_minimum_cross_singular_value",
            ),
            (
                self.global_minimum_cross_singular_value,
                "global_minimum_cross_singular_value",
            ),
            (
                self.pointwise_maximum_rank_cutoff,
                "pointwise_maximum_rank_cutoff",
            ),
            (self.global_rank_cutoff, "global_rank_cutoff"),
        ):
            if type(value) is not float or not isfinite(value):
                raise TypeError(f"{name} must be a finite built-in float")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


__all__ = ["Periodic1DRank2GaugeAlignmentResult"]
