"""Typed JSON decoding mechanics for periodic2d campaign serializers."""

from __future__ import annotations

import json

import numpy as np

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Periodic2DIsolatedBandJsonDecoder:
    """Decode strict UTF-8 JSON into a closed recursive representation."""

    __slots__ = ()

    def document(self, payload: bytes) -> dict[str, JsonValue]:
        """Decode one duplicate-free JSON object."""
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        try:
            raw: object = json.loads(
                payload.decode("utf-8"),
                object_pairs_hook=self._unique_object,
                parse_constant=self._reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as error:
            raise ValueError("payload must be valid strict UTF-8 JSON") from error
        value = self.value(raw, "root")
        return self.mapping(value, "root")

    def value(self, raw: object, name: str) -> JsonValue:
        """Validate and copy one closed JSON representation recursively."""
        if raw is None:
            return None
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, int):
            return raw
        if isinstance(raw, float):
            if not np.isfinite(raw):
                raise ValueError(f"{name} must not contain non-finite numbers")
            return raw
        if isinstance(raw, str):
            return raw
        if isinstance(raw, list):
            values: list[JsonValue] = []
            for index in range(len(raw)):
                item: object = raw[index]
                values.append(self.value(item, f"{name}[{index}]"))
            return values
        if isinstance(raw, dict):
            values_by_name: dict[str, JsonValue] = {}
            for raw_key in raw:
                key: object = raw_key
                if type(key) is not str:
                    raise TypeError(f"{name} keys must be strings")
                raw_item: object = raw[raw_key]
                values_by_name[key] = self.value(raw_item, f"{name}.{key}")
            return values_by_name
        raise TypeError(f"{name} contains an unsupported JSON representation")

    @staticmethod
    def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant is unsupported: {value}")

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object representation."""
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        """Return one JSON array representation."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Return one nonempty built-in string."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        if not value:
            raise ValueError(f"{name} must be nonempty")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite exact JSON floating-point number."""
        if type(value) is not float:
            raise TypeError(f"{name} must be a JSON floating-point number")
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one exact JSON integer while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        """Return one tuple of exact JSON floating-point numbers."""
        return tuple(self.real(item, name) for item in self.array(value, name))

    def integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one tuple of exact JSON integers."""
        return tuple(self.integer(item, name) for item in self.array(value, name))
