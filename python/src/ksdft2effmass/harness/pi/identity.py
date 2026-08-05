"""Identity and lexical primitive ownership for the generic PI harness."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import TypeAlias

Identifier: TypeAlias = str  # noqa: UP040 - contract requires built-in str aliases
ResourcePath: TypeAlias = str  # noqa: UP040
OwnershipScopePath: TypeAlias = str  # noqa: UP040
DiagnosticPath: TypeAlias = str  # noqa: UP040
Version: TypeAlias = int  # noqa: UP040

_MAX_VERSION = 2**53 - 1
_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*\Z", re.ASCII)
_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def _require_builtin_str(value: object, field: str, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if nonempty and not value:
        raise ValueError(f"{field} must be nonempty")
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise ValueError(f"{field} contains an unpaired surrogate")
    return value


def _require_identifier(value: object, field: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if not value:
        raise ValueError(f"PIH.ID.EMPTY: {field} must be nonempty")
    if _IDENTIFIER_RE.fullmatch(value) is None:
        raise ValueError(f"PIH.ID.INVALID_ASCII: {field} is not a version-1 Identifier")
    return value


def _require_version(
    value: object, field: str, *, minimum: int = 1, maximum: int = _MAX_VERSION
) -> int:
    if type(value) is not int:
        raise TypeError(f"{field} must be an int excluding bool")
    if not minimum <= value <= maximum:
        raise ValueError(f"{field} is outside [{minimum}, {maximum}]")
    return value


def _require_tuple(value: object, field: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{field} must be a tuple")
    return value


def _require_sorted_unique(values: tuple[str, ...], field: str) -> None:
    if tuple(sorted(values)) != values or len(set(values)) != len(values):
        raise ValueError(f"{field} must be unique and strictly sorted")


def _require_path(value: object, field: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if not value:
        raise ValueError(f"PIH.PATH.EMPTY: {field} must be nonempty")
    if value.startswith("/"):
        raise ValueError(f"PIH.PATH.ABSOLUTE: {field} must be relative")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"PIH.PATH.NONCANONICAL_UNICODE: {field} must be NFC")
    if _DRIVE_RE.match(value):
        raise ValueError(f"PIH.PATH.WINDOWS_SYNTAX: {field} has a drive prefix")
    if "\\" in value:
        code = (
            "PIH.PATH.WINDOWS_SYNTAX"
            if value.startswith("\\\\")
            else "PIH.PATH.INVALID_CHARACTER"
        )
        raise ValueError(f"{code}: {field} contains a backslash")
    if value.endswith("/") or "//" in value:
        raise ValueError(f"PIH.PATH.INVALID_SEGMENT: {field} has an empty segment")
    for part in value.split("/"):
        if part in {"", ".", ".."}:
            raise ValueError(
                f"PIH.PATH.INVALID_SEGMENT: {field} has a traversal segment"
            )
        stem = part.split(".", 1)[0].upper()
        if stem in _DEVICE_NAMES:
            raise ValueError(f"PIH.PATH.WINDOWS_SYNTAX: {field} has a device name")
    if any(
        ord(c) < 32
        or 0x7F <= ord(c) <= 0x9F
        or ord(c) in {0x2028, 0x2029}
        or 0xD800 <= ord(c) <= 0xDFFF
        for c in value
    ):
        raise ValueError(
            f"PIH.PATH.INVALID_CHARACTER: {field} has a prohibited character"
        )
    return value


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """SHA-256 identity of exact represented bytes."""

    schema_version: int
    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        _require_version(self.schema_version, "schema_version")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        _require_builtin_str(self.algorithm, "algorithm")
        if self.algorithm != "sha256":
            raise ValueError(
                "PIH.ARTIFACT.ALGORITHM_UNSUPPORTED: algorithm must equal 'sha256'"
            )
        _require_builtin_str(self.digest, "digest")
        if re.fullmatch(r"[0-9a-f]{64}", self.digest, re.ASCII) is None:
            raise ValueError(
                "PIH.ARTIFACT.DIGEST_INVALID: digest must contain 64 lowercase "
                "hexadecimal characters"
            )


class HarnessInternalError(RuntimeError):
    """Unexpected programming or post-selection runtime failure."""

    __slots__ = ("operation", "detail", "_locked")

    def __init__(self, operation: Identifier, detail: str) -> None:
        operation = _require_identifier(operation, "operation")
        detail = _require_builtin_str(detail, "detail", nonempty=False)
        RuntimeError.__init__(self, f"{operation}: {detail}")
        object.__setattr__(self, "operation", operation)
        object.__setattr__(self, "detail", detail)
        object.__setattr__(self, "_locked", True)

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_locked", False):
            raise AttributeError("HarnessInternalError attributes are immutable")
        object.__setattr__(self, name, value)
