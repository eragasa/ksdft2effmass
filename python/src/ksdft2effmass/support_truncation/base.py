"""Nominal scientific base for irreversible support truncation."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SupportTruncation(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal from a declared representation support.

    Concrete subclasses must identify the represented object, support index space,
    retained and omitted support, and any closure rule needed by that representation.
    This base does not select a physical domain, geometry, algorithm, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


class SupportTruncationAnalysisRequest(SupportTruncation, ABC):
    """Bind one exact irreversible support-removal analysis."""

    __slots__ = ()


class SupportTruncationAnalysis(SupportTruncation, ABC):
    """Retain one exact irreversible support-removal analysis."""

    __slots__ = ()


class SupportTruncationAnalyzer[
    SupportTruncationAnalysisRequestT: SupportTruncationAnalysisRequest,
    SupportTruncationAnalysisT: SupportTruncationAnalysis,
](SupportTruncation, ABC):
    """Execute one bound support-truncation analysis request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> SupportTruncationAnalysisRequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> SupportTruncationAnalysisT:
        """Execute irreversible support removal and retain its consequences."""


__all__ = [
    "SupportTruncation",
    "SupportTruncationAnalysis",
    "SupportTruncationAnalysisRequest",
    "SupportTruncationAnalyzer",
]
