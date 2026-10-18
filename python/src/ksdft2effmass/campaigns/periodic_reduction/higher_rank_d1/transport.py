"""Part 2-compatible sequential transport diagnostics for higher-rank D1."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import (
    immutable_complex128_array,
    validate_immutable_complex128_array,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from scipy.linalg import schur  # type: ignore[import-untyped]

from ._validation import require_nonnegative_float
from .numerical_backend import (
    HigherRankD1BackendExceptionCode,
    HigherRankD1TransportBackendError,
)
from .procrustes import higher_rank_d1_procrustes_tolerance


@dataclass(frozen=True, slots=True)
class HigherRankD1EndpointSewingDiagnostics:
    """Retain normalized direct endpoint frame and projector sewing defects."""

    frame_defect: float
    projector_defect: float

    def __post_init__(self) -> None:
        for name in ("frame_defect", "projector_defect"):
            require_nonnegative_float(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class HigherRankD1TransportDiagnostics:
    """Retain complete scalar evidence for one sequential periodic transport."""

    mesh_size: int
    rank: int
    endpoint_sewing: HigherRankD1EndpointSewingDiagnostics
    minimum_link_singular_value: float
    maximum_link_singular_value: float
    maximum_applied_rank_cutoff: float
    minimum_rank_margin: float
    maximum_link_unitarity_defect: float
    maximum_normalized_link_residual: float
    deficient_link_indices: tuple[int, ...]
    closure_singular_value_minimum: float
    closure_singular_value_maximum: float
    closure_applied_rank_cutoff: float
    closure_rank_margin: float
    closure_unitarity_defect: float
    primitive_closure_defect: float
    closure_eigenphases: tuple[float, ...]
    status: str = "qualified"

    def __post_init__(self) -> None:
        """Validate exact identities and finite nonnegative diagnostics."""
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank < 1:
            raise ValueError("rank must be a positive built-in int")
        if type(self.endpoint_sewing) is not HigherRankD1EndpointSewingDiagnostics:
            raise TypeError("endpoint_sewing has an invalid type")
        for name in (
            "minimum_link_singular_value",
            "maximum_link_singular_value",
            "maximum_applied_rank_cutoff",
            "minimum_rank_margin",
            "maximum_link_unitarity_defect",
            "maximum_normalized_link_residual",
            "closure_singular_value_minimum",
            "closure_singular_value_maximum",
            "closure_applied_rank_cutoff",
            "closure_rank_margin",
            "closure_unitarity_defect",
            "primitive_closure_defect",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if type(self.deficient_link_indices) is not tuple or any(
            type(index) is not int for index in self.deficient_link_indices
        ):
            raise TypeError("deficient_link_indices must contain built-in integers")
        if self.deficient_link_indices != ():
            raise ValueError("a qualified D1 transport cannot retain deficient links")
        if type(self.closure_eigenphases) is not tuple:
            raise TypeError("closure_eigenphases must be a tuple")
        if len(self.closure_eigenphases) != self.rank:
            raise ValueError("closure_eigenphases length must equal rank")
        if self.status != "qualified":
            raise ValueError("status must be qualified")
        if any(
            type(phase) is not float
            or not math.isfinite(phase)
            or not -math.pi < phase <= math.pi
            for phase in self.closure_eigenphases
        ):
            raise ValueError("closure_eigenphases must be finite principal phases")


@dataclass(frozen=True, slots=True)
class HigherRankD1TransportLinkRankDeficientDiagnostics:
    """Retain the first deficient sequential link without null-space completion."""

    mesh_size: int
    rank: int
    endpoint_sewing: HigherRankD1EndpointSewingDiagnostics
    evaluated_link_count: int
    minimum_link_singular_value: float
    maximum_link_singular_value: float
    maximum_applied_rank_cutoff: float
    minimum_rank_margin: float
    deficient_link_indices: tuple[int, ...]
    unattempted_link_indices: tuple[int, ...]
    status: str = "transport-link-rank-deficient"

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in int")
        if not 1 <= self.evaluated_link_count <= self.mesh_size:
            raise ValueError("evaluated_link_count is invalid")
        if type(self.endpoint_sewing) is not HigherRankD1EndpointSewingDiagnostics:
            raise TypeError("endpoint_sewing has an invalid type")
        for name in (
            "minimum_link_singular_value",
            "maximum_link_singular_value",
            "maximum_applied_rank_cutoff",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if type(self.minimum_rank_margin) is not float or not math.isfinite(
            self.minimum_rank_margin
        ):
            raise ValueError("minimum_rank_margin must be finite")
        expected_deficient = (self.evaluated_link_count - 1,)
        if self.deficient_link_indices != expected_deficient:
            raise ValueError("deficient_link_indices must identify the stopped link")
        expected_unattempted = tuple(range(self.evaluated_link_count, self.mesh_size))
        if self.unattempted_link_indices != expected_unattempted:
            raise ValueError("unattempted_link_indices are inconsistent")
        if self.status != "transport-link-rank-deficient":
            raise ValueError("status must be transport-link-rank-deficient")


@dataclass(frozen=True, slots=True)
class HigherRankD1TransportClosureRankDeficientDiagnostics:
    """Retain a deficient closure mismatch after all sequential links qualify."""

    mesh_size: int
    rank: int
    endpoint_sewing: HigherRankD1EndpointSewingDiagnostics
    minimum_link_singular_value: float
    maximum_link_singular_value: float
    maximum_applied_rank_cutoff: float
    minimum_rank_margin: float
    maximum_link_unitarity_defect: float
    maximum_normalized_link_residual: float
    closure_singular_value_minimum: float
    closure_singular_value_maximum: float
    closure_applied_rank_cutoff: float
    closure_rank_margin: float
    deficient_link_indices: tuple[int, ...] = ()
    status: str = "transport-closure-rank-deficient"

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in int")
        if type(self.endpoint_sewing) is not HigherRankD1EndpointSewingDiagnostics:
            raise TypeError("endpoint_sewing has an invalid type")
        for name in (
            "minimum_link_singular_value",
            "maximum_link_singular_value",
            "maximum_applied_rank_cutoff",
            "minimum_rank_margin",
            "maximum_link_unitarity_defect",
            "maximum_normalized_link_residual",
            "closure_singular_value_minimum",
            "closure_singular_value_maximum",
            "closure_applied_rank_cutoff",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if type(self.closure_rank_margin) is not float or not math.isfinite(
            self.closure_rank_margin
        ):
            raise ValueError("closure_rank_margin must be finite")
        if self.deficient_link_indices != ():
            raise ValueError("all neighbor links must qualify before closure")
        if self.status != "transport-closure-rank-deficient":
            raise ValueError("status must be transport-closure-rank-deficient")


@dataclass(frozen=True, slots=True)
class HigherRankD1TransportNumericallyUnresolvedDiagnostics:
    """Retain a bounded backend-failure disposition without invented numerics."""

    mesh_size: int
    rank: int
    stage: str
    attempted_link_count: int
    exception_code: HigherRankD1BackendExceptionCode
    status: str = "transport-numerically-unresolved"

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in int")
        if self.stage not in ("link", "closure"):
            raise ValueError("stage is invalid")
        if not 0 <= self.attempted_link_count <= self.mesh_size:
            raise ValueError("attempted_link_count is invalid")
        if type(self.exception_code) is not HigherRankD1BackendExceptionCode:
            raise TypeError("exception_code must be HigherRankD1BackendExceptionCode")
        if self.status != "transport-numerically-unresolved":
            raise ValueError("status must be transport-numerically-unresolved")


type HigherRankD1TransportComputedResult = (
    HigherRankD1TransportDiagnostics
    | HigherRankD1TransportLinkRankDeficientDiagnostics
    | HigherRankD1TransportClosureRankDeficientDiagnostics
)
type HigherRankD1TransportResult = (
    HigherRankD1TransportComputedResult
    | HigherRankD1TransportNumericallyUnresolvedDiagnostics
)


class HigherRankD1TransportAnalyzer:
    """Execute the Part 2 sequential route with D1 maximum-rule Procrustes gates."""

    __slots__ = ()

    def execute(
        self,
        frames: Complex128Array,
        endpoint_frame: Complex128Array,
    ) -> HigherRankD1TransportComputedResult:
        """Transport frames or return a bounded fail-closed disposition."""
        self._validate_frames(frames, endpoint_frame)
        mesh_size = int(frames.shape[0])
        rank = int(frames.shape[2])
        tolerance = higher_rank_d1_procrustes_tolerance()
        solver = NumpyBatchedComplexUnitaryProcrustesSolver()
        transported: list[Complex128Array] = [frames[0]]
        link_singular_values: list[float] = []
        cutoffs: list[float] = []
        margins: list[float] = []
        unitary_defects: list[float] = []
        normalized_residuals: list[float] = []
        identity = immutable_complex128_array(
            np.eye(rank, dtype=np.complex128), "identity"
        )
        targets = tuple(frames[index] for index in range(1, mesh_size)) + (
            endpoint_frame,
        )
        for target_index, raw_target in enumerate(targets):
            try:
                result = solver.solve(
                    NumpyBatchedComplexUnitaryProcrustesDefinition.from_immutable_arrays(
                        raw_target[None, :, :],
                        transported[-1][None, :, :],
                        tolerance,
                    )
                )
            except (ValueError, FloatingPointError, RuntimeError) as error:
                raise HigherRankD1TransportBackendError(
                    "link", target_index + 1, error
                ) from error
            if not bool(result.full_rank[0]):
                singular_values = result.cross_singular_values[0]
                cutoff = float(result.applied_rank_cutoffs[0])
                link_singular_values.extend(float(value) for value in singular_values)
                cutoffs.append(cutoff)
                margins.append(float(singular_values[-1] - cutoff))
                endpoint_sewing = self._endpoint_sewing(frames[0], endpoint_frame, rank)
                return HigherRankD1TransportLinkRankDeficientDiagnostics(
                    mesh_size=mesh_size,
                    rank=rank,
                    endpoint_sewing=endpoint_sewing,
                    evaluated_link_count=target_index + 1,
                    minimum_link_singular_value=min(link_singular_values),
                    maximum_link_singular_value=max(link_singular_values),
                    maximum_applied_rank_cutoff=max(cutoffs),
                    minimum_rank_margin=min(margins),
                    deficient_link_indices=(target_index,),
                    unattempted_link_indices=tuple(range(target_index + 1, mesh_size)),
                )
            transformation = result.require_unique_right_unitary_transformations()[0]
            transported.append(
                immutable_complex128_array(
                    np.asarray(raw_target @ transformation, dtype=np.complex128),
                    "transported_frame",
                )
            )
            singular_values = result.cross_singular_values[0]
            cutoff = float(result.applied_rank_cutoffs[0])
            link_singular_values.extend(float(value) for value in singular_values)
            cutoffs.append(cutoff)
            margins.append(float(singular_values[-1] - cutoff))
            unitary_defects.append(
                float(
                    np.linalg.norm(
                        transformation.conjugate().T @ transformation - identity
                    )
                )
            )
            normalized_residuals.append(
                float(result.optimal_residual_frobenius_norms[0]) / math.sqrt(rank)
            )

        start = transported[0]
        duplicate = transported[-1]
        mismatch = immutable_complex128_array(
            np.asarray(start.conjugate().T @ duplicate, dtype=np.complex128),
            "closure_mismatch",
        )
        try:
            closure_result = solver.solve(
                NumpyBatchedComplexUnitaryProcrustesDefinition.from_immutable_arrays(
                    identity[None, :, :], mismatch[None, :, :], tolerance
                )
            )
        except (ValueError, FloatingPointError, RuntimeError) as error:
            raise HigherRankD1TransportBackendError(
                "closure", mesh_size, error
            ) from error
        if not bool(closure_result.full_rank[0]):
            closure_singular = closure_result.cross_singular_values[0]
            closure_cutoff = float(closure_result.applied_rank_cutoffs[0])
            endpoint_sewing = self._endpoint_sewing(frames[0], endpoint_frame, rank)
            return HigherRankD1TransportClosureRankDeficientDiagnostics(
                mesh_size=mesh_size,
                rank=rank,
                endpoint_sewing=endpoint_sewing,
                minimum_link_singular_value=min(link_singular_values),
                maximum_link_singular_value=max(link_singular_values),
                maximum_applied_rank_cutoff=max(cutoffs),
                minimum_rank_margin=min(margins),
                maximum_link_unitarity_defect=max(unitary_defects),
                maximum_normalized_link_residual=max(normalized_residuals),
                closure_singular_value_minimum=float(closure_singular[-1]),
                closure_singular_value_maximum=float(closure_singular[0]),
                closure_applied_rank_cutoff=closure_cutoff,
                closure_rank_margin=float(closure_singular[-1] - closure_cutoff),
            )
        unitary_closure = closure_result.require_unique_right_unitary_transformations()[
            0
        ]
        triangular, eigenvectors = schur(unitary_closure, output="complex")
        phases = np.asarray(np.angle(np.diag(triangular)), dtype=np.float64)
        order = np.argsort(phases)
        phases = phases[order]
        eigenvectors = eigenvectors[:, order]
        corrected: list[Complex128Array] = []
        for index, frame in enumerate(transported):
            fraction = float(index) / float(mesh_size)
            correction = (
                eigenvectors
                @ np.diag(np.exp(-1.0j * fraction * phases))
                @ eigenvectors.conjugate().T
            )
            corrected.append(np.asarray(frame @ correction, dtype=np.complex128))
        closure_singular = closure_result.cross_singular_values[0]
        closure_cutoff = float(closure_result.applied_rank_cutoffs[0])
        endpoint_sewing = self._endpoint_sewing(frames[0], endpoint_frame, rank)
        return HigherRankD1TransportDiagnostics(
            mesh_size=mesh_size,
            rank=rank,
            endpoint_sewing=endpoint_sewing,
            minimum_link_singular_value=min(link_singular_values),
            maximum_link_singular_value=max(link_singular_values),
            maximum_applied_rank_cutoff=max(cutoffs),
            minimum_rank_margin=min(margins),
            maximum_link_unitarity_defect=max(unitary_defects),
            maximum_normalized_link_residual=max(normalized_residuals),
            deficient_link_indices=(),
            closure_singular_value_minimum=float(closure_singular[-1]),
            closure_singular_value_maximum=float(closure_singular[0]),
            closure_applied_rank_cutoff=closure_cutoff,
            closure_rank_margin=float(closure_singular[-1] - closure_cutoff),
            closure_unitarity_defect=float(
                np.linalg.norm(
                    unitary_closure.conjugate().T @ unitary_closure - identity
                )
            ),
            primitive_closure_defect=(
                float(np.linalg.norm(corrected[-1] - corrected[0])) / math.sqrt(rank)
            ),
            closure_eigenphases=tuple(float(phase) for phase in phases),
        )

    @staticmethod
    def _endpoint_sewing(
        start_frame: Complex128Array,
        endpoint_frame: Complex128Array,
        rank: int,
    ) -> HigherRankD1EndpointSewingDiagnostics:
        start_projector = start_frame @ start_frame.conjugate().T
        endpoint_projector = endpoint_frame @ endpoint_frame.conjugate().T
        return HigherRankD1EndpointSewingDiagnostics(
            frame_defect=(
                float(np.linalg.norm(endpoint_frame - start_frame)) / math.sqrt(rank)
            ),
            projector_defect=(
                float(np.linalg.norm(endpoint_projector - start_projector))
                / math.sqrt(rank)
            ),
        )

    @staticmethod
    def _validate_frames(
        frames: Complex128Array, endpoint_frame: Complex128Array
    ) -> None:
        for name, value in (("frames", frames), ("endpoint_frame", endpoint_frame)):
            validate_immutable_complex128_array(value, name)
        if frames.ndim != 3 or endpoint_frame.ndim != 2:
            raise ValueError("frames and endpoint_frame have invalid dimensions")
        if frames.shape[0] == 0 or frames.shape[1:] != endpoint_frame.shape:
            raise ValueError("endpoint_frame shape must match one sampled frame")
        if frames.shape[2] <= 0 or frames.shape[1] < frames.shape[2]:
            raise ValueError("frame dimensions must be nonempty and feasible")


__all__ = [
    "HigherRankD1EndpointSewingDiagnostics",
    "HigherRankD1TransportAnalyzer",
    "HigherRankD1TransportClosureRankDeficientDiagnostics",
    "HigherRankD1TransportDiagnostics",
    "HigherRankD1TransportLinkRankDeficientDiagnostics",
    "HigherRankD1TransportNumericallyUnresolvedDiagnostics",
    "HigherRankD1TransportResult",
]
