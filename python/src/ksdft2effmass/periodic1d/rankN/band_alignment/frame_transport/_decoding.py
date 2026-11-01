"""Wire decoding shared by rank-N frame-transport records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import final

from projectkoios.physkit.units import ComplexMatrixQuantity

from ksdft2effmass.serialization import SerializableValue


@final
class _Periodic1DRankNTransportRecordDecoder:
    """Decode repeated optional transport fields from one admitted mapping."""

    __slots__ = ("_values",)

    def __init__(self, values: Mapping[str, SerializableValue]) -> None:
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        self._values = values

    def optional_float(self, name: str) -> float | None:
        """Decode one optional built-in float field."""
        value = self._values[name]
        if value is None:
            return None
        if type(value) is not float:
            raise TypeError(f"{name} must decode to a built-in float or None")
        return value

    def optional_text(self, name: str) -> str | None:
        """Decode one optional built-in string field."""
        value = self._values[name]
        if value is None:
            return None
        if type(value) is not str:
            raise TypeError(f"{name} must decode to a string or None")
        return value

    def integer_tuple(self, name: str) -> tuple[int, ...]:
        """Decode one exact tuple of built-in integers."""
        value = self._values[name]
        if not isinstance(value, tuple):
            raise TypeError(f"{name} must decode to a tuple")
        decoded: list[int] = []
        for entry in value:
            if type(entry) is not int:
                raise TypeError(f"{name} must decode to built-in integers")
            decoded.append(entry)
        return tuple(decoded)

    def optional_complex_matrix(self, name: str) -> ComplexMatrixQuantity | None:
        """Decode one optional unit-bearing complex matrix quantity."""
        value = self._values[name]
        if value is None:
            return None
        if type(value) is not ComplexMatrixQuantity:
            raise TypeError(f"{name} must decode to ComplexMatrixQuantity or None")
        return value

    def optional_float_tuple(self, name: str) -> tuple[float, ...] | None:
        """Decode one optional exact tuple of built-in floats."""
        value = self._values[name]
        if value is None:
            return None
        if not isinstance(value, tuple):
            raise TypeError(f"{name} must decode to a tuple or None")
        decoded: list[float] = []
        for entry in value:
            if type(entry) is not float:
                raise TypeError(f"{name} must decode to built-in floats")
            decoded.append(entry)
        return tuple(decoded)


__all__: list[str] = []
