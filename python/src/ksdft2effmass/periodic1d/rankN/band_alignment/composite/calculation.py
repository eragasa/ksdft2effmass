"""Request-bound producer for the analytic higher-rank periodic-1D calculation."""

from __future__ import annotations

import math
from typing import final

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.result import (
    Periodic1DRankNProcrustesDiagnostics,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.selection import (
    Periodic1DRankNProcrustesSelection,
    Periodic1DRankNProcrustesSelectionAnalyzer,
    Periodic1DRankNProcrustesSelectionRequest,
)

from ..calculation_result import Periodic1DRankNAlignmentCalculationResult
from .construction_mesh import (
    Periodic1DRankNConstructionMeshAnalysisRequest,
    Periodic1DRankNConstructionMeshAnalyzer,
)
from .evaluation import Periodic1DRankNEvaluationIndependenceAnalyzer
from .refinement import (
    Periodic1DRankNRefinementAnalysisRequest,
    Periodic1DRankNRefinementAnalyzer,
)


@final
class Periodic1DRankNAlignmentAnalyzer:
    """Sequence one complete rank/depth calculation through explicit owners."""

    __slots__ = (
        "_request",
        "_procrustes_solver",
        "_transporter",
        "_scalar_refinement_analyzer",
    )

    def __init__(
        self,
        *,
        request: Periodic1DRankNAlignmentCalculationRequest,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
        transporter: ClosedLoopPolarFrameTransporter,
        scalar_refinement_analyzer: ScalarRefinementAnalyzer,
    ) -> None:
        """Bind the exact request and canonical numerical collaborators."""
        if type(request) is not Periodic1DRankNAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DRankNAlignmentCalculationRequest"
            )
        if type(procrustes_solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError(
                "procrustes_solver must be the canonical NumPy batched solver"
            )
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        if type(scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be the KSD refinement owner"
            )
        self._request = request
        self._procrustes_solver = procrustes_solver
        self._transporter = transporter
        self._scalar_refinement_analyzer = scalar_refinement_analyzer

    @property
    def request(self) -> Periodic1DRankNAlignmentCalculationRequest:
        """Return the exact calculation request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNAlignmentCalculationResult:
        """Produce the complete typed calculation for the bound rank/depth case."""
        request = self._request
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
        ).execute()
        samples = tuple(
            Periodic1DRankNAnalyticMeshSample(
                model,
                request.configuration,
                mesh_size,
            )
            for mesh_size in request.configuration.construction_mesh_sizes
        )
        global_sample = next(
            sample
            for sample in samples
            if sample.construction_mesh_size
            == request.configuration.global_unitary_selection_mesh_size
        )
        global_selection = self._global_selection(global_sample)
        meshes = tuple(
            Periodic1DRankNConstructionMeshAnalyzer(
                request=Periodic1DRankNConstructionMeshAnalysisRequest(
                    calculation_request=request,
                    sample=sample,
                    global_selection=global_selection,
                ),
                procrustes_solver=self._procrustes_solver,
                transporter=self._transporter,
            ).execute()
            for sample in samples
        )
        refinement = Periodic1DRankNRefinementAnalyzer(
            request=Periodic1DRankNRefinementAnalysisRequest(
                calculation_request=request,
                meshes=meshes,
            ),
            scalar_refinement_analyzer=self._scalar_refinement_analyzer,
        ).execute()
        evaluation_independence = Periodic1DRankNEvaluationIndependenceAnalyzer(
            request
        ).execute()
        return Periodic1DRankNAlignmentCalculationResult(
            request=request,
            global_selection=global_selection,
            meshes=meshes,
            evaluation_independence=evaluation_independence,
            block_refinements=refinement.blocks,
            scalar_refinements=refinement.scalars,
        )

    def _global_selection(
        self,
        sample: Periodic1DRankNAnalyticMeshSample,
    ) -> Periodic1DRankNProcrustesDiagnostics:
        model = sample.model
        mesh_size = sample.construction_mesh_size
        scale = math.sqrt(mesh_size)
        source = NumpyImmutableArrayConstructor(
            np.asarray(
                sample.attacked_frames.reshape(
                    1,
                    mesh_size * model.ambient_dimension,
                    model.retained_rank,
                )
                / scale,
                dtype=np.complex128,
            ),
            "global_selection_source",
            np.dtype(np.complex128),
        ).execute()
        target = NumpyImmutableArrayConstructor(
            np.asarray(
                sample.reference_frames.reshape(
                    1,
                    mesh_size * model.ambient_dimension,
                    model.retained_rank,
                )
                / scale,
                dtype=np.complex128,
            ),
            "global_selection_target",
            np.dtype(np.complex128),
        ).execute()
        return self._procrustes_selection(
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            selection_mesh_size=mesh_size,
            source=source,
            target=target,
        ).diagnostics

    def _procrustes_selection(
        self,
        *,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        selection_mesh_size: int,
        source: ComplexArray,
        target: ComplexArray,
    ) -> Periodic1DRankNProcrustesSelection:
        request = self._request
        return Periodic1DRankNProcrustesSelectionAnalyzer(
            request=Periodic1DRankNProcrustesSelectionRequest(
                case_identity=request.case_identity,
                retained_rank=request.retained_rank,
                circuit_depth=request.circuit_depth,
                gauge_alignment=gauge_alignment,
                selection_mesh_size=selection_mesh_size,
                source=source,
                target=target,
                tolerance=request.configuration.owner_transport_tolerance(),
                alignment_integrity_tolerance=(
                    request.controls.alignment_integrity_tolerance
                ),
            ),
            solver=self._procrustes_solver,
        ).execute()


__all__ = ["Periodic1DRankNAlignmentAnalyzer"]
