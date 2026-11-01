"""Authoritative ownership checks for rank-two support truncation."""

from importlib.util import find_spec

import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace import (
    rank2 as BandEquivalenceRank2,
)
from ksdft2effmass.periodic1d.rank2 import (
    support_truncation as RankFirstSupportTruncation,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.analysis import (
    Periodic1DRank2SupportTruncationAnalyzer,
    Periodic1DRank2TruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
    Periodic1DRank2TruncationRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2SupportTruncationAnalysis,
    Periodic1DRank2TruncationAnalysis,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.unit]


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
            "Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer",
        ],
    )
    def test__capability_packages__do_not_reexport_owner_values(
        self,
        name: str,
    ) -> None:
        assert not hasattr(BandEquivalenceRank2, name)
        assert not hasattr(RankFirstSupportTruncation, name)

    def test__capability_packages__are_non_eager_namespaces(self) -> None:
        for capability_package in (
            BandEquivalenceRank2,
            RankFirstSupportTruncation,
        ):
            assert not hasattr(capability_package, "__all__")
            assert not any(
                name.startswith("Periodic1D") for name in vars(capability_package)
            )

    def test__obsolete_study_owned_package__is_removed(self) -> None:
        assert (
            find_spec(
                "ksdft2effmass.periodic1d.band_equivalence_locality."
                "embedded_subspace.rank2.truncation"
            )
            is None
        )

    def test__established_short_names__retain_exact_type_identity(self) -> None:
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
