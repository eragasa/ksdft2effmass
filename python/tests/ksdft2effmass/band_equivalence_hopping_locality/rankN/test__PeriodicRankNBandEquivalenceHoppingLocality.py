"""Cross-dimensional ownership contracts for periodic rank-N aggregates."""

from __future__ import annotations

import pytest

from ksdft2effmass.band_equivalence_hopping_locality.rankN.analysis import (
    _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
)
from ksdft2effmass.band_equivalence_hopping_locality.rankN.base import (
    PeriodicRankNBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole,
    PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseValue,
    PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
    PeriodicRankNBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.band_equivalence_hopping_locality.rankN.fourier_reference import (
    _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic,
)
from ksdft2effmass.band_equivalence_hopping_locality.rankN.reference import (
    _IndependentPeriodicRankNCase,
)
from ksdft2effmass.band_equivalence_hopping_locality.rankN.result import (
    PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels,
    PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary,
    PeriodicRankNFittedAlignmentEvidence,
    PeriodicRankNPrescribedAlignmentEvidence,
    PeriodicRankNSupportSelected,
    PeriodicRankNSupportUnresolved,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.reference import (
    _IndependentPeriodic2DRankNCase,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary,
    Periodic2DRankNFittedAlignmentEvidence,
    Periodic2DRankNPrescribedAlignmentEvidence,
    Periodic2DRankNSupportSelected,
    Periodic2DRankNSupportUnresolved,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.reference import (
    _IndependentPeriodic3DRankNCase,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary,
    Periodic3DRankNFittedAlignmentEvidence,
    Periodic3DRankNPrescribedAlignmentEvidence,
    Periodic3DRankNSupportSelected,
    Periodic3DRankNSupportUnresolved,
)


class TestPeriodicRankNBandEquivalenceHoppingLocality:
    """Keep common ownership dimension-neutral and concrete values distinct."""

    def test_dimension_roles_inherit_their_common_rank_n_owner(self) -> None:
        common_roles = (
            PeriodicRankNBandEquivalenceHoppingLocalityCapability,
            PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
            PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest,
            PeriodicRankNBandEquivalenceHoppingLocalityCaseValue,
            PeriodicRankNBandEquivalenceHoppingLocalityCaseAction,
            PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
            PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole,
            PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole,
            PeriodicRankNBandEquivalenceHoppingLocalityValue,
            PeriodicRankNBandEquivalenceHoppingLocalityAction,
        )
        periodic2d_roles = (
            Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
            Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole,
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
            Periodic2DRankNBandEquivalenceHoppingLocalityValue,
            Periodic2DRankNBandEquivalenceHoppingLocalityAction,
        )
        periodic3d_roles = (
            Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
            Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
            Periodic3DRankNBandEquivalenceHoppingLocalityValue,
            Periodic3DRankNBandEquivalenceHoppingLocalityAction,
        )

        for common, periodic2d, periodic3d in zip(
            common_roles, periodic2d_roles, periodic3d_roles, strict=True
        ):
            assert issubclass(periodic2d, common)
            assert issubclass(periodic3d, common)
            assert not issubclass(periodic2d, periodic3d)
            assert not issubclass(periodic3d, periodic2d)

    def test_dimension_leaf_results_inherit_common_validation_parents(self) -> None:
        common_values = (
            PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels,
            PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary,
            PeriodicRankNSupportSelected,
            PeriodicRankNSupportUnresolved,
            PeriodicRankNFittedAlignmentEvidence,
            PeriodicRankNPrescribedAlignmentEvidence,
        )
        periodic2d_values = (
            Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels,
            Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary,
            Periodic2DRankNSupportSelected,
            Periodic2DRankNSupportUnresolved,
            Periodic2DRankNFittedAlignmentEvidence,
            Periodic2DRankNPrescribedAlignmentEvidence,
        )
        periodic3d_values = (
            Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
            Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary,
            Periodic3DRankNSupportSelected,
            Periodic3DRankNSupportUnresolved,
            Periodic3DRankNFittedAlignmentEvidence,
            Periodic3DRankNPrescribedAlignmentEvidence,
        )

        for common, periodic2d, periodic3d in zip(
            common_values, periodic2d_values, periodic3d_values, strict=True
        ):
            assert issubclass(periodic2d, common)
            assert issubclass(periodic3d, common)
            assert not issubclass(periodic2d, periodic3d)
            assert not issubclass(periodic3d, periodic2d)

    def test_production_and_reference_arithmetic_have_separate_common_owners(
        self,
    ) -> None:
        production = (
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
        )
        fourier_references = (
            Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
            Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
        )
        independent_cases = (
            _IndependentPeriodic2DRankNCase,
            _IndependentPeriodic3DRankNCase,
        )

        for analyzer in production:
            assert issubclass(
                analyzer,
                _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
            )
            assert not issubclass(
                analyzer,
                _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic,
            )
        for reference_analyzer in fourier_references:
            assert issubclass(
                reference_analyzer,
                _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic,
            )
            assert not issubclass(
                reference_analyzer,
                _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
            )
        for independent in independent_cases:
            assert issubclass(independent, _IndependentPeriodicRankNCase)
            assert not issubclass(
                independent,
                _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
            )

    def test_common_validation_preserves_exact_dimension_types(self) -> None:
        periodic2d = Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels(
            maximum_matrix_frobenius=1.0,
            root_mean_square_matrix_frobenius=2.0,
            maximum_ordered_spectrum=3.0,
            root_mean_square_ordered_spectrum=4.0,
        )
        periodic3d = Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels(
            maximum_matrix_frobenius=1.0,
            root_mean_square_matrix_frobenius=2.0,
            maximum_ordered_spectrum=3.0,
            root_mean_square_ordered_spectrum=4.0,
        )

        assert (
            type(periodic2d)
            is Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels
        )
        assert (
            type(periodic3d)
            is Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
        )
        with pytest.raises(TypeError, match="must be a built-in float"):
            Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels(
                maximum_matrix_frobenius=True,
                root_mean_square_matrix_frobenius=2.0,
                maximum_ordered_spectrum=3.0,
                root_mean_square_ordered_spectrum=4.0,
            )
