"""Periodic-1D retained-dimension-two Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic.periodic1d.models.blochhopping import (
    Periodic1DBlochHoppingModel,
)
from ksdft2effmass.periodic.periodic1d.rank2.models.base import Periodic1DRank2Model


class Periodic1DRank2BlochHoppingModel(
    Periodic1DRank2Model,
    Periodic1DBlochHoppingModel,
    ABC,
):
    """Identify periodic-1D models with retained dimension two.

    Notes
    -----
    Rank two remains a sibling of the arbitrary finite-rank owner. Concrete rank-two
    models retain responsibility for coefficient, basis, and scientific admissibility
    rules beyond this exact retained-space dimension.

    """

    __slots__ = ()


__all__ = ["Periodic1DRank2BlochHoppingModel"]
