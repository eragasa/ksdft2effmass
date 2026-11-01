"""Rank-two pointwise and global gauge-alignment analysis value."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.gauge_alignment import (
    Periodic1DGaugeAlignmentAnalysis,
)
from ksdft2effmass.solidstate import ReciprocalBandFramePath1D


@dataclass(frozen=True, slots=True)
class Periodic1DRank2GaugeAlignmentAnalysis(
    Periodic1DGaugeAlignmentAnalysis
):
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
        if self.pointwise_aligned.rank != 2 or self.globally_aligned.rank != 2:
            raise ValueError("aligned paths must both have rank two")
        if self.globally_aligned.mesh != self.pointwise_aligned.mesh:
            raise ValueError("aligned path meshes must agree")
        if (
            self.globally_aligned.ambient_dimension
            != self.pointwise_aligned.ambient_dimension
        ):
            raise ValueError("aligned path ambient dimensions must agree")
        if not np.array_equal(
            self.globally_aligned.sewing_map.magnitude,
            self.pointwise_aligned.sewing_map.magnitude,
        ):
            raise ValueError("aligned path sewing maps must agree")
        if not isinstance(self.pointwise_rotations, tuple) or any(
            type(value) is not ComplexMatrixQuantity
            or value.magnitude.shape != (2, 2)
            or not isinstance(value.unit, Unitless)
            for value in self.pointwise_rotations
        ):
            raise TypeError(
                "pointwise_rotations must contain unitless two-by-two matrices"
            )
        if len(self.pointwise_rotations) != self.pointwise_aligned.mesh.point_count:
            raise ValueError(
                "pointwise rotation count must equal the aligned mesh point count"
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

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the finite rank-two alignment identity."""
        return GaugeAlignmentAnalysisIdentity(
            retained_rank=2,
            gauge_group="U(2)",
            alignment_sample_count=self.pointwise_aligned.mesh.point_count,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=(
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL
            ),
        )


__all__ = ["Periodic1DRank2GaugeAlignmentAnalysis"]
