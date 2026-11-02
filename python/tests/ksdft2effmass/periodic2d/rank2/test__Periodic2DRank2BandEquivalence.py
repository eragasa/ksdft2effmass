"""Inheritance contracts for periodic-2D rank-two band equivalence."""

import inspect

from ksdft2effmass.periodic2d.rank2.band_equivalence.base import (
    Periodic2DRank2BandEquivalence,
    Periodic2DRank2BandEquivalenceAnalysis,
    Periodic2DRank2BandEquivalenceAnalyzer,
    Periodic2DRank2BandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.base import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole,
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalenceRequest,
)


class TestPeriodic2DRank2BandEquivalence:
    """Keep the existing aggregate implementation under its exact rank owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic2DRank2BandEquivalence)
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic2DRank2BandEquivalenceRequest,
        )
        assert not issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic2DRankNBandEquivalenceRequest,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRank2BandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRank2BandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
