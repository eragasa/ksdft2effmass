"""Ownership checks for rank-N support-truncation values and actions."""

import pytest

from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.locality import (
    Periodic1DRankNLocalityAnalysis as LegacyEquivalenceLocalityAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.locality import (
    Periodic1DRankNLocalityAnalysisRequest as LegacyEquivalenceLocalityAnalysisRequest,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.locality import (
    Periodic1DRankNLocalityAnalyzer as LegacyEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.results.support import (  # noqa: E501
    Periodic1DRankNSupportResult as LegacyEquivalenceSupportResult,
)
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
    """Establish canonical ownership without breaking historical imports."""

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

    @pytest.mark.legacy_equivalence
    def test__legacy_equivalence__paths_reexport_canonical_types(self) -> None:
        assert LegacyEquivalenceLocalityAnalysis is Periodic1DRankNLocalityAnalysis
        assert (
            LegacyEquivalenceLocalityAnalysisRequest
            is Periodic1DRankNLocalityAnalysisRequest
        )
        assert LegacyEquivalenceLocalityAnalyzer is Periodic1DRankNLocalityAnalyzer
        assert LegacyEquivalenceSupportResult is Periodic1DRankNSupportResult

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
