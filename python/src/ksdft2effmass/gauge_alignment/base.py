"""Scientific ownership and analysis-role bases for gauge alignment."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final


class GaugeAlignment(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify a gauge-alignment capability or its exact applicability boundary.

    Concrete subclasses must state the represented state space, gauge group, action
    convention, and whether a nontrivial alignment exists. Membership does not imply
    representation equivalence, frame transport, coefficient locality, support
    truncation, or successful numerical recovery. This base owns no solver, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class GaugeAlignmentAnalysisIdentity:
    """Retain the common finite scientific identity of one alignment analysis."""

    retained_rank: int
    gauge_group: str
    alignment_sample_count: int

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank <= 0:
            raise ValueError("retained_rank must be positive")
        if type(self.gauge_group) is not str:
            raise TypeError("gauge_group must be a built-in string")
        if not self.gauge_group:
            raise ValueError("gauge_group must not be empty")
        if type(self.alignment_sample_count) is not int:
            raise TypeError("alignment_sample_count must be a built-in integer")
        if self.alignment_sample_count <= 0:
            raise ValueError("alignment_sample_count must be positive")


class _GaugeAlignmentAnalysisIdentityOwner(GaugeAlignment, ABC):
    """Provide validated common accessors from one explicit analysis identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the immutable finite scientific identity of this analysis role."""

    @property
    @final
    def retained_rank(self) -> int:
        """Return the dimension of the represented retained state space."""
        return self.analysis_identity.retained_rank

    @property
    @final
    def gauge_group(self) -> str:
        """Return the explicitly declared retained-space gauge group."""
        return self.analysis_identity.gauge_group

    @property
    @final
    def alignment_sample_count(self) -> int:
        """Return the number of ordered samples covered by the analysis."""
        return self.analysis_identity.alignment_sample_count


class GaugeAlignmentAnalysisRequest(_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Bind the common scientific identity of one finite alignment analysis."""

    __slots__ = ()


class GaugeAlignmentAnalysis(_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Expose the common scientific identity retained by an alignment analysis."""

    __slots__ = ()


class GaugeAlignmentAnalyzer[
    GaugeAlignmentAnalysisRequestT: GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalysisT: GaugeAlignmentAnalysis,
](_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Execute one exact request and return one gauge-alignment analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> GaugeAlignmentAnalysisRequestT:
        """Return the complete immutable request bound to this action."""

    @property
    @final
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the scientific identity delegated by the bound request."""
        return self.request.analysis_identity

    @abstractmethod
    def execute(self) -> GaugeAlignmentAnalysisT:
        """Execute the bound gauge-alignment analysis without external effects."""


__all__ = [
    "GaugeAlignment",
    "GaugeAlignmentAnalysis",
    "GaugeAlignmentAnalysisIdentity",
    "GaugeAlignmentAnalysisRequest",
    "GaugeAlignmentAnalyzer",
]
