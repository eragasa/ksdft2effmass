"""Exact scalar and array validation for matrix-field diagnostics."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]


def positive_float(name: str, value: float) -> float:
    """Return one exact finite positive built-in float."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def nonnegative_float(name: str, value: float) -> float:
    """Return one exact finite nonnegative built-in float."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


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
