"""Periodic-3D arbitrary-rank hopping-locality analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.periodic3d.hopping_locality.base import (
    Periodic3DHoppingLocalityAnalysis,
)

from .request import Periodic3DRankNHoppingLocalityAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNHoppingLocalityAnalysis(
    MetricShellHoppingPowerResult,
    Periodic3DHoppingLocalityAnalysis,
):
    """Retain one channel's unchanged arbitrary-rank hopping powers by metric shell."""

    request: Periodic3DRankNHoppingLocalityAnalysisRequest

    def __post_init__(self) -> None:
        MetricShellHoppingPowerResult.__post_init__(self)
        if type(self.request) is not Periodic3DRankNHoppingLocalityAnalysisRequest:
            raise TypeError(
                "request must be the exact periodic-3D arbitrary-rank request"
            )
        if self.retained_rank != self.request.retained_rank:
            raise ValueError("retained_rank must match the request")
        if any(
            power.displacement.dimension is not LatticeDimension.THREE
            for power in self.powers
        ):
            raise ValueError("all hopping displacements must be three-dimensional")


__all__ = ["Periodic3DRankNHoppingLocalityAnalysis"]
