"""Independent support-decision reference for rank-two truncation."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    RealSpaceSupportTruncation,
    SupportToleranceSelectionOutcome,
    SupportToleranceUnresolved,
)

from .results import Periodic1DRank2TruncationPoint


@dataclass(frozen=True, slots=True)
class Periodic1DRank2TruncationToleranceSelectionIndependentReference(
    RealSpaceSupportTruncation
):
    """Retain four independently reconstructed support-decision outcomes."""

    reference_matrix_frobenius_maximum_error: SupportToleranceSelectionOutcome
    reference_ordered_eigenvalue_maximum_absolute_error: (
        SupportToleranceSelectionOutcome
    )
    comparison_matrix_frobenius_maximum_error: SupportToleranceSelectionOutcome
    comparison_ordered_eigenvalue_maximum_absolute_error: (
        SupportToleranceSelectionOutcome
    )

    def __post_init__(self) -> None:
        for name, outcome in (
            (
                "reference_matrix_frobenius_maximum_error",
                self.reference_matrix_frobenius_maximum_error,
            ),
            (
                "reference_ordered_eigenvalue_maximum_absolute_error",
                self.reference_ordered_eigenvalue_maximum_absolute_error,
            ),
            (
                "comparison_matrix_frobenius_maximum_error",
                self.comparison_matrix_frobenius_maximum_error,
            ),
            (
                "comparison_ordered_eigenvalue_maximum_absolute_error",
                self.comparison_ordered_eigenvalue_maximum_absolute_error,
            ),
        ):
            if type(outcome) not in (
                MinimumToleranceSatisfyingSupport,
                SupportToleranceUnresolved,
            ):
                raise TypeError(f"{name} must be one closed support outcome")


class Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer:
    """Independently scan rank-two truncation errors for support decisions."""

    __slots__ = ("_point", "_tolerance")

    def __init__(
        self,
        *,
        point: Periodic1DRank2TruncationPoint,
        tolerance: float,
    ) -> None:
        if type(point) is not Periodic1DRank2TruncationPoint:
            raise TypeError("point must be an exact truncation point")
        if type(tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(tolerance) or tolerance <= 0.0:
            raise ValueError("tolerance must be finite and positive")
        inventory = tuple(item.maximum_range for item in point.ranges)
        if inventory != tuple(range(inventory[-1] + 1)):
            raise ValueError(
                "support selection requires a dense zero-based range inventory"
            )
        self._point = point
        self._tolerance = tolerance

    def execute(
        self,
    ) -> Periodic1DRank2TruncationToleranceSelectionIndependentReference:
        """Return four decisions without calling a production selector."""
        supports = tuple(item.support_policy.support for item in self._point.ranges)
        error_channels = (
            tuple(
                item.reference_truncation_hamiltonian_maximum_error
                for item in self._point.ranges
            ),
            tuple(
                item.reference_truncation_spectral_maximum_error
                for item in self._point.ranges
            ),
            tuple(
                item.comparison_total_hamiltonian_maximum_error
                for item in self._point.ranges
            ),
            tuple(
                item.comparison_total_spectral_maximum_error
                for item in self._point.ranges
            ),
        )
        outcomes: list[SupportToleranceSelectionOutcome] = []
        for errors in error_channels:
            selected_index: int | None = None
            for index, error in enumerate(errors):
                if error <= self._tolerance:
                    selected_index = index
                    break
            if selected_index is None:
                outcomes.append(
                    SupportToleranceUnresolved(
                        comparison_count=len(errors),
                        minimum_observed_error=min(errors),
                        largest_support_error=errors[-1],
                    )
                )
            else:
                outcomes.append(
                    MinimumToleranceSatisfyingSupport(
                        comparison_index=selected_index,
                        support=supports[selected_index],
                        satisfying_error=errors[selected_index],
                        preceding_error=(
                            None if selected_index == 0 else errors[selected_index - 1]
                        ),
                    )
                )
        return Periodic1DRank2TruncationToleranceSelectionIndependentReference(
            reference_matrix_frobenius_maximum_error=outcomes[0],
            reference_ordered_eigenvalue_maximum_absolute_error=outcomes[1],
            comparison_matrix_frobenius_maximum_error=outcomes[2],
            comparison_ordered_eigenvalue_maximum_absolute_error=outcomes[3],
        )


__all__ = [
    "Periodic1DRank2TruncationToleranceSelectionIndependentReference",
    "Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer",
]
