"""Tests for parent-family momentum-refinement analysis."""

from __future__ import annotations

import math

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DRank2MomentumRefinementConverged,
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
    Periodic1DRank2MomentumRefinementFamilyAnalyzer,
    Periodic1DRank2MomentumRefinementFamilyRequest,
    Periodic1DRank2MomentumRefinementThresholds,
    Periodic1DRank2ParentFamilyRequest,
    Periodic1DRank2Request,
)


def _request() -> Periodic1DRank2MomentumRefinementFamilyRequest:
    template = Periodic1DRank2Request(
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
    thresholds = Periodic1DRank2MomentumRefinementThresholds(
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
    return Periodic1DRank2MomentumRefinementFamilyRequest(
        parent_family_request=Periodic1DRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=(0.0, 1.0),
        ),
        reciprocal_mesh_sizes=(8, 16),
        thresholds=thresholds,
        required_stable_refinements=1,
    )


class TestPeriodic1DRank2MomentumRefinementFamilyAnalyzer:
    """Establish ordered closed outcomes across the declared parent family."""

    def test_execute__returns_one_closed_outcome_per_parent_scale(self) -> None:
        result = Periodic1DRank2MomentumRefinementFamilyAnalyzer(
            request=_request(),
            transporter=ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert type(result) is (Periodic1DRank2MomentumRefinementFamilyAnalysis)
        assert tuple(
            member.request.template_request.parent_hopping_scale
            for member in result.members
        ) == (0.0, 1.0)
        assert tuple(type(member) for member in result.members) == (
            Periodic1DRank2MomentumRefinementConverged,
            Periodic1DRank2MomentumRefinementConverged,
        )
        assert tuple(
            tuple(
                analysis.request.reciprocal_mesh_size
                for analysis in member.mesh_analyses
            )
            for member in result.members
        ) == ((8, 16), (8, 16))
