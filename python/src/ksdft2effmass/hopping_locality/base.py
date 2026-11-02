"""Nominal scientific base for hopping-coefficient locality."""

from __future__ import annotations

from abc import ABC, abstractmethod


class HoppingLocality(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify locality diagnostics on an unchanged hopping representation.

    Concrete subclasses must declare their coefficient index space, support geometry,
    basis and gauge, normalization, and diagnostic range inventory. Membership never
    implies that coefficients were removed or that a finite-support operator was
    constructed. This base owns no lattice primitive, transform backend, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


class HoppingLocalityAnalysisRequest(HoppingLocality, ABC):
    """Bind one exact analysis of unchanged hopping coefficients."""

    __slots__ = ()


class HoppingLocalityAnalysis(HoppingLocality, ABC):
    """Retain one exact analysis of unchanged hopping coefficients."""

    __slots__ = ()


class HoppingLocalityAnalyzer[
    HoppingLocalityAnalysisRequestT: HoppingLocalityAnalysisRequest,
    HoppingLocalityAnalysisT: HoppingLocalityAnalysis,
](HoppingLocality, ABC):
    """Execute one bound hopping-locality analysis request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> HoppingLocalityAnalysisRequestT:
        """Return the complete immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> HoppingLocalityAnalysisT:
        """Execute the bound analysis without changing coefficient support."""


class PeriodicHoppingLocality(HoppingLocality, ABC):  # noqa: B024
    """Identify hopping locality under periodic boundary conditions."""

    __slots__ = ()


class PeriodicHoppingLocalityAnalysisRequest(
    HoppingLocalityAnalysisRequest,
    PeriodicHoppingLocality,
    ABC,
):
    """Bind one periodic hopping-locality analysis request."""

    __slots__ = ()


class PeriodicHoppingLocalityAnalysis(
    HoppingLocalityAnalysis,
    PeriodicHoppingLocality,
    ABC,
):
    """Retain one periodic hopping-locality analysis."""

    __slots__ = ()


class PeriodicHoppingLocalityAnalyzer[
    RequestT: PeriodicHoppingLocalityAnalysisRequest,
    AnalysisT: PeriodicHoppingLocalityAnalysis,
](
    HoppingLocalityAnalyzer[RequestT, AnalysisT],
    PeriodicHoppingLocality,
    ABC,
):
    """Execute one periodic hopping-locality analysis request."""

    __slots__ = ()


__all__ = [
    "HoppingLocality",
    "HoppingLocalityAnalysis",
    "HoppingLocalityAnalysisRequest",
    "HoppingLocalityAnalyzer",
    "PeriodicHoppingLocality",
    "PeriodicHoppingLocalityAnalysis",
    "PeriodicHoppingLocalityAnalysisRequest",
    "PeriodicHoppingLocalityAnalyzer",
]
