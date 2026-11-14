"""Inheritance contracts for periodic-2D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic2d.rank2.band_equivalence.base import (
    Periodic2DRank2BandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalence,
    Periodic2DRankNBandEquivalenceAnalysis,
    Periodic2DRankNBandEquivalenceAnalyzer,
    Periodic2DRankNBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
)


class TestPeriodic2DRankNBandEquivalence:
    """Keep aggregate and foundational rank-N ownership distinct."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic2DRankNBandEquivalence)
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic2DRankNBandEquivalenceRequest,
        )
        assert not issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic2DRank2BandEquivalenceRequest,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRankNBandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRankNBandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
        )
        assert not issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
        )
        assert not issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
        )
