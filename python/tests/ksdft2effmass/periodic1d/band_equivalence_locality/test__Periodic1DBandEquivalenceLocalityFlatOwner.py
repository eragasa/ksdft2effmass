"""Tests for the installed flat-parent band-equivalence locality owner."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest
from projectkoios.optimization.selection.harmonic import PeriodicHarmonicMaximizer

import ksdft2effmass.periodic1d.band_equivalence_locality as band_equivalence_locality
from ksdft2effmass.periodic1d.band_equivalence_locality.analysis import (
    Periodic1DBandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.records import (
    Periodic1DBandEquivalenceLocalityAnalysisRecord,
    Periodic1DBandEquivalenceLocalityAnalysisRecorder,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.reference import (
    Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.request import (
    Periodic1DBandEquivalenceLocalityRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.verification import (
    Periodic1DBandEquivalenceLocalityVerification,
    Periodic1DBandEquivalenceLocalityVerifier,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.visualizations.data import (
    Periodic1DBandEquivalenceLocalityVisualizationData,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.visualizations.inventory import (  # noqa: E501
    Periodic1DBandEquivalenceLocalityVisualizationPlotEnum,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.visualizations.visualizer import (  # noqa: E501
    Periodic1DBandEquivalenceLocalityVisualizer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


def _request() -> Periodic1DBandEquivalenceLocalityRequest:
    return Periodic1DBandEquivalenceLocalityRequest(
        parent_model_identifier="flat-two-level-parent.v1",
        represented_basis_identifier="fixed-real-rank-two-basis.v1",
        energy_reference_identifier="positive-reference-energy-E_ref.v1",
        reciprocal_coordinate_convention="centered-half-open-reduced-coordinate.v1",
        gauge_attack_identifier="real-sinusoidal-rotation.v1",
        construction_size=16,
        evaluation_size=33,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=3,
        amplitudes=(0.0, 0.4, 0.7853981633974483),
        maximum_ranges=(0, 1, 3),
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-12,
        numerical_absolute_tolerance=1.0e-12,
    )


def _analysis_bytes() -> bytes:
    request = _request()
    analysis = Periodic1DBandEquivalenceLocalityAnalyzer(
        request=request,
        harmonic_maximizer=PeriodicHarmonicMaximizer(
            absolute_degeneracy_tolerance=(
                request.harmonic_absolute_degeneracy_tolerance
            ),
            relative_degeneracy_tolerance=(
                request.harmonic_relative_degeneracy_tolerance
            ),
        ),
    ).execute()
    return (
        Periodic1DBandEquivalenceLocalityAnalysisRecorder(analysis).result().to_json()
    )


class TestPeriodic1DBandEquivalenceLocalityFlatOwner:
    """Establish one cohesive native flat-parent lifecycle slice."""

    def test__package__is_a_non_eager_namespace(self) -> None:
        assert not hasattr(band_equivalence_locality, "__all__")
        assert not any(
            name.startswith("Periodic1D") for name in vars(band_equivalence_locality)
        )

    def test_request_rejects_boolean_mesh_size(self) -> None:
        values = _request()
        with pytest.raises(TypeError, match="construction_size"):
            Periodic1DBandEquivalenceLocalityRequest(
                parent_model_identifier=values.parent_model_identifier,
                represented_basis_identifier=values.represented_basis_identifier,
                energy_reference_identifier=values.energy_reference_identifier,
                reciprocal_coordinate_convention=(
                    values.reciprocal_coordinate_convention
                ),
                gauge_attack_identifier=values.gauge_attack_identifier,
                construction_size=True,
                evaluation_size=values.evaluation_size,
                evaluation_shift_numerator=values.evaluation_shift_numerator,
                evaluation_shift_denominator=values.evaluation_shift_denominator,
                amplitudes=values.amplitudes,
                maximum_ranges=values.maximum_ranges,
                harmonic_absolute_degeneracy_tolerance=(
                    values.harmonic_absolute_degeneracy_tolerance
                ),
                harmonic_relative_degeneracy_tolerance=(
                    values.harmonic_relative_degeneracy_tolerance
                ),
                numerical_absolute_tolerance=values.numerical_absolute_tolerance,
            )

    def test_request_rejects_a_mislabeled_parent_identity(self) -> None:
        values = _request()
        with pytest.raises(ValueError, match="parent_model_identifier"):
            replace(values, parent_model_identifier="different-parent.v1")

    def test_analysis_preserves_separate_finite_channels(self) -> None:
        record = Periodic1DBandEquivalenceLocalityAnalysisRecord.from_json(
            _analysis_bytes()
        )
        zero, moderate, maximum = record.analysis.points
        assert zero.maximum_band_defect == 0.0
        assert zero.discrete_maximum_correlation == 1.0
        assert zero.minimum_operator_threshold == 0.0
        assert moderate.discrete_maximum_correlation == pytest.approx(
            0.8462873527504802, abs=1.0e-15
        )
        assert maximum.discrete_maximum_correlation == pytest.approx(
            0.4720012157682367, abs=1.0e-15
        )
        assert maximum.correlation_quadrature_defect < 2.0e-15
        assert maximum.cyclic_nyquist_power > 0.0
        assert maximum.interpolation_hamiltonian_maximum_error > 0.0
        assert maximum.ranges[0].total_hamiltonian_maximum_error > 1.0
        assert maximum.ranges[-1].total_hamiltonian_maximum_error < 0.03
        assert maximum.ranges[-1].total_spectral_maximum_error < 0.03

    def test_record_round_trip_preserves_exact_canonical_bytes(self) -> None:
        payload = _analysis_bytes()
        admitted = Periodic1DBandEquivalenceLocalityAnalysisRecord.from_json(payload)
        assert admitted.to_json() == payload

    def test_independent_reference_agrees_without_production_transform_owner(
        self,
    ) -> None:
        observed = Periodic1DBandEquivalenceLocalityAnalysisRecord.from_json(
            _analysis_bytes()
        ).analysis
        reference = Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer(
            observed.request
        ).execute()
        assert (
            max(
                abs(
                    candidate.discrete_maximum_correlation
                    - expected.discrete_maximum_correlation
                )
                for candidate, expected in zip(
                    observed.points, reference.points, strict=True
                )
            )
            < 1.0e-15
        )
        assert (
            max(
                abs(
                    candidate.ranges[-1].total_hamiltonian_maximum_error
                    - expected.ranges[-1].total_hamiltonian_maximum_error
                )
                for candidate, expected in zip(
                    observed.points, reference.points, strict=True
                )
            )
            < 1.0e-12
        )

    def test_verifier_authenticates_bytes_and_all_independent_channels(self) -> None:
        payload = _analysis_bytes()
        result = Periodic1DBandEquivalenceLocalityVerifier(payload).result()
        verification = result.verification
        verified_result_bytes = result.to_json()
        assert (
            type(result).from_json(verified_result_bytes).to_json()
            == verified_result_bytes
        )
        assert (
            type(result).from_dict(result.to_dict()).to_json() == verified_result_bytes
        )
        assert verification.passed
        assert (
            Periodic1DBandEquivalenceLocalityVerification.from_json(
                verification.to_json()
            ).to_json()
            == verification.to_json()
        )
        assert result.visualization_data.source_sha256 == verification.subject_sha256
        assert set(verification.components[0].observations) == {
            "point_scalar_maximum_absolute_defect",
            "hopping_inventory_defect",
            "hopping_power_maximum_absolute_defect",
            "range_inventory_defect",
            "range_value_maximum_absolute_defect",
        }
        assert set(verification.components[1].observations) == {
            "visualization_scalar_maximum_absolute_defect",
            "visualization_inventory_defect",
            "visualization_matrix_maximum_absolute_defect",
        }
        projection_bytes = result.visualization_data.to_json()
        assert (
            Periodic1DBandEquivalenceLocalityVisualizationData.from_json(
                projection_bytes
            ).to_json()
            == projection_bytes
        )

    def test_visualizer_requires_the_authenticated_projection_and_renders_inventory(
        self,
    ) -> None:
        result = Periodic1DBandEquivalenceLocalityVerifier(_analysis_bytes()).result()
        images = Periodic1DBandEquivalenceLocalityVisualizer(
            data=result.visualization_data,
            verification=result.verification,
            dpi=72,
        ).visualize()
        assert {image.plot for image in images} == set(
            Periodic1DBandEquivalenceLocalityVisualizationPlotEnum
        )
        assert all(image.png.startswith(b"\x89PNG\r\n\x1a\n") for image in images)

    def test_verifier_reports_failure_for_canonical_scientific_tampering(self) -> None:
        admitted = Periodic1DBandEquivalenceLocalityAnalysisRecord.from_json(
            _analysis_bytes()
        ).analysis
        first = replace(
            admitted.points[0],
            maximum_band_defect=admitted.points[0].maximum_band_defect + 1.0e-6,
        )
        modified = replace(admitted, points=(first, *admitted.points[1:]))
        modified_bytes = (
            Periodic1DBandEquivalenceLocalityAnalysisRecorder(modified)
            .result()
            .to_json()
        )
        verification = (
            Periodic1DBandEquivalenceLocalityVerifier(modified_bytes)
            .result()
            .verification
        )
        assert not verification.passed
        assert (
            not verification.components[0]
            .observations["point_scalar_maximum_absolute_defect"]
            .passed
        )

    def test_verifier_rejects_semantically_equivalent_noncanonical_bytes(self) -> None:
        payload = _analysis_bytes()
        decoded = json.loads(payload)
        noncanonical = json.dumps(decoded, indent=2).encode("utf-8")
        with pytest.raises(ValueError, match="canonical"):
            Periodic1DBandEquivalenceLocalityVerifier(noncanonical).result()
