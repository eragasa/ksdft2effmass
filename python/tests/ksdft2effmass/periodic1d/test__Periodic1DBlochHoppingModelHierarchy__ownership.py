"""Ownership contracts for the periodic-1D Bloch-hopping model hierarchy."""

import inspect

import pytest

from ksdft2effmass.model.blochhopping import BlochHoppingModel
from ksdft2effmass.periodic1d.model.blochhopping import Periodic1DBlochHoppingModel
from ksdft2effmass.periodic1d.rank1.model.blochhopping import (
    Periodic1DRank1BlochHoppingModel,
)
from ksdft2effmass.periodic1d.rank2.model.blochhopping import (
    Periodic1DRank2BlochHoppingModel,
)
from ksdft2effmass.periodic1d.rankN.model.blochhopping import (
    Periodic1DRankNBlochHoppingModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DBlochHoppingModelHierarchy:
    """Keep domain, dimension, and rank owners distinct and ordered."""

    def test__Periodic1DBlochHoppingModelHierarchy__retains_abstract_boundaries(
        self,
    ) -> None:
        """Keep only the implemented rank-one specialization concrete."""
        assert tuple(
            inspect.isabstract(owner)
            for owner in (
                BlochHoppingModel,
                Periodic1DBlochHoppingModel,
                Periodic1DRank1BlochHoppingModel,
                Periodic1DRank2BlochHoppingModel,
                Periodic1DRankNBlochHoppingModel,
            )
        ) == (True, True, False, True, True)

    def test__Periodic1DBlochHoppingModelHierarchy__orders_owner_layers(
        self,
    ) -> None:
        """Order the hierarchy from domain owner through dimension to rank."""
        # One tuple comparison exposes an omitted or reversed inheritance edge.
        assert (
            issubclass(Periodic1DBlochHoppingModel, BlochHoppingModel),
            issubclass(
                Periodic1DRank1BlochHoppingModel,
                Periodic1DBlochHoppingModel,
            ),
            issubclass(
                Periodic1DRank2BlochHoppingModel,
                Periodic1DBlochHoppingModel,
            ),
            issubclass(
                Periodic1DRankNBlochHoppingModel,
                Periodic1DBlochHoppingModel,
            ),
        ) == (True, True, True, True)

    def test__Periodic1DBlochHoppingModelHierarchy__keeps_rank_siblings(
        self,
    ) -> None:
        """Keep rank-two and rank-N as siblings rather than parent and child."""
        assert (
            issubclass(
                Periodic1DRank2BlochHoppingModel,
                Periodic1DRankNBlochHoppingModel,
            ),
            issubclass(
                Periodic1DRankNBlochHoppingModel,
                Periodic1DRank2BlochHoppingModel,
            ),
        ) == (False, False)

    def test__Periodic1DBlochHoppingModelHierarchy__retains_package_layers(
        self,
    ) -> None:
        """Retain each public class at its declared ownership layer."""
        assert tuple(
            owner.__module__
            for owner in (
                BlochHoppingModel,
                Periodic1DBlochHoppingModel,
                Periodic1DRank1BlochHoppingModel,
                Periodic1DRank2BlochHoppingModel,
                Periodic1DRankNBlochHoppingModel,
            )
        ) == (
            "ksdft2effmass.model.blochhopping.base",
            "ksdft2effmass.periodic1d.model.blochhopping.base",
            "ksdft2effmass.periodic1d.rank1.model.blochhopping.model",
            "ksdft2effmass.periodic1d.rank2.model.blochhopping.base",
            "ksdft2effmass.periodic1d.rankN.model.blochhopping.base",
        )
