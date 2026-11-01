"""Validate finite matrix-field array representations."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

type ComplexArray = NDArray[np.complex128]


def matrix_field(name: str, value: ComplexArray) -> ComplexArray:
    """Validate an exact finite complex128 field of nonempty square matrices."""
    if type(value) is not np.ndarray:
        raise TypeError(f"{name} must be an exact numpy.ndarray")
    if value.dtype != np.dtype(np.complex128):
        raise TypeError(f"{name} must have complex128 dtype")
    if value.ndim < 3 or value.shape[-1] == 0 or value.shape[-2] != value.shape[-1]:
        raise ValueError(f"{name} must contain nonempty square matrices")
    if not bool(np.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")
    return value


__all__ = ["matrix_field"]
