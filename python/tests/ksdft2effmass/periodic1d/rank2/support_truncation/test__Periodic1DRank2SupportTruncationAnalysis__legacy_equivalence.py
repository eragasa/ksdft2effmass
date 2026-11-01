"""Compatibility-only checks for the rank-two truncation facade."""

import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    truncation as LegacyEquivalenceSupportTruncation,
)
from ksdft2effmass.periodic1d.rank2 import (
    support_truncation as RankFirstSupportTruncation,
)
from ksdft2effmass.periodic1d.rank2.support_truncation import (
    Periodic1DRank2SupportTruncationAnalysis,
    Periodic1DRank2SupportTruncationAnalysisRequest,
    Periodic1DRank2SupportTruncationAnalyzer,
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationAnalyzer,
    Periodic1DRank2TruncationRequest,
)

pytestmark = [
    pytest.mark.legacy_equivalence,
    pytest.mark.software_verification,
    pytest.mark.unit,
]


class TestPeriodic1DRank2SupportTruncationAnalysis:
    @pytest.mark.parametrize(
        "name",
        [
            "EmbeddedSubspaceRank2TruncationFamilyVerification",
            "EmbeddedSubspaceRank2TruncationVerification",
            "Periodic1DRank2SupportTruncationAnalysis",
            "Periodic1DRank2SupportTruncationAnalysisRequest",
            "Periodic1DRank2SupportTruncationAnalyzer",
            "Periodic1DRank2TruncationAnalysis",
            "Periodic1DRank2TruncationAnalyzer",
            "Periodic1DRank2TruncationCompleted",
            "Periodic1DRank2TruncationFamilyAnalysis",
            "Periodic1DRank2TruncationFamilyAnalyzer",
            "Periodic1DRank2TruncationFamilyIndependentVerifier",
            "Periodic1DRank2TruncationFamilyRequest",
            "Periodic1DRank2TruncationIndependentReferenceAnalyzer",
            "Periodic1DRank2TruncationIndependentVerifier",
            "Periodic1DRank2TruncationMeshStabilityAssessment",
            "Periodic1DRank2TruncationPoint",
            "Periodic1DRank2TruncationQualificationStopped",
            "Periodic1DRank2TruncationRange",
            "Periodic1DRank2TruncationRequest",
            "Periodic1DRank2TruncationToleranceSelector",
            "Periodic1DRank2TruncationToleranceSelectionIndependentReference",
            ("Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer"),
        ],
    )
    def test__legacy_bound_name__reexports_identical_type(self, name: str) -> None:
        """Establish import identity only, not scientific or numerical validity."""
        assert getattr(RankFirstSupportTruncation, name) is getattr(
            LegacyEquivalenceSupportTruncation,
            name,
        )

    def test__historical_short_names__are_identity_aliases(self) -> None:
        """Historical names remain aliases rather than wrappers or subclasses."""
        assert (
            Periodic1DRank2TruncationAnalysis
            is Periodic1DRank2SupportTruncationAnalysis
        )
        assert (
            Periodic1DRank2TruncationAnalyzer
            is Periodic1DRank2SupportTruncationAnalyzer
        )
        assert (
            Periodic1DRank2TruncationRequest
            is Periodic1DRank2SupportTruncationAnalysisRequest
        )
