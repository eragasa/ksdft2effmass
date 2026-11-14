"""Scientific ownership bases for finite-periodic Fourier analysis."""

from __future__ import annotations

from abc import ABC, abstractmethod


class FourierAnalysis(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify Fourier analysis of one represented field.

    Concrete subclasses must declare the sampled domain, coefficient index space,
    basis, energy reference, transform convention, and reconstruction diagnostics.
    Membership does not imply interpolation, hopping locality, support truncation, or
    scientific adequacy. This base owns no transform backend, mesh, tolerance, or wire
    format.
    """

    __slots__ = ()


class FourierAnalysisRequest(FourierAnalysis, ABC):
    """Bind one immutable Fourier-analysis request."""

    __slots__ = ()


class FourierAnalysisResult(FourierAnalysis, ABC):
    """Retain one Fourier analysis and its structural diagnostics."""

    __slots__ = ()


class FourierAnalyzer[
    RequestT: FourierAnalysisRequest,
    ResultT: FourierAnalysisResult,
](FourierAnalysis, ABC):
    """Execute one exact Fourier-analysis request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> ResultT:
        """Execute the bound Fourier analysis without external effects."""


class PeriodicFourierAnalysis(FourierAnalysis, ABC):  # noqa: B024
    """Identify Fourier analysis on a finite periodic domain."""

    __slots__ = ()


class PeriodicRankNFourierAnalysisCapability(PeriodicFourierAnalysis, ABC):
    """Identify periodic Fourier analysis of finite-rank matrix-valued fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class PeriodicFourierAnalysisRequest(
    FourierAnalysisRequest,
    PeriodicFourierAnalysis,
    ABC,
):
    """Bind one periodic Fourier-analysis request."""

    __slots__ = ()


class PeriodicFourierAnalysisResult(
    FourierAnalysisResult,
    PeriodicFourierAnalysis,
    ABC,
):
    """Retain one periodic Fourier analysis."""

    __slots__ = ()


class PeriodicFourierAnalyzer[
    RequestT: PeriodicFourierAnalysisRequest,
    ResultT: PeriodicFourierAnalysisResult,
](
    FourierAnalyzer[RequestT, ResultT],
    PeriodicFourierAnalysis,
    ABC,
):
    """Execute one periodic Fourier-analysis request."""

    __slots__ = ()


__all__ = [
    "FourierAnalysis",
    "FourierAnalysisRequest",
    "FourierAnalysisResult",
    "FourierAnalyzer",
    "PeriodicFourierAnalysis",
    "PeriodicFourierAnalysisRequest",
    "PeriodicFourierAnalysisResult",
    "PeriodicFourierAnalyzer",
    "PeriodicRankNFourierAnalysisCapability",
]
