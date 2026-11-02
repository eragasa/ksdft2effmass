"""Ownership contracts for the inert periodic-3D rank-one specialization."""

import inspect

from ksdft2effmass.periodic3d.rank1.band_equivalence.base import (
    Periodic3DRank1BandEquivalence,
    Periodic3DRank1BandEquivalenceAnalysis,
    Periodic3DRank1BandEquivalenceAnalyzer,
    Periodic3DRank1BandEquivalenceRequest,
)


class TestPeriodic3DRank1BandEquivalence:
    """Reserve exact rank ownership without fabricating a scientific study."""

    def test__roles__own_rank_without_a_concrete_analyzer(self) -> None:
        assert inspect.isabstract(Periodic3DRank1BandEquivalence)
        assert inspect.isabstract(Periodic3DRank1BandEquivalenceRequest)
        assert inspect.isabstract(Periodic3DRank1BandEquivalenceAnalysis)
        assert inspect.isabstract(Periodic3DRank1BandEquivalenceAnalyzer)
