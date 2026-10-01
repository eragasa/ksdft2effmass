"""Strict wire decoding for independent PIAB1D verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]


class ParticleInBoxCampaignResultDecoder:
    """Own strict JSON mechanics shared only by independent campaign verifiers."""

    __slots__ = ()

    def decode(self, path: Path) -> dict[str, JsonValue]:
        """Decode one existing UTF-8 JSON result object."""
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        if not path.is_file():
            raise ValueError("path must be an existing file")
        return self.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), "result"
        )

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
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @classmethod
    def integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one JSON integer sequence."""
        return tuple(cls.integer(item, name) for item in cls.sequence(value, name))

    @classmethod
    def real_sequence(cls, value: JsonValue, name: str) -> tuple[float, ...]:
        """Return one JSON real sequence."""
        return tuple(cls.real(item, name) for item in cls.sequence(value, name))

    @classmethod
    def matrix(cls, value: JsonValue, name: str) -> RealMatrix:
        """Return one finite binary64 matrix from nested JSON arrays."""
        rows = cls.sequence(value, name)
        matrix = np.asarray(rows, dtype=np.float64)
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix")
        return matrix
