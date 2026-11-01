"""Software ownership contracts for :class:`SupportTruncation`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.results import (
    BandEquivalenceLocalityShellAnalysis,
)
from ksdft2effmass.periodic1d.rank1.support_truncation import (
    Periodic1DRank1SupportResult,
    Periodic1DRank1SupportTruncationAnalysis,
    Periodic1DRank1SupportTruncationAnalysisRequest,
    Periodic1DRank1SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.analysis import (
    Periodic1DRank2SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyAnalysis,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2SupportTruncationAnalysis,
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationRange,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.tolerance_selection import (
    Periodic1DRank2TruncationToleranceSelector,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.tolerance_selection_reference import (  # noqa: E501
    Periodic1DRank2TruncationToleranceSelectionIndependentReference,
)
from ksdft2effmass.periodic1d.rankN.support_truncation import (
    Periodic1DRankNLocalityAnalysis,
    Periodic1DRankNSupportResult,
    Periodic1DRankNSupportTruncationAnalysis,
    Periodic1DRankNSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellSupportInventory,
    MinimumToleranceSatisfyingSupport,
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncation,
    RealSpaceSupportTruncationComparison,
    RealSpaceSupportTruncationErrors,
    RealSpaceSupportTruncationFamily,
    RealSpaceSupportTruncationModelToleranceSelection,
    RealSpaceSupportTruncationToleranceSelection,
    RealSpaceSupportTruncationToleranceSelectionRequest,
    RealSpaceSupportTruncationToleranceSelector,
    SupportToleranceUnresolved,
)
from ksdft2effmass.support_truncation import SupportTruncation

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSupportTruncation:
    def test__real_space_and_periodic1d__form_specialization_chain(self) -> None:
        """Periodic 1D support removal remains a real-space truncation."""
        assert issubclass(RealSpaceSupportTruncation, SupportTruncation)
        assert issubclass(
            Periodic1DSupportTruncation,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DRank1SupportTruncationAnalysis,
            Periodic1DSupportTruncation,
        )
        assert issubclass(
            Periodic1DRank1SupportResult,
            Periodic1DSupportTruncation,
        )
        assert issubclass(
            Periodic1DRank2SupportTruncationAnalysis,
            Periodic1DSupportTruncation,
        )
        assert issubclass(
            Periodic1DRankNSupportTruncationAnalysis,
            Periodic1DSupportTruncation,
        )

    def test__rank_specific_action_names__are_mirrored(self) -> None:
        """Rank-one, rank-two, and rank-N expose mirrored action vocabulary."""
        assert Periodic1DRank1SupportTruncationAnalysis.__name__ == (
            "Periodic1DRank1SupportTruncationAnalysis"
        )
        assert Periodic1DRank2SupportTruncationAnalysis.__name__ == (
            "Periodic1DRank2SupportTruncationAnalysis"
        )
        assert Periodic1DRankNSupportTruncationAnalysis.__name__ == (
            "Periodic1DRankNSupportTruncationAnalysis"
        )
        assert Periodic1DRank1SupportTruncationAnalysisRequest.__name__ == (
            "Periodic1DRank1SupportTruncationAnalysisRequest"
        )
        assert Periodic1DRank2SupportTruncationAnalysisRequest.__name__ == (
            "Periodic1DRank2SupportTruncationAnalysisRequest"
        )
        assert Periodic1DRankNSupportTruncationAnalysisRequest.__name__ == (
            "Periodic1DRankNSupportTruncationAnalysisRequest"
        )
        assert Periodic1DRank1SupportTruncationAnalyzer.__name__ == (
            "Periodic1DRank1SupportTruncationAnalyzer"
        )
        assert Periodic1DRank2SupportTruncationAnalyzer.__name__ == (
            "Periodic1DRank2SupportTruncationAnalyzer"
        )
        assert Periodic1DRankNSupportTruncationAnalyzer.__name__ == (
            "Periodic1DRankNSupportTruncationAnalyzer"
        )

    @pytest.mark.legacy_equivalence
    def test__historical_rank2_name__is_identical_class_alias(self) -> None:
        """The shorter historical name preserves exact class identity."""
        assert (
            Periodic1DRank2TruncationAnalysis
            is Periodic1DRank2SupportTruncationAnalysis
        )

    @pytest.mark.parametrize(
        "subject_type",
        [
            pytest.param(
                Periodic1DRank2TruncationRange,
                id="Periodic1DRank2TruncationRange",
            ),
            pytest.param(
                Periodic1DRankNSupportResult,
                id="Periodic1DRankNSupportResult",
            ),
            pytest.param(
                Periodic1DRankNLocalityAnalysis,
                id="Periodic1DRankNLocalityAnalysis",
            ),
            pytest.param(
                BandEquivalenceLocalityShellAnalysis,
                id="BandEquivalenceLocalityShellAnalysis",
            ),
            pytest.param(
                MetricShellSupportInventory,
                id="MetricShellSupportInventory",
            ),
            pytest.param(
                RankNormalizedMatrixFrobeniusErrors,
                id="RankNormalizedMatrixFrobeniusErrors",
            ),
            pytest.param(
                OrderedEigenvalueErrors,
                id="OrderedEigenvalueErrors",
            ),
            pytest.param(
                RealSpaceSupportTruncationErrors,
                id="RealSpaceSupportTruncationErrors",
            ),
            pytest.param(
                RealSpaceSupportTruncationComparison,
                id="RealSpaceSupportTruncationComparison",
            ),
            pytest.param(
                RealSpaceSupportTruncationFamily,
                id="RealSpaceSupportTruncationFamily",
            ),
            pytest.param(
                Periodic1DRank2TruncationFamilyAnalysis,
                id="Periodic1DRank2TruncationFamilyAnalysis",
            ),
            pytest.param(
                Periodic1DRank2TruncationToleranceSelectionIndependentReference,
                id=("Periodic1DRank2TruncationToleranceSelectionIndependentReference"),
            ),
            pytest.param(
                MinimumToleranceSatisfyingSupport,
                id="MinimumToleranceSatisfyingSupport",
            ),
            pytest.param(
                SupportToleranceUnresolved,
                id="SupportToleranceUnresolved",
            ),
            pytest.param(
                RealSpaceSupportTruncationModelToleranceSelection,
                id="RealSpaceSupportTruncationModelToleranceSelection",
            ),
            pytest.param(
                RealSpaceSupportTruncationToleranceSelection,
                id="RealSpaceSupportTruncationToleranceSelection",
            ),
            pytest.param(
                RealSpaceSupportTruncationToleranceSelectionRequest,
                id="RealSpaceSupportTruncationToleranceSelectionRequest",
            ),
            pytest.param(
                RealSpaceSupportTruncationToleranceSelector,
                id="RealSpaceSupportTruncationToleranceSelector",
            ),
            pytest.param(
                Periodic1DRank2TruncationToleranceSelector,
                id="Periodic1DRank2TruncationToleranceSelector",
            ),
        ],
    )
    def test__dimension_slice__remains_real_space_support_truncation(
        self,
        subject_type: type[RealSpaceSupportTruncation],
    ) -> None:
        """Each range, support, family, or shell value keeps its owner."""
        assert issubclass(subject_type, RealSpaceSupportTruncation)

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone cannot admit an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        assert not isinstance(UnrelatedResult(), SupportTruncation)
