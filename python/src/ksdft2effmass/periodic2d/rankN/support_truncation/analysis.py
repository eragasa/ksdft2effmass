"""Periodic-2D arbitrary-rank support-truncation analysis action."""

from __future__ import annotations

from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationErrorToleranceSelectionRequest,
    RealSpaceSupportTruncationErrorToleranceSelector,
    SupportToleranceSelectionOutcome,
)

from .base import Periodic2DRankNSupportTruncationAnalyzerRole
from .request import Periodic2DRankNSupportTruncationAnalysisRequest
from .result import Periodic2DRankNSupportTruncationAnalysis


class Periodic2DRankNSupportTruncationAnalyzer(
    Periodic2DRankNSupportTruncationAnalyzerRole[
        Periodic2DRankNSupportTruncationAnalysisRequest,
        Periodic2DRankNSupportTruncationAnalysis,
    ]
):
    """Select one channel's minimum admitted support at one tolerance."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNSupportTruncationAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic2DRankNSupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be the exact periodic-2D arbitrary-rank request"
            )
        self._request = request

    @property
    def request(self) -> Periodic2DRankNSupportTruncationAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def _select(self, errors: tuple[float, ...]) -> SupportToleranceSelectionOutcome:
        supports = tuple(
            self._request.support_inventory.support_through(index)
            for index in range(len(errors))
        )
        return RealSpaceSupportTruncationErrorToleranceSelector(
            request=RealSpaceSupportTruncationErrorToleranceSelectionRequest(
                supports=supports,
                errors=errors,
                tolerance=self._request.tolerance,
            )
        ).execute()

    def execute(self) -> Periodic2DRankNSupportTruncationAnalysis:
        """Return matrix and ordered-band support-selection outcomes."""
        matrix_errors = tuple(
            errors.support_truncation_errors.matrix_frobenius.maximum_error
            for errors in self._request.total_errors
        )
        eigenvalue_errors = tuple(
            errors.support_truncation_errors.ordered_eigenvalues.maximum_absolute_error
            for errors in self._request.total_errors
        )
        return Periodic2DRankNSupportTruncationAnalysis(
            matrix_frobenius_maximum_error=self._select(matrix_errors),
            ordered_eigenvalue_maximum_absolute_error=self._select(eigenvalue_errors),
            request=self._request,
        )


__all__ = ["Periodic2DRankNSupportTruncationAnalyzer"]
