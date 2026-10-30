"""Gauge-aligned represented-operator and frame fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.validation import (
    NumpyImmutableArrayConstructor,
    NumpyImmutableArrayValidator,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.analysis.matrix_field.diagnostics import MatrixFieldIsometryAnalyzer

from ..calculation import Periodic1DHigherRankAlignmentCalculationRequest
from ..diagnostics import Periodic1DHigherRankProcrustesDiagnostics
from ..model import Periodic1DHigherRankAnalyticCase
from .definition import Periodic1DHigherRankGaugeAlignment


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankGaugeAlignedFields:
    """Store immutable represented operators and frames for one gauge alignment."""

    case_identity: str
    gauge_alignment: Periodic1DHigherRankGaugeAlignment
    coordinates: RealArray
    represented_operators: ComplexArray
    frames: ComplexArray

    def __post_init__(self) -> None:
        if type(self.case_identity) is not str or not self.case_identity:
            raise ValueError("case_identity must be a nonempty built-in string")
        if type(self.gauge_alignment) is not Periodic1DHigherRankGaugeAlignment:
            raise TypeError("gauge_alignment must be the exact gauge-alignment enum")
        coordinates = NumpyImmutableArrayValidator(
            self.coordinates,
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        represented_operators = NumpyImmutableArrayValidator(
            self.represented_operators,
            "represented_operators",
            np.dtype(np.complex128),
        ).execute()
        frames = NumpyImmutableArrayValidator(
            self.frames,
            "frames",
            np.dtype(np.complex128),
        ).execute()
        if coordinates.ndim != 1:
            raise ValueError("coordinates must be one-dimensional")
        if represented_operators.ndim != 3 or frames.ndim != 3:
            raise ValueError(
                "represented operators and frames must be rank-three arrays"
            )
        if represented_operators.shape[0] != coordinates.size:
            raise ValueError("represented operators must match the coordinate count")
        if frames.shape[0] != coordinates.size:
            raise ValueError("frames must match the coordinate count")
        rank = represented_operators.shape[-1]
        if represented_operators.shape[1:] != (rank, rank):
            raise ValueError("represented operators must be square")
        if frames.shape[-1] != rank:
            raise ValueError("frame rank must match the represented-operator rank")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankGaugeAlignmentConstructionRequest:
    """Bind the scientific inputs for constructing one gauge-aligned field pair."""

    calculation_request: Periodic1DHigherRankAlignmentCalculationRequest
    model: Periodic1DHigherRankAnalyticCase
    gauge_alignment: Periodic1DHigherRankGaugeAlignment
    coordinates: RealArray
    global_selection: Periodic1DHigherRankProcrustesDiagnostics
    pointwise_alignment: NumpyBatchedComplexUnitaryProcrustesResult | None = None

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DHigherRankAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.model) is not Periodic1DHigherRankAnalyticCase:
            raise TypeError("model must be Periodic1DHigherRankAnalyticCase")
        if type(self.gauge_alignment) is not Periodic1DHigherRankGaugeAlignment:
            raise TypeError("gauge_alignment must be the exact gauge-alignment enum")
        if type(self.global_selection) is not Periodic1DHigherRankProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        coordinates = NumpyImmutableArrayValidator(
            self.coordinates,
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim != 1:
            raise ValueError("coordinates must be one-dimensional")
        request = self.calculation_request
        if (
            self.model.retained_rank != request.retained_rank
            or self.model.circuit_depth != request.circuit_depth
        ):
            raise ValueError("model rank and depth must match the calculation request")
        if self.gauge_alignment not in request.configuration.gauge_alignments:
            raise ValueError("gauge alignment must belong to the calculation request")
        selection_status = self.global_selection.status
        if (
            selection_status.case_identity != request.case_identity
            or selection_status.retained_rank != request.retained_rank
            or selection_status.circuit_depth != request.circuit_depth
            or selection_status.gauge_alignment
            is not Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY
            or selection_status.construction_mesh_size
            != request.configuration.global_unitary_selection_mesh_size
            or self.global_selection.selection_mesh_size
            != request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must match the calculation request")
        if self.gauge_alignment is Periodic1DHigherRankGaugeAlignment.POINTWISE_UNITARY:
            if (
                type(self.pointwise_alignment)
                is not NumpyBatchedComplexUnitaryProcrustesResult
            ):
                raise TypeError(
                    "pointwise alignment requires the exact Procrustes result"
                )
            if (
                self.pointwise_alignment.row_count != self.model.ambient_dimension
                or self.pointwise_alignment.batch_shape != (coordinates.size,)
                or not bool(self.pointwise_alignment.full_rank.all())
            ):
                raise ValueError(
                    "pointwise alignment must be full rank and match the coordinates"
                )
        elif self.pointwise_alignment is not None:
            raise ValueError(
                "pointwise_alignment is reserved for pointwise-unitary alignment"
            )


@final
class Periodic1DHigherRankGaugeAlignmentConstructor:
    """Construct represented operators and frames in one prescribed gauge alignment."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DHigherRankGaugeAlignmentConstructionRequest,
    ) -> None:
        if type(request) is not Periodic1DHigherRankGaugeAlignmentConstructionRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankGaugeAlignmentConstructionRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DHigherRankGaugeAlignmentConstructionRequest:
        """Return the exact request bound to this constructor."""
        return self._request

    def execute(self) -> Periodic1DHigherRankGaugeAlignedFields:
        """Return immutable represented operators and frames in the selected gauge."""
        request = self._request
        model = request.model
        coordinates = request.coordinates
        rank = model.retained_rank
        attacked = model.attacked_reduced_hamiltonians(coordinates)
        attacked_frames = model.attacked_frames(coordinates)
        gauge_alignment = request.gauge_alignment
        if gauge_alignment is Periodic1DHigherRankGaugeAlignment.IDENTITY:
            right_action = np.broadcast_to(
                np.eye(rank, dtype=np.complex128),
                (coordinates.size, rank, rank),
            )
        elif gauge_alignment is Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY:
            selected = request.global_selection.selected_global_right_unitary
            if selected is None:
                raise ValueError(
                    "global-unitary alignment requires a selected right unitary"
                )
            right_action = np.broadcast_to(
                selected.magnitude,
                (coordinates.size, rank, rank),
            )
        elif gauge_alignment is Periodic1DHigherRankGaugeAlignment.POINTWISE_UNITARY:
            pointwise_alignment = request.pointwise_alignment
            if pointwise_alignment is None:
                raise ValueError("pointwise alignment requires a Procrustes result")
            right_action = pointwise_alignment.right_unitary_completions
        else:
            gauge = model.gauge_unitaries(coordinates)
            right_action = np.swapaxes(gauge.conjugate(), -1, -2)
        if right_action.shape != (coordinates.size, rank, rank):
            raise ValueError("gauge right action must match the case and coordinates")
        right_isometry = MatrixFieldIsometryAnalyzer().execute(right_action)
        if (
            right_isometry.normalized_maximum_frobenius_defect
            > request.calculation_request.controls.model_structure_tolerance
        ):
            raise ValueError("gauge right action must remain unitary")
        right_adjoint = np.swapaxes(right_action.conjugate(), -1, -2)
        represented_operators = np.asarray(
            right_adjoint @ attacked @ right_action,
            dtype=np.complex128,
        )
        frames = np.asarray(attacked_frames @ right_action, dtype=np.complex128)
        return Periodic1DHigherRankGaugeAlignedFields(
            case_identity=request.calculation_request.case_identity,
            gauge_alignment=gauge_alignment,
            coordinates=coordinates,
            represented_operators=NumpyImmutableArrayConstructor(
                represented_operators,
                "represented_operators",
                np.dtype(np.complex128),
            ).execute(),
            frames=NumpyImmutableArrayConstructor(
                frames,
                "frames",
                np.dtype(np.complex128),
            ).execute(),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankGaugeAlignmentEvaluationRequest:
    """Bind one direct represented-operator evaluation in a prescribed gauge."""

    calculation_request: Periodic1DHigherRankAlignmentCalculationRequest
    model: Periodic1DHigherRankAnalyticCase
    gauge_alignment: Periodic1DHigherRankGaugeAlignment
    coordinates: RealArray
    global_selection: Periodic1DHigherRankProcrustesDiagnostics

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DHigherRankAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.model) is not Periodic1DHigherRankAnalyticCase:
            raise TypeError("model must be Periodic1DHigherRankAnalyticCase")
        if type(self.gauge_alignment) is not Periodic1DHigherRankGaugeAlignment:
            raise TypeError("gauge_alignment must be the exact gauge-alignment enum")
        if type(self.global_selection) is not Periodic1DHigherRankProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        coordinates = NumpyImmutableArrayValidator(
            self.coordinates,
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim != 1:
            raise ValueError("coordinates must be one-dimensional")
        calculation_request = self.calculation_request
        if (
            self.model.retained_rank != calculation_request.retained_rank
            or self.model.circuit_depth != calculation_request.circuit_depth
        ):
            raise ValueError("model rank and depth must match the calculation request")
        if (
            self.gauge_alignment
            not in calculation_request.configuration.gauge_alignments
        ):
            raise ValueError("gauge alignment must belong to the calculation request")
        selection_status = self.global_selection.status
        if (
            selection_status.case_identity != calculation_request.case_identity
            or selection_status.retained_rank != calculation_request.retained_rank
            or selection_status.circuit_depth != calculation_request.circuit_depth
            or selection_status.gauge_alignment
            is not Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY
            or selection_status.construction_mesh_size
            != calculation_request.configuration.global_unitary_selection_mesh_size
            or self.global_selection.selection_mesh_size
            != calculation_request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must match the calculation request")


@final
class Periodic1DHigherRankGaugeAlignmentEvaluator:
    """Evaluate the analytic represented operator in one prescribed gauge."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DHigherRankGaugeAlignmentEvaluationRequest,
    ) -> None:
        if type(request) is not Periodic1DHigherRankGaugeAlignmentEvaluationRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankGaugeAlignmentEvaluationRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DHigherRankGaugeAlignmentEvaluationRequest:
        """Return the exact direct-evaluation request bound to this action."""
        return self._request

    def execute(self) -> ComplexArray:
        """Return the immutable direct represented-operator field."""
        request = self._request
        model = request.model
        coordinates = request.coordinates
        gauge_alignment = request.gauge_alignment
        if gauge_alignment is Periodic1DHigherRankGaugeAlignment.IDENTITY:
            values = model.attacked_reduced_hamiltonians(coordinates)
        elif gauge_alignment is Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY:
            selected = request.global_selection.selected_global_right_unitary
            if selected is None:
                raise ValueError(
                    "global-unitary direct evaluation requires a selected unitary"
                )
            attacked = model.attacked_reduced_hamiltonians(coordinates)
            right = np.broadcast_to(
                selected.magnitude,
                (coordinates.size, model.retained_rank, model.retained_rank),
            )
            adjoint = np.swapaxes(right.conjugate(), -1, -2)
            values = np.asarray(adjoint @ attacked @ right, dtype=np.complex128)
        else:
            values = model.exact_reduced_hamiltonians(coordinates)
        return NumpyImmutableArrayConstructor(
            values,
            "direct_represented_operators",
            np.dtype(np.complex128),
        ).execute()


__all__ = [
    "Periodic1DHigherRankGaugeAlignedFields",
    "Periodic1DHigherRankGaugeAlignmentConstructionRequest",
    "Periodic1DHigherRankGaugeAlignmentConstructor",
    "Periodic1DHigherRankGaugeAlignmentEvaluationRequest",
    "Periodic1DHigherRankGaugeAlignmentEvaluator",
]
