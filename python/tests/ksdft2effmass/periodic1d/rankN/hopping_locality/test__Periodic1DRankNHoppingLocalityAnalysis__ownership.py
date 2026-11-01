"""Ownership checks for rank-N hopping-locality values and actions."""

import pytest

from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.rankN.hopping_locality import (
    Periodic1DRankNHoppingLocalityAnalysis,
    Periodic1DRankNHoppingLocalityAnalysisRequest,
    Periodic1DRankNHoppingLocalityAnalyzer,
    Periodic1DRankNHoppingTailResult,
)
from ksdft2effmass.real_space_support_truncation import RealSpaceSupportTruncation

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNHoppingLocalityAnalysis:
    """Keep coefficient-distribution diagnostics separate from support removal."""

    def test_canonical_types_have_hopping_locality_module_identity(self) -> None:
        for value in (
            Periodic1DRankNHoppingLocalityAnalysis,
            Periodic1DRankNHoppingLocalityAnalysisRequest,
            Periodic1DRankNHoppingLocalityAnalyzer,
        ):
            assert value.__module__ == (
                "ksdft2effmass.periodic1d.rankN.hopping_locality.analysis"
            )
        assert Periodic1DRankNHoppingTailResult.__module__ == (
            "ksdft2effmass.periodic1d.rankN.hopping_locality.result"
        )

    def test_hopping_locality_uses_the_periodic1d_base(self) -> None:
        assert issubclass(
            Periodic1DRankNHoppingLocalityAnalysis,
            Periodic1DHoppingLocality,
        )
        assert issubclass(
            Periodic1DRankNHoppingTailResult,
            Periodic1DHoppingLocality,
        )

    def test_hopping_locality_does_not_claim_support_truncation(self) -> None:
        assert not issubclass(
            Periodic1DRankNHoppingLocalityAnalysis,
            RealSpaceSupportTruncation,
        )
        assert not issubclass(
            Periodic1DRankNHoppingTailResult,
            RealSpaceSupportTruncation,
        )
