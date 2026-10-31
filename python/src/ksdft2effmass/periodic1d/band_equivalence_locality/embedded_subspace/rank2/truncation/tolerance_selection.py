"""Support-tolerance selection for embedded rank-two periodic-1D truncation."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.real_space_support_truncation import (
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncation,
    RealSpaceSupportTruncationComparison,
    RealSpaceSupportTruncationErrors,
    RealSpaceSupportTruncationToleranceSelection,
    RealSpaceSupportTruncationToleranceSelectionRequest,
    RealSpaceSupportTruncationToleranceSelector,
)

from .results import Periodic1DEmbeddedSubspaceRank2TruncationPoint


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2TruncationToleranceSelector(
    RealSpaceSupportTruncation
):
    """Adapt one dense symmetric-range inventory to the shared selector."""

    point: Periodic1DEmbeddedSubspaceRank2TruncationPoint
    tolerance: float

    def __post_init__(self) -> None:
        if type(self.point) is not Periodic1DEmbeddedSubspaceRank2TruncationPoint:
            raise TypeError("point must be an exact truncation point")
        if type(self.tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(self.tolerance) or self.tolerance <= 0.0:
            raise ValueError("tolerance must be finite and positive")
        inventory = tuple(item.maximum_range for item in self.point.ranges)
        if inventory != tuple(range(inventory[-1] + 1)):
            raise ValueError(
                "support selection requires a dense zero-based range inventory"
            )

    def execute(self) -> RealSpaceSupportTruncationToleranceSelection:
        """Return minimum tolerance-satisfying symmetric-range supports."""
        request = RealSpaceSupportTruncationToleranceSelectionRequest(
            comparisons=tuple(
                RealSpaceSupportTruncationComparison(
                    support=item.support_policy.support,
                    reference_model_errors=RealSpaceSupportTruncationErrors(
                        matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
                            maximum_error=(
                                item.reference_truncation_hamiltonian_maximum_error
                            ),
                            root_mean_square_error=(
                                item.reference_truncation_hamiltonian_rms_error
                            ),
                        ),
                        ordered_eigenvalues=OrderedEigenvalueErrors(
                            maximum_absolute_error=(
                                item.reference_truncation_spectral_maximum_error
                            ),
                            root_mean_square_error=(
                                item.reference_truncation_spectral_rms_error
                            ),
                        ),
                    ),
                    comparison_model_errors=RealSpaceSupportTruncationErrors(
                        matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
                            maximum_error=(
                                item.comparison_total_hamiltonian_maximum_error
                            ),
                            root_mean_square_error=(
                                item.comparison_total_hamiltonian_rms_error
                            ),
                        ),
                        ordered_eigenvalues=OrderedEigenvalueErrors(
                            maximum_absolute_error=(
                                item.comparison_total_spectral_maximum_error
                            ),
                            root_mean_square_error=(
                                item.comparison_total_spectral_rms_error
                            ),
                        ),
                    ),
                )
                for item in self.point.ranges
            ),
            tolerance=self.tolerance,
        )
        return RealSpaceSupportTruncationToleranceSelector().execute(request)


__all__ = ["Periodic1DEmbeddedSubspaceRank2TruncationToleranceSelector"]
