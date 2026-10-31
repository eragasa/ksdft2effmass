"""Tests for embedded rank-two ordinary-lattice truncation."""

from __future__ import annotations

import importlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2Request,
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationAnalyzer,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationIndependentVerifier,
    Periodic1DRank2TruncationQualificationStopped,
    Periodic1DRank2TruncationRequest,
    Periodic1DRank2TruncationToleranceSelector,
)


def _template() -> Periodic1DRank2Request:
    return Periodic1DRank2Request(
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


def _request(
    template: Periodic1DRank2Request | None = None,
) -> Periodic1DRank2TruncationRequest:
    return Periodic1DRank2TruncationRequest.every_integer_through(
        template_request=_template() if template is None else template,
        maximum_range=3,
        evaluation_mesh_size=17,
    )


def _analyze(
    request: Periodic1DRank2TruncationRequest,
) -> Periodic1DRank2TruncationAnalysis:
    return Periodic1DRank2TruncationAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


class TestPeriodic1DRank2Truncation:
    """Establish conversion, consequence, stop, and independent-check behavior."""

    def test_request_requires_ordinary_cutoffs_and_rejects_booleans(self) -> None:
        request = _request()
        assert request.maximum_ranges == (0, 1, 2, 3)
        assert request.has_dense_integer_inventory
        with pytest.raises(TypeError, match="built-in int"):
            Periodic1DRank2TruncationRequest.every_integer_through(
                template_request=_template(),
                maximum_range=True,
                evaluation_mesh_size=17,
            )
        with pytest.raises(TypeError, match="built-in int"):
            replace(request, evaluation_mesh_size=True)
        with pytest.raises(TypeError, match="built-in ints"):
            replace(request, maximum_ranges=(0, True))
        with pytest.raises(ValueError, match="exclude the cyclic Nyquist"):
            replace(request, maximum_ranges=(0, 4))
        with pytest.raises(ValueError, match=r"at least 2\*N\+1"):
            replace(request, evaluation_mesh_size=16)

    def test_completed_result_separates_conversion_and_ordinary_power(self) -> None:
        result = _analyze(_request())
        assert type(result) is Periodic1DRank2TruncationCompleted
        assert result.completed
        assert result.minimum_construction_evaluation_separation > 0.0
        assert tuple(point.amplitude for point in result.points) == (
            0.0,
            0.2,
            math.pi / 4.0,
        )
        for point in result.points:
            assert tuple(item.maximum_range for item in point.ranges) == (0, 1, 2, 3)
            full = point.ranges[-1]
            assert full.support_policy.maximum_range == 3
            assert tuple(
                displacement.components
                for displacement in full.support_policy.support.displacements
            ) == ((-3,), (-2,), (-1,), (0,), (1,), (2,), (3,))
            assert full.reference_ordinary_omitted_power == 0.0
            assert full.comparison_ordinary_omitted_power == 0.0
            assert full.reference_total_omitted_power == pytest.approx(
                point.reference_nyquist_power, rel=0.0, abs=1.0e-20
            )
            assert full.comparison_total_omitted_power == pytest.approx(
                point.comparison_nyquist_power, rel=0.0, abs=1.0e-20
            )

    def test_zero_attack_has_no_interpolation_or_total_full_range_error(self) -> None:
        result = _analyze(_request())
        assert type(result) is Periodic1DRank2TruncationCompleted
        point = result.points[0]
        assert point.amplitude == 0.0
        assert point.comparison_interpolation_hamiltonian_maximum_error == 0.0
        assert point.comparison_interpolation_spectral_maximum_error == 0.0
        assert point.ranges[-1].comparison_total_hamiltonian_maximum_error == 0.0
        assert point.ranges[-1].comparison_total_spectral_maximum_error == 0.0

    def test_hamiltonian_and_spectral_maxima_are_independent_channels(self) -> None:
        result = _analyze(_request())
        assert type(result) is Periodic1DRank2TruncationCompleted
        final = result.points[-1]
        first_range = final.ranges[0]
        assert (
            first_range.comparison_truncation_hamiltonian_maximum_error
            != first_range.comparison_truncation_spectral_maximum_error
        )
        assert (
            final.comparison_interpolation_hamiltonian_maximum_error
            != final.comparison_interpolation_spectral_maximum_error
        )

    def test_tolerance_selector_adapts_symmetric_range_errors(self) -> None:
        result = _analyze(_request())
        assert type(result) is Periodic1DRank2TruncationCompleted
        point = result.points[-1]

        selection = Periodic1DRank2TruncationToleranceSelector(
            point=point,
            tolerance=1.0,
        ).execute()

        assert tuple(
            comparison.support for comparison in selection.request.comparisons
        ) == tuple(item.support_policy.support for item in point.ranges)
        assert (
            selection.request.comparisons[
                1
            ].reference_model_errors.matrix_frobenius.maximum_error
            == point.ranges[1].reference_truncation_hamiltonian_maximum_error
        )
        assert (
            selection.request.comparisons[
                1
            ].comparison_model_errors.ordered_eigenvalues.maximum_absolute_error
            == point.ranges[1].comparison_total_spectral_maximum_error
        )

    def test_parent_qualification_stops_before_truncation(self) -> None:
        template = replace(_template(), minimum_external_gap=2.0)
        result = _analyze(_request(template))
        assert type(result) is (Periodic1DRank2TruncationQualificationStopped)
        assert not result.completed
        assert type(result.qualification) is (Periodic1DRank2ExternalGapFailure)
        assert not hasattr(result, "points")
        verification = Periodic1DRank2TruncationIndependentVerifier(result).result()
        assert verification.passed

    def test_independent_direct_reconstruction_passes_and_detects_tampering(
        self,
    ) -> None:
        result = _analyze(_request())
        assert type(result) is Periodic1DRank2TruncationCompleted
        verification = Periodic1DRank2TruncationIndependentVerifier(result).result()
        assert verification.passed
        first_point = result.points[0]
        first_range = first_point.ranges[0]
        tampered_range = replace(
            first_range,
            comparison_total_spectral_maximum_error=(
                first_range.comparison_total_spectral_maximum_error + 1.0e-4
            ),
        )
        tampered = replace(
            result,
            points=(
                replace(
                    first_point,
                    ranges=(tampered_range, *first_point.ranges[1:]),
                ),
                *result.points[1:],
            ),
        )
        assert not (
            Periodic1DRank2TruncationIndependentVerifier(tampered).result().passed
        )

    def test_independent_reference_does_not_call_production_scientific_owners(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        result = _analyze(_request())
        root = (
            "ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2"
        )
        production_parent = importlib.import_module(
            f"{root}.parent_scale.parent_hamiltonian"
        )
        production_analysis = importlib.import_module(f"{root}.parent_scale.analysis")
        production_truncation = importlib.import_module(f"{root}.truncation.analysis")
        solidstate = importlib.import_module("ksdft2effmass.solidstate")

        def forbidden(*args: object, **kwargs: object) -> None:
            raise AssertionError("production owner was called")

        monkeypatch.setattr(
            production_parent._Periodic1DRank2ParentConstructor,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            production_analysis.Periodic1DRank2Analyzer,
            "_prepare",
            forbidden,
        )
        monkeypatch.setattr(
            production_truncation.Periodic1DRank2TruncationAnalyzer,
            "execute",
            forbidden,
        )
        for name in (
            "ReciprocalOperatorFourierTransformer1D",
            "CenteredEvenMeshCyclicToOrdinaryConverter1D",
            "BlockHoppingInterpolator1D",
            "BlockHoppingTruncator1D",
        ):
            monkeypatch.setattr(getattr(solidstate, name), "execute", forbidden)
        assert Periodic1DRank2TruncationIndependentVerifier(result).result().passed
