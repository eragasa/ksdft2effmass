"""Inheritance contracts for :class:`BandEquivalenceAnalyzer`."""

from __future__ import annotations

from inspect import isabstract

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalenceAnalyzer,
    BandEquivalenceRequest,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalenceAnalyzer,
    Periodic1DBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalenceAnalyzer,
    Periodic3DBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceAnalyzer:
    """Keep analyzer ownership aligned with its exact request hierarchy."""

    def test_periodic_and_dimensional_bases_form_one_inheritance_chain(self) -> None:
        assert issubclass(PeriodicBandEquivalenceAnalyzer, BandEquivalenceAnalyzer)
        for analyzer_base in (
            Periodic1DBandEquivalenceAnalyzer,
            Periodic2DBandEquivalenceAnalyzer,
            Periodic3DBandEquivalenceAnalyzer,
        ):
            assert issubclass(analyzer_base, PeriodicBandEquivalenceAnalyzer)

    def test_request_bounds_narrow_at_each_inheritance_level(self) -> None:
        (domain_request,) = BandEquivalenceAnalyzer.__type_params__
        (periodic_request,) = PeriodicBandEquivalenceAnalyzer.__type_params__
        assert domain_request.__bound__ is BandEquivalenceRequest
        assert periodic_request.__bound__ is PeriodicBandEquivalenceRequest

        for request_base, analyzer_base in (
            (
                Periodic1DBandEquivalenceRequest,
                Periodic1DBandEquivalenceAnalyzer,
            ),
            (
                Periodic2DBandEquivalenceRequest,
                Periodic2DBandEquivalenceAnalyzer,
            ),
            (
                Periodic3DBandEquivalenceRequest,
                Periodic3DBandEquivalenceAnalyzer,
            ),
        ):
            (request_type,) = analyzer_base.__type_params__
            assert request_type.__bound__ is request_base

    def test_rank_two_and_rank_n_analyzers_are_dimensional_siblings(self) -> None:
        for dimensional_base, rank_two, rank_n in (
            (
                Periodic1DBandEquivalenceAnalyzer,
                Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
                Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
            ),
            (
                Periodic2DBandEquivalenceAnalyzer,
                Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
                Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
            ),
            (
                Periodic3DBandEquivalenceAnalyzer,
                Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
                Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
            ),
        ):
            assert issubclass(rank_two, dimensional_base)
            assert issubclass(rank_n, dimensional_base)
            assert not issubclass(rank_two, rank_n)
            assert not issubclass(rank_n, rank_two)
            assert not isabstract(rank_two)
            assert not isabstract(rank_n)

    def test_hopping_locality_is_not_owned_by_band_equivalence(self) -> None:
        assert issubclass(
            Rank2BandEquivalenceHoppingLocalityAnalyzer,
            BandEquivalenceAnalyzer,
        )
        assert not hasattr(BandEquivalenceAnalyzer, "analyze_ordinary_hopping_locality")
        assert hasattr(
            Rank2BandEquivalenceHoppingLocalityAnalyzer,
            "analyze_ordinary_hopping_locality",
        )
