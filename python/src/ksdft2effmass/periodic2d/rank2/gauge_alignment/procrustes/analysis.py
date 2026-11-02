"""Periodic-2D rank-two pointwise Procrustes analysis action."""

from __future__ import annotations

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalyzer,
)

from .request import Periodic2DRank2ProcrustesAnalysisRequest
from .result import Periodic2DRank2ProcrustesAnalysis


class Periodic2DRank2ProcrustesAnalyzer(
    Periodic2DGaugeAlignmentAnalyzer[
        Periodic2DRank2ProcrustesAnalysisRequest,
        Periodic2DRank2ProcrustesAnalysis,
    ]
):
    """Select pointwise complex-unitary right actions through Project Koios."""

    __slots__ = ("_request",)

    def __init__(self, *, request: Periodic2DRank2ProcrustesAnalysisRequest) -> None:
        if type(request) is not Periodic2DRank2ProcrustesAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D Procrustes request")
        self._request = request

    @property
    def request(self) -> Periodic2DRank2ProcrustesAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRank2ProcrustesAnalysis:
        """Return complete polar factors and invariant numerical evidence."""
        result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source_matrices=self._request.source,
                target_matrices=self._request.target,
                tolerance=self._request.tolerance,
            )
        )
        return Periodic2DRank2ProcrustesAnalysis(
            request=self._request,
            owner_result=result,
        )


__all__ = ["Periodic2DRank2ProcrustesAnalyzer"]
