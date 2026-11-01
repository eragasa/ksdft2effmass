"""Procrustes selection diagnostics for higher-rank gauge alignment."""

from __future__ import annotations

import math

import numpy as np
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)

from ..calculation import Periodic1DRankNAlignmentCalculationRequest
from ..definition import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
)
from ..diagnostics import Periodic1DRankNProcrustesDiagnostics
from ..result import Periodic1DRankNAlignmentStatusResult
from .mesh import _status


def _adjoint(value: ComplexArray) -> ComplexArray:
    return np.swapaxes(value.conjugate(), -1, -2)


def _procrustes_integrity(
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> tuple[RealArray, float, float, float, float]:
    rank = result.right_unitary_completions.shape[-1]
    right = result.right_unitary_completions
    residuals = np.asarray(
        result.optimal_residual_frobenius_norms / math.sqrt(rank),
        dtype=np.float64,
    )
    identity = np.eye(rank, dtype=np.complex128)
    unitary = float(
        np.max(np.linalg.norm(_adjoint(right) @ right - identity, axis=(-2, -1)))
    )
    cross = _adjoint(source) @ target
    stationary = _adjoint(right) @ cross
    stationarity = float(
        np.max(np.linalg.norm(stationary - _adjoint(stationary), axis=(-2, -1)))
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


def _procrustes_backend_exception_code(
    exception: ArithmeticError | RuntimeError | ValueError,
) -> Periodic1DRankNAlignmentBackendExceptionCode:
    if isinstance(exception, FloatingPointError):
        return Periodic1DRankNAlignmentBackendExceptionCode.ARITHMETIC_NONFINITE
    if isinstance(exception, (np.linalg.LinAlgError, RuntimeError)):
        return Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
    return Periodic1DRankNAlignmentBackendExceptionCode.VALIDATION_FAILED


def _failed_procrustes_record(
    *,
    request: Periodic1DRankNAlignmentCalculationRequest,
    gauge_alignment: Periodic1DRankNGaugeAlignment,
    selection_mesh_size: int,
    exception: ArithmeticError | RuntimeError | ValueError,
) -> Periodic1DRankNProcrustesDiagnostics:
    status = Periodic1DRankNAlignmentStatusResult(
        case_identity=request.case_identity,
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
        construction_mesh_size=selection_mesh_size,
        gauge_alignment=gauge_alignment,
        status=Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
        global_unitary_downstream_applicability=None,
        backend_exception_code=_procrustes_backend_exception_code(exception),
    )
    return Periodic1DRankNProcrustesDiagnostics(
        status=status,
        selection_mesh_size=selection_mesh_size,
        cross_singular_values=np.empty((0, request.retained_rank), dtype=np.float64),
        numerical_ranks=np.empty(0, dtype=np.int64),
        applied_rank_cutoffs=np.empty(0, dtype=np.float64),
        rank_margins=np.empty(0, dtype=np.float64),
        spectral_condition_numbers=(),
        deficient_point_indices=(),
        deficient_point_count=0,
        normalized_optimal_residuals=np.empty(0, dtype=np.float64),
        normalized_objective_maximum=None,
        normalized_objective_rms=None,
        minimum_rank_margin=None,
        maximum_unitarity_defect=None,
        maximum_stationarity_defect=None,
        maximum_objective_identity_defect=None,
        maximum_psd_defect=None,
        selected_global_right_unitary=None,
        backend_identifier=None,
        backend_version=None,
    )


def _procrustes_record(
    *,
    request: Periodic1DRankNAlignmentCalculationRequest,
    gauge_alignment: Periodic1DRankNGaugeAlignment,
    selection_mesh_size: int,
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> Periodic1DRankNProcrustesDiagnostics:
    full_rank = bool(np.all(result.full_rank))
    residuals, unitarity, stationarity, objective_identity, psd = _procrustes_integrity(
        source, target, result
    )
    integrity_passes = (
        max(
            unitarity,
            stationarity,
            objective_identity,
            psd,
        )
        <= request.controls.alignment_integrity_tolerance
    )
    if gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
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
        gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
        and outcome is Periodic1DRankNAlignmentStatus.QUALIFIED
    ):
        selected = ComplexMatrixQuantity(
            np.asarray(result.right_unitary_completions[0], dtype=np.complex128),
            Unitless(),
        )
    if result.backend_identifier is None or result.backend_version is None:
        raise ValueError("nonempty Procrustes selection requires backend evidence")
    return Periodic1DRankNProcrustesDiagnostics(
        status=_status(request, selection_mesh_size, gauge_alignment, outcome),
        selection_mesh_size=selection_mesh_size,
        cross_singular_values=np.asarray(
            result.cross_singular_values, dtype=np.float64
        ),
        numerical_ranks=np.asarray(result.numerical_ranks, dtype=np.int64),
        applied_rank_cutoffs=np.asarray(result.applied_rank_cutoffs, dtype=np.float64),
        rank_margins=np.asarray(
            result.cross_singular_values[..., -1] - result.applied_rank_cutoffs,
            dtype=np.float64,
        ),
        spectral_condition_numbers=tuple(
            float(values[0] / values[-1])
            if rank == request.retained_rank and values[-1] > cutoff
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
            if gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
            else ()
        ),
        deficient_point_count=(
            int(np.count_nonzero(~result.full_rank))
            if gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
            else 0
        ),
        normalized_optimal_residuals=residuals,
        normalized_objective_maximum=float(np.max(residuals)),
        normalized_objective_rms=float(np.sqrt(np.mean(residuals**2))),
        minimum_rank_margin=float(
            np.min(result.cross_singular_values[..., -1] - result.applied_rank_cutoffs)
        ),
        maximum_unitarity_defect=unitarity,
        maximum_stationarity_defect=stationarity,
        maximum_objective_identity_defect=objective_identity,
        maximum_psd_defect=psd,
        selected_global_right_unitary=selected,
        backend_identifier=result.backend_identifier,
        backend_version=result.backend_version,
    )
