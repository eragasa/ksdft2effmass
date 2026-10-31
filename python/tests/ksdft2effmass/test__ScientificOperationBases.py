"""Software contracts for cross-dimensional scientific-operation bases."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementDiagnostics
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.geometry import (
    BandEquivalenceLocalityMetricCovarianceDefectResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement_records import (  # noqa: E501
    BandEquivalenceLocalityRefinementAssessment,
    BandEquivalenceLocalityRefinementPair,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.results import (
    BandEquivalenceLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
    BandEquivalenceLocalityRepresentationEquivalenceAnalysis,
    BandEquivalenceLocalityShellAnalysis,
)
from ksdft2effmass.hamiltonian import SpectralReduction
from ksdft2effmass.numerical_consistency import (
    NumericalConsistency,
    ReciprocalMeshRefinementFamily,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
    Periodic1DRank2PointAnalysis,
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationFamilyAnalysis,
    Periodic1DRank2TruncationRange,
    Periodic1DRank2TruncationToleranceSelectionIndependentReference,
    Periodic1DRank2TruncationToleranceSelector,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.fourier import (
    Periodic1DHigherRankFourierAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.interpolation import (  # noqa: E501
    Periodic1DHigherRankInterpolationAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.locality import (
    Periodic1DHigherRankLocalityAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.recovery import (
    Periodic1DHigherRankRecoveryAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.results import (
    Periodic1DHigherRankSupportResult,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.refinement import (
    Periodic1DHigherRankRefinementAnalysis,
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
from ksdft2effmass.representation_equivalence import RepresentationEquivalence
from ksdft2effmass.subspace_reduction import SubspaceReduction

pytestmark = pytest.mark.software_verification


class TestScientificOperationBases:
    """Keep the first nominal ownership assignments explicit and nonstructural."""

    def test_subspace_reduction__spectral_reduction__has_nominal_owner(self) -> None:
        """Existing Hamiltonian compression adopts the subspace-reduction base."""
        assert issubclass(SpectralReduction, SubspaceReduction)

    def test_representation_equivalence__family_results__share_owner(self) -> None:
        """Rank-two and rank-N recovery results share equivalence ownership."""
        assert issubclass(
            Periodic1DRank2PointAnalysis,
            RepresentationEquivalence,
        )
        assert issubclass(
            Periodic1DHigherRankRecoveryAnalysis,
            RepresentationEquivalence,
        )
        assert issubclass(
            BandEquivalenceLocalityRepresentationEquivalenceAnalysis,
            RepresentationEquivalence,
        )

    def test_real_space_support_truncation__dimension_slices__share_owner(
        self,
    ) -> None:
        """Range, support, and metric-shell results share spatial ownership."""
        assert issubclass(
            Periodic1DRank2TruncationAnalysis,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DRank2TruncationRange,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DHigherRankSupportResult,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            Periodic1DHigherRankLocalityAnalysis,
            RealSpaceSupportTruncation,
        )
        assert issubclass(
            BandEquivalenceLocalityShellAnalysis,
            RealSpaceSupportTruncation,
        )
        shared_selection_types = (
            MetricShellSupportInventory,
            RankNormalizedMatrixFrobeniusErrors,
            OrderedEigenvalueErrors,
            RealSpaceSupportTruncationErrors,
            RealSpaceSupportTruncationComparison,
            RealSpaceSupportTruncationFamily,
            Periodic1DRank2TruncationFamilyAnalysis,
            Periodic1DRank2TruncationToleranceSelectionIndependentReference,
            MinimumToleranceSatisfyingSupport,
            SupportToleranceUnresolved,
            RealSpaceSupportTruncationModelToleranceSelection,
            RealSpaceSupportTruncationToleranceSelection,
            RealSpaceSupportTruncationToleranceSelectionRequest,
            RealSpaceSupportTruncationToleranceSelector,
            Periodic1DRank2TruncationToleranceSelector,
        )
        assert all(
            issubclass(result_type, RealSpaceSupportTruncation)
            for result_type in shared_selection_types
        )

    def test_numerical_consistency__family_slices__share_owner(self) -> None:
        """Family-specific finite-route results share numerical ownership."""
        numerical_results = (
            ScalarRefinementDiagnostics,
            ReciprocalMeshRefinementFamily,
            Periodic1DRank2MomentumRefinementAnalysis,
            Periodic1DRank2MomentumRefinementFamilyAnalysis,
            Periodic1DRank2AdaptiveAmplitudeAnalysis,
            Periodic1DHigherRankFourierAnalysis,
            Periodic1DHigherRankInterpolationAnalysis,
            Periodic1DHigherRankRefinementAnalysis,
            BandEquivalenceLocalityMetricCovarianceDefectResult,
            BandEquivalenceLocalityRefinementPair,
            BandEquivalenceLocalityRefinementAssessment,
            BandEquivalenceLocalityAmplitudeMidpointAnalysis,
            BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
        )
        assert all(
            issubclass(result_type, NumericalConsistency)
            for result_type in numerical_results
        )

    def test_bases__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone never admits an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        value = UnrelatedResult()
        assert not isinstance(value, SubspaceReduction)
        assert not isinstance(value, RepresentationEquivalence)
        assert not isinstance(value, RealSpaceSupportTruncation)
        assert not isinstance(value, NumericalConsistency)
