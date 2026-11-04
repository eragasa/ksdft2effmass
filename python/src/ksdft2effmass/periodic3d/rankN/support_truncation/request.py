"""Periodic-3D arbitrary-rank support-truncation request values."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.real_space_support_truncation import MetricShellSupportInventory
from ksdft2effmass.serialization.enums import StrWireEnum

from .base import Periodic3DRankNSupportTruncationAnalysisRequestRole


class Periodic3DRankNSupportTruncationChannelEnum(StrWireEnum):
    """Identify one model channel whose support is irreversibly removed."""

    REFERENCE = "reference"
    COMPARISON = "comparison"


@dataclass(frozen=True, slots=True)
class Periodic3DRankNSupportTruncationAnalysisRequest(
    Periodic3DRankNSupportTruncationAnalysisRequestRole
):
    """Bind one error channel to nested metric-shell supports and a tolerance."""

    retained_rank: int
    channel: Periodic3DRankNSupportTruncationChannelEnum
    support_inventory: MetricShellSupportInventory
    total_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...]
    tolerance: float

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return self.retained_rank

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        if type(self.channel) is not Periodic3DRankNSupportTruncationChannelEnum:
            raise TypeError("channel must be the exact periodic-3D channel enum")
        if type(self.support_inventory) is not MetricShellSupportInventory:
            raise TypeError("support_inventory must be MetricShellSupportInventory")
        if (
            self.support_inventory.displacements[0].dimension
            is not LatticeDimension.THREE
        ):
            raise ValueError("support_inventory must be periodic three-dimensional")
        if type(self.total_errors) is not tuple or not self.total_errors:
            raise TypeError("total_errors must be a nonempty tuple")
        if any(
            type(errors) is not BandEquivalenceHoppingLocalityErrorChannels
            for errors in self.total_errors
        ):
            raise TypeError("total_errors must contain exact error-channel values")
        if len(self.total_errors) > (
            self.support_inventory.maximum_ordinal_shell_index + 1
        ):
            raise ValueError("total_errors exceed the admitted support inventory")
        if type(self.tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(self.tolerance) or self.tolerance < 0.0:
            raise ValueError("tolerance must be finite and nonnegative")


__all__ = [
    "Periodic3DRankNSupportTruncationAnalysisRequest",
    "Periodic3DRankNSupportTruncationChannelEnum",
]
