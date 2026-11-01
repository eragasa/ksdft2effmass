"""Synthetic complete-five-scale retention lifecycle tests."""

from __future__ import annotations

import hashlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DRank2AdaptiveAmplitudeRequest,
    Periodic1DRank2AmplitudeRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.analysis import (  # noqa: E501
    Periodic1DRank2MomentumRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.family import (  # noqa: E501
    Periodic1DRank2MomentumRefinementFamilyAnalyzer,
    Periodic1DRank2MomentumRefinementFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyAnalyzer,
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleCalculationRecord,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale_verification import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleVerifier,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale_visualization_data import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleVisualizationData,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.visualizations.complete_five_scale import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleSummaryRenderer,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.visualizations.complete_five_scale_figures import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleFigureData,
    Periodic1DRank2CompleteFiveScaleFigureEnum,
    Periodic1DRank2CompleteFiveScaleFigureRenderer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyAnalyzer,
    Periodic1DRank2TruncationFamilyRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.mesh_stability import (
    Periodic1DRank2TruncationMeshStabilityAssessment,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRank2CompleteFiveScaleCalculationRecordLifecycle:
    """Establish synthetic canonical calculation, verification, and projection."""

    @pytest.fixture(scope="class")
    @classmethod
    def record(cls) -> Periodic1DRank2CompleteFiveScaleCalculationRecord:
        scales = (0.0, 0.25, 0.5, 0.75, 1.0)
        amplitudes = (0.0, math.pi / 8.0, math.pi / 4.0)
        transporter = ClosedLoopPolarFrameTransporter()
        template = Periodic1DRank2Request(
            reciprocal_mesh_size=16,
            amplitudes=amplitudes,
            parent_hopping_scale=1.0,
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.99,
            frame_absolute_tolerance=1.0e-10,
            transport_rank_relative_tolerance=1.0e-12,
            transport_validation_relative_tolerance=1.0e-10,
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
        )
        parent_request = Periodic1DRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=scales,
        )
        parent_family = Periodic1DRank2ParentFamilyAnalyzer(
            request=parent_request,
            transporter=transporter,
        ).execute()
        strict_thresholds = Periodic1DRank2MomentumRefinementThresholds(
            maximum_parent_diagnostic_change=1.0e-30,
            maximum_correlation_change=1.0e-30,
            maximum_threshold_change=1.0e-30,
            maximum_hopping_weight_change=1.0e-30,
            maximum_hopping_power_change=1.0e-30,
            maximum_angle_change=1.0e-30,
            maximum_band_defect=1.0e-30,
            maximum_reconstruction_defect=1.0e-30,
            maximum_parseval_defect=1.0e-30,
        )
        momentum_family = Periodic1DRank2MomentumRefinementFamilyAnalyzer(
            request=Periodic1DRank2MomentumRefinementFamilyRequest(
                parent_family_request=replace(
                    parent_request,
                    template_request=replace(template, reciprocal_mesh_size=8),
                ),
                reciprocal_mesh_sizes=(8, 16, 32),
                thresholds=strict_thresholds,
                required_stable_refinements=2,
            ),
            transporter=transporter,
        ).execute()
        adaptive = Periodic1DRank2AdaptiveAmplitudeAnalyzer(
            request=Periodic1DRank2AdaptiveAmplitudeRequest(
                template_request=template,
                thresholds=Periodic1DRank2AmplitudeRefinementThresholds(
                    maximum_correlation_defect=1.0e-8,
                    maximum_operator_threshold_defect=1.0e-8,
                    maximum_joint_threshold_defect=1.0e-8,
                    maximum_hopping_weight_defect=1.0e-8,
                    maximum_hopping_power_defect=1.0e-8,
                ),
                maximum_refinement_levels=2,
                maximum_evaluated_amplitudes=5,
            ),
            transporter=transporter,
        ).execute()
        truncation_families = tuple(
            Periodic1DRank2TruncationFamilyAnalyzer(
                request=Periodic1DRank2TruncationFamilyRequest.every_integer_through(
                    parent_family_request=replace(
                        parent_request,
                        template_request=replace(
                            template,
                            reciprocal_mesh_size=mesh_size,
                        ),
                    ),
                    maximum_range=2,
                    evaluation_mesh_size=4 * mesh_size + 1,
                    support_tolerance=1.0e-8,
                ),
                transporter=transporter,
            ).execute()
            for mesh_size in (8, 16)
        )
        return Periodic1DRank2CompleteFiveScaleCalculationRecord(
            parent_family=parent_family,
            momentum_refinement_family=momentum_family,
            adaptive_amplitude=adaptive,
            truncation_mesh_stability=(
                Periodic1DRank2TruncationMeshStabilityAssessment(truncation_families)
            ),
        )

    def test_mesh_stability_distinguishes_invalid_type_and_value(self) -> None:
        with pytest.raises(TypeError):
            Periodic1DRank2TruncationMeshStabilityAssessment([])  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            Periodic1DRank2TruncationMeshStabilityAssessment(())

    def test_canonical_round_trip_preserves_the_complete_aggregate(
        self,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
    ) -> None:
        canonical_bytes = record.to_json()

        admitted = type(record).from_json(canonical_bytes)

        assert admitted == record
        assert admitted.to_json() == canonical_bytes
        assert admitted.parent_family.request.parent_hopping_scales == (
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
        )
        assert admitted.principal_truncation_family.request.maximum_ranges == (
            0,
            1,
            2,
        )

    def test_independent_verification_authenticates_subject_and_projection(
        self,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
    ) -> None:
        subject_bytes = record.to_json()
        verifier = Periodic1DRank2CompleteFiveScaleVerifier(subject_bytes)

        verification = verifier.result()
        verification_bytes = verification.to_json()

        assert verification.passed
        assert verification.subject_sha256 == hashlib.sha256(subject_bytes).hexdigest()
        assert type(verification).from_json(verification_bytes) == verification
        assert verifier.admit_stored(verification) == record

    def test_projection_preserves_unresolved_momentum_and_mesh_decisions(
        self,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
    ) -> None:
        source_sha256 = hashlib.sha256(record.to_json()).hexdigest()

        projection = Periodic1DRank2CompleteFiveScaleVisualizationData.from_record(
            record,
            source_sha256=source_sha256,
        )

        assert projection.source_sha256 == source_sha256
        assert projection.momentum_dispositions == ("unresolved",) * 5
        assert projection.construction_mesh_sizes == (8, 16)
        assert len(projection.adjacent_decision_change_counts) == 1
        assert type(projection).from_json(projection.to_json()) == projection
        summary = Periodic1DRank2CompleteFiveScaleSummaryRenderer(projection).render()
        assert summary.startswith(b"# Complete five-scale finite-control summary\n")
        assert b"| 0 | unresolved |" in summary
        assert b"does not establish continuum convergence" in summary

    def test_admitted_record_renders_the_closed_publication_figure_inventory(
        self,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
    ) -> None:
        source_sha256 = hashlib.sha256(record.to_json()).hexdigest()
        data = Periodic1DRank2CompleteFiveScaleFigureData.from_record(
            record,
            source_sha256=source_sha256,
        )

        visualizations = Periodic1DRank2CompleteFiveScaleFigureRenderer(
            data,
            dpi=40,
        ).execute()

        assert data.source_sha256 == source_sha256
        assert tuple(item.plot for item in visualizations) == tuple(
            Periodic1DRank2CompleteFiveScaleFigureEnum
        )
        assert all(item.png.startswith(b"\x89PNG\r\n\x1a\n") for item in visualizations)

    def test_tampered_subject_bytes_are_rejected_before_re_admission(
        self,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
    ) -> None:
        subject_bytes = record.to_json()
        verification = Periodic1DRank2CompleteFiveScaleVerifier(subject_bytes).result()
        tampered = subject_bytes.replace(b"0.25", b"0.24", 1)

        with pytest.raises((TypeError, ValueError)):
            Periodic1DRank2CompleteFiveScaleVerifier(tampered).admit_stored(
                verification
            )
