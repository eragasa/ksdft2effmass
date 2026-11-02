"""Inheritance contracts for periodic-2D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalence,
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
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
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
