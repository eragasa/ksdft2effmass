"""Shared strict JSON decoding mechanics for scientific campaigns.

``CampaignJsonDecoder`` owns only the closed JSON value representation and
primitive wire checks shared by campaign serializers and artifact decoders.
Campaign-specific subclasses remain responsible for schema fields, schema
versions, scientific records, and source authentication.
"""

from __future__ import annotations

import json

import numpy as np

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class CampaignJsonDecoder:
    """Decode strict UTF-8 JSON and exact primitive campaign values.

    The decoder rejects duplicate object keys, nonstandard nonfinite constants,
    unsupported Python values, booleans where numbers are required, and numeric
    strings. It performs no schema selection, scientific construction, source
    authentication, filesystem access, or acceptance decision.
    """

    __slots__ = ()

    def document(self, payload: bytes) -> dict[str, JsonValue]:
        """Decode one duplicate-free UTF-8 JSON object.

        Parameters
        ----------
        payload
            Exact JSON wire bytes.

        Returns
        -------
        dict[str, JsonValue]
            Recursively checked top-level object.

        Raises
        ------
        TypeError
            If ``payload`` is not exact built-in :class:`bytes`, or a decoded
            value lies outside the closed JSON representation.
        ValueError
            If the bytes are not strict UTF-8 JSON, contain duplicate keys or
            nonstandard nonfinite constants, or do not encode an object.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            raw: object = json.loads(
                payload.decode("utf-8"),
                object_pairs_hook=self._unique_object,
                parse_constant=self._reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid strict UTF-8 JSON") from error
        return self.mapping(raw, "root")

    def value(self, raw: object, name: str) -> JsonValue:
        """Validate and copy one closed JSON value recursively."""
        if raw is None:
            return None
        if type(raw) is bool:
            return raw
        if type(raw) is int:
            return raw
        if type(raw) is str:
            return raw
        if type(raw) is float:
            if not np.isfinite(raw):
                raise ValueError(f"{name} must be finite")
            return raw
        if type(raw) is list:
            return [
                self.value(item, f"{name}[{index}]") for index, item in enumerate(raw)
            ]
        if type(raw) is dict:
            mapping_result: dict[str, JsonValue] = {}
            for key, item in raw.items():
                if type(key) is not str:
                    raise TypeError(f"{name} keys must be strings")
                mapping_result[key] = self.value(item, f"{name}.{key}")
            return mapping_result
        raise TypeError(f"{name} contains an unsupported JSON representation")

    def mapping(self, value: object, name: str) -> dict[str, JsonValue]:
        """Validate and return one exact JSON object representation."""
        if type(value) is not dict:
            raise TypeError(f"{name} must be a JSON object")
        result: dict[str, JsonValue] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise TypeError(f"{name} keys must be strings")
            result[key] = self.value(item, f"{name}.{key}")
        return result

    def array(self, value: object, name: str) -> list[JsonValue]:
        """Validate and return one exact JSON array representation."""
        if type(value) is not list:
            raise TypeError(f"{name} must be a JSON array")
        return [
            self.value(item, f"{name}[{index}]") for index, item in enumerate(value)
        ]

    @staticmethod
    def string(value: object, name: str) -> str:
        """Return one exact built-in string, including the empty string."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        return value

    def nonempty_string(self, value: object, name: str) -> str:
        """Return one nonempty exact built-in string."""
        result = self.string(value, name)
        if not result:
            raise ValueError(f"{name} must be nonempty")
        return result

    @staticmethod
    def boolean(value: object, name: str) -> bool:
        """Return one exact built-in Boolean."""
        if type(value) is not bool:
            raise TypeError(f"{name} must be a built-in bool")
        return value

    @staticmethod
    def integer(value: object, name: str) -> int:
        """Return one exact built-in integer while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def real(value: object, name: str) -> float:
        """Return one finite JSON real converted to binary64."""
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{name} must be a real number")
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def integers(self, value: object, name: str) -> tuple[int, ...]:
        """Return one tuple of exact built-in integers."""
        return tuple(self.integer(item, name) for item in self.array(value, name))

    def reals(self, value: object, name: str) -> tuple[float, ...]:
        """Return one tuple of finite binary64 real values."""
        return tuple(self.real(item, name) for item in self.array(value, name))

    def sha256(self, value: object, name: str) -> str:
        """Return one exact lowercase SHA-256 hexadecimal digest."""
        digest = self.nonempty_string(value, name)
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        return digest

    @staticmethod
    def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        """Construct one object while rejecting duplicate keys."""
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(value: str) -> object:
        """Reject JSON extensions such as ``NaN`` and ``Infinity``."""
        raise ValueError(f"non-finite JSON constant is unsupported: {value}")
