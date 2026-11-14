"""Typed ownership guardrails for band-equivalence capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final


class BandEquivalence(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify comparison of spectra on one explicitly aligned state space.

    Concrete subclasses must identify both represented operators, their common state
    space, basis and gauge conventions, energy reference, units, sampling domain, and
    ordered-spectrum comparison. Membership does not imply gauge alignment, frame
    transport, hopping locality, support truncation, or scientific adequacy. This base
    owns no lattice geometry, numerical method, tolerance, or wire format.
    """

    __slots__ = ()

    @property
    @final
    def analysis_domain_identifier(self) -> str:
        """Return the stable scientific-domain identifier."""
        return "band-equivalence"


class BandEquivalenceRequest(BandEquivalence, ABC):
    """Identify immutable requests belonging to band-equivalence studies."""

    __slots__ = ()


class BandEquivalenceAnalysis[RequestT: BandEquivalenceRequest](
    BandEquivalence,
    ABC,
):
    """Identify analyses produced from typed band-equivalence requests."""

    __slots__ = ()


class BandEquivalenceAnalyzer[RequestT: BandEquivalenceRequest](
    BandEquivalence,
    ABC,
):
    """Require one typed request and a public zero-argument analysis action."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to the analyzer."""

    @abstractmethod
    def execute(self) -> BandEquivalenceAnalysis[RequestT]:
        """Execute the complete bound analysis without additional arguments."""


class PeriodicBandEquivalence(BandEquivalence, ABC):  # noqa: B024
    """Identify band equivalence under periodic boundary conditions."""

    __slots__ = ()

    @property
    @final
    def boundary_condition_identifier(self) -> str:
        """Return the periodic boundary-condition identity."""
        return "periodic"


class PeriodicRankNBandEquivalenceCapability(PeriodicBandEquivalence, ABC):
    """Identify periodic band equivalence over finite-rank subspaces."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the represented finite-rank inventory."""


class PeriodicBandEquivalenceRequest(
    BandEquivalenceRequest,
    PeriodicBandEquivalence,
    ABC,
):
    """Identify band-equivalence requests with periodic boundary conditions."""

    __slots__ = ()


class PeriodicBandEquivalenceAnalysis[RequestT: PeriodicBandEquivalenceRequest](
    BandEquivalenceAnalysis[RequestT],
    PeriodicBandEquivalence,
    ABC,
):
    """Identify analyses of periodic band-equivalence requests."""

    __slots__ = ()


class PeriodicBandEquivalenceAnalyzer[
    RequestT: PeriodicBandEquivalenceRequest,
](
    BandEquivalenceAnalyzer[RequestT],
    PeriodicBandEquivalence,
    ABC,
):
    """Require an exact lattice dimension for periodic band equivalence."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> PeriodicBandEquivalenceAnalysis[RequestT]:
        """Execute one periodic analysis bound to the exact request type."""


__all__ = [
    "BandEquivalence",
    "BandEquivalenceAnalysis",
    "BandEquivalenceAnalyzer",
    "BandEquivalenceRequest",
    "PeriodicBandEquivalence",
    "PeriodicBandEquivalenceAnalysis",
    "PeriodicBandEquivalenceAnalyzer",
    "PeriodicBandEquivalenceRequest",
    "PeriodicRankNBandEquivalenceCapability",
]
