"""Strict wire decoding for independent PIAB1D verification."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]


class Piab1dResultDecoder:
    """Own strict JSON mechanics shared only by independent campaign verifiers."""

    __slots__ = ()

    def decode(self, path: Path) -> dict[str, JsonValue]:
        """Decode one existing UTF-8 JSON result object."""
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        if not path.is_file():
            raise ValueError("path must be an existing file")
        decoded = json.loads(path.read_text(encoding="utf-8"))
        return self.mapping(self.json_value(decoded), "result")

    @classmethod
    def json_value(cls, value: JsonValue) -> JsonValue:
        """Return a recursively validated closed JSON value.

        Parameters
        ----------
        value : JsonValue
            Value produced at the standard-library JSON boundary.

        Returns
        -------
        JsonValue
            Newly reconstructed value containing only exact JSON semantic types.

        Raises
        ------
        TypeError
            If any value or mapping key has a type outside ``JsonValue``.
        ValueError
            If a floating value is not finite.
        """
        if value is None or type(value) in (bool, int, str):
            return value
        if type(value) is float:
            if not np.isfinite(value):
                raise ValueError("JSON floating values must be finite")
            return value
        if type(value) is list:
            return [cls.json_value(item) for item in value]
        if type(value) is dict:
            if any(type(key) is not str for key in value):
                raise TypeError("JSON object keys must be strings")
            return {key: cls.json_value(item) for key, item in value.items()}
        raise TypeError("decoded value has a type outside JsonValue")

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object with string keys."""
        if not isinstance(value, dict) or not all(type(key) is str for key in value):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def sequence(value: JsonValue, name: str) -> list[JsonValue]:
        """Return one JSON array."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Return one nonempty JSON string."""
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @classmethod
    def sha256_string(cls, value: JsonValue, name: str) -> str:
        """Return one lowercase SHA-256 string."""
        result = cls.string(value, name)
        if len(result) != 64 or any(
            character not in "0123456789abcdef" for character in result
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        return result

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one built-in JSON integer excluding booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite JSON real excluding booleans."""
        if type(value) is int:
            result = value * 1.0
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{name} must be a JSON real")
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @classmethod
    def integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one JSON integer sequence."""
        return tuple(cls.integer(item, name) for item in cls.sequence(value, name))

    @classmethod
    def positive_integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return a nonempty, strictly increasing sequence of positive integers."""
        result = cls.integer_sequence(value, name)
        if not result or any(item <= 0 for item in result):
            raise ValueError(f"{name} must contain positive integers")
        if result != tuple(sorted(set(result))):
            raise ValueError(f"{name} must be strictly increasing")
        return result

    @classmethod
    def real_sequence(cls, value: JsonValue, name: str) -> tuple[float, ...]:
        """Return one JSON real sequence."""
        return tuple(cls.real(item, name) for item in cls.sequence(value, name))

    @classmethod
    def positive_real(cls, value: JsonValue, name: str) -> float:
        """Return one positive finite real without Boolean or string coercion."""
        result = cls.real(value, name)
        if result <= 0.0:
            raise ValueError(f"{name} must be positive")
        return result

    @classmethod
    def nonnegative_real(cls, value: JsonValue, name: str) -> float:
        """Return one nonnegative finite real without Boolean or string coercion."""
        result = cls.real(value, name)
        if result < 0.0:
            raise ValueError(f"{name} must be nonnegative")
        return result

    @classmethod
    def matrix(cls, value: JsonValue, name: str) -> RealMatrix:
        """Return a finite binary64 matrix without scalar coercion."""
        rows = tuple(cls.real_sequence(row, name) for row in cls.sequence(value, name))
        try:
            matrix = np.asarray(rows, dtype=np.float64)
        except ValueError as error:
            raise ValueError(f"{name} must be a rectangular matrix") from error
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix")
        return matrix
