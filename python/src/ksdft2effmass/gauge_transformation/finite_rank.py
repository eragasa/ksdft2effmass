"""Dimension-neutral sampled finite-rank gauge transformations."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray


@dataclass(frozen=True, slots=True, eq=False)
class SampledFiniteRankGaugeTransformation:
    """Store one ordered unitary field and its explicit right actions."""

    unitaries: ComplexArray = field(repr=False)

    def __post_init__(self) -> None:
        admitted = NumpyImmutableArrayConstructor(
            self.unitaries,
            "unitaries",
            np.dtype(np.complex128),
        ).execute()
        if admitted.ndim != 3 or admitted.shape[0] == 0:
            raise ValueError("unitaries must have shape (N, r, r) with N positive")
        if admitted.shape[1] == 0 or admitted.shape[1] != admitted.shape[2]:
            raise ValueError("unitaries must have positive square matrix dimensions")
        rank = admitted.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        defect = np.max(
            np.linalg.norm(
                np.swapaxes(admitted.conjugate(), -1, -2) @ admitted - identity,
                axis=(-2, -1),
            )
        )
        if not np.isfinite(defect) or float(defect) > 1.0e-12:
            raise ValueError("unitaries must be unitary within 1.0e-12")
        object.__setattr__(self, "unitaries", admitted)

    @property
    def sample_count(self) -> int:
        """Return the number of ordered transformation samples."""
        return int(self.unitaries.shape[0])

    @property
    def represented_rank(self) -> int:
        """Return the finite dimension acted on by each unitary."""
        return int(self.unitaries.shape[1])

    @property
    def inverse_right_actions(self) -> ComplexArray:
        """Return the exact adjoint right-action field."""
        return NumpyImmutableArrayConstructor(
            np.swapaxes(self.unitaries.conjugate(), -1, -2),
            "inverse_right_actions",
            np.dtype(np.complex128),
        ).execute()

    def transform_frames(self, frames: ComplexArray) -> ComplexArray:
        """Apply the sampled transformation from the right to frame matrices."""
        admitted = NumpyImmutableArrayConstructor(
            frames,
            "frames",
            np.dtype(np.complex128),
        ).execute()
        expected_shape = (
            self.sample_count,
            admitted.shape[-2],
            self.represented_rank,
        )
        if admitted.ndim != 3 or admitted.shape != expected_shape:
            raise ValueError("frames must have shape (N, ambient_dimension, r)")
        return NumpyImmutableArrayConstructor(
            np.asarray(admitted @ self.unitaries, dtype=np.complex128),
            "gauge_transformed_frames",
            np.dtype(np.complex128),
        ).execute()

    def transform_operators(self, operators: ComplexArray) -> ComplexArray:
        """Represent sampled operators in the transformed basis."""
        admitted = NumpyImmutableArrayConstructor(
            operators,
            "operators",
            np.dtype(np.complex128),
        ).execute()
        expected_shape = (
            self.sample_count,
            self.represented_rank,
            self.represented_rank,
        )
        if admitted.ndim != 3 or admitted.shape != expected_shape:
            raise ValueError("operators must have shape (N, r, r)")
        values = self.inverse_right_actions @ admitted @ self.unitaries
        return NumpyImmutableArrayConstructor(
            np.asarray(values, dtype=np.complex128),
            "gauge_transformed_operators",
            np.dtype(np.complex128),
        ).execute()


__all__ = ["SampledFiniteRankGaugeTransformation"]
