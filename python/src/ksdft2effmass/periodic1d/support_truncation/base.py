"""Periodic one-dimensional specialization of real-space support truncation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic1d.base import Periodic1DCapability
from ksdft2effmass.real_space_support_truncation.base import (
    RealSpaceSupportTruncation,
)
from ksdft2effmass.support_truncation.base import (
    SupportTruncationAnalysis,
    SupportTruncationAnalysisRequest,
    SupportTruncationAnalyzer,
)


class Periodic1DSupportTruncation(
    RealSpaceSupportTruncation,
    Periodic1DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal of periodic 1D translation support.

    Concrete subclasses must state the integer-translation support, conjugate-closure
    rule, basis and gauge, and normalization used to assess removal consequences.
    :attr:`lattice_dimension` fixes only the PhysKit one-dimensional identity. The
    specialization owns no cutoff inventory, transform backend, tolerance, selection
    policy, or wire format.
    """

    __slots__ = ()


class Periodic1DSupportTruncationAnalysisRequest(
    SupportTruncationAnalysisRequest,
    Periodic1DSupportTruncation,
    ABC,
):
    """Bind one periodic-1D support-removal analysis request."""

    __slots__ = ()


class Periodic1DSupportTruncationAnalysis(
    SupportTruncationAnalysis,
    Periodic1DSupportTruncation,
    ABC,
):
    """Retain one periodic-1D support-removal analysis."""

    __slots__ = ()


class Periodic1DSupportTruncationAnalyzer[
    SupportTruncationRequestT: Periodic1DSupportTruncationAnalysisRequest,
    SupportTruncationAnalysisT: Periodic1DSupportTruncationAnalysis,
](
    SupportTruncationAnalyzer[
        SupportTruncationRequestT,
        SupportTruncationAnalysisT,
    ],
    Periodic1DSupportTruncation,
    ABC,
):
    """Execute one periodic-1D support-removal analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic1DSupportTruncation",
    "Periodic1DSupportTruncationAnalysis",
    "Periodic1DSupportTruncationAnalysisRequest",
    "Periodic1DSupportTruncationAnalyzer",
]
