"""Tests for independent embedded-subspace rank-two byte verification."""

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
    Periodic1DRank2Analysis,
    Periodic1DRank2AnalysisRecord,
    Periodic1DRank2AnalysisRecorder,
    Periodic1DRank2Analyzer,
    Periodic1DRank2Request,
    Periodic1DRank2Verification,
    Periodic1DRank2Verifier,
    Periodic1DRank2VisualizationPlot,
    Periodic1DRank2Visualizer,
)


def _request() -> Periodic1DRank2Request:
    return Periodic1DRank2Request(
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
    request: Periodic1DRank2Request,
) -> Periodic1DRank2Analysis:
    return Periodic1DRank2Analyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


def _analysis_bytes(
    request: Periodic1DRank2Request | None = None,
) -> bytes:
    analysis = _analyze(request or _request())
    return Periodic1DRank2AnalysisRecorder(analysis).result().to_json()


class TestPeriodic1DRank2Verifier:
    """Establish canonical admission, independence, and tamper detection."""

    def test_canonical_qualified_subject_passes_independent_verification(self) -> None:
        subject = _analysis_bytes()
        verification = Periodic1DRank2Verifier(subject).result()

        assert verification.passed
        assert verification.subject_sha256 == hashlib.sha256(subject).hexdigest()
        assert set(verification.checks) == {
            "qualification_variant_defect",
            "minimum_external_gap_absolute_defect",
            "qualification_scalar_maximum_absolute_defect",
            "closure_phase_maximum_absolute_defect",
            "point_inventory_defect",
            "point_scalar_maximum_absolute_defect",
            "harmonic_scalar_maximum_absolute_defect",
            "harmonic_argument_maximum_absolute_defect",
            "harmonic_identity_defect",
            "hopping_inventory_defect",
            "hopping_power_maximum_absolute_defect",
            "visualization_vector_maximum_absolute_defect",
            "visualization_matrix_maximum_absolute_defect",
            "visualization_inventory_defect",
        }
        retained = verification.to_json()
        assert Periodic1DRank2Verification.from_json(retained).to_json() == retained

    def test_zero_amplitude_identity_passes_for_dispersive_family_members(
        self,
    ) -> None:
        for parent_hopping_scale in (0.5, 0.75):
            request = replace(
                _request(),
                reciprocal_mesh_size=256,
                amplitudes=(0.0, 0.2),
                parent_hopping_scale=parent_hopping_scale,
            )
            subject = _analysis_bytes(request)
            analysis = Periodic1DRank2AnalysisRecord.from_json(subject).analysis
            verification = Periodic1DRank2Verifier(subject).result()

            assert analysis.points[0].discrete_maximum_correlation == 1.0
            assert analysis.points[0].minimum_operator_threshold == 0.0
            assert analysis.points[0].exact_spectrum_joint_operator_threshold == 0.0
            assert verification.passed

    def test_authenticated_projection_renders_the_closed_inventory(self) -> None:
        result = Periodic1DRank2Verifier(_analysis_bytes()).result_with_visualization()

        verified_result_bytes = result.to_json()
        assert (
            type(result).from_json(verified_result_bytes).to_json()
            == verified_result_bytes
        )
        assert (
            type(result).from_dict(result.to_dict()).to_json() == verified_result_bytes
        )
        projection_bytes = result.visualization_data.to_json()
        assert (
            type(result.visualization_data).from_json(projection_bytes).to_json()
            == projection_bytes
        )
        visualizations = Periodic1DRank2Visualizer(
            data=result.visualization_data,
            verification=result.verification,
            dpi=72,
        ).visualize()

        assert {value.plot for value in visualizations} == set(
            Periodic1DRank2VisualizationPlot
        )
        assert all(
            value.png.startswith(b"\x89PNG\r\n\x1a\n") for value in visualizations
        )

    def test_visualizer_rejects_a_tampered_projection(self) -> None:
        result = Periodic1DRank2Verifier(_analysis_bytes()).result_with_visualization()
        tampered = replace(
            result.visualization_data,
            correlations=(
                result.visualization_data.correlations[0] - 1.0e-6,
                *result.visualization_data.correlations[1:],
            ),
        )

        with pytest.raises(ValueError, match="different visualization data"):
            Periodic1DRank2Visualizer(
                data=tampered,
                verification=result.verification,
            )

    def test_verifier_does_not_call_the_production_analyzer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        subject = _analysis_bytes()

        def prohibited_execute(
            analyzer: Periodic1DRank2Analyzer,
        ) -> Periodic1DRank2Analysis:
            raise AssertionError(f"production analyzer called: {analyzer!r}")

        def prohibited_coordinates(
            request: Periodic1DRank2Request,
        ) -> tuple[float, ...]:
            raise AssertionError(f"production mesh construction called: {request!r}")

        monkeypatch.setattr(
            Periodic1DRank2Analyzer,
            "execute",
            prohibited_execute,
        )
        monkeypatch.setattr(
            Periodic1DRank2Request,
            "construction_reduced_momenta",
            prohibited_coordinates,
        )
        assert Periodic1DRank2Verifier(subject).result().passed

    def test_verifier_passes_explicit_gap_and_transport_threshold_stops(self) -> None:
        gap_subject = _analysis_bytes(replace(_request(), minimum_external_gap=2.0))
        threshold_subject = _analysis_bytes(
            replace(_request(), minimum_transport_singular_value=1.0)
        )

        assert Periodic1DRank2Verifier(gap_subject).result().passed
        assert Periodic1DRank2Verifier(threshold_subject).result().passed

    def test_canonical_scientific_tampering_fails_the_reference_comparison(
        self,
    ) -> None:
        analysis = Periodic1DRank2AnalysisRecord.from_json(_analysis_bytes()).analysis
        first = replace(
            analysis.points[0],
            minimum_operator_threshold=(
                analysis.points[0].minimum_operator_threshold + 1.0e-6
            ),
        )
        tampered = replace(analysis, points=(first, *analysis.points[1:]))
        subject = Periodic1DRank2AnalysisRecorder(tampered).result().to_json()

        verification = Periodic1DRank2Verifier(subject).result()
        assert not verification.passed
        assert (
            not verification.components[0]
            .observations["point_scalar_maximum_absolute_defect"]
            .passed
        )

    def test_fixed_verification_policy_rejects_joint_tolerance_and_value_tampering(
        self,
    ) -> None:
        record = Periodic1DRank2AnalysisRecord.from_json(_analysis_bytes())
        mapping = dict(record.to_dict())
        request_value = mapping["request"]
        assert isinstance(request_value, Mapping)
        request = dict(request_value)
        request["verification_absolute_tolerance"] = 1.0
        mapping["request"] = request
        points_value = mapping["points"]
        assert isinstance(points_value, tuple)
        points = list(points_value)
        assert isinstance(points[0], Mapping)
        first = dict(points[0])
        first["minimum_operator_threshold"] = 0.5
        points[0] = first
        mapping["points"] = tuple(points)

        with pytest.raises(ValueError, match="installed policy"):
            Periodic1DRank2AnalysisRecord.from_dict(mapping)

    def test_verifier_rejects_noncanonical_and_tampered_typed_transport_bytes(
        self,
    ) -> None:
        subject = _analysis_bytes()
        decoded = json.loads(subject)
        noncanonical = json.dumps(decoded, indent=2).encode("utf-8")
        with pytest.raises(ValueError, match="canonical"):
            Periodic1DRank2Verifier(noncanonical).result()

        threshold_subject = _analysis_bytes(
            replace(_request(), minimum_transport_singular_value=1.0)
        )
        threshold_mapping = dict(
            Periodic1DRank2AnalysisRecord.from_json(threshold_subject).to_dict()
        )
        qualification = threshold_mapping["qualification"]
        assert isinstance(qualification, Mapping)
        tampered_qualification = dict(qualification)
        tampered_qualification["variant"] = "band-transport-numerically-unresolved"
        tampered_qualification["band_transport_status"] = "not-a-transport-status"
        threshold_mapping["qualification"] = tampered_qualification
        with pytest.raises(ValueError, match="typed band-transport status"):
            Periodic1DRank2AnalysisRecord.from_dict(threshold_mapping)
