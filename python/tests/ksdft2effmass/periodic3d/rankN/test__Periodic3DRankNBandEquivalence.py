"""Inheritance contracts for periodic-3D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic3d.rankN.band_equivalence.base import (
    Periodic3DRankNBandEquivalence,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
)


class TestPeriodic3DRankNBandEquivalence:
    """Keep aggregate and foundational rank-N ownership distinct."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic3DRankNBandEquivalence)
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert not inspect.isabstract(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
        )
        assert not issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
        )
        assert not issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
        )
