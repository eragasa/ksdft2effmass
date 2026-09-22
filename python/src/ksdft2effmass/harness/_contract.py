"""Private mechanics shared by strict Architecture-v2 Harness contracts."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import unicodedata
from dataclasses import fields, is_dataclass
from datetime import datetime
from typing import Any

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*\Z", re.ASCII)
_DIGEST = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_UINT64_MAX = 2**64 - 1


def require_str(value: object, name: str, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if nonempty and not value:
        raise ValueError(f"{name} must be nonempty")
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise ValueError(f"{name} contains an unpaired surrogate")
    return value


def require_identifier(value: object, name: str) -> str:
    result = require_str(value, name)
    if _IDENTIFIER.fullmatch(result) is None:
        raise ValueError(f"{name} must satisfy the Identifier grammar")
    return result


def require_digest(value: object, name: str) -> str:
    result = require_str(value, name)
    if _DIGEST.fullmatch(result) is None:
        raise ValueError(f"{name} must be a SHA-256 digest")
    return result


def require_uint64(value: object, name: str, *, positive: bool = False) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int excluding bool")
    minimum = 1 if positive else 0
    if not minimum <= value <= _UINT64_MAX:
        raise ValueError(f"{name} must be between {minimum} and 2^64-1")
    return value


def require_path(value: object, name: str) -> str:
    result = require_str(value, name)
    if unicodedata.normalize("NFC", result) != result:
        raise ValueError(f"{name} must be NFC")
    if result.startswith("/") or "\\" in result or result.endswith("/"):
        raise ValueError(f"{name} must be a root-relative POSIX path")
    if any(part in {"", ".", ".."} for part in result.split("/")):
        raise ValueError(f"{name} contains an invalid path segment")
    if any(ord(char) < 32 or 0x7F <= ord(char) <= 0x9F for char in result):
        raise ValueError(f"{name} contains a prohibited character")
    return result


def require_timestamp(value: object, name: str) -> str:
    result = require_str(value, name)
    if not result.endswith("Z"):
        raise ValueError(f"{name} must be RFC 3339 UTC text")
    try:
        parsed = datetime.fromisoformat(result[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{name} must be RFC 3339 UTC text") from exc
    offset = parsed.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise ValueError(f"{name} must be UTC")
    return result


def require_tuple(
    value: object, name: str, *, nonempty: bool = False
) -> tuple[Any, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be a tuple")
    if nonempty and not value:
        raise ValueError(f"{name} must be nonempty")
    return value


def require_canonical(
    values: tuple[str, ...], name: str, *, nonempty: bool = False
) -> None:
    require_tuple(values, name, nonempty=nonempty)
    if values != tuple(sorted(set(values))):
        raise ValueError(f"{name} must be strictly sorted and duplicate-free")


def b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def b64_decode(value: object, name: str, size: int) -> bytes:
    text = require_str(value, name)
    if "=" in text:
        raise ValueError(f"{name} must be unpadded canonical base64url")
    try:
        decoded = base64.b64decode(
            text + "=" * (-len(text) % 4), altchars=b"-_", validate=True
        )
    except ValueError as exc:
        raise ValueError(f"{name} must be canonical base64url") from exc
    if len(decoded) != size or b64_encode(decoded) != text:
        raise ValueError(f"{name} must encode exactly {size} bytes canonically")
    return decoded


def wire_value(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: wire_value(getattr(value, field.name))
            for field in fields(value)
        }
    if type(value) is dict:
        return {key: wire_value(item) for key, item in value.items()}
    if type(value) in {tuple, list}:
        return [wire_value(item) for item in value]
    if type(value) is bytes:
        return b64_encode(value)
    return value


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            wire_value(value),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def strict_json(payload: bytes) -> Any:
    if type(payload) is not bytes:
        raise TypeError("payload must be built-in bytes")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise ValueError("payload must not contain a UTF-8 BOM")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key {key}")
            result[key] = value
        return result

    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("payload must contain one UTF-8 JSON value") from exc


def closed(value: object, expected: set[str], name: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise TypeError(f"{name} must be a JSON object")
    missing, unknown = expected - set(value), set(value) - expected
    if missing:
        raise ValueError(f"missing {name} field {sorted(missing)[0]}")
    if unknown:
        raise ValueError(f"unknown {name} field {sorted(unknown)[0]}")
    return value


def derived_identity(domain: str, value: object, identity_field: str) -> str:
    body = wire_value(value)
    if type(body) is not dict:
        raise TypeError("identity-bearing value must be a record")
    body[identity_field] = None
    encoded = canonical_bytes(body)
    framed = (
        domain.encode("ascii")
        + b"\x00v1\x00"
        + len(encoded).to_bytes(8, "big")
        + encoded
    )
    return hashlib.sha256(framed).hexdigest()


def require_derived_identity(value: object, field: str, domain: str) -> None:
    observed = require_digest(getattr(value, field), field)
    if observed != derived_identity(domain, value, field):
        raise ValueError(f"{field} does not match the derived identity")


def identity_from_fields(domain: str, body: dict[str, object]) -> str:
    """Return the framed identity of an already prepared body."""
    encoded = canonical_bytes(body)
    framed = (
        domain.encode("ascii")
        + b"\x00v1\x00"
        + len(encoded).to_bytes(8, "big")
        + encoded
    )
    return hashlib.sha256(framed).hexdigest()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
