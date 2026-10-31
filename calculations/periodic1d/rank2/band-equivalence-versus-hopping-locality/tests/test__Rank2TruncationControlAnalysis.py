"""Tests for calculation-local rank-two truncation control composition."""

from __future__ import annotations

import math

import pytest
from rank2_control_analysis import (
    completed_truncation,
    truncation_analysis,
    truncation_verification_defect,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    Periodic1DRank2TruncationToleranceSelector,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
)

pytestmark = pytest.mark.software_verification


class TestRank2TruncationControlAnalysis:
    """Establish support selections over verified calculation-local controls."""

    def test_dense_inventory_has_independently_verified_channel_decisions(self) -> None:
        analysis = completed_truncation(
            truncation_analysis(
                construction_mesh_size=16,
                evaluation_mesh_size=65,
                amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
                parent_hopping_scale=1.0,
                maximum_range=3,
            )
        )

        assert truncation_verification_defect(analysis) <= 1.0e-10
        endpoint = analysis.points[-1]
        assert tuple(item.maximum_range for item in endpoint.ranges) == (0, 1, 2, 3)
        selection = Periodic1DRank2TruncationToleranceSelector(
            point=endpoint,
            tolerance=1.0,
        ).execute()
        reference_eigenvalue = (
            selection.reference_model.ordered_eigenvalue_maximum_absolute_error
        )
        reference_matrix = selection.reference_model.matrix_frobenius_maximum_error
        assert type(reference_eigenvalue) is MinimumToleranceSatisfyingSupport
        assert type(reference_matrix) is MinimumToleranceSatisfyingSupport
        assert (
            type(selection.comparison_model.ordered_eigenvalue_maximum_absolute_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert (
            type(selection.comparison_model.matrix_frobenius_maximum_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert reference_eigenvalue.comparison_index == 0
        assert reference_matrix.comparison_index == 0
