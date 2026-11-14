"""Nominal periodic-1D rank-two scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic1d.rankN.models import Periodic1DRankNModel


class Periodic1DRank2Model(Periodic1DRankNModel, ABC):
    """Refine periodic-1D finite-rank models to retained rank two.

    Notes
    -----
    The inherited basis contract remains abstract. A concrete rank-two family must
    supply an exact ``Periodic1DBasisIdentity`` containing two ordered coordinates.
    """

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two.

        Returns
        -------
        Literal[2]
            Built-in integer two.

        Notes
        -----
        The final property prevents descendants from weakening the rank-two identity.
        Constructor validation remains responsible for correlating the inherited basis
        coordinate count and any represented operator shape with this value.
        """
        return 2


__all__ = ["Periodic1DRank2Model"]
