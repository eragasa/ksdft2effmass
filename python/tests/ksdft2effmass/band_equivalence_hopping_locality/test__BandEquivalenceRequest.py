"""Inheritance contracts for :class:`BandEquivalenceRequest`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalenceRequest,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.request import (
    Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceRequest:
    """Keep request ownership aligned from domain through rank specialization."""

    def test_periodic_and_dimensional_bases_form_one_inheritance_chain(self) -> None:
        assert issubclass(PeriodicBandEquivalenceRequest, BandEquivalenceRequest)
        for request_base in (
            Periodic1DBandEquivalenceRequest,
            Periodic2DBandEquivalenceRequest,
            Periodic3DBandEquivalenceRequest,
        ):
            assert issubclass(request_base, PeriodicBandEquivalenceRequest)

    def test_shared_aggregate_request_retains_periodic_band_ownership(self) -> None:
        assert issubclass(
            BandEquivalenceHoppingLocalityRequest,
            PeriodicBandEquivalenceRequest,
        )

    def test_rank_two_and_rank_n_requests_are_dimensional_siblings(self) -> None:
        for dimensional_base, rank_two, rank_n in (
            (
                Periodic1DBandEquivalenceRequest,
                Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
                Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
            ),
            (
                Periodic2DBandEquivalenceRequest,
                Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
                Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
            ),
            (
                Periodic3DBandEquivalenceRequest,
                Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
                Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
            ),
        ):
            assert issubclass(rank_two, dimensional_base)
            assert issubclass(rank_n, dimensional_base)
            assert not issubclass(rank_two, rank_n)
            assert not issubclass(rank_n, rank_two)
