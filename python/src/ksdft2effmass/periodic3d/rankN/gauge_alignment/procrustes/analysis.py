"""Periodic-3D arbitrary-rank pointwise Procrustes analysis action."""

from __future__ import annotations

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalyzer,
)

from .request import Periodic3DRankNProcrustesAnalysisRequest
from .result import Periodic3DRankNProcrustesAnalysis


class Periodic3DRankNProcrustesAnalyzer(
    Periodic3DGaugeAlignmentAnalyzer[
        Periodic3DRankNProcrustesAnalysisRequest,
        Periodic3DRankNProcrustesAnalysis,
    ]
):
    """Select pointwise finite-rank unitary right actions through Project Koios."""

    __slots__ = ("_request",)

    def __init__(self, *, request: Periodic3DRankNProcrustesAnalysisRequest) -> None:
        if type(request) is not Periodic3DRankNProcrustesAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic3DRankNProcrustesAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic3DRankNProcrustesAnalysis:
        """Return complete polar factors and invariant numerical evidence."""
        result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source_matrices=self._request.source,
                target_matrices=self._request.target,
                tolerance=self._request.tolerance,
            )
        )
        return Periodic3DRankNProcrustesAnalysis(
            request=self._request,
            owner_result=result,
        )


__all__ = ["Periodic3DRankNProcrustesAnalyzer"]
