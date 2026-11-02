"""Periodic-2D rank-two restricted gauge-alignment request."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.base import (
    Periodic2DRank2GaugeAlignmentAnalysisRequest,
)


class Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest(
    Periodic2DRank2GaugeAlignmentAnalysisRequest
):
    """Bind two represented rank-two matrix fields on one periodic-2D mesh."""

    __slots__ = ("_analysis_identity", "_comparison", "_reference")

    def __init__(
        self,
        *,
        reference: Complex128Array,
        comparison: Complex128Array,
    ) -> None:
        admitted_reference = NumpyImmutableArrayConstructor(
            reference,
            "reference",
            np.dtype(np.complex128),
        ).execute()
        admitted_comparison = NumpyImmutableArrayConstructor(
            comparison,
            "comparison",
            np.dtype(np.complex128),
        ).execute()
        if admitted_reference.shape != admitted_comparison.shape:
            raise ValueError("reference and comparison shapes must match")
        if admitted_reference.ndim != 4 or admitted_reference.shape[-2:] != (2, 2):
            raise ValueError("matrix fields must have shape (N1, N2, 2, 2)")
        if any(size <= 0 for size in admitted_reference.shape[:2]):
            raise ValueError("periodic mesh axes must be nonempty")
        self._reference = admitted_reference
        self._comparison = admitted_comparison
        self._analysis_identity = GaugeAlignmentAnalysisIdentity(
            gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
                represented_dimension=2
            ),
            alignment_sample_count=int(np.prod(admitted_reference.shape[:2])),
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=GaugeAlignmentInnerProductConvention.EUCLIDEAN,
        )

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit retained-space alignment identity."""
        return self._analysis_identity

    @property
    def reference(self) -> Complex128Array:
        """Return the immutable reference represented-operator field."""
        return self._reference

    @property
    def comparison(self) -> Complex128Array:
        """Return the immutable comparison represented-operator field."""
        return self._comparison


__all__ = ["Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest"]
