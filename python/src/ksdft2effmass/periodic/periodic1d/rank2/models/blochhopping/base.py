"""Periodic-1D retained-dimension-two Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.periodic.periodic1d.rank2.models.base import Periodic1DRank2Model
from ksdft2effmass.periodic.periodic1d.rankN.models.blochhopping import (
    Periodic1DRankNBlochHoppingModel,
)


class Periodic1DRank2BlochHoppingModel(
    Periodic1DRank2Model,
    Periodic1DRankNBlochHoppingModel,
    ABC,
):
    """Identify periodic-1D models with retained dimension two.

    Notes
    -----
    This owner refines the arbitrary finite-rank Bloch-hopping contract rather than
    duplicating it as a sibling. Concrete rank-two models retain responsibility for
    coefficient, structured-basis, and scientific admissibility rules beyond this exact
    retained-space dimension.

    """

    __slots__ = ()


__all__ = ["Periodic1DRank2BlochHoppingModel"]
