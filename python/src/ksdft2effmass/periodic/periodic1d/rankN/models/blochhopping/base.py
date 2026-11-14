"""Periodic-1D arbitrary-retained-dimension Bloch-hopping contract."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic.periodic1d.models.blochhopping import (
    Periodic1DBlochHoppingModel,
)
from ksdft2effmass.periodic.periodic1d.rankN.models.base import Periodic1DRankNModel


class Periodic1DRankNBlochHoppingModel(
    Periodic1DRankNModel,
    Periodic1DBlochHoppingModel,
    ABC,
):
    """Identify a declared finite retained-dimension Bloch-hopping model.

    Notes
    -----
    This owner is the finite-rank Bloch-hopping contract refined by fixed-rank
    descendants such as the rank-two owner. Concrete finite-rank families must enforce
    their reviewed retained-dimension inventories; ``N`` denotes the retained
    state-space dimension rather than algebraic matrix rank.
    """

    __slots__ = ()


__all__ = ["Periodic1DRankNBlochHoppingModel"]
