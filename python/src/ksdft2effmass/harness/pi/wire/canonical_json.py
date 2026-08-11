"""Strict parsing and canonical encoding for harness JSON wire payloads."""

from __future__ import annotations

import json
from typing import Any


class _DuplicateKey(ValueError):
    """Identify one duplicate object key in an otherwise parseable payload."""


class _CanonicalJsonSerializer:
    """Own strict parsing and canonical encoding for harness JSON objects."""

    __slots__ = ()

    @staticmethod
    def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise _DuplicateKey(key)
            result[key] = value
        return result

    def encode(self, value: dict[str, object]) -> bytes:
        """Encode one wire object using the accepted canonical JSON form."""
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")

    def decode(self, text: str) -> Any:
        """Parse strict RFC 8259 JSON while rejecting duplicate object keys."""
        return json.loads(
            text,
            object_pairs_hook=self._pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
