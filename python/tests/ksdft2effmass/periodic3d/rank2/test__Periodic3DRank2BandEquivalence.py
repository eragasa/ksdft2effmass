"""Inheritance contracts for periodic-3D rank-two band equivalence."""

import inspect

from ksdft2effmass.periodic3d.rank2.band_equivalence.base import (
    Periodic3DRank2BandEquivalence,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.base import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRole,
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)


class TestPeriodic3DRank2BandEquivalence:
    """Keep the existing aggregate implementation under its exact rank owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic3DRank2BandEquivalence)
        assert issubclass(
            Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
            Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert not inspect.isabstract(
            Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer
        )
