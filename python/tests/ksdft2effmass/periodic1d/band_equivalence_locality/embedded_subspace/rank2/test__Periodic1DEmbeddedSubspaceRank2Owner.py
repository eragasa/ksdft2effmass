"""Tests for the installed nonflat embedded-subspace/rank2 band-equivalence owner."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import replace

import pytest
from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2Analyzer,
    Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure,
    Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved,
    Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure,
    Periodic1DEmbeddedSubspaceRank2ExternalGapFailure,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
    Periodic1DEmbeddedSubspaceRank2Request,
)
from ksdft2effmass.periodic1d.band_equivalence_locality import (
    Periodic1DEmbeddedSubspaceRank2AnalysisRecord,
    Periodic1DEmbeddedSubspaceRank2AnalysisRecorder,
    Periodic1DEmbeddedSubspaceRank2QualificationRecord,
)


def _request() -> Periodic1DEmbeddedSubspaceRank2Request:
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=16,
        amplitudes=(0.0, 0.2, math.pi / 4.0),
        parent_hopping_scale=1.0,
        minimum_external_gap=0.1,
        minimum_transport_singular_value=0.8,
        frame_absolute_tolerance=1.0e-10,
        transport_rank_relative_tolerance=1.0e-12,
        transport_validation_relative_tolerance=1.0e-10,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-12,
    )


def _analyze(
    request: Periodic1DEmbeddedSubspaceRank2Request,
) -> Periodic1DEmbeddedSubspaceRank2Analysis:
    return Periodic1DEmbeddedSubspaceRank2Analyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


class TestPeriodic1DEmbeddedSubspaceRank2Owner:
    """Establish qualification, separated channels, and explicit stop states."""

    def test_qualified_parent_preserves_transport_and_representation_channels(
        self,
    ) -> None:
        analysis = _analyze(_request())
        qualification = analysis.qualification
        assert type(qualification) is Periodic1DEmbeddedSubspaceRank2QualifiedParent
        assert qualification.qualified
        assert qualification.minimum_external_gap > 0.1
        assert qualification.minimum_transport_singular_value > 0.8
        assert len(qualification.closure_holonomy_phases) == 2
        assert qualification.closure_alignment_residual >= 0.0
        assert qualification.maximum_primitive_link_frobenius_residual >= 0.0
        assert len(analysis.points) == 3
        assert max(point.maximum_band_defect for point in analysis.points) < 1.0e-14
        assert (
            max(point.minimum_loss_reconstruction_defect for point in analysis.points)
            < 1.0e-14
        )
        assert analysis.points[0].discrete_maximum_correlation == 1.0
        assert analysis.points[-1].discrete_maximum_correlation < 1.0
        for power in analysis.points[0].hopping_powers:
            assert power.comparison_normalized_squared_frobenius_norm == pytest.approx(
                power.reference_normalized_squared_frobenius_norm,
                rel=0.0,
                abs=1.0e-15,
            )
        assert (
            math.fsum(
                power.comparison_normalized_squared_frobenius_norm
                for power in analysis.points[-1].hopping_powers
            )
            > 0.0
        )
        for point in analysis.points:
            assert tuple(item.displacement for item in point.hopping_powers) == tuple(
                range(-8, 8)
            )
            assert point.reference_parseval_defect < 1.0e-14
            assert point.comparison_parseval_defect < 1.0e-14

    def test_external_gap_gate_stops_before_transport_and_points(self) -> None:
        analysis = _analyze(replace(_request(), minimum_external_gap=2.0))
        assert (
            type(analysis.qualification)
            is Periodic1DEmbeddedSubspaceRank2ExternalGapFailure
        )
        assert not analysis.qualification.qualified
        assert not hasattr(analysis.qualification, "band_transport_status")
        assert analysis.points == ()

    def test_scientific_transport_threshold_is_distinct_from_owner_rank_status(
        self,
    ) -> None:
        analysis = _analyze(replace(_request(), minimum_transport_singular_value=1.0))
        assert (
            type(analysis.qualification)
            is Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure
        )
        assert not hasattr(analysis.qualification, "band_transport_status")
        assert analysis.points == ()

    def test_record_round_trip_preserves_exact_canonical_bytes(self) -> None:
        analysis = _analyze(_request())
        payload = (
            Periodic1DEmbeddedSubspaceRank2AnalysisRecorder(analysis).result().to_json()
        )
        admitted = Periodic1DEmbeddedSubspaceRank2AnalysisRecord.from_json(payload)
        assert admitted.analysis == analysis
        assert admitted.to_json() == payload

    def test_qualification_records_preserve_each_closed_variant(self) -> None:
        qualified = _analyze(_request()).qualification
        variants = (
            Periodic1DEmbeddedSubspaceRank2ExternalGapFailure(0.05),
            Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure(
                minimum_external_gap=0.2,
                operation=ClosedLoopPolarFrameTransportBackendOperation.PROCRUSTES_SVD,
                reason=(
                    ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE
                ),
                link_index=0,
            ),
            Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved(
                minimum_external_gap=0.2,
                band_transport_status=(
                    ClosedLoopPolarFrameTransportStatus.RANK_DEFICIENT
                ),
                minimum_transport_singular_value=0.0,
            ),
            Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure(
                minimum_external_gap=0.2,
                minimum_transport_singular_value=0.5,
            ),
            qualified,
        )
        for variant in variants:
            payload = Periodic1DEmbeddedSubspaceRank2QualificationRecord(
                variant
            ).to_json()
            admitted = Periodic1DEmbeddedSubspaceRank2QualificationRecord.from_json(
                payload
            )
            assert admitted.qualification == variant
            assert admitted.to_json() == payload

    def test_qualification_record_rejects_unknown_wire_variant(self) -> None:
        mapping = dict(
            Periodic1DEmbeddedSubspaceRank2QualificationRecord(
                Periodic1DEmbeddedSubspaceRank2ExternalGapFailure(0.05)
            ).to_dict()
        )
        mapping["variant"] = "band-transport-backend-failuer"
        with pytest.raises(ValueError, match="unknown.*qualification variant"):
            Periodic1DEmbeddedSubspaceRank2QualificationRecord.from_dict(mapping)

    def test_request_rejects_boolean_mesh_and_record_rejects_identity_tampering(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="reciprocal_mesh_size"):
            replace(_request(), reciprocal_mesh_size=True)
        mapping = dict(
            Periodic1DEmbeddedSubspaceRank2AnalysisRecord(
                _analyze(_request())
            ).to_dict()
        )
        request_mapping = mapping["request"]
        assert isinstance(request_mapping, Mapping)
        tampered_request = dict(request_mapping)
        tampered_request["parent_model_identifier"] = "different-parent.v1"
        mapping["request"] = tampered_request
        with pytest.raises(ValueError, match="parent_model_identifier"):
            Periodic1DEmbeddedSubspaceRank2AnalysisRecord.from_dict(mapping)
