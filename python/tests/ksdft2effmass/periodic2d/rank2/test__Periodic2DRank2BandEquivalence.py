"""Inheritance contracts for periodic-2D rank-two band equivalence."""

import inspect

from ksdft2effmass.periodic2d.rank2.band_equivalence.base import (
    Periodic2DRank2BandEquivalence,
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


class TestPeriodic2DRank2BandEquivalence:
    """Keep the existing aggregate implementation under its exact rank owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic2DRank2BandEquivalence)
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert not inspect.isabstract(
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
