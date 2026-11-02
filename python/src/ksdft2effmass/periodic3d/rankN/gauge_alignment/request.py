"""Periodic-3D arbitrary-rank global unitary-alignment request."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.base import (
    Periodic3DRankNGaugeAlignmentAnalysisRequest,
)

_Periodic3DRankNRequestBase = Periodic3DRankNGaugeAlignmentAnalysisRequest


class Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest(
    _Periodic3DRankNRequestBase
):
    """Bind one constant right-unitary selection over a periodic-3D frame field."""

    __slots__ = ("_analysis_identity", "_source", "_target", "_tolerance")

    def __init__(
        self,
        *,
        retained_rank: int,
        source: Complex128Array,
        target: Complex128Array,
        tolerance: ComplexUnitaryProcrustesTolerance,
    ) -> None:
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        if type(tolerance) is not ComplexUnitaryProcrustesTolerance:
            raise TypeError("tolerance must be ComplexUnitaryProcrustesTolerance")
        admitted_source = NumpyImmutableArrayConstructor(
            source,
            "source",
            np.dtype(np.complex128),
        ).execute()
        admitted_target = NumpyImmutableArrayConstructor(
            target,
            "target",
            np.dtype(np.complex128),
        ).execute()
        if admitted_source.shape != admitted_target.shape:
            raise ValueError("source and target shapes must match")
        if admitted_source.ndim != 5 or admitted_source.shape[-1] != retained_rank:
            raise ValueError(
                "frames must have shape (N1, N2, N3, ambient, retained_rank)"
            )
        if admitted_source.shape[-2] < retained_rank:
            raise ValueError("frame ambient dimension must be at least retained_rank")
        if any(size <= 0 for size in admitted_source.shape[:3]):
            raise ValueError("periodic mesh axes must be nonempty")
        self._source = admitted_source
        self._target = admitted_target
        self._tolerance = tolerance
        self._analysis_identity = GaugeAlignmentAnalysisIdentity(
            gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
                represented_dimension=retained_rank
            ),
            alignment_sample_count=int(np.prod(admitted_source.shape[:3])),
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=GaugeAlignmentInnerProductConvention.EUCLIDEAN,
        )

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit global-alignment identity."""
        return self._analysis_identity

    @property
    def source(self) -> Complex128Array:
        """Return the immutable source-frame field."""
        return self._source

    @property
    def target(self) -> Complex128Array:
        """Return the immutable target-frame field."""
        return self._target

    @property
    def tolerance(self) -> ComplexUnitaryProcrustesTolerance:
        """Return the exact numerical-rank policy."""
        return self._tolerance


__all__ = ["Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest"]
