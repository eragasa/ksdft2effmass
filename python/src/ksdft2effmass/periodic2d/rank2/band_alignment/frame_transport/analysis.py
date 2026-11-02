"""Periodic-2D rank-two frame-transport analysis action."""

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
from ksdft2effmass.periodic2d.rank2.gauge_alignment.procrustes.analysis import (
    Periodic2DRank2ProcrustesAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.procrustes.request import (
    Periodic2DRank2ProcrustesAnalysisRequest,
)

from .request import Periodic2DRank2TransportAnalysisRequest
from .result import Periodic2DRank2TransportDiagnosticAnalysis


class Periodic2DRank2TransportAnalyzer(Periodic2DCapability):
    """Measure rank-two neighbor transport on a periodic-2D tensor mesh."""

    __slots__ = ("_request",)

    def __init__(self, *, request: Periodic2DRank2TransportAnalysisRequest) -> None:
        if type(request) is not Periodic2DRank2TransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D transport request")
        self._request = request

    @property
    def request(self) -> Periodic2DRank2TransportAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    @staticmethod
    def _solve_procrustes(
        source: Complex128Array,
        target: Complex128Array,
        tolerance: ComplexUnitaryProcrustesTolerance,
    ) -> NumpyBatchedComplexUnitaryProcrustesResult:
        """Route one neighbor-link family through the pointwise owner."""
        return (
            Periodic2DRank2ProcrustesAnalyzer(
                request=Periodic2DRank2ProcrustesAnalysisRequest(
                    source=source,
                    target=target,
                    tolerance=tolerance,
                )
            )
            .execute()
            .owner_result
        )

    def execute(self) -> Periodic2DRank2TransportDiagnosticAnalysis:
        """Return neighbor-link, closure, and plaquette diagnostics."""
        diagnostic = frame_transport_diagnostics(
            self._request.frame,
            dimension=2,
            rank_absolute=self._request.rank_absolute,
            rank_relative=self._request.rank_relative,
            procrustes_solve=self._solve_procrustes,
        )
        return Periodic2DRank2TransportDiagnosticAnalysis(
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


__all__ = ["Periodic2DRank2TransportAnalyzer"]
