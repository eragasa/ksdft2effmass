"""Typed Procrustes selection outcomes for rank-N gauge alignment."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.validation import (
    NumpyImmutableArrayConstructor,
    NumpyImmutableArrayValidator,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray

from ...band_alignment.protocol import (
    CIRCUIT_DEPTHS,
    CONSTRUCTION_MESH_SIZES,
    RETAINED_RANKS,
)
from ..definition import Periodic1DRankNGaugeAlignment
from ..status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
)
from .analysis import Periodic1DRankNProcrustesDiagnosticsAnalyzer
from .result import Periodic1DRankNProcrustesDiagnostics


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNProcrustesSelectionRequest:
    """Bind one global or pointwise Procrustes selection problem."""

    case_identity: str
    retained_rank: int
    circuit_depth: int
    gauge_alignment: Periodic1DRankNGaugeAlignment
    selection_mesh_size: int
    source: ComplexArray
    target: ComplexArray
    tolerance: ComplexUnitaryProcrustesTolerance
    alignment_integrity_tolerance: float

    def __post_init__(self) -> None:
        if type(self.case_identity) is not str:
            raise TypeError("case_identity must be a built-in string")
        for value, name, inventory in (
            (self.retained_rank, "retained_rank", RETAINED_RANKS),
            (self.circuit_depth, "circuit_depth", CIRCUIT_DEPTHS),
            (
                self.selection_mesh_size,
                "selection_mesh_size",
                CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value not in inventory:
                raise ValueError(f"{name} is not in the frozen inventory")
        if self.case_identity != f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}":
            raise ValueError("case_identity is inconsistent with rank and depth")
        if self.gauge_alignment not in (
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
        ):
            raise ValueError("Procrustes selection must be global or pointwise")
        if type(self.tolerance) is not ComplexUnitaryProcrustesTolerance:
            raise TypeError("tolerance must be ComplexUnitaryProcrustesTolerance")
        if (
            type(self.alignment_integrity_tolerance) is not float
            or not math.isfinite(self.alignment_integrity_tolerance)
            or self.alignment_integrity_tolerance < 0.0
        ):
            raise ValueError(
                "alignment_integrity_tolerance must be finite and nonnegative"
            )
        source = NumpyImmutableArrayValidator(
            self.source,
            "source",
            np.dtype(np.complex128),
        ).execute()
        target = NumpyImmutableArrayValidator(
            self.target,
            "target",
            np.dtype(np.complex128),
        ).execute()
        if source.ndim != 3 or target.shape != source.shape:
            raise ValueError("source and target must be matching rank-three arrays")
        if source.shape[-1] != self.retained_rank:
            raise ValueError("source and target must match the retained rank")
        expected_batch_size = (
            1
            if self.gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            else self.selection_mesh_size
        )
        if source.shape[0] != expected_batch_size:
            raise ValueError("selection batch does not match the gauge alignment")
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "target", target)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNResolvedProcrustesSelection:
    """Retain diagnostics and immutable right actions from a completed solve."""

    diagnostics: Periodic1DRankNProcrustesDiagnostics
    right_unitaries: ComplexArray

    def __post_init__(self) -> None:
        if type(self.diagnostics) is not Periodic1DRankNProcrustesDiagnostics:
            raise TypeError("diagnostics must be the exact Procrustes record")
        if (
            self.diagnostics.status.status
            is Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
        ):
            raise ValueError("resolved selection cannot retain unresolved diagnostics")
        right_unitaries = NumpyImmutableArrayValidator(
            self.right_unitaries,
            "right_unitaries",
            np.dtype(np.complex128),
        ).execute()
        expected_count = (
            1
            if self.diagnostics.status.gauge_alignment
            is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            else self.diagnostics.selection_mesh_size
        )
        rank = self.diagnostics.status.retained_rank
        if right_unitaries.shape != (expected_count, rank, rank):
            raise ValueError("right_unitaries do not match the selection diagnostics")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNUnresolvedProcrustesSelection:
    """Retain diagnostics for a Procrustes solve that did not produce actions."""

    diagnostics: Periodic1DRankNProcrustesDiagnostics

    def __post_init__(self) -> None:
        if type(self.diagnostics) is not Periodic1DRankNProcrustesDiagnostics:
            raise TypeError("diagnostics must be the exact Procrustes record")
        if (
            self.diagnostics.status.status
            is not Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
        ):
            raise ValueError("unresolved selection requires unresolved diagnostics")


type Periodic1DRankNProcrustesSelection = (
    Periodic1DRankNResolvedProcrustesSelection
    | Periodic1DRankNUnresolvedProcrustesSelection
)


@final
class Periodic1DRankNProcrustesSelectionAnalyzer:
    """Execute one bound Procrustes request and return a typed selection outcome."""

    __slots__ = ("_request", "_solver")

    def __init__(
        self,
        request: Periodic1DRankNProcrustesSelectionRequest,
        solver: NumpyBatchedComplexUnitaryProcrustesSolver,
    ) -> None:
        if type(request) is not Periodic1DRankNProcrustesSelectionRequest:
            raise TypeError("request must be the exact Procrustes selection request")
        if type(solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError("solver must be the canonical NumPy batched solver")
        self._request = request
        self._solver = solver

    @property
    def request(self) -> Periodic1DRankNProcrustesSelectionRequest:
        """Return the immutable selection problem bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNProcrustesSelection:
        """Return completed right actions or typed unresolved diagnostics."""
        request = self._request
        definition = NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
            request.source,
            request.target,
            request.tolerance,
        )
        try:
            result = self._solver.solve(definition)
        except (ArithmeticError, RuntimeError, ValueError) as exception:
            return Periodic1DRankNUnresolvedProcrustesSelection(
                diagnostics=Periodic1DRankNProcrustesDiagnostics.numerically_unresolved(
                    case_identity=request.case_identity,
                    retained_rank=request.retained_rank,
                    circuit_depth=request.circuit_depth,
                    gauge_alignment=request.gauge_alignment,
                    selection_mesh_size=request.selection_mesh_size,
                    backend_exception_code=(
                        Periodic1DRankNAlignmentBackendExceptionCode.from_procrustes_exception(
                            exception
                        )
                    ),
                )
            )
        diagnostics = Periodic1DRankNProcrustesDiagnosticsAnalyzer(
            case_identity=request.case_identity,
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
            alignment_integrity_tolerance=request.alignment_integrity_tolerance,
            gauge_alignment=request.gauge_alignment,
            selection_mesh_size=request.selection_mesh_size,
            source=request.source,
            target=request.target,
            result=result,
        ).execute()
        right_unitaries = NumpyImmutableArrayConstructor(
            result.right_unitary_completions,
            "right_unitaries",
            np.dtype(np.complex128),
        ).execute()
        return Periodic1DRankNResolvedProcrustesSelection(
            diagnostics=diagnostics,
            right_unitaries=right_unitaries,
        )


__all__ = [
    "Periodic1DRankNProcrustesSelection",
    "Periodic1DRankNProcrustesSelectionAnalyzer",
    "Periodic1DRankNProcrustesSelectionRequest",
    "Periodic1DRankNResolvedProcrustesSelection",
    "Periodic1DRankNUnresolvedProcrustesSelection",
]
