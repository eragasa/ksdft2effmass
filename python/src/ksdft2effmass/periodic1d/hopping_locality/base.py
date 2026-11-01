"""Periodic one-dimensional specialization of hopping locality."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.hopping_locality.base import (
    HoppingLocality,
    HoppingLocalityAnalysis,
    HoppingLocalityAnalysisRequest,
    HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.base import Periodic1DCapability


class Periodic1DHoppingLocality(
    HoppingLocality,
    Periodic1DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify unchanged hopping coefficients indexed by 1D translations.

    Concrete subclasses must state the integer-translation inventory, range convention,
    conjugate relation, basis and gauge, and normalization. :attr:`lattice_dimension`
    fixes only the PhysKit one-dimensional identity. The specialization does not imply
    support removal and owns no Fourier algorithm, tolerance, or wire format.
    """

    __slots__ = ()


class Periodic1DHoppingLocalityAnalysisRequest(
    HoppingLocalityAnalysisRequest,
    Periodic1DHoppingLocality,
    ABC,
):
    """Bind one periodic-1D hopping-locality analysis request."""

    __slots__ = ()


class Periodic1DHoppingLocalityAnalysis(
    HoppingLocalityAnalysis,
    Periodic1DHoppingLocality,
    ABC,
):
    """Retain one periodic-1D hopping-locality analysis."""

    __slots__ = ()


class Periodic1DHoppingLocalityAnalyzer[
    Periodic1DHoppingLocalityAnalysisRequestT: Periodic1DHoppingLocalityAnalysisRequest,
    Periodic1DHoppingLocalityAnalysisT: Periodic1DHoppingLocalityAnalysis,
](
    HoppingLocalityAnalyzer[
        Periodic1DHoppingLocalityAnalysisRequestT,
        Periodic1DHoppingLocalityAnalysisT,
    ],
    Periodic1DHoppingLocality,
    ABC,
):
    """Execute one periodic-1D hopping-locality analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic1DHoppingLocality",
    "Periodic1DHoppingLocalityAnalysis",
    "Periodic1DHoppingLocalityAnalysisRequest",
    "Periodic1DHoppingLocalityAnalyzer",
]
