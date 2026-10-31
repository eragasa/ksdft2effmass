"""Tests for embedded rank-two nested momentum refinement."""

from __future__ import annotations

import importlib
import math
from dataclasses import replace

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved,
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


def _thresholds(
    value: float = 1.0,
) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds:
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds(
        maximum_parent_diagnostic_change=value,
        maximum_correlation_change=value,
        maximum_threshold_change=value,
        maximum_hopping_weight_change=value,
        maximum_hopping_power_change=value,
        maximum_angle_change=value,
        maximum_band_defect=value,
        maximum_reconstruction_defect=value,
        maximum_parseval_defect=value,
    )


def _request(
    *,
    template: Periodic1DEmbeddedSubspaceRank2Request | None = None,
    thresholds: (
        Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds | None
    ) = None,
) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest:
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest(
        template_request=_template() if template is None else template,
        reciprocal_mesh_sizes=(8, 16),
        thresholds=_thresholds() if thresholds is None else thresholds,
        required_stable_refinements=1,
    )


def _analyze(
    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
):
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer(
        request=request,
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()


class TestPeriodic1DEmbeddedSubspaceRank2MomentumRefinement:
    """Establish nested inventory, outcomes, and independent reconstruction."""

    def test_nested_doubling_request_changes_only_the_mesh(self) -> None:
        request = _request()
        fine = request.request_at(16)
        assert fine.reciprocal_mesh_size == 16
        assert replace(fine, reciprocal_mesh_size=8) == request.template_request
        with pytest.raises(ValueError, match="nested doubling"):
            replace(request, reciprocal_mesh_sizes=(8, 24))
        with pytest.raises(TypeError, match="built-in int"):
            replace(request, required_stable_refinements=True)

    def test_generous_thresholds_produce_a_closed_converged_outcome(self) -> None:
        result = _analyze(_request())
        assert type(result) is (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged
        )
        assert result.converged
        assert tuple(
            item.request.reciprocal_mesh_size for item in result.mesh_analyses
        ) == (8, 16)
        assert len(result.refinements) == 1
        refinement = result.refinements[0]
        assert refinement.maximum_shared_parent_eigenvalue_defect < 1.0e-14
        assert refinement.maximum_shared_parent_projector_defect < 1.0e-14
        assert refinement.maximizing_angle_dispositions_stable
        assert refinement.within_tolerances

    def test_strict_stability_threshold_produces_unresolved_not_failure(self) -> None:
        thresholds = replace(
            _thresholds(),
            maximum_parent_diagnostic_change=1.0e-12,
        )
        result = _analyze(_request(thresholds=thresholds))
        assert type(result) is (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved
        )
        assert not result.converged
        assert not result.refinements[0].within_tolerances

    def test_unqualified_mesh_stops_before_refinement_comparison(self) -> None:
        template = replace(_template(), minimum_external_gap=2.0)
        result = _analyze(_request(template=template))
        assert type(result) is (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped
        )
        assert not result.converged
        assert len(result.mesh_analyses) == 2
        assert result.refinements == ()

    def test_independent_comparison_passes_without_a_new_wire_format(self) -> None:
        result = _analyze(_request())
        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier(
                result
            ).result()
        )
        assert verification.passed
        assert verification.observations

    def test_independent_comparison_does_not_call_production_factories(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        module_root = (
            "ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2"
        )
        production_analysis = importlib.import_module(f"{module_root}.analysis")
        production_parent = importlib.import_module(f"{module_root}.parent")
        production_refinement = importlib.import_module(f"{module_root}.refinement")

        result = _analyze(_request())

        def forbidden(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("independent comparison called a production factory")

        monkeypatch.setattr(
            production_analysis.Periodic1DEmbeddedSubspaceRank2Analyzer,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            production_parent._Periodic1DEmbeddedSubspaceRank2ParentConstructor,
            "execute",
            forbidden,
        )
        monkeypatch.setattr(
            production_refinement.Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
            "request_at",
            forbidden,
        )
        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier(
                result
            ).result()
        )
        assert verification.passed

    def test_independent_comparison_detects_tampered_refinement_metric(self) -> None:
        result = _analyze(_request())
        assert type(result) is (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged
        )
        tampered_step = replace(
            result.refinements[0],
            maximum_correlation_change=(
                result.refinements[0].maximum_correlation_change + 1.0e-5
            ),
        )
        tampered = replace(result, refinements=(tampered_step,))
        verification = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier(
                tampered
            ).result()
        )
        assert not verification.passed
        assert not verification.observations[
            "refinement_0_maximum_correlation_change_absolute_defect"
        ].passed
