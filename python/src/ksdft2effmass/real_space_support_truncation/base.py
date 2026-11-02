"""Scientific ownership bases for real-space support truncation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.support_truncation.base import (
    SupportTruncation,
    SupportTruncationAnalysis,
    SupportTruncationAnalysisRequest,
    SupportTruncationAnalyzer,
)


class RealSpaceSupportTruncation(
    SupportTruncation,
    ABC,
):  # noqa: B024 - intentionally nominal marker
    """Identify one irreversible truncation of represented real-space support.

    This specialization fixes the generic support domain to represented real space.
    Concrete subclasses must declare the support geometry and conjugate-closure rule.
    Operator and band errors retained by subclasses are consequences of spatial support
    removal; they are not spectral-subspace truncation errors. This base owns no lattice
    primitive, Fourier backend, threshold policy, or serialization format.
    """

    __slots__ = ()


class RealSpaceSupportTruncationAnalysisRequest(
    SupportTruncationAnalysisRequest,
    RealSpaceSupportTruncation,
    ABC,
):
    """Bind one irreversible real-space support-removal request."""

    __slots__ = ()


class RealSpaceSupportTruncationAnalysis(
    SupportTruncationAnalysis,
    RealSpaceSupportTruncation,
    ABC,
):
    """Retain one real-space support-removal analysis."""

    __slots__ = ()


class RealSpaceSupportTruncationAnalyzer[
    RequestT: RealSpaceSupportTruncationAnalysisRequest,
    AnalysisT: RealSpaceSupportTruncationAnalysis,
](
    SupportTruncationAnalyzer[RequestT, AnalysisT],
    RealSpaceSupportTruncation,
    ABC,
):
    """Execute one real-space support-removal request."""

    __slots__ = ()


class PeriodicRealSpaceSupportTruncation(
    RealSpaceSupportTruncation,
    ABC,
):  # noqa: B024 - intentionally nominal marker
    """Identify real-space support truncation under periodic boundaries."""

    __slots__ = ()


class PeriodicRealSpaceSupportTruncationAnalysisRequest(
    RealSpaceSupportTruncationAnalysisRequest,
    PeriodicRealSpaceSupportTruncation,
    ABC,
):
    """Bind one periodic real-space support-removal request."""

    __slots__ = ()


class PeriodicRealSpaceSupportTruncationAnalysis(
    RealSpaceSupportTruncationAnalysis,
    PeriodicRealSpaceSupportTruncation,
    ABC,
):
    """Retain one periodic real-space support-removal analysis."""

    __slots__ = ()


class PeriodicRealSpaceSupportTruncationAnalyzer[
    RequestT: PeriodicRealSpaceSupportTruncationAnalysisRequest,
    AnalysisT: PeriodicRealSpaceSupportTruncationAnalysis,
](
    RealSpaceSupportTruncationAnalyzer[RequestT, AnalysisT],
    PeriodicRealSpaceSupportTruncation,
    ABC,
):
    """Execute one periodic real-space support-removal request."""

    __slots__ = ()


__all__ = [
    "PeriodicRealSpaceSupportTruncation",
    "PeriodicRealSpaceSupportTruncationAnalysis",
    "PeriodicRealSpaceSupportTruncationAnalysisRequest",
    "PeriodicRealSpaceSupportTruncationAnalyzer",
    "RealSpaceSupportTruncation",
    "RealSpaceSupportTruncationAnalysis",
    "RealSpaceSupportTruncationAnalysisRequest",
    "RealSpaceSupportTruncationAnalyzer",
]
