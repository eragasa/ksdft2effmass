"""Scientific ownership and analysis-role bases for gauge alignment."""

from __future__ import annotations

from abc import ABC, abstractmethod


class GaugeAlignment(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify a gauge-alignment capability or its exact applicability boundary.

    Concrete subclasses must state the represented state space, gauge group, action
    convention, and whether a nontrivial alignment exists. Membership does not imply
    representation equivalence, frame transport, coefficient locality, support
    truncation, or successful numerical recovery. This base owns no solver, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


class GaugeAlignmentAnalysisRequest(GaugeAlignment, ABC):
    """Bind the common scientific identity of one finite alignment analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def retained_rank(self) -> int:
        """Return the dimension of the represented retained state space."""

    @property
    @abstractmethod
    def gauge_group(self) -> str:
        """Return the explicitly declared retained-space gauge group."""

    @property
    @abstractmethod
    def alignment_sample_count(self) -> int:
        """Return the number of ordered samples covered by the analysis."""


class GaugeAlignmentAnalysis(GaugeAlignment, ABC):
    """Expose the common scientific identity retained by an alignment analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def retained_rank(self) -> int:
        """Return the dimension of the represented retained state space."""

    @property
    @abstractmethod
    def gauge_group(self) -> str:
        """Return the explicitly declared retained-space gauge group."""

    @property
    @abstractmethod
    def alignment_sample_count(self) -> int:
        """Return the number of ordered samples covered by the analysis."""


class GaugeAlignmentAnalyzer[
    GaugeAlignmentAnalysisRequestT: GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalysisT: GaugeAlignmentAnalysis,
](GaugeAlignment, ABC):
    """Execute one exact request and return one gauge-alignment analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> GaugeAlignmentAnalysisRequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> GaugeAlignmentAnalysisT:
        """Execute the bound gauge-alignment analysis without external effects."""


__all__ = [
    "GaugeAlignment",
    "GaugeAlignmentAnalysis",
    "GaugeAlignmentAnalysisRequest",
    "GaugeAlignmentAnalyzer",
]
