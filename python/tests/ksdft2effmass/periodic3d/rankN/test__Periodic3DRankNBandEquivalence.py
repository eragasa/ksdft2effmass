"""Inheritance contracts for periodic-3D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic3d.rankN.band_equivalence.base import (
    Periodic3DRankNBandEquivalence,
    Periodic3DRankNBandEquivalenceAnalysis,
    Periodic3DRankNBandEquivalenceAnalyzer,
    Periodic3DRankNBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
)


class TestPeriodic3DRankNBandEquivalence:
    """Keep the existing aggregate implementation under its rank-N owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic3DRankNBandEquivalence)
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic3DRankNBandEquivalenceRequest,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic3DRankNBandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic3DRankNBandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic3DRankNBandEquivalence,
        )
        assert not issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic3DRankNBandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic3DRankNBandEquivalence,
        )
        assert not issubclass(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic3DRankNBandEquivalenceAnalyzer,
        )
