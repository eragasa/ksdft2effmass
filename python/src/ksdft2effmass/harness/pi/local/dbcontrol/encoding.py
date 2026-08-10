"""Deterministic hashing, JSON encoding, and identifier slugging."""

from __future__ import annotations

import hashlib
import json
import re


class _ControlEncoding:
    """Own deterministic control identities and textual encodings."""

    __slots__ = ()

    @staticmethod
    def sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def json_bytes(value: object) -> bytes:
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()

    @staticmethod
    def canonical_json_bytes(value: object) -> bytes:
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode()

    @staticmethod
    def slug(value: str) -> str:
        value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
        return re.sub(r"-+", "-", value) or "unnamed"
