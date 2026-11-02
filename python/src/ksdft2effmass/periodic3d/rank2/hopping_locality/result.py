"""Periodic-3D rank-two hopping-locality analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    MetricShellHoppingPowerResult,
)

from .base import Periodic3DRank2HoppingLocalityAnalysisRole
from .request import Periodic3DRank2HoppingLocalityAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2HoppingLocalityAnalysis(
    MetricShellHoppingPowerResult,
    Periodic3DRank2HoppingLocalityAnalysisRole,
):
    """Retain one channel's unchanged rank-two hopping powers by metric shell."""

    request: Periodic3DRank2HoppingLocalityAnalysisRequest

    def __post_init__(self) -> None:
        MetricShellHoppingPowerResult.__post_init__(self)
        if type(self.request) is not Periodic3DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-two request")
        if self.retained_rank != 2:
            raise ValueError("retained_rank must be two")
        if any(
            power.displacement.dimension is not LatticeDimension.THREE
            for power in self.powers
        ):
            raise ValueError("all hopping displacements must be three-dimensional")


__all__ = ["Periodic3DRank2HoppingLocalityAnalysis"]
