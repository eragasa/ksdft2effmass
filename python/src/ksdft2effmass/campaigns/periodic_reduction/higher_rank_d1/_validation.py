"""Private exact-value validation primitives for higher-rank D1 records."""

from __future__ import annotations

import math

from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array


def require_finite_float(value: float, name: str) -> None:
    """Require one exact finite built-in float without coercion."""
    if type(name) is not str or not name:
        raise ValueError("name must be a nonempty built-in str")
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def require_nonnegative_float(value: float, name: str) -> None:
    """Require one exact finite nonnegative built-in float without coercion."""
    require_finite_float(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")


def require_exact_instance[T](value: T, required_type: type[T], name: str) -> None:
    """Require one exact nominal value without coercion or subclass admission."""
    if type(name) is not str or not name:
        raise ValueError("name must be a nonempty built-in str")
    if type(value) is not required_type:
        raise TypeError(f"{name} must be {required_type.__name__}")


def require_exact_tuple[T](
    values: tuple[T, ...], required_type: type[T], name: str
) -> None:
    """Require one exact tuple containing only one exact nominal value type."""
    if type(name) is not str or not name:
        raise ValueError("name must be a nonempty built-in str")
    if type(values) is not tuple or any(
        type(value) is not required_type for value in values
    ):
        raise TypeError(f"{name} must contain {required_type.__name__} values")


def require_array_shape(
    value: Complex128Array | Float64Array,
    required_shape: tuple[int, ...],
    name: str,
) -> None:
    """Require one already typed array to have one exact shape."""
    if type(required_shape) is not tuple or any(
        type(size) is not int or size < 0 for size in required_shape
    ):
        raise ValueError("required_shape must contain nonnegative built-in integers")
    if type(name) is not str or not name:
        raise ValueError("name must be a nonempty built-in str")
    if value.shape != required_shape:
        raise ValueError(f"{name} must have shape {required_shape}")


__all__ = [
    "require_array_shape",
    "require_exact_instance",
    "require_finite_float",
    "require_nonnegative_float",
    "require_exact_tuple",
]
