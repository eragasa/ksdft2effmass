"""Tests for the embedded-subspace rank-two parent-hopping family owner."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2Analyzer,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecorder,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizer,
    Periodic1DEmbeddedSubspaceRank2Request,
)


def _template() -> Periodic1DEmbeddedSubspaceRank2Request:
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=8,
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


def _request() -> Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest:
    return Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
        template_request=_template(),
        parent_hopping_scales=(0.0, 0.5, 1.0),
    )


def _analyze() -> Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis:
    request = _request()
    return Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


def _subject_bytes() -> bytes:
    return Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecorder(
        _analyze()
    ).result().to_json()


class TestPeriodic1DEmbeddedSubspaceRank2ParentFamily:
    """Establish family correlation, retention, and independent verification."""

    def test_analyzer_preserves_the_complete_declared_homotopy(self) -> None:
        analysis = _analyze()

        assert tuple(
            member.request.parent_hopping_scale for member in analysis.members
        ) == (0.0, 0.5, 1.0)
        assert all(member.qualification.qualified for member in analysis.members)
        assert all(len(member.points) == 3 for member in analysis.members)

    def test_record_round_trip_preserves_exact_canonical_bytes(self) -> None:
        subject = _subject_bytes()
        admitted = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord.from_json(
                subject
            )
        )

        assert admitted.to_json() == subject
        assert admitted.analysis == _analyze()

    def test_canonical_family_passes_independent_verification(self) -> None:
        subject = _subject_bytes()
        verification = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(subject).result()
        )

        assert verification.passed
        assert verification.subject_sha256 == hashlib.sha256(subject).hexdigest()
        assert "member_inventory_defect" in verification.checks
        assert "member_2_hopping_power_maximum_absolute_defect" in (
            verification.checks
        )
        retained = verification.to_json()
        assert (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification.from_json(
                retained
            ).to_json()
            == retained
        )

    def test_authenticated_family_projection_renders_closed_inventory(self) -> None:
        result = Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
            _subject_bytes()
        ).result_with_visualization()

        verified_result_bytes = result.to_json()
        assert type(result).from_json(
            verified_result_bytes
        ).to_json() == verified_result_bytes
        assert type(result).from_dict(
            result.to_dict()
        ).to_json() == verified_result_bytes
        projection_bytes = result.visualization_data.to_json()
        assert type(result.visualization_data).from_json(
            projection_bytes
        ).to_json() == projection_bytes
        visualizations = Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizer(
            data=result.visualization_data,
            verification=result.verification,
            dpi=72,
        ).visualize()

        assert {value.plot for value in visualizations} == set(
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot
        )
        assert all(
            value.png.startswith(b"\x89PNG\r\n\x1a\n")
            for value in visualizations
        )

    def test_verifier_does_not_call_production_family_or_member_analyzers(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        subject = _subject_bytes()

        def prohibited_member(
            analyzer: Periodic1DEmbeddedSubspaceRank2Analyzer,
        ) -> Periodic1DEmbeddedSubspaceRank2Analysis:
            raise AssertionError(f"production member analyzer called: {analyzer!r}")

        def prohibited_family(
            analyzer: Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer,
        ) -> Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis:
            raise AssertionError(f"production family analyzer called: {analyzer!r}")

        monkeypatch.setattr(
            Periodic1DEmbeddedSubspaceRank2Analyzer,
            "execute",
            prohibited_member,
        )
        def prohibited_member_materialization(
            request: Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
            scale: float,
        ) -> Periodic1DEmbeddedSubspaceRank2Request:
            raise AssertionError(
                f"production member materialization called: {request!r}, {scale}"
            )

        def prohibited_coordinates(
            request: Periodic1DEmbeddedSubspaceRank2Request,
        ) -> tuple[float, ...]:
            raise AssertionError(f"production mesh construction called: {request!r}")

        monkeypatch.setattr(
            Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer,
            "execute",
            prohibited_family,
        )
        monkeypatch.setattr(
            Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
            "request_at",
            prohibited_member_materialization,
        )
        monkeypatch.setattr(
            Periodic1DEmbeddedSubspaceRank2Request,
            "construction_reduced_momenta",
            prohibited_coordinates,
        )

        assert Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
            subject
        ).result().passed

    def test_member_tampering_fails_and_noncanonical_bytes_are_rejected(self) -> None:
        subject = _subject_bytes()
        record = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord.from_json(
            subject
        )
        member = record.analysis.members[1]
        point = replace(
            member.points[1],
            minimum_operator_threshold=(
                member.points[1].minimum_operator_threshold + 1.0e-6
            ),
        )
        tampered_member = replace(
            member,
            points=(member.points[0], point, member.points[2]),
        )
        tampered_analysis = replace(
            record.analysis,
            members=(
                record.analysis.members[0],
                tampered_member,
                record.analysis.members[2],
            ),
        )
        tampered_subject = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecorder(
                tampered_analysis
            ).result().to_json()
        )

        verification = Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
            tampered_subject
        ).result()
        assert not verification.passed
        assert not verification.components[0].observations[
            "member_1_point_scalar_maximum_absolute_defect"
        ].passed

        noncanonical = json.dumps(json.loads(subject), indent=2).encode("utf-8")
        with pytest.raises(ValueError, match="canonical"):
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
                noncanonical
            ).result()

    def test_family_admission_rejects_joint_tolerance_and_value_tampering(
        self,
    ) -> None:
        record = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord.from_json(
            _subject_bytes()
        )
        mapping = dict(record.to_dict())
        request_value = mapping["request"]
        assert isinstance(request_value, Mapping)
        request = dict(request_value)
        template_value = request["template_request"]
        assert isinstance(template_value, Mapping)
        template = dict(template_value)
        template["verification_absolute_tolerance"] = 1.0
        request["template_request"] = template
        mapping["request"] = request
        members_value = mapping["members"]
        assert isinstance(members_value, tuple)
        members = list(members_value)
        assert isinstance(members[1], Mapping)
        member = dict(members[1])
        points_value = member["points"]
        assert isinstance(points_value, tuple)
        points = list(points_value)
        assert isinstance(points[1], Mapping)
        point = dict(points[1])
        point["minimum_operator_threshold"] = 0.5
        points[1] = point
        member["points"] = tuple(points)
        members[1] = member
        mapping["members"] = tuple(members)

        with pytest.raises(ValueError, match="installed policy"):
            Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord.from_dict(
                mapping
            )

    def test_request_rejects_boolean_scales_and_incomplete_endpoints(self) -> None:
        with pytest.raises(TypeError, match="built-in floats"):
            Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
                template_request=_template(),
                parent_hopping_scales=(0.0, True, 1.0),
            )
        with pytest.raises(ValueError, match="end at one"):
            Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
                template_request=_template(),
                parent_hopping_scales=(0.0, 0.5),
            )
