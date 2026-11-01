"""Tests for parent-family truncation request adaptation."""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


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
            parent_hopping_scales=(0.0, 0.5, 1.0),
        ),
        maximum_range=3,
        evaluation_mesh_size=17,
        support_tolerance=1.0e-6,
    )


class TestPeriodic1DRank2TruncationFamilyRequest:
    """Establish common controls and scale-specific request projection."""

    def test_request_at__changes_only_the_declared_parent_scale(self) -> None:
        request = _request()

        member = request.request_at(0.5)

        assert member.template_request.parent_hopping_scale == 0.5
        assert member.maximum_ranges == (0, 1, 2, 3)
        assert member.evaluation_mesh_size == 17
        assert request.truncation_family_request.family_coordinates == (0.0, 0.5, 1.0)

    def test_init__rejects_invalid_tolerance_and_integer_controls(self) -> None:
        request = _request()
        with pytest.raises(TypeError, match="support_tolerance"):
            replace(request, support_tolerance=True)
        with pytest.raises(ValueError, match="finite and positive"):
            replace(request, support_tolerance=0.0)
        with pytest.raises(TypeError, match="built-in int"):
            Periodic1DRank2TruncationFamilyRequest.every_integer_through(
                parent_family_request=request.parent_family_request,
                maximum_range=True,
                evaluation_mesh_size=17,
                support_tolerance=1.0e-6,
            )
