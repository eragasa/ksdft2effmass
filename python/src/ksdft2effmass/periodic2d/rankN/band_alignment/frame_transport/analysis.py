"""Periodic-2D arbitrary-rank frame-transport analysis action."""

from __future__ import annotations

from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    frame_transport_diagnostics,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.periodic2d.rankN.gauge_alignment.procrustes.analysis import (
    Periodic2DRankNProcrustesAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.procrustes.request import (
    Periodic2DRankNProcrustesAnalysisRequest,
)

from .request import Periodic2DRankNTransportAnalysisRequest
from .result import Periodic2DRankNTransportDiagnosticAnalysis


class Periodic2DRankNTransportAnalyzer(Periodic2DCapability):
    """Measure finite-rank neighbor transport on a periodic-2D tensor mesh."""

    __slots__ = ("_request",)

    def __init__(self, *, request: Periodic2DRankNTransportAnalysisRequest) -> None:
        if type(request) is not Periodic2DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic2DRankNTransportAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def _solve_procrustes(
        self,
        source: Complex128Array,
        target: Complex128Array,
        tolerance: ComplexUnitaryProcrustesTolerance,
    ) -> NumpyBatchedComplexUnitaryProcrustesResult:
        """Route one neighbor-link family through the rank-N pointwise owner."""
        return (
            Periodic2DRankNProcrustesAnalyzer(
                request=Periodic2DRankNProcrustesAnalysisRequest(
                    retained_rank=self._request.retained_rank,
                    source=source,
                    target=target,
                    tolerance=tolerance,
                )
            )
            .execute()
            .owner_result
        )

    def execute(self) -> Periodic2DRankNTransportDiagnosticAnalysis:
        """Return neighbor-link, closure, and plaquette diagnostics."""
        diagnostic = frame_transport_diagnostics(
            self._request.frame,
            dimension=2,
            rank_absolute=self._request.rank_absolute,
            rank_relative=self._request.rank_relative,
            procrustes_solve=self._solve_procrustes,
        )
        return Periodic2DRankNTransportDiagnosticAnalysis(
            minimum_singular_value=diagnostic.minimum_singular_value,
            maximum_procrustes_residual=diagnostic.maximum_procrustes_residual,
            maximum_squared_residual_roundoff_cutoff=(
                diagnostic.maximum_squared_residual_roundoff_cutoff
            ),
            maximum_unitarity_defect=diagnostic.maximum_unitarity_defect,
            maximum_rank_cutoff=diagnostic.maximum_rank_cutoff,
            rank_deficient_link_count=diagnostic.rank_deficient_link_count,
            closure_and_plaquette_applicable=(
                diagnostic.closure_and_plaquette_applicable
            ),
            closure_and_plaquette_inapplicable_reason=(
                diagnostic.closure_and_plaquette_inapplicable_reason
            ),
            maximum_absolute_closure_phases=(
                diagnostic.maximum_absolute_closure_phases
            ),
            maximum_closure_unitarity_defect=(
                diagnostic.maximum_closure_unitarity_defect
            ),
            maximum_plaquette_phase=diagnostic.maximum_plaquette_phase,
            request=self._request,
        )


__all__ = ["Periodic2DRankNTransportAnalyzer"]
