"""Construct rank-two Procrustes selection diagnostics."""

from __future__ import annotations

import math

import numpy as np
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from .result import (
    Periodic1DRank2ProcrustesDiagnostics,
    Periodic1DRank2ProcrustesSelectionScope,
)


class Periodic1DRank2ProcrustesDiagnosticsAnalyzer:
    """Construct complete diagnostics from one successful rank-two selection."""

    __slots__ = ("_scope", "_source", "_target", "_result")

    def __init__(
        self,
        *,
        scope: Periodic1DRank2ProcrustesSelectionScope,
        source: ComplexArray,
        target: ComplexArray,
        result: NumpyBatchedComplexUnitaryProcrustesResult,
    ) -> None:
        if type(scope) is not Periodic1DRank2ProcrustesSelectionScope:
            raise TypeError("scope must be the exact rank-two selection scope")
        if type(result) is not NumpyBatchedComplexUnitaryProcrustesResult:
            raise TypeError("result must be the exact Procrustes result type")
        if source.shape != target.shape or source.ndim != 3 or source.shape[-1] != 2:
            raise ValueError(
                "source and target must be correlated batched rank-two arrays"
            )
        expected_count = source.shape[0]
        if result.right_unitary_completions.shape != (expected_count, 2, 2):
            raise ValueError("Procrustes outcome does not match the source inventory")
        if (
            scope is Periodic1DRank2ProcrustesSelectionScope.GLOBAL
            and expected_count != 1
        ):
            raise ValueError("global diagnostics require one stacked selection")
        self._scope = scope
        self._source = source
        self._target = target
        self._result = result

    def execute(self) -> Periodic1DRank2ProcrustesDiagnostics:
        """Return rank, objective, integrity, and backend evidence."""
        result = self._result
        if not bool(np.all(result.full_rank)):
            raise ValueError(
                "rank-two Procrustes selection must be numerically full rank"
            )
        if result.backend_identifier is None or result.backend_version is None:
            raise ValueError("Procrustes selection must identify its numerical backend")
        residuals, unitarity, stationarity, objective_identity, psd = _integrity(
            self._source,
            self._target,
            result,
        )
        singular = np.asarray(result.cross_singular_values, dtype=np.float64)
        cutoffs = np.asarray(result.applied_rank_cutoffs, dtype=np.float64)
        margins = np.asarray(singular[:, -1] - cutoffs, dtype=np.float64)
        return Periodic1DRank2ProcrustesDiagnostics(
            scope=self._scope,
            selection_count=self._source.shape[0],
            cross_singular_values=singular,
            numerical_ranks=np.asarray(result.numerical_ranks, dtype=np.int64),
            applied_rank_cutoffs=cutoffs,
            rank_margins=margins,
            spectral_condition_numbers=tuple(
                float(values[0] / values[-1]) for values in singular
            ),
            normalized_optimal_residuals=residuals,
            normalized_objective_maximum=float(np.max(residuals)),
            normalized_objective_rms=float(np.sqrt(np.mean(residuals**2))),
            minimum_rank_margin=float(np.min(margins)),
            maximum_unitarity_defect=unitarity,
            maximum_stationarity_defect=stationarity,
            maximum_objective_identity_defect=objective_identity,
            maximum_psd_defect=psd,
            backend_identifier=result.backend_identifier,
            backend_version=result.backend_version,
        )


def _integrity(
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> tuple[RealArray, float, float, float, float]:
    """Return normalized objective and structural integrity defects."""
    rank = 2
    right = result.right_unitary_completions
    residuals = np.asarray(
        result.optimal_residual_frobenius_norms / math.sqrt(rank),
        dtype=np.float64,
    )
    identity = np.eye(rank, dtype=np.complex128)
    adjoint_right = _adjoint(right)
    unitarity = float(
        np.max(np.linalg.norm(adjoint_right @ right - identity, axis=(-2, -1)))
    )
    cross = _adjoint(source) @ target
    stationary = adjoint_right @ cross
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
        np.sum(np.abs(source @ right - target) ** 2, axis=(-2, -1), dtype=np.float64)
        / rank
    )
    covariance_objectives = (
        np.sum(np.abs(source) ** 2, axis=(-2, -1), dtype=np.float64)
        + np.sum(np.abs(target) ** 2, axis=(-2, -1), dtype=np.float64)
        - 2.0 * np.real(np.trace(_adjoint(cross) @ right, axis1=-2, axis2=-1))
    ) / rank
    objective_identity = float(
        np.max(np.abs(direct_objectives - covariance_objectives))
    )
    hermitian_part = 0.5 * (stationary + _adjoint(stationary))
    minimum_eigenvalues = np.linalg.eigvalsh(hermitian_part)[..., 0]
    psd_defect = float(max(0.0, -float(np.min(minimum_eigenvalues))))
    return residuals, unitarity, stationarity, objective_identity, psd_defect


def _adjoint(value: ComplexArray) -> ComplexArray:
    """Return the adjoint over the final two array axes."""
    return np.swapaxes(value.conjugate(), -1, -2)


__all__ = ["Periodic1DRank2ProcrustesDiagnosticsAnalyzer"]
