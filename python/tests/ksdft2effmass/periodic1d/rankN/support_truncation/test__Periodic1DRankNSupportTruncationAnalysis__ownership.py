"""Ownership checks for rank-N support-truncation values and actions."""

import pytest

from ksdft2effmass.periodic1d.rankN.support_truncation import (
    Periodic1DRankNLocalityAnalysis,
    Periodic1DRankNLocalityAnalysisRequest,
    Periodic1DRankNLocalityAnalyzer,
    Periodic1DRankNSupportResult,
    Periodic1DRankNSupportTruncationAnalysis,
    Periodic1DRankNSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.real_space_support_truncation import RealSpaceSupportTruncation

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNSupportTruncationAnalysis:
    """Establish canonical support-truncation ownership."""

    def test_canonical_types_have_support_truncation_module_identity(self) -> None:
        assert Periodic1DRankNLocalityAnalysis.__module__ == (
            "ksdft2effmass.periodic1d.rankN.support_truncation.analysis"
        )
        assert Periodic1DRankNLocalityAnalysisRequest.__module__ == (
            "ksdft2effmass.periodic1d.rankN.support_truncation.analysis"
        )
        assert Periodic1DRankNLocalityAnalyzer.__module__ == (
            "ksdft2effmass.periodic1d.rankN.support_truncation.analysis"
        )
        assert Periodic1DRankNSupportResult.__module__ == (
            "ksdft2effmass.periodic1d.rankN.support_truncation.result"
        )
        for value in (
            Periodic1DRankNSupportTruncationAnalysis,
            Periodic1DRankNSupportTruncationAnalysisRequest,
            Periodic1DRankNSupportTruncationAnalyzer,
        ):
            assert value.__module__ == (
                "ksdft2effmass.periodic1d.rankN.support_truncation.analysis"
            )

    def test_values_keep_the_installed_scientific_base(self) -> None:
        assert issubclass(
            Periodic1DRankNLocalityAnalysis,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DRankNSupportResult,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DRankNSupportTruncationAnalysis,
            Periodic1DSupportTruncation,
        )
