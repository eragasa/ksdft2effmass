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
)
from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2SupportTruncationAnalysis,
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

    def test__obsolete_short_names__are_absent_from_defining_modules(self) -> None:
        from ksdft2effmass.periodic1d.rank2.support_truncation import (
            analysis,
            request,
            results,
        )

        assert not hasattr(results, "Periodic1DRank2TruncationAnalysis")
        assert not hasattr(analysis, "Periodic1DRank2TruncationAnalyzer")
        assert not hasattr(request, "Periodic1DRank2TruncationRequest")
        assert Periodic1DRank2SupportTruncationAnalysis.__module__.endswith(".results")
        assert Periodic1DRank2SupportTruncationAnalyzer.__module__.endswith(".analysis")
        assert Periodic1DRank2SupportTruncationAnalysisRequest.__module__.endswith(
            ".request"
        )
