"""Periodic-2D arbitrary-rank pointwise Procrustes result."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)

from ksdft2effmass.gauge_alignment.base import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalysis,
)

from .request import Periodic2DRankNProcrustesAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNProcrustesAnalysis(Periodic2DGaugeAlignmentAnalysis):
    """Correlate one finite-rank request with complete Project Koios evidence."""

    request: Periodic2DRankNProcrustesAnalysisRequest
    owner_result: NumpyBatchedComplexUnitaryProcrustesResult

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic2DRankNProcrustesAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        if type(self.owner_result) is not NumpyBatchedComplexUnitaryProcrustesResult:
            raise TypeError("owner_result must be the exact Project Koios result")
        if self.owner_result.tolerance is not self.request.tolerance:
            raise ValueError("owner result tolerance must be the requested tolerance")
        rank = self.request.retained_rank
        expected_shape = (*self.request.source.shape[:-2], rank, rank)
        if self.owner_result.right_unitary_completions.shape != expected_shape:
            raise ValueError("owner result does not match the requested mesh and rank")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the request-bound pointwise alignment identity."""
        return self.request.analysis_identity


__all__ = ["Periodic2DRankNProcrustesAnalysis"]
