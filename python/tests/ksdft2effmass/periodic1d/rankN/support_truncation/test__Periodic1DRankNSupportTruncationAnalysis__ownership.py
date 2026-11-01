"""Ownership checks for rank-N support-truncation values and actions."""

import pytest

from ksdft2effmass.periodic1d.rankN import (
    support_truncation as support_truncation_namespace,
)
from ksdft2effmass.periodic1d.rankN.support_truncation.analysis import (
    Periodic1DRankNSupportTruncationAnalysis,
    Periodic1DRankNSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.support_truncation.result import (
    Periodic1DRankNSupportResult,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.real_space_support_truncation import RealSpaceSupportTruncation

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNSupportTruncationAnalysis:
    """Establish canonical support-truncation ownership."""

    def test_canonical_types_have_support_truncation_module_identity(self) -> None:
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
            Periodic1DRankNSupportResult,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DRankNSupportTruncationAnalysis,
            Periodic1DSupportTruncation,
        )

    def test_namespace_is_inert_and_historical_combined_view_is_absent(self) -> None:
        assert not hasattr(support_truncation_namespace, "__all__")
        assert not any(
            name.startswith("Periodic1D") for name in vars(support_truncation_namespace)
        )
        for name in (
            "Periodic1DRankNLocalityAnalysis",
            "Periodic1DRankNLocalityAnalysisRequest",
            "Periodic1DRankNLocalityAnalyzer",
        ):
            assert not hasattr(support_truncation_namespace, name)
