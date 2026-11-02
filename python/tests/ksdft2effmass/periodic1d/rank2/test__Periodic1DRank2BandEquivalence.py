"""Inheritance contracts for periodic-1D rank-two band equivalence."""

import inspect

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalenceAnalysis,
    BandEquivalenceAnalyzer,
    BandEquivalenceRequest,
)
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
    """Keep aggregate band equivalence founded but separately specialized."""

    def test__aggregate_roles__retain_band_equivalence_without_sibling_identity(
        self,
    ) -> None:
        assert inspect.isabstract(Periodic1DRank2BandEquivalence)
        role_pairs = (
            (
                Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
                BandEquivalenceRequest,
                Periodic1DRank2BandEquivalenceRequest,
            ),
            (
                Periodic1DRank2BandEquivalenceHoppingLocalityAnalysis,
                BandEquivalenceAnalysis,
                Periodic1DRank2BandEquivalenceAnalysis,
            ),
            (
                Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer,
                BandEquivalenceAnalyzer,
                Periodic1DRank2BandEquivalenceAnalyzer,
            ),
        )
        for aggregate_role, foundational_role, sibling_role in role_pairs:
            assert issubclass(aggregate_role, foundational_role)
            assert not issubclass(aggregate_role, sibling_role)
        assert not inspect.isabstract(
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
