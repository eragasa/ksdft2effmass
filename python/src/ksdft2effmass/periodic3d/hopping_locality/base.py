"""Periodic three-dimensional specialization of hopping locality."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.hopping_locality.base import (
    PeriodicHoppingLocality,
    PeriodicHoppingLocalityAnalysis,
    PeriodicHoppingLocalityAnalysisRequest,
    PeriodicHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DHoppingLocality(
    PeriodicHoppingLocality,
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
    PeriodicHoppingLocalityAnalysisRequest,
    Periodic3DHoppingLocality,
    ABC,
):
    """Bind one periodic-3D hopping-locality analysis request."""

    __slots__ = ()


class Periodic3DHoppingLocalityAnalysis(
    PeriodicHoppingLocalityAnalysis,
    Periodic3DHoppingLocality,
    ABC,
):
    """Retain one periodic-3D hopping-locality analysis."""

    __slots__ = ()


class Periodic3DHoppingLocalityAnalyzer[
    RequestT: Periodic3DHoppingLocalityAnalysisRequest,
    AnalysisT: Periodic3DHoppingLocalityAnalysis,
](
    PeriodicHoppingLocalityAnalyzer[RequestT, AnalysisT],
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
