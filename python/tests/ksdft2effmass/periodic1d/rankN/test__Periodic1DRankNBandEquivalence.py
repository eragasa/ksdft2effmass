"""Inheritance contracts for periodic-1D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic1d.rankN.band_equivalence.base import (
    Periodic1DRankNBandEquivalence,
    Periodic1DRankNBandEquivalenceAnalysis,
    Periodic1DRankNBandEquivalenceAnalyzer,
    Periodic1DRankNBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
)


class TestPeriodic1DRankNBandEquivalence:
    """Keep the existing aggregate implementation under its rank-N owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic1DRankNBandEquivalence)
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic1DRankNBandEquivalenceRequest,
        )
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic1DRankNBandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic1DRankNBandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
