"""Scientific ownership bases for represented-field interpolation."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Interpolation(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify evaluation of a represented field away from its source samples.

    Concrete subclasses must declare the source representation, evaluation coordinates,
    basis, energy reference, and comparison target. Membership does not imply Fourier
    construction, hopping locality, support truncation, or acceptance of interpolation
    error. This base owns no evaluator backend, mesh, tolerance, or wire format.
    """

    __slots__ = ()


class InterpolationAnalysisRequest(Interpolation, ABC):
    """Bind one immutable interpolation-analysis request."""

    __slots__ = ()


class InterpolationAnalysis(Interpolation, ABC):
    """Retain one interpolation analysis and its comparison diagnostics."""

    __slots__ = ()


class InterpolationAnalyzer[
    RequestT: InterpolationAnalysisRequest,
    AnalysisT: InterpolationAnalysis,
](Interpolation, ABC):
    """Execute one exact interpolation-analysis request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound interpolation analysis without external effects."""


class PeriodicInterpolation(Interpolation, ABC):  # noqa: B024
    """Identify interpolation of a field represented on a periodic domain."""

    __slots__ = ()


class PeriodicRankNInterpolationCapability(PeriodicInterpolation, ABC):
    """Identify periodic interpolation of finite-rank matrix-valued fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class PeriodicInterpolationAnalysisRequest(
    InterpolationAnalysisRequest,
    PeriodicInterpolation,
    ABC,
):
    """Bind one periodic interpolation-analysis request."""

    __slots__ = ()


class PeriodicInterpolationAnalysis(
    InterpolationAnalysis,
    PeriodicInterpolation,
    ABC,
):
    """Retain one periodic interpolation analysis."""

    __slots__ = ()


class PeriodicInterpolationAnalyzer[
    RequestT: PeriodicInterpolationAnalysisRequest,
    AnalysisT: PeriodicInterpolationAnalysis,
](
    InterpolationAnalyzer[RequestT, AnalysisT],
    PeriodicInterpolation,
    ABC,
):
    """Execute one periodic interpolation-analysis request."""

    __slots__ = ()


__all__ = [
    "Interpolation",
    "InterpolationAnalysis",
    "InterpolationAnalysisRequest",
    "InterpolationAnalyzer",
    "PeriodicInterpolation",
    "PeriodicInterpolationAnalysis",
    "PeriodicInterpolationAnalysisRequest",
    "PeriodicInterpolationAnalyzer",
    "PeriodicRankNInterpolationCapability",
]
