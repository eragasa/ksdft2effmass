"""Inheritance contracts for periodic-1D rank-two band equivalence."""

import inspect

from ksdft2effmass.periodic1d.rank2.band_equivalence.base import (
    Periodic1DRank2BandEquivalence,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.base import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.request import (
    Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.result import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
)


class TestPeriodic1DRank2BandEquivalence:
    """Keep the aggregate implementation under its exact rank-two owners."""

    def test__aggregate_roles__inherit_exact_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic1DRank2BandEquivalence)
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert not inspect.isabstract(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
