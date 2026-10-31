"""Tests for parent-family momentum-refinement requests."""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
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


def _thresholds() -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds:
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds(
        maximum_parent_diagnostic_change=1.0,
        maximum_correlation_change=1.0,
        maximum_threshold_change=1.0,
        maximum_hopping_weight_change=1.0,
        maximum_hopping_power_change=1.0,
        maximum_angle_change=1.0,
        maximum_band_defect=1.0,
        maximum_reconstruction_defect=1.0,
        maximum_parseval_defect=1.0,
    )


def _request() -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest:
    return Periodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest(
        parent_family_request=(
            Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
                template_request=_template(),
                parent_hopping_scales=(0.0, 0.5, 1.0),
            )
        ),
        reciprocal_mesh_sizes=(8, 16),
        thresholds=_thresholds(),
        required_stable_refinements=1,
    )


class TestPeriodic1DEmbeddedSubspaceRank2MomentumRefinementFamilyRequest:
    """Establish family inventory and scale-specific request derivation."""

    def test_request_at__changes_only_the_parent_hopping_scale(self) -> None:
        request = _request()

        member = request.request_at(0.5)

        assert member.template_request.parent_hopping_scale == 0.5
        assert member.reciprocal_mesh_sizes == (8, 16)
        assert member.thresholds == request.thresholds
        assert member.required_stable_refinements == 1
        assert replace(member.template_request, parent_hopping_scale=1.0) == _template()

    def test_init__rejects_non_nested_meshes_and_boolean_stability_count(
        self,
    ) -> None:
        request = _request()

        with pytest.raises(ValueError, match="nested doubling"):
            replace(request, reciprocal_mesh_sizes=(8, 24))
        with pytest.raises(TypeError, match="built-in int"):
            replace(request, required_stable_refinements=True)
