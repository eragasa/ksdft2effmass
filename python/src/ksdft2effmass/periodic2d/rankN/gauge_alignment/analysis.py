"""Periodic-2D arbitrary-rank global unitary-alignment action."""

from __future__ import annotations

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalyzer,
)

from .request import Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest
from .result import Periodic2DRankNGlobalGaugeAlignmentAnalysis


class Periodic2DRankNGlobalGaugeAlignmentAnalyzer(
    Periodic2DGaugeAlignmentAnalyzer[
        Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest,
        Periodic2DRankNGlobalGaugeAlignmentAnalysis,
    ]
):
    """Select one constant finite-rank right unitary through Project Koios."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRankNGlobalGaugeAlignmentAnalysis:
        """Return one aggregate polar factor and invariant rank evidence."""
        rank = self._request.retained_rank
        source = self._request.source.reshape(1, -1, rank)
        target = self._request.target.reshape(1, -1, rank)
        owner_result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source_matrices=source,
                target_matrices=target,
                tolerance=self._request.tolerance,
            )
        )
        return Periodic2DRankNGlobalGaugeAlignmentAnalysis(
            request=self._request,
            owner_result=owner_result,
        )


__all__ = ["Periodic2DRankNGlobalGaugeAlignmentAnalyzer"]
