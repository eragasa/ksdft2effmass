"""Shared exact-type admission for higher-rank typed evidence records."""

from __future__ import annotations

import math
from collections.abc import Mapping

from projectkoios.numerics.numpy.typing import Float64Array, Int64Array
from projectkoios.numerics.numpy.validation import (
    immutable_float64_array,
    immutable_int64_array,
)

from ksdft2effmass.serialization import SerializableValue


def _nonempty(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must be nonempty")


def _finite_nonnegative(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _float_array(
    value: Float64Array,
    name: str,
    *,
    ndim: int = 1,
) -> Float64Array:
    if value.ndim != ndim:
        raise ValueError(f"{name} must have {ndim} dimensions")
    return immutable_float64_array(value, name)


def _int_array(value: Int64Array, name: str) -> Int64Array:
    if value.ndim != 1:
        raise ValueError(f"{name} must be one dimensional")
    return immutable_int64_array(value, name)


def _decoded_float(value: SerializableValue, name: str) -> float:
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float")
    return value


def _decoded_bool(value: SerializableValue, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must decode to a built-in bool")
    return value


def _decoded_int(value: SerializableValue, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer")
    return value


def _decoded_optional_float(
    value: SerializableValue,
    name: str,
) -> float | None:
    if value is None:
        return None
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float or None")
    return value


def _mapping_value(
    value: SerializableValue, name: str
) -> Mapping[str, SerializableValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must decode to a mapping")
    return value


def _tuple_of_mappings(
    value: SerializableValue,
    name: str,
) -> tuple[Mapping[str, SerializableValue], ...]:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must decode to a tuple")
    decoded: list[Mapping[str, SerializableValue]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise TypeError(f"{name} entries must decode to mappings")
        decoded.append(item)
    return tuple(decoded)
