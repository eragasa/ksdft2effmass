"""Periodic-2D arbitrary-rank pointwise Procrustes analysis action."""

from __future__ import annotations

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic2d.rankN.gauge_alignment.base import (
    Periodic2DRankNGaugeAlignmentAnalyzer,
)

from .request import Periodic2DRankNProcrustesAnalysisRequest
from .result import Periodic2DRankNProcrustesAnalysis


class Periodic2DRankNProcrustesAnalyzer(
    Periodic2DRankNGaugeAlignmentAnalyzer[
        Periodic2DRankNProcrustesAnalysisRequest,
        Periodic2DRankNProcrustesAnalysis,
    ]
):
    """Select pointwise finite-rank unitary right actions through Project Koios."""

    __slots__ = ("_request",)

    def __init__(self, *, request: Periodic2DRankNProcrustesAnalysisRequest) -> None:
        if type(request) is not Periodic2DRankNProcrustesAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic2DRankNProcrustesAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRankNProcrustesAnalysis:
        """Return complete polar factors and invariant numerical evidence."""
        result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source_matrices=self._request.source,
                target_matrices=self._request.target,
                tolerance=self._request.tolerance,
            )
        )
        return Periodic2DRankNProcrustesAnalysis(
            request=self._request,
            owner_result=result,
        )


__all__ = ["Periodic2DRankNProcrustesAnalyzer"]
