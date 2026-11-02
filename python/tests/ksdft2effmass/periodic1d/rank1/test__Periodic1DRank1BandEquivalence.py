"""Inheritance contracts for periodic-1D rank-one band equivalence."""

import inspect

from ksdft2effmass.periodic1d.fourier_locality.analysis import (
    Periodic1DFourierLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.fourier_locality.configuration import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.fourier_locality.result import (
    Periodic1DFourierLocalityCalculationResult,
)
from ksdft2effmass.periodic1d.rank1.band_equivalence.base import (
    Periodic1DRank1BandEquivalence,
    Periodic1DRank1BandEquivalenceAnalysis,
    Periodic1DRank1BandEquivalenceAnalyzer,
    Periodic1DRank1BandEquivalenceRequest,
)


class TestPeriodic1DRank1BandEquivalence:
    """Keep the existing Fourier implementation under its exact rank owner."""

    def test__existing_concrete_roles__inherit_rank_ownership(self) -> None:
        assert inspect.isabstract(Periodic1DRank1BandEquivalence)
        assert issubclass(
            Periodic1DFourierLocalityConfiguration,
            Periodic1DRank1BandEquivalenceRequest,
        )
        assert issubclass(
            Periodic1DFourierLocalityCalculationResult,
            Periodic1DRank1BandEquivalenceAnalysis,
        )
        assert issubclass(
            Periodic1DFourierLocalityAnalyzer,
            Periodic1DRank1BandEquivalenceAnalyzer,
        )
        assert not inspect.isabstract(Periodic1DFourierLocalityAnalyzer)
