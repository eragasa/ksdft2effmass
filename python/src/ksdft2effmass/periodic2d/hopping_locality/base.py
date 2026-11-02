"""Periodic two-dimensional specialization of hopping locality."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.hopping_locality.base import (
    HoppingLocality,
    HoppingLocalityAnalysis,
    HoppingLocalityAnalysisRequest,
    HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DHoppingLocality(
    HoppingLocality,
    Periodic2DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify unchanged hopping coefficients indexed by 2D translations.

    Concrete subclasses must state the integer-translation inventory, physical-metric
    range convention, conjugate relation, basis and gauge, and normalization. This
    specialization does not imply support removal and owns no Fourier algorithm,
    tolerance, direct lattice, or wire format.
    """

    __slots__ = ()


class Periodic2DHoppingLocalityAnalysisRequest(
    HoppingLocalityAnalysisRequest,
    Periodic2DHoppingLocality,
    ABC,
):
    """Bind one periodic-2D hopping-locality analysis request."""

    __slots__ = ()


class Periodic2DHoppingLocalityAnalysis(
    HoppingLocalityAnalysis,
    Periodic2DHoppingLocality,
    ABC,
):
    """Retain one periodic-2D hopping-locality analysis."""

    __slots__ = ()


class Periodic2DHoppingLocalityAnalyzer[
    Periodic2DHoppingLocalityAnalysisRequestT: (
        Periodic2DHoppingLocalityAnalysisRequest
    ),
    Periodic2DHoppingLocalityAnalysisT: Periodic2DHoppingLocalityAnalysis,
](
    HoppingLocalityAnalyzer[
        Periodic2DHoppingLocalityAnalysisRequestT,
        Periodic2DHoppingLocalityAnalysisT,
    ],
    Periodic2DHoppingLocality,
    ABC,
):
    """Execute one periodic-2D hopping-locality analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic2DHoppingLocality",
    "Periodic2DHoppingLocalityAnalysis",
    "Periodic2DHoppingLocalityAnalysisRequest",
    "Periodic2DHoppingLocalityAnalyzer",
]
