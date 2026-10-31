"""Tests for independently reconstructed rank-two support decisions."""

from __future__ import annotations

import math

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    Periodic1DRank2Request,
    Periodic1DRank2TruncationAnalyzer,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationPoint,
    Periodic1DRank2TruncationRequest,
    Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    SupportToleranceUnresolved,
)


def _point() -> Periodic1DRank2TruncationPoint:
    template = Periodic1DRank2Request(
        reciprocal_mesh_size=8,
        amplitudes=(0.0, 0.2, math.pi / 4.0),
        parent_hopping_scale=0.0,
        minimum_external_gap=0.1,
        minimum_transport_singular_value=0.8,
        frame_absolute_tolerance=1.0e-10,
        transport_rank_relative_tolerance=1.0e-12,
        transport_validation_relative_tolerance=1.0e-10,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-12,
    )
    outcome = Periodic1DRank2TruncationAnalyzer(
        request=Periodic1DRank2TruncationRequest(
            template_request=template,
            maximum_ranges=(0, 1, 2, 3),
            evaluation_mesh_size=17,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    assert type(outcome) is Periodic1DRank2TruncationCompleted
    return outcome.points[-1]


class TestPeriodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer:
    """Establish selected and unresolved independent decision variants."""

    def test_execute__independently_scans_all_four_error_channels(self) -> None:
        point = _point()
        selected = (
            Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer(
                point=point,
                tolerance=1.0,
            ).execute()
        )

        assert (
            type(selected.reference_matrix_frobenius_maximum_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert selected.reference_matrix_frobenius_maximum_error.comparison_index == 0
        assert (
            type(selected.reference_ordered_eigenvalue_maximum_absolute_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert (
            type(selected.comparison_matrix_frobenius_maximum_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert (
            type(selected.comparison_ordered_eigenvalue_maximum_absolute_error)
            is MinimumToleranceSatisfyingSupport
        )

        comparison_lower_bound = min(
            min(
                item.comparison_total_hamiltonian_maximum_error for item in point.ranges
            ),
            min(item.comparison_total_spectral_maximum_error for item in point.ranges),
        )
        unresolved = (
            Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer(
                point=point,
                tolerance=comparison_lower_bound / 2.0,
            ).execute()
        )

        assert (
            type(unresolved.reference_matrix_frobenius_maximum_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert (
            type(unresolved.reference_ordered_eigenvalue_maximum_absolute_error)
            is MinimumToleranceSatisfyingSupport
        )
        assert (
            type(unresolved.comparison_matrix_frobenius_maximum_error)
            is SupportToleranceUnresolved
        )
        assert (
            type(unresolved.comparison_ordered_eigenvalue_maximum_absolute_error)
            is SupportToleranceUnresolved
        )
