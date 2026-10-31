"""Tests for parent-family real-space-support truncation analysis."""

from __future__ import annotations

import math
from dataclasses import replace

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DRank2ParentFamilyRequest,
    Periodic1DRank2Request,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationFamilyAnalysis,
    Periodic1DRank2TruncationFamilyAnalyzer,
    Periodic1DRank2TruncationFamilyRequest,
    Periodic1DRank2TruncationQualificationStopped,
    Periodic1DRank2TruncationToleranceSelector,
)


def _request() -> Periodic1DRank2TruncationFamilyRequest:
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
    return Periodic1DRank2TruncationFamilyRequest.every_integer_through(
        parent_family_request=Periodic1DRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=(0.0, 1.0),
        ),
        maximum_range=3,
        evaluation_mesh_size=17,
        support_tolerance=1.0e-6,
    )


class TestPeriodic1DRank2TruncationFamilyAnalyzer:
    """Establish ordered outcomes and request-derived support selections."""

    def test_execute__returns_one_outcome_and_selection_set_per_scale(self) -> None:
        result = Periodic1DRank2TruncationFamilyAnalyzer(
            request=_request(),
            transporter=ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert type(result) is Periodic1DRank2TruncationFamilyAnalysis
        assert tuple(
            member.request.template_request.parent_hopping_scale
            for member in result.members
        ) == (0.0, 1.0)
        assert tuple(type(member) for member in result.members) == (
            Periodic1DRank2TruncationCompleted,
            Periodic1DRank2TruncationCompleted,
        )
        assert tuple(
            len(selections)
            for selections in result.support_tolerance_selections_by_member
        ) == (
            3,
            3,
        )
        first_member = result.members[0]
        assert type(first_member) is Periodic1DRank2TruncationCompleted
        assert result.support_tolerance_selections_by_member[0][0] == (
            Periodic1DRank2TruncationToleranceSelector(
                point=first_member.points[0],
                tolerance=result.request.support_tolerance,
            ).execute()
        )

    def test_execute__retains_qualification_stops_as_closed_outcomes(self) -> None:
        request = _request()
        stopped_template = replace(
            request.parent_family_request.template_request,
            minimum_external_gap=100.0,
        )
        stopped_request = replace(
            request,
            parent_family_request=replace(
                request.parent_family_request,
                template_request=stopped_template,
            ),
        )

        result = Periodic1DRank2TruncationFamilyAnalyzer(
            request=stopped_request,
            transporter=ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert tuple(type(member) for member in result.members) == (
            Periodic1DRank2TruncationQualificationStopped,
            Periodic1DRank2TruncationQualificationStopped,
        )
        assert result.support_tolerance_selections_by_member == ((), ())
