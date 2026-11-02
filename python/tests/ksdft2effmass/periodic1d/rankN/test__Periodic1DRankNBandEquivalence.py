"""Inheritance contracts for periodic-1D rank-N band equivalence."""

import inspect

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalenceAnalysis,
    BandEquivalenceAnalyzer,
    BandEquivalenceRequest,
)
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
    """Keep aggregate band equivalence founded but separately specialized."""

    def test__aggregate_roles__retain_band_equivalence_without_sibling_identity(
        self,
    ) -> None:
        assert inspect.isabstract(Periodic1DRankNBandEquivalence)
        role_pairs = (
            (
                Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
                BandEquivalenceRequest,
                Periodic1DRankNBandEquivalenceRequest,
            ),
            (
                Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
                BandEquivalenceAnalysis,
                Periodic1DRankNBandEquivalenceAnalysis,
            ),
            (
                Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
                BandEquivalenceAnalyzer,
                Periodic1DRankNBandEquivalenceAnalyzer,
            ),
        )
        for aggregate_role, foundational_role, sibling_role in role_pairs:
            assert issubclass(aggregate_role, foundational_role)
            assert not issubclass(aggregate_role, sibling_role)
        assert not inspect.isabstract(
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer
        )
