"""Periodic-2D rank-two hopping-locality analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.periodic2d.hopping_locality.base import (
    Periodic2DHoppingLocalityAnalysis,
)

from .request import Periodic2DRank2HoppingLocalityAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2HoppingLocalityAnalysis(
    MetricShellHoppingPowerResult,
    Periodic2DHoppingLocalityAnalysis,
):
    """Retain one channel's unchanged rank-two hopping powers by metric shell."""

    request: Periodic2DRank2HoppingLocalityAnalysisRequest

    def __post_init__(self) -> None:
        MetricShellHoppingPowerResult.__post_init__(self)
        if type(self.request) is not Periodic2DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-two request")
        if self.retained_rank != 2:
            raise ValueError("retained_rank must be two")
        if any(
            power.displacement.dimension is not LatticeDimension.TWO
            for power in self.powers
        ):
            raise ValueError("all hopping displacements must be two-dimensional")


__all__ = ["Periodic2DRank2HoppingLocalityAnalysis"]
