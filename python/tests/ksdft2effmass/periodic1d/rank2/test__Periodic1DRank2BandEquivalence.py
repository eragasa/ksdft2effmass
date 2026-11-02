"""Inheritance contracts for periodic-1D rank-two band equivalence."""

import inspect

from ksdft2effmass.periodic1d.rank2.band_equivalence.base import (
    Periodic1DRank2BandEquivalence,
    Periodic1DRank2BandEquivalenceAnalysis,
    Periodic1DRank2BandEquivalenceAnalyzer,
    Periodic1DRank2BandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.request import (
    Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.result import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
)


class TestPeriodic1DRank2BandEquivalence:
    """Keep the existing aggregate implementation under its exact rank owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic1DRank2BandEquivalence)
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic1DRank2BandEquivalenceRequest,
        )
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic1DRank2BandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic1DRank2BandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
