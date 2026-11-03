"""Periodic-1D retained-dimension-two Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DBlochHoppingModel,
)


class Periodic1DRank2BlochHoppingModel(Periodic1DBlochHoppingModel, ABC):
    """Identify periodic-1D models with retained dimension two.

    Notes
    -----
    Rank two remains a sibling of the arbitrary finite-rank owner. Concrete rank-two
    models retain responsibility for coefficient, basis, and scientific admissibility
    rules beyond this exact retained-space dimension.
    """

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[2]:
        """Return the retained-space dimension.

        Returns
        -------
        Literal[2]
            Exact retained basis size two.
        """
        return 2


__all__ = ["Periodic1DRank2BlochHoppingModel"]
