"""Tests for maintained parent-family and momentum-study composition."""

from __future__ import annotations

import math

import pytest
from development_study import parent_family, qualified_parent

pytestmark = pytest.mark.software_verification


class TestSmoothFourStateExperiment:
    """Establish the parent family through installed typed scientific owners."""

    def test_two_endpoint_scales_share_one_bound_family_request(self) -> None:
        family = parent_family(
            reciprocal_mesh_size=16,
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            parent_hopping_scales=(0.0, 1.0),
        )

        assert tuple(
            member.request.parent_hopping_scale for member in family.members
        ) == (0.0, 1.0)
        flat, nonflat = family.members
        assert qualified_parent(flat).minimum_external_gap >= 1.0
        assert qualified_parent(nonflat).minimum_external_gap >= 1.0
        assert flat.points[-1].reference_nonzero_hopping_weight == 0.0
        assert nonflat.points[-1].reference_nonzero_hopping_weight > 0.0
        assert nonflat.points[-1].comparison_nonzero_hopping_weight > 0.0
