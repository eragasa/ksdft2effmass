"""Periodic-3D rank-two pointwise Procrustes result."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)

from ksdft2effmass.gauge_alignment.base import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic3d.rank2.gauge_alignment.base import (
    Periodic3DRank2GaugeAlignmentAnalysis,
)

from .request import Periodic3DRank2ProcrustesAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2ProcrustesAnalysis(
    Periodic3DRank2GaugeAlignmentAnalysis
):
    """Correlate one pointwise request with complete Project Koios evidence."""

    request: Periodic3DRank2ProcrustesAnalysisRequest
    owner_result: NumpyBatchedComplexUnitaryProcrustesResult

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic3DRank2ProcrustesAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D Procrustes request")
        if type(self.owner_result) is not NumpyBatchedComplexUnitaryProcrustesResult:
            raise TypeError("owner_result must be the exact Project Koios result")
        if self.owner_result.tolerance is not self.request.tolerance:
            raise ValueError("owner result tolerance must be the requested tolerance")
        expected_shape = (*self.request.source.shape[:-2], 2, 2)
        if self.owner_result.right_unitary_completions.shape != expected_shape:
            raise ValueError("owner result does not match the requested mesh")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the request-bound pointwise alignment identity."""
        return self.request.analysis_identity


__all__ = ["Periodic3DRank2ProcrustesAnalysis"]
