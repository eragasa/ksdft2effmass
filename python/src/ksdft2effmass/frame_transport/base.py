"""Scientific ownership and analysis-role bases for frame transport."""

from __future__ import annotations

from abc import ABC, abstractmethod


class FrameTransport(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify transport of represented frames along an explicit route.

    Concrete subclasses must identify the represented state space, frame convention,
    route and orientation, link construction, action convention, inner product, and
    any closure or sewing condition. Membership does not imply gauge recovery, band
    equivalence, hopping locality, support truncation, or successful numerical
    transport. This base owns no solver, tolerance, lattice, or wire format.
    """

    __slots__ = ()


class FrameTransportAnalysisRequest(FrameTransport, ABC):
    """Bind one immutable frame-transport analysis request."""

    __slots__ = ()


class FrameTransportAnalysis(FrameTransport, ABC):
    """Retain one frame-transport analysis or typed applicability outcome."""

    __slots__ = ()


class FrameTransportAnalyzer[
    RequestT: FrameTransportAnalysisRequest,
    AnalysisT: FrameTransportAnalysis,
](FrameTransport, ABC):
    """Execute one exact frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis without external effects."""


class PeriodicFrameTransport(FrameTransport, ABC):  # noqa: B024
    """Identify frame transport under periodic boundary conditions."""

    __slots__ = ()


class PeriodicRankNFrameTransportCapability(PeriodicFrameTransport, ABC):
    """Identify periodic frame transport on a finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite transported band-subspace rank."""


class PeriodicFrameTransportAnalysisRequest(
    FrameTransportAnalysisRequest,
    PeriodicFrameTransport,
    ABC,
):
    """Bind one periodic frame-transport analysis request."""

    __slots__ = ()


class PeriodicFrameTransportAnalysis(
    FrameTransportAnalysis,
    PeriodicFrameTransport,
    ABC,
):
    """Retain one periodic frame-transport analysis outcome."""

    __slots__ = ()


class PeriodicFrameTransportAnalyzer[
    RequestT: PeriodicFrameTransportAnalysisRequest,
    AnalysisT: PeriodicFrameTransportAnalysis,
](
    FrameTransportAnalyzer[RequestT, AnalysisT],
    PeriodicFrameTransport,
    ABC,
):
    """Execute one periodic frame-transport request."""

    __slots__ = ()


__all__ = [
    "FrameTransport",
    "FrameTransportAnalysis",
    "FrameTransportAnalysisRequest",
    "FrameTransportAnalyzer",
    "PeriodicFrameTransport",
    "PeriodicFrameTransportAnalysis",
    "PeriodicFrameTransportAnalysisRequest",
    "PeriodicFrameTransportAnalyzer",
    "PeriodicRankNFrameTransportCapability",
]
