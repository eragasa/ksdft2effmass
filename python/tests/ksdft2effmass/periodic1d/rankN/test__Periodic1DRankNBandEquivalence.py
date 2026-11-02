"""Inheritance contracts for periodic-1D rank-N band equivalence."""

import inspect

from ksdft2effmass.periodic1d.rankN.band_equivalence.base import (
    Periodic1DRankNBandEquivalence,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.base import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
)


class TestPeriodic1DRankNBandEquivalence:
    """Keep the aggregate implementation under its exact rank-N owners."""

    def test__aggregate_roles__inherit_exact_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic1DRankNBandEquivalence)
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert not inspect.isabstract(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
