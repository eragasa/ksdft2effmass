"""Closed JSON decoding support for operator serializer tests."""

from __future__ import annotations

import json
from typing import cast

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


class OperatorJsonTestDecoder:
    """Decode standard JSON text into an explicitly closed test representation."""

    @classmethod
    def decode(cls, text: str) -> JsonValue:
        """Return recursively type-checked JSON state from ``text``."""

        raw_value: object = json.loads(text)
        return cls._parse_value(raw_value)

    @classmethod
    def decode_object(cls, text: str) -> JsonObject:
        """Return a recursively checked top-level JSON object from ``text``."""

        value = cls.decode(text)
        if not isinstance(value, dict):
            msg = "operator serializer test payload must be a JSON object"
            raise TypeError(msg)
        return value

    @classmethod
    def _parse_value(cls, value: object) -> JsonValue:
        """Convert one parser value into the closed JSON test representation."""

        if value is None or isinstance(value, bool | int | float | str):
            return value
        if type(value) is list:
            raw_array = cast(list[object], value)
            return [cls._parse_value(item) for item in raw_array]
        if type(value) is dict:
            raw_object = cast(dict[object, object], value)
            parsed_object: JsonObject = {}
            for key, item in raw_object.items():
                if not isinstance(key, str):
                    msg = "JSON object keys must be strings"
                    raise TypeError(msg)
                parsed_object[key] = cls._parse_value(item)
            return parsed_object
        msg = "parsed JSON test values must use standard JSON types"
        raise TypeError(msg)
