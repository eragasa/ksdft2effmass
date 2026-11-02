"""Ownership contracts for the inert periodic-2D rank-one specialization."""

import inspect

from ksdft2effmass.periodic2d.rank1.band_equivalence.base import (
    Periodic2DRank1BandEquivalence,
    Periodic2DRank1BandEquivalenceAnalysis,
    Periodic2DRank1BandEquivalenceAnalyzer,
    Periodic2DRank1BandEquivalenceRequest,
)


class TestPeriodic2DRank1BandEquivalence:
    """Reserve exact rank ownership without fabricating a scientific study."""

    def test__roles__own_rank_without_a_concrete_analyzer(self) -> None:
        assert inspect.isabstract(Periodic2DRank1BandEquivalence)
        assert inspect.isabstract(Periodic2DRank1BandEquivalenceRequest)
        assert inspect.isabstract(Periodic2DRank1BandEquivalenceAnalysis)
        assert inspect.isabstract(Periodic2DRank1BandEquivalenceAnalyzer)
