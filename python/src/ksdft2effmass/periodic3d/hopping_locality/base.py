"""Periodic three-dimensional specialization of hopping locality."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.hopping_locality.base import (
    HoppingLocality,
    HoppingLocalityAnalysis,
    HoppingLocalityAnalysisRequest,
    HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DHoppingLocality(
    HoppingLocality,
    Periodic3DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify unchanged hopping coefficients indexed by 3D translations.

    Concrete subclasses must state the integer-translation inventory, physical-metric
    range convention, conjugate relation, basis and gauge, and normalization. This
    specialization does not imply support removal and owns no Fourier algorithm,
    tolerance, direct lattice, or wire format.
    """

    __slots__ = ()


class Periodic3DHoppingLocalityAnalysisRequest(
    HoppingLocalityAnalysisRequest,
    Periodic3DHoppingLocality,
    ABC,
):
    """Bind one periodic-3D hopping-locality analysis request."""

    __slots__ = ()


class Periodic3DHoppingLocalityAnalysis(
    HoppingLocalityAnalysis,
    Periodic3DHoppingLocality,
    ABC,
):
    """Retain one periodic-3D hopping-locality analysis."""

    __slots__ = ()


class Periodic3DHoppingLocalityAnalyzer[
    Periodic3DHoppingLocalityAnalysisRequestT: (
        Periodic3DHoppingLocalityAnalysisRequest
    ),
    Periodic3DHoppingLocalityAnalysisT: Periodic3DHoppingLocalityAnalysis,
](
    HoppingLocalityAnalyzer[
        Periodic3DHoppingLocalityAnalysisRequestT,
        Periodic3DHoppingLocalityAnalysisT,
    ],
    Periodic3DHoppingLocality,
    ABC,
):
    """Execute one periodic-3D hopping-locality analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic3DHoppingLocality",
    "Periodic3DHoppingLocalityAnalysis",
    "Periodic3DHoppingLocalityAnalysisRequest",
    "Periodic3DHoppingLocalityAnalyzer",
]
