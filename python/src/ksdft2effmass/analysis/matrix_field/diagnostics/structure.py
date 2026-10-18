"""Structural diagnostics for finite matrix, frame, and projector fields."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

type ComplexArray = NDArray[np.complex128]


def _positive_float(name: str, value: float) -> float:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _complex_matrix_field(name: str, value: ComplexArray) -> ComplexArray:
    if type(value) is not np.ndarray:
        raise TypeError(f"{name} must be an exact numpy.ndarray")
    if value.dtype != np.dtype(np.complex128):
        raise TypeError(f"{name} must have complex128 dtype")
    if value.ndim < 3 or value.shape[-2] <= 0 or value.shape[-1] <= 0:
        raise ValueError(f"{name} must contain nonempty matrices")
    if not bool(np.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True, slots=True)
class MatrixFieldHermiticityDiagnostics:
    """Retain the maximum raw and normalized Hermiticity defect."""

    matrix_size: int
    energy_reference: float
    maximum_frobenius_defect: float
    normalized_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate dimensions, values, and normalization."""
        if type(self.matrix_size) is not int:
            raise TypeError("matrix_size must be a built-in int")
        if self.matrix_size <= 0:
            raise ValueError("matrix_size must be positive")
        energy_reference = _positive_float("energy_reference", self.energy_reference)
        for name, value in (
            ("maximum_frobenius_defect", self.maximum_frobenius_defect),
            (
                "normalized_maximum_frobenius_defect",
                self.normalized_maximum_frobenius_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        expected = self.maximum_frobenius_defect / (
            math.sqrt(self.matrix_size) * energy_reference
        )
        if self.normalized_maximum_frobenius_defect != expected:
            raise ValueError("normalized Hermiticity defect is inconsistent")


class MatrixFieldHermiticityAnalyzer:
    """Measure ``H-H^dagger`` without assigning a pass threshold."""

    __slots__ = ()

    def execute(
        self,
        matrices: ComplexArray,
        energy_reference: float,
    ) -> MatrixFieldHermiticityDiagnostics:
        """Return the maximum pointwise Frobenius Hermiticity defect."""
        matrices = _complex_matrix_field("matrices", matrices)
        if matrices.shape[-2] != matrices.shape[-1]:
            raise ValueError("matrices must be square")
        energy_reference = _positive_float("energy_reference", energy_reference)
        matrix_size = int(matrices.shape[-1])
        adjoints = np.swapaxes(matrices.conjugate(), -1, -2)
        defect = float(np.max(np.linalg.norm(matrices - adjoints, axis=(-2, -1))))
        return MatrixFieldHermiticityDiagnostics(
            matrix_size=matrix_size,
            energy_reference=energy_reference,
            maximum_frobenius_defect=defect,
            normalized_maximum_frobenius_defect=(
                defect / (math.sqrt(matrix_size) * energy_reference)
            ),
        )


@dataclass(frozen=True, slots=True)
class MatrixFieldIsometryDiagnostics:
    """Retain the maximum defect in ``F^dagger F=I`` for a frame field."""

    ambient_dimension: int
    rank: int
    maximum_frobenius_defect: float
    normalized_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate dimensions, nonnegative defects, and rank normalization."""
        if type(self.ambient_dimension) is not int or type(self.rank) is not int:
            raise TypeError("frame dimensions must be built-in integers")
        if self.rank <= 0 or self.ambient_dimension < self.rank:
            raise ValueError("frame dimensions must be positive and feasible")
        for name, value in (
            ("maximum_frobenius_defect", self.maximum_frobenius_defect),
            (
                "normalized_maximum_frobenius_defect",
                self.normalized_maximum_frobenius_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        expected = self.maximum_frobenius_defect / math.sqrt(self.rank)
        if self.normalized_maximum_frobenius_defect != expected:
            raise ValueError("normalized isometry defect is inconsistent")


class MatrixFieldIsometryAnalyzer:
    """Measure frame or unitary Gram defects without selecting transformations."""

    __slots__ = ()

    def execute(self, frames: ComplexArray) -> MatrixFieldIsometryDiagnostics:
        """Return the maximum pointwise Frobenius defect in ``F^dagger F=I``."""
        frames = _complex_matrix_field("frames", frames)
        ambient_dimension = int(frames.shape[-2])
        rank = int(frames.shape[-1])
        if rank > ambient_dimension:
            raise ValueError("frame rank must not exceed ambient dimension")
        identity = np.eye(rank, dtype=np.complex128)
        gram = np.swapaxes(frames.conjugate(), -1, -2) @ frames
        defect = float(np.max(np.linalg.norm(gram - identity, axis=(-2, -1))))
        return MatrixFieldIsometryDiagnostics(
            ambient_dimension=ambient_dimension,
            rank=rank,
            maximum_frobenius_defect=defect,
            normalized_maximum_frobenius_defect=defect / math.sqrt(rank),
        )


@dataclass(frozen=True, slots=True)
class MatrixProjectorFieldDiagnostics:
    """Retain Hermiticity and idempotency defects for square projector candidates."""

    dimension: int
    maximum_hermiticity_frobenius_defect: float
    maximum_idempotency_frobenius_defect: float
    normalized_maximum_hermiticity_frobenius_defect: float
    normalized_maximum_idempotency_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate dimension, finite defects, and square-root normalization."""
        if type(self.dimension) is not int:
            raise TypeError("dimension must be a built-in int")
        if self.dimension <= 0:
            raise ValueError("dimension must be positive")
        for name, value in (
            (
                "maximum_hermiticity_frobenius_defect",
                self.maximum_hermiticity_frobenius_defect,
            ),
            (
                "maximum_idempotency_frobenius_defect",
                self.maximum_idempotency_frobenius_defect,
            ),
            (
                "normalized_maximum_hermiticity_frobenius_defect",
                self.normalized_maximum_hermiticity_frobenius_defect,
            ),
            (
                "normalized_maximum_idempotency_frobenius_defect",
                self.normalized_maximum_idempotency_frobenius_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        scale = math.sqrt(self.dimension)
        if self.normalized_maximum_hermiticity_frobenius_defect != (
            self.maximum_hermiticity_frobenius_defect / scale
        ):
            raise ValueError("normalized projector Hermiticity defect is inconsistent")
        if self.normalized_maximum_idempotency_frobenius_defect != (
            self.maximum_idempotency_frobenius_defect / scale
        ):
            raise ValueError("normalized projector idempotency defect is inconsistent")


class MatrixProjectorFieldAnalyzer:
    """Measure projector Hermiticity and idempotency without a rank claim."""

    __slots__ = ()

    def execute(self, projectors: ComplexArray) -> MatrixProjectorFieldDiagnostics:
        """Return maximum pointwise defects in ``P=P^dagger`` and ``P^2=P``."""
        projectors = _complex_matrix_field("projectors", projectors)
        if projectors.shape[-2] != projectors.shape[-1]:
            raise ValueError("projectors must be square")
        dimension = int(projectors.shape[-1])
        adjoints = np.swapaxes(projectors.conjugate(), -1, -2)
        hermiticity = float(
            np.max(np.linalg.norm(projectors - adjoints, axis=(-2, -1)))
        )
        idempotency = float(
            np.max(
                np.linalg.norm(
                    projectors @ projectors - projectors,
                    axis=(-2, -1),
                )
            )
        )
        scale = math.sqrt(dimension)
        return MatrixProjectorFieldDiagnostics(
            dimension=dimension,
            maximum_hermiticity_frobenius_defect=hermiticity,
            maximum_idempotency_frobenius_defect=idempotency,
            normalized_maximum_hermiticity_frobenius_defect=hermiticity / scale,
            normalized_maximum_idempotency_frobenius_defect=idempotency / scale,
        )


__all__ = [
    "MatrixFieldHermiticityAnalyzer",
    "MatrixFieldHermiticityDiagnostics",
    "MatrixFieldIsometryAnalyzer",
    "MatrixFieldIsometryDiagnostics",
    "MatrixProjectorFieldAnalyzer",
    "MatrixProjectorFieldDiagnostics",
]
