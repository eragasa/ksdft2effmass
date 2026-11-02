"""Ownership tests for the embedded-subspace rank-two aggregate."""

from __future__ import annotations

from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.base import (
    Periodic1DRank2BandEquivalenceHoppingLocalityAction,
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
    Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
    Periodic1DRank2BandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DRank2AdaptiveAmplitudeRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.momentum_refinement.analysis import (  # noqa: E501
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementAnalyzer,
    Periodic1DRank2MomentumRefinementRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyAnalysis,
    Periodic1DRank2ParentFamilyAnalyzer,
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.parent_scale.analysis import (  # noqa: E501
    Periodic1DRank2Analyzer,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.parent_scale.results import (  # noqa: E501
    Periodic1DRank2Analysis,
    Periodic1DRank2HoppingPower,
    Periodic1DRank2PointAnalysis,
    Periodic1DRank2Qualification,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.retention.records import (  # noqa: E501
    Periodic1DRank2AnalysisRecord,
    Periodic1DRank2AnalysisRecorder,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.retention.visualization_data import (  # noqa: E501
    Periodic1DRank2CalculationVisualizationData,
    Periodic1DRank2ParentFamilyVisualizationData,
    Periodic1DRank2VisualizationData,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.visualizations.visualizer import (  # noqa: E501
    Periodic1DRank2CalculationVisualizer,
    Periodic1DRank2ParentFamilyVisualizer,
    Periodic1DRank2Visualizer,
)


class TestPeriodic1DRank2AggregateOwnership:
    """Establish truthful ownership for aggregate and supporting leaves."""

    def test_primary_owners_use_request_analysis_analyzer_roles(self) -> None:
        assert issubclass(
            Periodic1DRank2Request,
            Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic1DRank2Analysis,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic1DRank2Analyzer,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )
        assert issubclass(
            Periodic1DRank2ParentFamilyRequest,
            Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
        )
        assert issubclass(
            Periodic1DRank2ParentFamilyAnalysis,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert issubclass(
            Periodic1DRank2ParentFamilyAnalyzer,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
        )

    def test_refinements_remain_numerical_consistency_values(self) -> None:
        for request_type in (
            Periodic1DRank2AdaptiveAmplitudeRequest,
            Periodic1DRank2MomentumRefinementRequest,
        ):
            assert issubclass(
                request_type,
                Periodic1DRank2BandEquivalenceHoppingLocalityValue,
            )
        for analysis_type in (
            Periodic1DRank2AdaptiveAmplitudeAnalysis,
            Periodic1DRank2MomentumRefinementAnalysis,
        ):
            assert issubclass(analysis_type, NumericalConsistency)
            assert issubclass(
                analysis_type,
                Periodic1DRank2BandEquivalenceHoppingLocalityValue,
            )
        for analyzer_type in (
            Periodic1DRank2AdaptiveAmplitudeAnalyzer,
            Periodic1DRank2MomentumRefinementAnalyzer,
        ):
            assert issubclass(
                analyzer_type,
                Periodic1DRank2BandEquivalenceHoppingLocalityAction,
            )

    def test_subanalyses_do_not_claim_top_level_analysis_roles(self) -> None:
        assert issubclass(
            Periodic1DRank2Qualification,
            Periodic1DRank2BandEquivalenceHoppingLocalityValue,
        )
        assert issubclass(
            Periodic1DRank2PointAnalysis,
            Periodic1DRank2BandEquivalenceHoppingLocalityValue,
        )
        assert not issubclass(
            Periodic1DRank2PointAnalysis,
            Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole,
        )
        assert not issubclass(
            Periodic1DRank2HoppingPower,
            Periodic1DRank2BandEquivalenceHoppingLocalityValue,
        )

    def test_visualization_inputs_and_actions_retain_aggregate_ownership(self) -> None:
        for data_type in (
            Periodic1DRank2VisualizationData,
            Periodic1DRank2ParentFamilyVisualizationData,
            Periodic1DRank2CalculationVisualizationData,
        ):
            assert issubclass(
                data_type,
                Periodic1DRank2BandEquivalenceHoppingLocalityValue,
            )
        for visualizer_type in (
            Periodic1DRank2Visualizer,
            Periodic1DRank2ParentFamilyVisualizer,
            Periodic1DRank2CalculationVisualizer,
        ):
            assert issubclass(
                visualizer_type,
                Periodic1DRank2BandEquivalenceHoppingLocalityAction,
            )

    def test_recorders_are_actions_but_wire_records_are_not_capabilities(self) -> None:
        assert issubclass(
            Periodic1DRank2AnalysisRecorder,
            Periodic1DRank2BandEquivalenceHoppingLocalityAction,
        )
        assert not issubclass(
            Periodic1DRank2AnalysisRecord,
            Periodic1DRank2BandEquivalenceHoppingLocalityValue,
        )
