"""Periodic-2D rank-two pointwise Procrustes request."""

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
from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalysisRequest,
)

_Periodic2DRequestBase = Periodic2DGaugeAlignmentAnalysisRequest


class Periodic2DRank2ProcrustesAnalysisRequest(_Periodic2DRequestBase):
    """Bind correlated rank-two source and target frames on one periodic-2D mesh."""

    __slots__ = ("_analysis_identity", "_source", "_target", "_tolerance")

    def __init__(
        self,
        *,
        source: Complex128Array,
        target: Complex128Array,
        tolerance: ComplexUnitaryProcrustesTolerance,
    ) -> None:
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
        if admitted_source.ndim != 4 or admitted_source.shape[-1] != 2:
            raise ValueError("frames must have shape (N1, N2, ambient, 2)")
        if admitted_source.shape[-2] < 2:
            raise ValueError("frame ambient dimension must be at least two")
        self._source = admitted_source
        self._target = admitted_target
        self._tolerance = tolerance
        self._analysis_identity = GaugeAlignmentAnalysisIdentity(
            gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
                represented_dimension=2
            ),
            alignment_sample_count=int(np.prod(admitted_source.shape[:2])),
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=GaugeAlignmentInnerProductConvention.EUCLIDEAN,
        )

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit pointwise alignment identity."""
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
        """Return the exact numerical-rank and backend-validation policy."""
        return self._tolerance


__all__ = ["Periodic2DRank2ProcrustesAnalysisRequest"]
