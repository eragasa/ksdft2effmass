"""Tests for embedded rank-two adaptive amplitude refinement."""

from __future__ import annotations

import importlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DRank2AdaptiveAmplitudeRequest,
    Periodic1DRank2AmplitudeRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.verification import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeIndependentVerifier,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


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


def _thresholds(
    value: float = 1.0,
) -> Periodic1DRank2AmplitudeRefinementThresholds:
    return Periodic1DRank2AmplitudeRefinementThresholds(
        maximum_correlation_defect=value,
        maximum_operator_threshold_defect=value,
        maximum_joint_threshold_defect=value,
        maximum_hopping_weight_defect=value,
        maximum_hopping_power_defect=value,
    )


def _request(
    *,
    template: Periodic1DRank2Request | None = None,
    threshold: float = 1.0,
    maximum_refinement_levels: int = 2,
    maximum_evaluated_amplitudes: int = 20,
) -> Periodic1DRank2AdaptiveAmplitudeRequest:
    return Periodic1DRank2AdaptiveAmplitudeRequest(
        template_request=_template() if template is None else template,
        thresholds=_thresholds(threshold),
        maximum_refinement_levels=maximum_refinement_levels,
        maximum_evaluated_amplitudes=maximum_evaluated_amplitudes,
    )


def _analyze(
    request: Periodic1DRank2AdaptiveAmplitudeRequest,
) -> Periodic1DRank2AdaptiveAmplitudeAnalysis:
    return Periodic1DRank2AdaptiveAmplitudeAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


class TestPeriodic1DRank2AdaptiveAmplitude:
    """Establish direct sampling, closed stops, and policy separation."""

    def test_evaluation_request_changes_only_amplitudes_and_rejects_booleans(
        self,
    ) -> None:
        request = _request()
        inventory = (0.0, 0.1, 0.2, math.pi / 4.0)
        evaluation = request.evaluation_request(inventory)
        assert evaluation.amplitudes == inventory
        assert replace(evaluation, amplitudes=request.template_request.amplitudes) == (
            request.template_request
        )
        with pytest.raises(TypeError, match="built-in int"):
            replace(request, maximum_refinement_levels=True)
        with pytest.raises(TypeError, match="built-in float"):
            replace(
                request,
                thresholds=replace(
                    request.thresholds,
                    maximum_correlation_defect=True,
                ),
            )

    def test_generous_thresholds_require_midpoints_and_disjoint_validation(
        self,
    ) -> None:
        result = _analyze(_request())
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeConverged)
        assert result.converged
        assert len(result.levels) == 1
        assert len(result.validations) == 1
        level = result.levels[0]
        validation = result.validations[0]
        assert level.within_tolerances
        assert validation.within_tolerances
        assert not set(validation.evaluated_amplitudes) & set(
            validation.interpolation_nodes
        )
        assert tuple(point.amplitude for point in result.all_evaluated_points) == (
            0.0,
            0.05,
            0.1,
            0.15000000000000002,
            0.2,
            0.3463495408493621,
            0.4926990816987241,
            0.6390486225480863,
            math.pi / 4.0,
        )

    def test_strict_thresholds_reach_the_level_cap_as_unresolved(self) -> None:
        result = _analyze(_request(threshold=1.0e-16, maximum_refinement_levels=1))
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted)
        assert not result.converged
        assert len(result.levels) == 1
        assert not result.levels[0].within_tolerances

    def test_sample_cap_has_its_own_closed_stop_variant(self) -> None:
        result = _analyze(
            _request(
                threshold=1.0e-16,
                maximum_refinement_levels=3,
                maximum_evaluated_amplitudes=5,
            )
        )
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted)
        assert not result.converged
        assert len(result.all_evaluated_points) == 5
        assert (
            len(
                set(result.blocked_amplitudes)
                - {point.amplitude for point in result.all_evaluated_points}
            )
            > 0
        )

    def test_parent_qualification_stops_before_interpolation_comparison(self) -> None:
        template = replace(_template(), minimum_external_gap=2.0)
        result = _analyze(_request(template=template))
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeQualificationStopped)
        assert not result.converged
        assert len(result.evaluations) == 1
        assert not result.evaluations[0].qualification.qualified
        assert not hasattr(result, "levels")

    def test_threshold_classification_does_not_use_verification_policy(self) -> None:
        request = _request(threshold=0.05, maximum_refinement_levels=1)
        assert not hasattr(request, "verification_absolute_tolerance")
        result = _analyze(request)
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted)
        level = result.levels[0]
        assert level.maximum_correlation_defect > 0.05
        assert not level.within_tolerances

    def test_production_reuses_one_qualified_parent_preparation(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        root = (
            "ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2"
        )
        production_parent = importlib.import_module(
            f"{root}.parent_scale.parent_hamiltonian"
        )
        constructor = production_parent._Periodic1DRank2ParentConstructor
        original = constructor.execute
        call_count = 0

        def counted(self: object) -> object:
            nonlocal call_count
            call_count += 1
            return original(self)

        monkeypatch.setattr(constructor, "execute", counted)
        result = _analyze(_request())
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeConverged)
        assert len(result.evaluations) == 2
        assert call_count == 1

    def test_independent_direct_reconstruction_passes(self) -> None:
        result = _analyze(_request())
        verification = Periodic1DRank2AdaptiveAmplitudeIndependentVerifier(
            result
        ).result()
        assert verification.passed
        assert verification.observations

    def test_independent_reconstruction_does_not_call_production_factories(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        root = (
            "ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2"
        )
        production_analysis = importlib.import_module(f"{root}.parent_scale.analysis")
        production_adaptive = importlib.import_module(
            f"{root}.amplitude_refinement.analysis"
        )
        result = _analyze(_request())

        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("independent reconstruction called production")

        monkeypatch.setattr(
            production_analysis.Periodic1DRank2Analyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            production_adaptive.Periodic1DRank2AdaptiveAmplitudeAnalyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            production_adaptive.Periodic1DRank2AdaptiveAmplitudeRequest,
            "evaluation_request",
            forbidden,
        )
        verification = Periodic1DRank2AdaptiveAmplitudeIndependentVerifier(
            result
        ).result()
        assert verification.passed

    def test_independent_reconstruction_detects_tampered_level_metric(self) -> None:
        result = _analyze(_request())
        assert type(result) is (Periodic1DRank2AdaptiveAmplitudeConverged)
        tampered_level = replace(
            result.levels[0],
            maximum_correlation_defect=(
                result.levels[0].maximum_correlation_defect + 1.0e-5
            ),
        )
        tampered = replace(result, levels=(tampered_level,))
        verification = Periodic1DRank2AdaptiveAmplitudeIndependentVerifier(
            tampered
        ).result()
        assert not verification.passed
        assert not verification.observations[
            "level_0_maximum_correlation_defect_absolute_defect"
        ].passed
