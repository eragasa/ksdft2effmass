"""Periodic three-dimensional specialization of real-space support truncation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic3d.base import Periodic3DCapability
from ksdft2effmass.real_space_support_truncation.base import (
    PeriodicRealSpaceSupportTruncation,
    PeriodicRealSpaceSupportTruncationAnalysis,
    PeriodicRealSpaceSupportTruncationAnalysisRequest,
    PeriodicRealSpaceSupportTruncationAnalyzer,
)


class Periodic3DSupportTruncation(
    PeriodicRealSpaceSupportTruncation,
    Periodic3DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal of periodic 3D translation support.

    Concrete subclasses must state the integer-translation support, physical-metric
    shell geometry, conjugate-closure rule, basis and gauge, and normalization used to
    assess removal consequences. This specialization owns no cutoff inventory,
    transform backend, tolerance, selection policy, direct lattice, or wire format.
    """

    __slots__ = ()


class Periodic3DSupportTruncationAnalysisRequest(
    PeriodicRealSpaceSupportTruncationAnalysisRequest,
    Periodic3DSupportTruncation,
    ABC,
):
    """Bind one periodic-3D support-removal analysis request."""

    __slots__ = ()


class Periodic3DSupportTruncationAnalysis(
    PeriodicRealSpaceSupportTruncationAnalysis,
    Periodic3DSupportTruncation,
    ABC,
):
    """Retain one periodic-3D support-removal analysis."""

    __slots__ = ()


class Periodic3DSupportTruncationAnalyzer[
    RequestT: Periodic3DSupportTruncationAnalysisRequest,
    AnalysisT: Periodic3DSupportTruncationAnalysis,
](
    PeriodicRealSpaceSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic3DSupportTruncation,
    ABC,
):
    """Execute one periodic-3D support-removal analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic3DSupportTruncation",
    "Periodic3DSupportTruncationAnalysis",
    "Periodic3DSupportTruncationAnalysisRequest",
    "Periodic3DSupportTruncationAnalyzer",
]
