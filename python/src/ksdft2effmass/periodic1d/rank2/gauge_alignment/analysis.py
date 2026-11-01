"""Rank-two pointwise and global right-unitary gauge alignment."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.gauge_alignment import (
    Periodic1DGaugeAlignmentAnalysisRequest,
    Periodic1DGaugeAlignmentAnalyzer,
)
from ksdft2effmass.solidstate import ReciprocalBandFramePath1D

from .result import Periodic1DRank2GaugeAlignmentAnalysis


@dataclass(frozen=True, slots=True)
class Periodic1DRank2GaugeAlignmentAnalysisRequest(
    Periodic1DGaugeAlignmentAnalysisRequest
):
    """Bind two rank-two frame paths and the declared Procrustes tolerances."""

    reference: ReciprocalBandFramePath1D
    attacked: ReciprocalBandFramePath1D
    rank_absolute_tolerance: float
    rank_relative_tolerance: float
    validation_absolute_tolerance: float

    def __post_init__(self) -> None:
        if type(self.reference) is not ReciprocalBandFramePath1D:
            raise TypeError("reference must be ReciprocalBandFramePath1D")
        if type(self.attacked) is not ReciprocalBandFramePath1D:
            raise TypeError("attacked must be ReciprocalBandFramePath1D")
        if self.reference.rank != 2 or self.attacked.rank != 2:
            raise ValueError("reference and attacked paths must both have rank two")
        if self.attacked.mesh != self.reference.mesh:
            raise ValueError("reference and attacked meshes must agree")
        if self.attacked.ambient_dimension != self.reference.ambient_dimension:
            raise ValueError("reference and attacked ambient dimensions must agree")
        if not np.array_equal(
            self.attacked.sewing_map.magnitude,
            self.reference.sewing_map.magnitude,
        ):
            raise ValueError("reference and attacked sewing maps must agree")
        for value, name in (
            (self.rank_absolute_tolerance, "rank_absolute_tolerance"),
            (self.rank_relative_tolerance, "rank_relative_tolerance"),
            (self.validation_absolute_tolerance, "validation_absolute_tolerance"),
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
            alignment_sample_count=self.reference.mesh.point_count,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=(
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL
            ),
        )


class Periodic1DRank2GaugeAlignmentAnalyzer(
    Periodic1DGaugeAlignmentAnalyzer[
        Periodic1DRank2GaugeAlignmentAnalysisRequest,
        Periodic1DRank2GaugeAlignmentAnalysis,
    ]
):
    """Select pointwise and aggregate right-unitary transformations."""

    __slots__ = ("_request", "_solver")

    def __init__(
        self,
        request: Periodic1DRank2GaugeAlignmentAnalysisRequest,
        solver: NumpyBatchedComplexUnitaryProcrustesSolver,
    ) -> None:
        if type(request) is not Periodic1DRank2GaugeAlignmentAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DRank2GaugeAlignmentAnalysisRequest"
            )
        if type(solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError(
                "solver must be NumpyBatchedComplexUnitaryProcrustesSolver"
            )
        self._request = request
        self._solver = solver

    @property
    def request(self) -> Periodic1DRank2GaugeAlignmentAnalysisRequest:
        """Return the complete immutable alignment request."""
        return self._request

    @property
    def solver(self) -> NumpyBatchedComplexUnitaryProcrustesSolver:
        """Return the explicitly selected Procrustes collaborator."""
        return self._solver

    def execute(self) -> Periodic1DRank2GaugeAlignmentAnalysis:
        """Return pointwise and one-global-unitary aligned frame paths."""
        request = self.request
        tolerance = ComplexUnitaryProcrustesTolerance(
            rank_absolute=request.rank_absolute_tolerance,
            rank_relative=request.rank_relative_tolerance,
            validation_absolute=request.validation_absolute_tolerance,
            validation_relative=0.0,
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        )
        source = np.asarray(
            [frame.magnitude for frame in request.attacked.frames],
            dtype=np.complex128,
        )
        target = np.asarray(
            [frame.magnitude for frame in request.reference.frames],
            dtype=np.complex128,
        )
        pointwise_selection = self.solver.solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source,
                target,
                tolerance,
            )
        )
        pointwise_values = (
            pointwise_selection.require_unique_right_unitary_transformations()
        )
        pointwise_aligned = _rotate_path(
            request.attacked,
            tuple(pointwise_values[index] for index in range(source.shape[0])),
        )
        global_selection = self.solver.solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source.reshape(1, -1, source.shape[-1]),
                target.reshape(1, -1, target.shape[-1]),
                tolerance,
            )
        )
        global_value = (
            global_selection.require_unique_right_unitary_transformations()[0]
        )
        globally_aligned = _rotate_path(
            request.attacked,
            tuple(global_value for _ in range(request.attacked.mesh.point_count)),
        )
        unit = Unitless()
        return Periodic1DRank2GaugeAlignmentAnalysis(
            pointwise_aligned=pointwise_aligned,
            globally_aligned=globally_aligned,
            pointwise_rotations=tuple(
                ComplexMatrixQuantity(value, unit) for value in pointwise_values
            ),
            global_rotation=ComplexMatrixQuantity(global_value, unit),
            pointwise_minimum_cross_singular_value=float(
                np.min(pointwise_selection.cross_singular_values)
            ),
            global_minimum_cross_singular_value=float(
                np.min(global_selection.cross_singular_values)
            ),
            pointwise_maximum_rank_cutoff=float(
                np.max(pointwise_selection.applied_rank_cutoffs)
            ),
            global_rank_cutoff=float(global_selection.applied_rank_cutoffs[0]),
        )


def _rotate_path(
    source: ReciprocalBandFramePath1D,
    rotations: tuple[Complex128Array, ...],
) -> ReciprocalBandFramePath1D:
    if len(rotations) != source.mesh.point_count:
        raise ValueError("one rotation is required per reciprocal point")
    return ReciprocalBandFramePath1D(
        mesh=source.mesh,
        frames=tuple(
            ComplexMatrixQuantity(frame.magnitude @ rotation, Unitless())
            for frame, rotation in zip(source.frames, rotations, strict=True)
        ),
        sewing_map=source.sewing_map,
        orthonormality_absolute_tolerance=source.orthonormality_absolute_tolerance,
    )


__all__ = [
    "Periodic1DRank2GaugeAlignmentAnalyzer",
    "Periodic1DRank2GaugeAlignmentAnalysisRequest",
]
