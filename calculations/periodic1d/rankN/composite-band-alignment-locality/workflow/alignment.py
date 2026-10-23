"""Reviewed maximum-rule A1/A2 alignment selection for higher-rank D1."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import (
    immutable_complex128_array,
    validate_immutable_complex128_array,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ._validation import require_nonnegative_float
from .definition import FINAL_CONSTRUCTION_MESH_SIZE
from .numerical_backend import (
    HigherRankD1AlignmentBackendError,
    HigherRankD1BackendExceptionCode,
)
from .procrustes import higher_rank_d1_procrustes_tolerance


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankD1A1QualifiedSelection:
    """Retain one qualified final-mesh global right-unitary selection."""

    selection_mesh_size: int
    singular_values: tuple[float, ...]
    applied_rank_cutoff: float
    rank_margin: float
    condition_number: float
    direct_objective: float
    covariance_objective: float
    objective_identity_defect: float
    unitarity_defect: float
    stationarity_defect: float
    positive_semidefinite_defect: float
    transformation: Complex128Array = field(repr=False)
    status: str = "qualified"

    def __post_init__(self) -> None:
        """Validate exact status, values, ordering, and immutable transformation."""
        if type(self.selection_mesh_size) is not int or self.selection_mesh_size <= 0:
            raise ValueError("selection_mesh_size must be a positive built-in int")
        if type(self.singular_values) is not tuple or not self.singular_values:
            raise TypeError("singular_values must be a nonempty tuple")
        if tuple(sorted(self.singular_values, reverse=True)) != self.singular_values:
            raise ValueError("singular_values must be nonincreasing")
        for name in (
            "applied_rank_cutoff",
            "rank_margin",
            "condition_number",
            "direct_objective",
            "covariance_objective",
            "objective_identity_defect",
            "unitarity_defect",
            "stationarity_defect",
            "positive_semidefinite_defect",
        ):
            require_nonnegative_float(getattr(self, name), name)
        validate_immutable_complex128_array(self.transformation, "transformation")
        rank = len(self.singular_values)
        if self.transformation.shape != (rank, rank):
            raise ValueError("transformation shape must equal the selected rank")
        if self.status != "qualified":
            raise ValueError("status must be qualified")


@dataclass(frozen=True, slots=True)
class HigherRankD1A1RankDeficientSelection:
    """Retain aggregate evidence without inventing a global transformation."""

    selection_mesh_size: int
    singular_values: tuple[float, ...]
    applied_rank_cutoff: float
    rank_margin: float
    numerical_rank: int
    status: str = "aggregate-rank-deficient"

    def __post_init__(self) -> None:
        """Validate the bounded deficiency disposition and omitted transformation."""
        if type(self.selection_mesh_size) is not int or self.selection_mesh_size <= 0:
            raise ValueError("selection_mesh_size must be a positive built-in int")
        if type(self.singular_values) is not tuple or not self.singular_values:
            raise TypeError("singular_values must be a nonempty tuple")
        require_nonnegative_float(self.applied_rank_cutoff, "applied_rank_cutoff")
        if type(self.rank_margin) is not float or not math.isfinite(self.rank_margin):
            raise ValueError("rank_margin must be a finite built-in float")
        if self.rank_margin > 0.0:
            raise ValueError("a deficient rank margin must be nonpositive")
        if type(self.numerical_rank) is not int:
            raise TypeError("numerical_rank must be a built-in int")
        if not 0 <= self.numerical_rank < len(self.singular_values):
            raise ValueError("numerical_rank must be deficient")
        if self.status != "aggregate-rank-deficient":
            raise ValueError("status must be aggregate-rank-deficient")


@dataclass(frozen=True, slots=True)
class HigherRankD1A1NumericallyUnresolvedSelection:
    """Retain a bounded A1 backend-failure disposition without a transformation."""

    selection_mesh_size: int
    exception_code: HigherRankD1BackendExceptionCode
    status: str = "alignment-numerically-unresolved"

    def __post_init__(self) -> None:
        if self.selection_mesh_size != FINAL_CONSTRUCTION_MESH_SIZE:
            raise ValueError("A1 selection_mesh_size must equal the final D1 mesh")
        if type(self.exception_code) is not HigherRankD1BackendExceptionCode:
            raise TypeError("exception_code must be HigherRankD1BackendExceptionCode")
        if self.status != "alignment-numerically-unresolved":
            raise ValueError("status must be alignment-numerically-unresolved")


type HigherRankD1A1ComputedSelection = (
    HigherRankD1A1QualifiedSelection | HigherRankD1A1RankDeficientSelection
)
type HigherRankD1A1Selection = (
    HigherRankD1A1ComputedSelection | HigherRankD1A1NumericallyUnresolvedSelection
)


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankD1A2Selection:
    """Retain complete pointwise rank and integrity evidence for one mesh."""

    mesh_size: int
    smallest_singular_values: tuple[float, ...]
    applied_rank_cutoffs: tuple[float, ...]
    rank_margins: tuple[float, ...]
    numerical_ranks: tuple[int, ...]
    deficient_indices: tuple[int, ...]
    condition_number_minimum: float
    condition_number_maximum: float
    objective_maximum: float
    objective_rms: float
    unitarity_defect_maximum: float
    stationarity_defect_maximum: float
    objective_identity_defect_maximum: float
    positive_semidefinite_defect_maximum: float
    transformations: Complex128Array = field(repr=False)
    status: str = "qualified"

    def __post_init__(self) -> None:
        """Validate full pointwise coverage and immutable selected transformations."""
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        inventories: tuple[tuple[float, ...], ...] = (
            self.smallest_singular_values,
            self.applied_rank_cutoffs,
            self.rank_margins,
        )
        if any(type(values) is not tuple for values in inventories):
            raise TypeError("pointwise float inventories must be tuples")
        if any(len(values) != self.mesh_size for values in inventories):
            raise ValueError("pointwise float inventories must cover the mesh")
        if any(
            type(value) is not float or not math.isfinite(value)
            for values in inventories
            for value in values
        ):
            raise ValueError("pointwise float inventories must be finite")
        if (
            type(self.numerical_ranks) is not tuple
            or len(self.numerical_ranks) != self.mesh_size
        ):
            raise ValueError("numerical_ranks must cover the mesh")
        if any(type(value) is not int for value in self.numerical_ranks):
            raise TypeError("numerical_ranks must contain built-in integers")
        if self.deficient_indices != ():
            raise ValueError("a qualified A2 selection cannot retain deficient indices")
        for name in (
            "condition_number_minimum",
            "condition_number_maximum",
            "objective_maximum",
            "objective_rms",
            "unitarity_defect_maximum",
            "stationarity_defect_maximum",
            "objective_identity_defect_maximum",
            "positive_semidefinite_defect_maximum",
        ):
            require_nonnegative_float(getattr(self, name), name)
        validate_immutable_complex128_array(self.transformations, "transformations")
        rank = int(self.transformations.shape[-1])
        if self.transformations.shape != (self.mesh_size, rank, rank):
            raise ValueError("transformations must cover one square matrix per point")
        if any(value != rank for value in self.numerical_ranks):
            raise ValueError("qualified A2 numerical ranks must all equal rank")
        if self.status != "qualified":
            raise ValueError("status must be qualified")


@dataclass(frozen=True, slots=True)
class HigherRankD1A2RankDeficientSelection:
    """Retain complete pointwise rank evidence without completing null spaces."""

    mesh_size: int
    rank: int
    smallest_singular_values: tuple[float, ...]
    applied_rank_cutoffs: tuple[float, ...]
    rank_margins: tuple[float, ...]
    numerical_ranks: tuple[int, ...]
    deficient_indices: tuple[int, ...]
    status: str = "pointwise-rank-deficient"

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in int")
        inventories = (
            self.smallest_singular_values,
            self.applied_rank_cutoffs,
            self.rank_margins,
        )
        if any(type(values) is not tuple for values in inventories):
            raise TypeError("pointwise float inventories must be tuples")
        if any(len(values) != self.mesh_size for values in inventories):
            raise ValueError("pointwise float inventories must cover the mesh")
        if any(
            type(value) is not float or not math.isfinite(value)
            for values in inventories
            for value in values
        ):
            raise ValueError("pointwise float inventories must be finite")
        if (
            type(self.numerical_ranks) is not tuple
            or len(self.numerical_ranks) != self.mesh_size
            or any(type(value) is not int for value in self.numerical_ranks)
        ):
            raise TypeError("numerical_ranks must cover the mesh with built-in ints")
        if type(self.deficient_indices) is not tuple or not self.deficient_indices:
            raise ValueError("deficient_indices must be a nonempty tuple")
        expected = tuple(
            index
            for index, (smallest, cutoff) in enumerate(
                zip(
                    self.smallest_singular_values,
                    self.applied_rank_cutoffs,
                    strict=True,
                )
            )
            if smallest <= cutoff
        )
        if self.deficient_indices != expected:
            raise ValueError("deficient_indices must match the strict rank decisions")
        if any(not 0 <= value <= self.rank for value in self.numerical_ranks):
            raise ValueError("numerical_ranks must lie between zero and rank")
        if any(self.numerical_ranks[index] >= self.rank for index in expected):
            raise ValueError("deficient numerical ranks must be below rank")
        if self.status != "pointwise-rank-deficient":
            raise ValueError("status must be pointwise-rank-deficient")


@dataclass(frozen=True, slots=True)
class HigherRankD1A2NumericallyUnresolvedSelection:
    """Retain a bounded A2 backend-failure disposition without transformations."""

    mesh_size: int
    rank: int
    exception_code: HigherRankD1BackendExceptionCode
    status: str = "alignment-numerically-unresolved"

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in int")
        if type(self.exception_code) is not HigherRankD1BackendExceptionCode:
            raise TypeError("exception_code must be HigherRankD1BackendExceptionCode")
        if self.status != "alignment-numerically-unresolved":
            raise ValueError("status must be alignment-numerically-unresolved")


type HigherRankD1A2ComputedSelection = (
    HigherRankD1A2Selection | HigherRankD1A2RankDeficientSelection
)
type HigherRankD1A2SelectionResult = (
    HigherRankD1A2ComputedSelection | HigherRankD1A2NumericallyUnresolvedSelection
)


class HigherRankD1AlignmentSelector:
    """Select D1 A1/A2 right actions through the reviewed owner implementation."""

    __slots__ = ()

    @staticmethod
    def tolerance() -> ComplexUnitaryProcrustesTolerance:
        """Return the frozen D1 Procrustes tolerance."""
        return higher_rank_d1_procrustes_tolerance()

    def select_a1(
        self,
        candidate_frames: Complex128Array,
        reference_frames: Complex128Array,
    ) -> HigherRankD1A1ComputedSelection:
        """Select one equally weighted global unitary on the final mesh."""
        self._pointwise_definition(candidate_frames, reference_frames)
        mesh_size = int(candidate_frames.shape[0])
        if mesh_size != FINAL_CONSTRUCTION_MESH_SIZE:
            raise ValueError("A1 selection requires the final D1 mesh")
        rank = int(candidate_frames.shape[-1])
        scale = math.sqrt(float(mesh_size))
        source = immutable_complex128_array(
            np.asarray(
                candidate_frames.reshape((-1, rank)) / scale,
                dtype=np.complex128,
            ),
            "a1_source",
        )
        target = immutable_complex128_array(
            np.asarray(
                reference_frames.reshape((-1, rank)) / scale,
                dtype=np.complex128,
            ),
            "a1_target",
        )
        try:
            result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
                NumpyBatchedComplexUnitaryProcrustesDefinition.from_immutable_arrays(
                    source[None, :, :], target[None, :, :], self.tolerance()
                )
            )
        except (ValueError, FloatingPointError, RuntimeError) as error:
            raise HigherRankD1AlignmentBackendError(error) from error
        singular_values = tuple(
            float(value) for value in result.cross_singular_values[0]
        )
        cutoff = float(result.applied_rank_cutoffs[0])
        margin = float(result.cross_singular_values[0, -1] - cutoff)
        if not bool(result.full_rank[0]):
            return HigherRankD1A1RankDeficientSelection(
                selection_mesh_size=mesh_size,
                singular_values=singular_values,
                applied_rank_cutoff=cutoff,
                rank_margin=margin,
                numerical_rank=int(result.numerical_ranks[0]),
            )
        transformation = result.require_unique_right_unitary_transformations()[0]
        cross = np.asarray(
            np.mean(
                np.swapaxes(candidate_frames.conjugate(), -1, -2) @ reference_frames,
                axis=0,
            ),
            dtype=np.complex128,
        )
        residual = candidate_frames @ transformation - reference_frames
        direct = float(np.mean(np.sum(np.abs(residual) ** 2, axis=(-2, -1))) / rank)
        covariance = max(
            0.0,
            float(
                2.0
                - (2.0 / rank) * np.real(np.trace(cross.conjugate().T @ transformation))
            ),
        )
        integrity = self._integrity(cross[None, :, :], transformation[None, :, :])
        return HigherRankD1A1QualifiedSelection(
            selection_mesh_size=mesh_size,
            singular_values=singular_values,
            applied_rank_cutoff=cutoff,
            rank_margin=margin,
            condition_number=float(singular_values[0] / singular_values[-1]),
            direct_objective=direct,
            covariance_objective=covariance,
            objective_identity_defect=abs(direct - covariance),
            unitarity_defect=float(integrity[0][0]),
            stationarity_defect=float(integrity[1][0]),
            positive_semidefinite_defect=float(integrity[2][0]),
            transformation=immutable_complex128_array(transformation, "transformation"),
        )

    def select_a2(
        self,
        candidate_frames: Complex128Array,
        reference_frames: Complex128Array,
    ) -> HigherRankD1A2ComputedSelection:
        """Select complete pointwise unitaries or retain a fail-closed disposition."""
        definition = self._pointwise_definition(candidate_frames, reference_frames)
        mesh_size = int(candidate_frames.shape[0])
        rank = int(candidate_frames.shape[-1])
        try:
            result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(definition)
        except (ValueError, FloatingPointError, RuntimeError) as error:
            raise HigherRankD1AlignmentBackendError(error) from error
        deficient = tuple(int(index) for index in np.flatnonzero(~result.full_rank))
        singular = result.cross_singular_values
        if deficient:
            cutoffs = tuple(float(value) for value in result.applied_rank_cutoffs)
            smallest = tuple(float(value) for value in singular[:, -1])
            return HigherRankD1A2RankDeficientSelection(
                mesh_size=mesh_size,
                rank=rank,
                smallest_singular_values=smallest,
                applied_rank_cutoffs=cutoffs,
                rank_margins=tuple(
                    value - cutoff
                    for value, cutoff in zip(smallest, cutoffs, strict=True)
                ),
                numerical_ranks=tuple(int(value) for value in result.numerical_ranks),
                deficient_indices=deficient,
            )
        transformations = result.require_unique_right_unitary_transformations()
        cross = np.swapaxes(candidate_frames.conjugate(), -1, -2) @ reference_frames
        residual = candidate_frames @ transformations - reference_frames
        objectives = np.asarray(
            np.sum(np.abs(residual) ** 2, axis=(-2, -1)) / rank,
            dtype=np.float64,
        )
        covariance = np.asarray(
            np.maximum(
                0.0,
                2.0
                - (2.0 / rank)
                * np.real(
                    np.trace(
                        np.swapaxes(cross.conjugate(), -1, -2) @ transformations,
                        axis1=-2,
                        axis2=-1,
                    )
                ),
            ),
            dtype=np.float64,
        )
        integrity = self._integrity(cross, transformations)
        conditions = singular[:, 0] / singular[:, -1]
        return HigherRankD1A2Selection(
            mesh_size=mesh_size,
            smallest_singular_values=tuple(float(value) for value in singular[:, -1]),
            applied_rank_cutoffs=tuple(
                float(value) for value in result.applied_rank_cutoffs
            ),
            rank_margins=tuple(
                float(value) for value in singular[:, -1] - result.applied_rank_cutoffs
            ),
            numerical_ranks=tuple(int(value) for value in result.numerical_ranks),
            deficient_indices=(),
            condition_number_minimum=float(np.min(conditions)),
            condition_number_maximum=float(np.max(conditions)),
            objective_maximum=float(np.max(objectives)),
            objective_rms=float(np.sqrt(np.mean(objectives**2))),
            unitarity_defect_maximum=float(np.max(integrity[0])),
            stationarity_defect_maximum=float(np.max(integrity[1])),
            objective_identity_defect_maximum=float(
                np.max(np.abs(objectives - covariance))
            ),
            positive_semidefinite_defect_maximum=float(np.max(integrity[2])),
            transformations=immutable_complex128_array(
                transformations, "transformations"
            ),
        )

    @staticmethod
    def _integrity(
        cross: Complex128Array,
        transformations: Complex128Array,
    ) -> tuple[Float64Array, Float64Array, Float64Array]:
        rank = int(transformations.shape[-1])
        identity = np.eye(rank, dtype=np.complex128)
        adjoint = np.swapaxes(transformations.conjugate(), -1, -2)
        unitary = np.asarray(
            np.linalg.norm(adjoint @ transformations - identity, axis=(-2, -1)),
            dtype=np.float64,
        )
        stationarity = np.asarray(
            np.linalg.norm(
                adjoint @ cross
                - np.swapaxes(cross.conjugate(), -1, -2) @ transformations,
                axis=(-2, -1),
            )
            / math.sqrt(rank),
            dtype=np.float64,
        )
        hermitian_part = (
            adjoint @ cross + np.swapaxes(cross.conjugate(), -1, -2) @ transformations
        ) / 2.0
        minimum = np.linalg.eigvalsh(hermitian_part)[..., 0]
        psd = np.asarray(np.maximum(0.0, -minimum), dtype=np.float64)
        return unitary, stationarity, psd

    @staticmethod
    def _pointwise_definition(
        candidate_frames: Complex128Array,
        reference_frames: Complex128Array,
    ) -> NumpyBatchedComplexUnitaryProcrustesDefinition:
        definition = (
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_immutable_arrays(
                candidate_frames,
                reference_frames,
                HigherRankD1AlignmentSelector.tolerance(),
            )
        )
        if candidate_frames.shape[-2] < candidate_frames.shape[-1]:
            raise ValueError("frame fields must have feasible dimensions")
        return definition


__all__ = [
    "HigherRankD1A1NumericallyUnresolvedSelection",
    "HigherRankD1A1QualifiedSelection",
    "HigherRankD1A1RankDeficientSelection",
    "HigherRankD1A1Selection",
    "HigherRankD1A2NumericallyUnresolvedSelection",
    "HigherRankD1A2RankDeficientSelection",
    "HigherRankD1A2Selection",
    "HigherRankD1A2SelectionResult",
    "HigherRankD1AlignmentSelector",
]
