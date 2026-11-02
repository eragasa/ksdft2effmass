"""Periodic two-dimensional specialization of real-space support truncation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.real_space_support_truncation.base import (
    PeriodicRealSpaceSupportTruncation,
    PeriodicRealSpaceSupportTruncationAnalysis,
    PeriodicRealSpaceSupportTruncationAnalysisRequest,
    PeriodicRealSpaceSupportTruncationAnalyzer,
)


class Periodic2DSupportTruncation(
    PeriodicRealSpaceSupportTruncation,
    Periodic2DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal of periodic 2D translation support.

    Concrete subclasses must state the integer-translation support, physical-metric
    shell geometry, conjugate-closure rule, basis and gauge, and normalization used to
    assess removal consequences. This specialization owns no cutoff inventory,
    transform backend, tolerance, selection policy, direct lattice, or wire format.
    """

    __slots__ = ()


class Periodic2DSupportTruncationAnalysisRequest(
    PeriodicRealSpaceSupportTruncationAnalysisRequest,
    Periodic2DSupportTruncation,
    ABC,
):
    """Bind one periodic-2D support-removal analysis request."""

    __slots__ = ()


class Periodic2DSupportTruncationAnalysis(
    PeriodicRealSpaceSupportTruncationAnalysis,
    Periodic2DSupportTruncation,
    ABC,
):
    """Retain one periodic-2D support-removal analysis."""

    __slots__ = ()


class Periodic2DSupportTruncationAnalyzer[
    RequestT: Periodic2DSupportTruncationAnalysisRequest,
    AnalysisT: Periodic2DSupportTruncationAnalysis,
](
    PeriodicRealSpaceSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic2DSupportTruncation,
    ABC,
):
    """Execute one periodic-2D support-removal analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic2DSupportTruncation",
    "Periodic2DSupportTruncationAnalysis",
    "Periodic2DSupportTruncationAnalysisRequest",
    "Periodic2DSupportTruncationAnalyzer",
]
