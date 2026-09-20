"""Reciprocal-path band frames and one-dimensional polar transport."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import schur  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless

from .reciprocal_paths import CenteredUniformReciprocalMesh1D


@dataclass(frozen=True, slots=True, eq=False)
class ReciprocalBandFramePath1D:
    """Retain ordered orthonormal band frames and their endpoint sewing map."""

    mesh: CenteredUniformReciprocalMesh1D
    frames: tuple[ComplexMatrixQuantity, ...]
    sewing_map: ComplexMatrixQuantity
    orthonormality_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate path length, dimensions, units, and frame orthonormality."""
        if type(self.mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh1D")
        if not isinstance(self.frames, tuple) or not self.frames:
            raise TypeError("frames must be a nonempty tuple")
        if len(self.frames) != self.mesh.point_count:
            raise ValueError("frame count must equal reciprocal mesh point count")
        if type(self.sewing_map) is not ComplexMatrixQuantity:
            raise TypeError("sewing_map must be ComplexMatrixQuantity")
        if not isinstance(self.sewing_map.unit, Unitless):
            raise ValueError("sewing_map must be unitless")
        if type(self.orthonormality_absolute_tolerance) is not float:
            raise TypeError(
                "orthonormality_absolute_tolerance must be a built-in float"
            )
        if (
            not np.isfinite(self.orthonormality_absolute_tolerance)
            or self.orthonormality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "orthonormality_absolute_tolerance must be finite and nonnegative"
            )
        first = self.frames[0]
        if type(first) is not ComplexMatrixQuantity:
            raise TypeError("every frame must be ComplexMatrixQuantity")
        ambient_dimension, rank = first.magnitude.shape
        if ambient_dimension == 0 or rank == 0 or rank > ambient_dimension:
            raise ValueError("frames must have nonzero feasible dimensions")
        if self.sewing_map.magnitude.shape != (
            ambient_dimension,
            ambient_dimension,
        ):
            raise ValueError("sewing_map shape must match frame ambient dimension")
        identity = np.eye(rank, dtype=np.complex128)
        for frame in self.frames:
            if type(frame) is not ComplexMatrixQuantity:
                raise TypeError("every frame must be ComplexMatrixQuantity")
            if not isinstance(frame.unit, Unitless):
                raise ValueError("frames must be unitless")
            if frame.magnitude.shape != (ambient_dimension, rank):
                raise ValueError("all frames must have equal shape")
            defect = float(
                np.linalg.norm(frame.magnitude.conj().T @ frame.magnitude - identity)
            )
            if defect > self.orthonormality_absolute_tolerance:
                raise ValueError("frame exceeds the orthonormality tolerance")

    @property
    def ambient_dimension(self) -> int:
        """Return the dimension of the represented parent basis."""
        return int(self.frames[0].magnitude.shape[0])

    @property
    def rank(self) -> int:
        """Return the retained band-subspace rank."""
        return int(self.frames[0].magnitude.shape[1])


@dataclass(frozen=True, slots=True, eq=False)
class PolarBandFrameTransportResult1D:
    """Retain one polar-transported frame path and its overlap diagnostics."""

    source: ReciprocalBandFramePath1D
    transported: ReciprocalBandFramePath1D
    minimum_overlap_singular_value: float
    overlap_singular_value_threshold: float
    closure_eigenphases: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate transport correlations and retained diagnostics."""
        if type(self.source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if type(self.transported) is not ReciprocalBandFramePath1D:
            raise TypeError("transported must be ReciprocalBandFramePath1D")
        if self.transported.mesh != self.source.mesh:
            raise ValueError("source and transported meshes must agree")
        if self.transported.rank != self.source.rank:
            raise ValueError("source and transported ranks must agree")
        if self.transported.ambient_dimension != self.source.ambient_dimension:
            raise ValueError("source and transported ambient dimensions must agree")
        if type(self.minimum_overlap_singular_value) is not float:
            raise TypeError("minimum_overlap_singular_value must be a built-in float")
        if (
            not np.isfinite(self.minimum_overlap_singular_value)
            or self.minimum_overlap_singular_value < 0.0
        ):
            raise ValueError(
                "minimum_overlap_singular_value must be finite and nonnegative"
            )
        if type(self.overlap_singular_value_threshold) is not float:
            raise TypeError(
                "overlap_singular_value_threshold must be a built-in float"
            )
        if (
            not np.isfinite(self.overlap_singular_value_threshold)
            or self.overlap_singular_value_threshold < 0.0
        ):
            raise ValueError(
                "overlap_singular_value_threshold must be finite and nonnegative"
            )
        if self.minimum_overlap_singular_value <= self.overlap_singular_value_threshold:
            raise ValueError("retained overlap singular value does not pass threshold")
        if (
            not isinstance(self.closure_eigenphases, tuple)
            or len(self.closure_eigenphases) != self.source.rank
        ):
            raise ValueError("closure_eigenphases length must equal retained rank")
        if any(
            type(phase) is not float or not np.isfinite(phase)
            for phase in self.closure_eigenphases
        ):
            raise ValueError("closure_eigenphases must contain finite built-in floats")


class PolarBandFrameTransporter1D:
    """Construct a closed smooth gauge by neighborwise unitary polar transport."""

    __slots__ = ()

    def execute(
        self,
        path: ReciprocalBandFramePath1D,
        overlap_singular_value_threshold: float,
    ) -> PolarBandFrameTransportResult1D:
        """Transport scalar or composite frames and distribute closure holonomy."""
        if type(path) is not ReciprocalBandFramePath1D:
            raise TypeError("path must be ReciprocalBandFramePath1D")
        if type(overlap_singular_value_threshold) is not float:
            raise TypeError(
                "overlap_singular_value_threshold must be a built-in float"
            )
        if (
            not np.isfinite(overlap_singular_value_threshold)
            or overlap_singular_value_threshold < 0.0
        ):
            raise ValueError(
                "overlap_singular_value_threshold must be finite and nonnegative"
            )
        raw = tuple(frame.magnitude for frame in path.frames)
        transported = [raw[0].copy()]
        singular_values: list[float] = []
        for index in range(len(raw) - 1):
            overlap = transported[index].conj().T @ raw[index + 1]
            left, values, right_h = np.linalg.svd(overlap)
            singular_values.extend(float(value) for value in values)
            rotation = right_h.conj().T @ left.conj().T
            transported.append(raw[index + 1] @ rotation)
        sewn_first = path.sewing_map.magnitude @ transported[0]
        closure = transported[-1].conj().T @ sewn_first
        left, values, right_h = np.linalg.svd(closure)
        singular_values.extend(float(value) for value in values)
        minimum = min(singular_values)
        if minimum <= overlap_singular_value_threshold:
            raise ValueError("neighbor or closure overlap does not pass threshold")
        unitary_closure = left @ right_h
        triangular, eigenvectors = schur(unitary_closure, output="complex")
        phases = np.angle(np.diag(triangular)).astype(np.float64)
        order = np.argsort(phases)
        phases = phases[order]
        eigenvectors = eigenvectors[:, order]
        count = len(transported)
        for index in range(count):
            fraction = float(index) / float(count)
            distributed_root = (
                eigenvectors
                @ np.diag(np.exp(1j * phases * fraction))
                @ eigenvectors.conj().T
            )
            transported[index] = transported[index] @ distributed_root
        transported_path = ReciprocalBandFramePath1D(
            path.mesh,
            tuple(
                ComplexMatrixQuantity(frame, Unitless()) for frame in transported
            ),
            path.sewing_map,
            path.orthonormality_absolute_tolerance,
        )
        return PolarBandFrameTransportResult1D(
            path,
            transported_path,
            float(minimum),
            overlap_singular_value_threshold,
            tuple(float(phase) for phase in phases),
        )
