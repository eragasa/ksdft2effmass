"""Inheritance contracts for :class:`BandEquivalenceAnalysis`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalenceAnalysis,
    BandEquivalenceRequest,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalenceAnalysis,
    Periodic1DBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.result import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalenceAnalysis,
    Periodic3DBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceAnalysis:
    """Keep analysis ownership aligned with its exact request hierarchy."""

    def test_periodic_and_dimensional_bases_form_one_inheritance_chain(self) -> None:
        assert issubclass(PeriodicBandEquivalenceAnalysis, BandEquivalenceAnalysis)
        for analysis_base in (
            Periodic1DBandEquivalenceAnalysis,
            Periodic2DBandEquivalenceAnalysis,
            Periodic3DBandEquivalenceAnalysis,
        ):
            assert issubclass(analysis_base, PeriodicBandEquivalenceAnalysis)

    def test_request_bounds_narrow_at_each_inheritance_level(self) -> None:
        (domain_request,) = BandEquivalenceAnalysis.__type_params__
        (periodic_request,) = PeriodicBandEquivalenceAnalysis.__type_params__
        assert domain_request.__bound__ is BandEquivalenceRequest
        assert periodic_request.__bound__ is PeriodicBandEquivalenceRequest

        for request_base, analysis_base in (
            (
                Periodic1DBandEquivalenceRequest,
                Periodic1DBandEquivalenceAnalysis,
            ),
            (
                Periodic2DBandEquivalenceRequest,
                Periodic2DBandEquivalenceAnalysis,
            ),
            (
                Periodic3DBandEquivalenceRequest,
                Periodic3DBandEquivalenceAnalysis,
            ),
        ):
            (request_type,) = analysis_base.__type_params__
            assert request_type.__bound__ is request_base

    def test_rank_two_and_rank_n_analyses_are_dimensional_siblings(self) -> None:
        for dimensional_base, rank_two, rank_n in (
            (
                Periodic1DBandEquivalenceAnalysis,
                Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
                Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
            ),
            (
                Periodic2DBandEquivalenceAnalysis,
                Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
                Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
            ),
            (
                Periodic3DBandEquivalenceAnalysis,
                Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
                Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
            ),
        ):
            assert issubclass(rank_two, dimensional_base)
            assert issubclass(rank_n, dimensional_base)
            assert not issubclass(rank_two, rank_n)
            assert not issubclass(rank_n, rank_two)
