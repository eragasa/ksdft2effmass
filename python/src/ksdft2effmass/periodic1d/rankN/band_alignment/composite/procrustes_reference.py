"""Producer-independent Procrustes reference for higher-rank gauge alignment.

This bounded reference reconstructs the analytic attack matrices directly and uses an
Hermitian eigendecomposition of the cross Gram matrix for the global polar factor.  It
does not invoke the maintained model, Procrustes solver, or producer analysis actions.
The slice covers the one global-unitary selection and all three pointwise-unitary
selections; it is not complete protocol verification.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

import numpy as np
from projectkoios.physkit.numerics.typing.numpy.arrays import (
    ComplexArray,
    IntegerArray,
    RealArray,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.result import (
    Periodic1DRankNProcrustesDiagnostics,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentStatus,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..calculation_result import Periodic1DRankNAlignmentCalculationResult
from .analytic_reference import (
    _Periodic1DRankNAnalyticReferenceModel,
    _reduced_coordinates,
)

_REFERENCE_SCALAR_ABSOLUTE_TOLERANCE = 1.0e-11
_REFERENCE_ARRAY_ABSOLUTE_TOLERANCE = 1.0e-10


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNProcrustesReferenceRequest:
    """Bind one exact producer result to the bounded Procrustes reference action."""

    calculation_result: Periodic1DRankNAlignmentCalculationResult

    def __post_init__(self) -> None:
        if (
            type(self.calculation_result)
            is not Periodic1DRankNAlignmentCalculationResult
        ):
            raise TypeError("calculation_result must be the exact calculation result")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNProcrustesReference:
    """Store immutable independently reconstructed Procrustes comparisons."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(key) is not str
            or not key
            or type(value) is not MaximumAbsoluteErrorComparison
            for key, value in self.comparisons.items()
        ):
            raise TypeError("comparison inventory contains an invalid entry")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@dataclass(frozen=True, slots=True)
class _ProcrustesValues:
    singular_values: RealArray
    numerical_ranks: IntegerArray
    cutoffs: RealArray
    margins: RealArray
    condition_numbers: RealArray
    residuals: RealArray
    objective_maximum: float
    objective_rms: float
    minimum_rank_margin: float
    unitarity_defect: float
    stationarity_defect: float
    objective_identity_defect: float
    psd_defect: float
    right_unitaries: ComplexArray


@final
class Periodic1DRankNProcrustesReferenceAnalyzer:
    """Recompute global and pointwise selections without the producer solver."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DRankNProcrustesReferenceRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNProcrustesReferenceRequest:
            raise TypeError("request must be the exact Procrustes reference request")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNProcrustesReferenceRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNProcrustesReference:
        """Return bounded global and pointwise Procrustes comparisons."""
        calculation = self._request.calculation_result
        request = calculation.request
        rank = request.retained_rank
        depth = request.circuit_depth
        configuration = request.configuration
        reference_model = _Periodic1DRankNAnalyticReferenceModel(rank, depth)
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}

        global_size = configuration.global_unitary_selection_mesh_size
        global_coordinates = _reduced_coordinates(global_size)
        global_gauge = reference_model.gauge_unitaries(global_coordinates)
        global_cross = np.mean(
            np.swapaxes(global_gauge.conjugate(), -1, -2),
            axis=0,
        )[None, ...]
        global_right = _polar_factors(global_cross)
        global_values = _values(
            crosses=global_cross,
            right_unitaries=global_right,
            gauges=global_gauge,
            rank_absolute_tolerance=configuration.rank_absolute_tolerance,
            rank_relative_tolerance=configuration.rank_relative_tolerance,
            global_selection=True,
        )
        _add_selection_comparisons(
            comparisons,
            f"global-selection[{global_size}]",
            global_values,
            calculation.global_selection,
        )
        selected = calculation.global_selection.selected_global_right_unitary
        if selected is None:
            raise ValueError("qualified global selection must retain its right unitary")
        comparisons[f"global-selection[{global_size}].right_unitary"] = _comparison(
            ComplexMatrixQuantity(global_right[0], Unitless()),
            selected,
            _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
        )

        for mesh in calculation.meshes:
            size = mesh.construction_mesh_size
            coordinates = _reduced_coordinates(size)
            gauge = reference_model.gauge_unitaries(coordinates)
            cross = np.swapaxes(gauge.conjugate(), -1, -2)
            pointwise_values = _values(
                crosses=cross,
                right_unitaries=cross,
                gauges=gauge,
                rank_absolute_tolerance=configuration.rank_absolute_tolerance,
                rank_relative_tolerance=configuration.rank_relative_tolerance,
                global_selection=False,
            )
            _add_selection_comparisons(
                comparisons,
                f"mesh[{size}].pointwise-selection",
                pointwise_values,
                mesh.pointwise_selection,
            )

        return Periodic1DRankNProcrustesReference(comparisons=comparisons)


def _polar_factors(crosses: ComplexArray) -> ComplexArray:
    """Return unique right polar factors through Hermitian eigendecomposition."""
    gram = np.swapaxes(crosses.conjugate(), -1, -2) @ crosses
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    if bool((eigenvalues <= 0.0).any()):
        raise ValueError("bounded Procrustes reference requires positive cross Gram")
    inverse_roots = 1.0 / np.sqrt(eigenvalues)
    inverse_square_roots = (eigenvectors * inverse_roots[..., None, :]) @ np.swapaxes(
        eigenvectors.conjugate(), -1, -2
    )
    return np.asarray(crosses @ inverse_square_roots, dtype=np.complex128)


def _values(
    *,
    crosses: ComplexArray,
    right_unitaries: ComplexArray,
    gauges: ComplexArray,
    rank_absolute_tolerance: float,
    rank_relative_tolerance: float,
    global_selection: bool,
) -> _ProcrustesValues:
    rank = crosses.shape[-1]
    gram = np.swapaxes(crosses.conjugate(), -1, -2) @ crosses
    eigenvalues = np.linalg.eigvalsh(gram)
    singular_values = np.sqrt(np.maximum(eigenvalues, 0.0))[..., ::-1]
    cutoffs = np.maximum(
        rank_absolute_tolerance,
        rank_relative_tolerance * singular_values[..., 0],
    )
    numerical_ranks = np.sum(
        singular_values > cutoffs[..., None],
        axis=-1,
        dtype=np.int64,
    )
    margins = singular_values[..., -1] - cutoffs
    condition_numbers = singular_values[..., 0] / singular_values[..., -1]

    if global_selection:
        differences = gauges @ right_unitaries[0] - np.eye(rank, dtype=np.complex128)
        squared_residuals = np.asarray(
            [np.mean(np.sum(np.abs(differences) ** 2, axis=(-2, -1)))],
            dtype=np.float64,
        )
    else:
        differences = gauges @ right_unitaries - np.eye(rank, dtype=np.complex128)
        squared_residuals = np.sum(
            np.abs(differences) ** 2,
            axis=(-2, -1),
            dtype=np.float64,
        )
    residuals = np.sqrt(squared_residuals / rank)

    adjoint_right = np.swapaxes(right_unitaries.conjugate(), -1, -2)
    stationary = adjoint_right @ crosses
    adjoint_stationary = np.swapaxes(stationary.conjugate(), -1, -2)
    identity = np.eye(rank, dtype=np.complex128)
    unitarity = float(
        np.max(
            np.linalg.norm(
                adjoint_right @ right_unitaries - identity,
                axis=(-2, -1),
            )
        )
    )
    stationarity = float(
        np.max(np.linalg.norm(stationary - adjoint_stationary, axis=(-2, -1)))
        / math.sqrt(rank)
    )
    direct_objectives = squared_residuals / rank
    covariance_objectives = 2.0 - (2.0 / rank) * np.real(
        np.trace(
            np.swapaxes(crosses.conjugate(), -1, -2) @ right_unitaries,
            axis1=-2,
            axis2=-1,
        )
    )
    objective_identity = float(
        np.max(np.abs(direct_objectives - covariance_objectives))
    )
    hermitian_part = 0.5 * (stationary + adjoint_stationary)
    psd = float(max(0.0, -float(np.min(np.linalg.eigvalsh(hermitian_part)[..., 0]))))
    return _ProcrustesValues(
        singular_values=np.asarray(singular_values, dtype=np.float64),
        numerical_ranks=np.asarray(numerical_ranks, dtype=np.int64),
        cutoffs=np.asarray(cutoffs, dtype=np.float64),
        margins=np.asarray(margins, dtype=np.float64),
        condition_numbers=np.asarray(condition_numbers, dtype=np.float64),
        residuals=np.asarray(residuals, dtype=np.float64),
        objective_maximum=float(np.max(residuals)),
        objective_rms=float(np.sqrt(np.mean(residuals**2))),
        minimum_rank_margin=float(np.min(margins)),
        unitarity_defect=unitarity,
        stationarity_defect=stationarity,
        objective_identity_defect=objective_identity,
        psd_defect=psd,
        right_unitaries=right_unitaries,
    )


def _add_selection_comparisons(
    comparisons: dict[str, MaximumAbsoluteErrorComparison],
    prefix: str,
    calculated: _ProcrustesValues,
    observed: Periodic1DRankNProcrustesDiagnostics,
) -> None:
    if type(observed) is not Periodic1DRankNProcrustesDiagnostics:
        raise TypeError("observed selection must be exact Procrustes diagnostics")
    if observed.status.status is not Periodic1DRankNAlignmentStatus.QUALIFIED:
        raise ValueError("bounded Procrustes reference requires qualified selections")
    if any(value is None for value in observed.spectral_condition_numbers):
        raise ValueError("qualified bounded selection must retain condition numbers")
    scalar_observed = (
        observed.normalized_objective_maximum,
        observed.normalized_objective_rms,
        observed.minimum_rank_margin,
        observed.maximum_unitarity_defect,
        observed.maximum_stationarity_defect,
        observed.maximum_objective_identity_defect,
        observed.maximum_psd_defect,
    )
    if any(value is None for value in scalar_observed):
        raise ValueError(
            "qualified bounded selection must retain integrity diagnostics"
        )

    for name, calculated_array, observed_array in (
        (
            "cross_singular_values",
            MatrixQuantity(calculated.singular_values, Unitless()),
            MatrixQuantity(observed.cross_singular_values, Unitless()),
        ),
        (
            "numerical_ranks",
            VectorQuantity(
                np.asarray(calculated.numerical_ranks, dtype=np.float64), Unitless()
            ),
            VectorQuantity(
                np.asarray(observed.numerical_ranks, dtype=np.float64), Unitless()
            ),
        ),
        (
            "applied_rank_cutoffs",
            VectorQuantity(calculated.cutoffs, Unitless()),
            VectorQuantity(observed.applied_rank_cutoffs, Unitless()),
        ),
        (
            "rank_margins",
            VectorQuantity(calculated.margins, Unitless()),
            VectorQuantity(observed.rank_margins, Unitless()),
        ),
        (
            "spectral_condition_numbers",
            VectorQuantity(calculated.condition_numbers, Unitless()),
            VectorQuantity(
                np.asarray(observed.spectral_condition_numbers, dtype=np.float64),
                Unitless(),
            ),
        ),
        (
            "normalized_optimal_residuals",
            VectorQuantity(calculated.residuals, Unitless()),
            VectorQuantity(observed.normalized_optimal_residuals, Unitless()),
        ),
    ):
        comparisons[f"{prefix}.{name}"] = _comparison(
            calculated_array,
            observed_array,
            _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
        )

    assert observed.normalized_objective_maximum is not None
    assert observed.normalized_objective_rms is not None
    assert observed.minimum_rank_margin is not None
    assert observed.maximum_unitarity_defect is not None
    assert observed.maximum_stationarity_defect is not None
    assert observed.maximum_objective_identity_defect is not None
    assert observed.maximum_psd_defect is not None
    for name, calculated_scalar, observed_scalar in (
        (
            "normalized_objective_maximum",
            calculated.objective_maximum,
            observed.normalized_objective_maximum,
        ),
        (
            "normalized_objective_rms",
            calculated.objective_rms,
            observed.normalized_objective_rms,
        ),
        (
            "minimum_rank_margin",
            calculated.minimum_rank_margin,
            observed.minimum_rank_margin,
        ),
        (
            "maximum_unitarity_defect",
            calculated.unitarity_defect,
            observed.maximum_unitarity_defect,
        ),
        (
            "maximum_stationarity_defect",
            calculated.stationarity_defect,
            observed.maximum_stationarity_defect,
        ),
        (
            "maximum_objective_identity_defect",
            calculated.objective_identity_defect,
            observed.maximum_objective_identity_defect,
        ),
        ("maximum_psd_defect", calculated.psd_defect, observed.maximum_psd_defect),
        (
            "deficient_point_count",
            float(
                np.count_nonzero(
                    calculated.numerical_ranks != calculated.singular_values.shape[-1]
                )
            ),
            float(observed.deficient_point_count),
        ),
    ):
        comparisons[f"{prefix}.{name}"] = _comparison(
            ScalarQuantity(calculated_scalar, Unitless()),
            ScalarQuantity(observed_scalar, Unitless()),
            _REFERENCE_SCALAR_ABSOLUTE_TOLERANCE,
        )


def _comparison(
    calculated: (
        ScalarQuantity | VectorQuantity | MatrixQuantity | ComplexMatrixQuantity
    ),
    expected: ScalarQuantity | VectorQuantity | MatrixQuantity | ComplexMatrixQuantity,
    tolerance: float,
) -> MaximumAbsoluteErrorComparison:
    return MaximumAbsoluteErrorComparison(
        observed=calculated,
        reference=expected,
        tolerance=ScalarQuantity(tolerance, calculated.unit),
    )


__all__ = [
    "Periodic1DRankNProcrustesReference",
    "Periodic1DRankNProcrustesReferenceAnalyzer",
    "Periodic1DRankNProcrustesReferenceRequest",
]
