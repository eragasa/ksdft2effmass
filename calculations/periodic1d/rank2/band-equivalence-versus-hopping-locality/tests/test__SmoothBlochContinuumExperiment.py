"""Tests for the maintained flat-parent development-study composition."""

from __future__ import annotations

import math

import pytest
from rank2_control_analysis import momentum_refinement

pytestmark = pytest.mark.software_verification


class TestSmoothBlochContinuumExperiment:
    """Establish the flat scale through the installed rank-two owners."""

    def test_flat_scale_refinement_is_independently_verified(self) -> None:
        analysis = momentum_refinement(
            reciprocal_mesh_sizes=(8, 16),
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            parent_hopping_scale=0.0,
            draft_tolerance=1.0,
            required_stable_refinements=1,
        )

        assert tuple(
            item.request.reciprocal_mesh_size for item in analysis.mesh_analyses
        ) == (8, 16)
        assert len(analysis.refinements) == 1
        endpoint = analysis.mesh_analyses[-1].points[-1]
        assert endpoint.maximum_band_defect < 1.0e-12
        assert endpoint.reference_nonzero_hopping_weight == 0.0
        assert endpoint.comparison_nonzero_hopping_weight > 0.0
