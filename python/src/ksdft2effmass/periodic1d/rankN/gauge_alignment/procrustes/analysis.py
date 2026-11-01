"""Procrustes selection diagnostics for higher-rank gauge alignment."""

from __future__ import annotations

import math
from typing import final

import numpy as np
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ..definition import Periodic1DRankNGaugeAlignment
from ..status import (
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
)
from .result import Periodic1DRankNProcrustesDiagnostics


@final
class Periodic1DRankNProcrustesDiagnosticsAnalyzer:
    """Construct complete diagnostics from one bound Procrustes outcome."""

    __slots__ = (
        "_case_identity",
        "_retained_rank",
        "_circuit_depth",
        "_alignment_integrity_tolerance",
        "_gauge_alignment",
        "_selection_mesh_size",
        "_source",
        "_target",
        "_result",
    )

    def __init__(
        self,
        *,
        case_identity: str,
        retained_rank: int,
        circuit_depth: int,
        alignment_integrity_tolerance: float,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        selection_mesh_size: int,
        source: ComplexArray,
        target: ComplexArray,
        result: NumpyBatchedComplexUnitaryProcrustesResult,
    ) -> None:
        if type(case_identity) is not str or not case_identity:
            raise ValueError("case_identity must be a nonempty built-in string")
        if type(retained_rank) is not int or retained_rank <= 0:
            raise ValueError("retained_rank must be a positive built-in integer")
        if type(circuit_depth) is not int or circuit_depth <= 0:
            raise ValueError("circuit_depth must be a positive built-in integer")
        if (
            type(alignment_integrity_tolerance) is not float
            or not math.isfinite(alignment_integrity_tolerance)
            or alignment_integrity_tolerance < 0.0
        ):
            raise ValueError(
                "alignment_integrity_tolerance must be finite and nonnegative"
            )
        if type(gauge_alignment) is not Periodic1DRankNGaugeAlignment:
            raise TypeError("gauge_alignment must be the exact rank-N enum")
        if type(selection_mesh_size) is not int or selection_mesh_size <= 0:
            raise ValueError("selection_mesh_size must be a positive built-in integer")
        if type(result) is not NumpyBatchedComplexUnitaryProcrustesResult:
            raise TypeError("result must be the exact Procrustes result type")
        self._case_identity = case_identity
        self._retained_rank = retained_rank
        self._circuit_depth = circuit_depth
        self._alignment_integrity_tolerance = alignment_integrity_tolerance
        self._gauge_alignment = gauge_alignment
        self._selection_mesh_size = selection_mesh_size
        self._source = source
        self._target = target
        self._result = result

    def execute(self) -> Periodic1DRankNProcrustesDiagnostics:
        """Return diagnostics for the bound successful Procrustes result."""
        return self._successful(self._result)

    def _successful(
        self,
        result: NumpyBatchedComplexUnitaryProcrustesResult,
    ) -> Periodic1DRankNProcrustesDiagnostics:
        residuals, unitarity, stationarity, objective_identity, psd = _integrity(
            self._source,
            self._target,
            result,
        )
        full_rank = bool(np.all(result.full_rank))
        integrity_passes = (
            max(unitarity, stationarity, objective_identity, psd)
            <= self._alignment_integrity_tolerance
        )
        if self._gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
            outcome = (
                Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT
                if not full_rank
                else (
                    Periodic1DRankNAlignmentStatus.QUALIFIED
                    if integrity_passes
                    else Periodic1DRankNAlignmentStatus.INTEGRITY_FAILED
                )
            )
        else:
            outcome = (
                Periodic1DRankNAlignmentStatus.POINTWISE_RANK_DEFICIENT
                if not full_rank
                else (
                    Periodic1DRankNAlignmentStatus.QUALIFIED
                    if integrity_passes
                    else Periodic1DRankNAlignmentStatus.INTEGRITY_FAILED
                )
            )
        selected = None
        if (
            self._gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            and outcome is Periodic1DRankNAlignmentStatus.QUALIFIED
        ):
            selected = ComplexMatrixQuantity(
                np.asarray(result.right_unitary_completions[0], dtype=np.complex128),
                Unitless(),
            )
        if result.backend_identifier is None or result.backend_version is None:
            raise ValueError("nonempty Procrustes selection requires backend evidence")
        return Periodic1DRankNProcrustesDiagnostics(
            status=Periodic1DRankNAlignmentStatusResult.from_disposition(
                case_identity=self._case_identity,
                retained_rank=self._retained_rank,
                circuit_depth=self._circuit_depth,
                construction_mesh_size=self._selection_mesh_size,
                gauge_alignment=self._gauge_alignment,
                status=outcome,
            ),
            selection_mesh_size=self._selection_mesh_size,
            cross_singular_values=np.asarray(
                result.cross_singular_values, dtype=np.float64
            ),
            numerical_ranks=np.asarray(result.numerical_ranks, dtype=np.int64),
            applied_rank_cutoffs=np.asarray(
                result.applied_rank_cutoffs, dtype=np.float64
            ),
            rank_margins=np.asarray(
                result.cross_singular_values[..., -1] - result.applied_rank_cutoffs,
                dtype=np.float64,
            ),
            spectral_condition_numbers=tuple(
                float(values[0] / values[-1])
                if rank == self._retained_rank and values[-1] > cutoff
                else None
                for values, rank, cutoff in zip(
                    result.cross_singular_values,
                    result.numerical_ranks,
                    result.applied_rank_cutoffs,
                    strict=True,
                )
            ),
            deficient_point_indices=(
                tuple(int(index) for index in np.flatnonzero(~result.full_rank))
                if self._gauge_alignment
                is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                else ()
            ),
            deficient_point_count=(
                int(np.count_nonzero(~result.full_rank))
                if self._gauge_alignment
                is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                else 0
            ),
            normalized_optimal_residuals=residuals,
            normalized_objective_maximum=float(np.max(residuals)),
            normalized_objective_rms=float(np.sqrt(np.mean(residuals**2))),
            minimum_rank_margin=float(
                np.min(
                    result.cross_singular_values[..., -1] - result.applied_rank_cutoffs
                )
            ),
            maximum_unitarity_defect=unitarity,
            maximum_stationarity_defect=stationarity,
            maximum_objective_identity_defect=objective_identity,
            maximum_psd_defect=psd,
            selected_global_right_unitary=selected,
            backend_identifier=result.backend_identifier,
            backend_version=result.backend_version,
        )


def _integrity(
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> tuple[RealArray, float, float, float, float]:
    """Return normalized objective and structural integrity defects."""
    rank = result.right_unitary_completions.shape[-1]
    right = result.right_unitary_completions
    residuals = np.asarray(
        result.optimal_residual_frobenius_norms / math.sqrt(rank),
        dtype=np.float64,
    )
    identity = np.eye(rank, dtype=np.complex128)
    unitary = float(
        np.max(
            np.linalg.norm(
                _adjoint(right) @ right - identity,
                axis=(-2, -1),
            )
        )
    )
    cross = _adjoint(source) @ target
    stationary = _adjoint(right) @ cross
    stationarity = float(
        np.max(
            np.linalg.norm(
                stationary - _adjoint(stationary),
                axis=(-2, -1),
            )
        )
        / math.sqrt(rank)
    )
    direct_objectives = (
        np.sum(
            np.abs(source @ right - target) ** 2,
            axis=(-2, -1),
            dtype=np.float64,
        )
        / rank
    )
    covariance_objectives = 2.0 - (2.0 / rank) * np.real(
        np.trace(_adjoint(cross) @ right, axis1=-2, axis2=-1)
    )
    objective_identity = float(
        np.max(np.abs(direct_objectives - covariance_objectives))
    )
    hermitian_part = 0.5 * (stationary + _adjoint(stationary))
    minimum_eigenvalues = np.linalg.eigvalsh(hermitian_part)[..., 0]
    psd_defect = float(max(0.0, -float(np.min(minimum_eigenvalues))))
    return residuals, unitary, stationarity, objective_identity, psd_defect


def _adjoint(value: ComplexArray) -> ComplexArray:
    """Return the adjoint over the final two array axes."""
    return np.swapaxes(value.conjugate(), -1, -2)


__all__ = ["Periodic1DRankNProcrustesDiagnosticsAnalyzer"]
