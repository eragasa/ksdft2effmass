"""Immutable SHA-256 identities for Architecture-v2 harness values."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """SHA-256 identity of exact source bytes."""

    schema_version: int
    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        _validate_identity(self.schema_version, self.algorithm, self.digest)


@dataclass(frozen=True, slots=True)
class SnapshotIdentity:
    """SHA-256 identity of one framed resolved configuration snapshot."""

    schema_version: int
    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        _validate_identity(self.schema_version, self.algorithm, self.digest)


def _validate_identity(
    schema_version: object, algorithm: object, digest: object
) -> None:
    if type(schema_version) is not int:
        raise TypeError("schema_version must be an int excluding bool")
    if schema_version != 1:
        raise ValueError("schema_version must equal 1")
    if type(algorithm) is not str:
        raise TypeError("algorithm must be a built-in str")
    if algorithm != "sha256":
        raise ValueError("algorithm must equal sha256")
    if type(digest) is not str:
        raise TypeError("digest must be a built-in str")
    if re.fullmatch(r"[0-9a-f]{64}", digest, re.ASCII) is None:
        raise ValueError("digest must contain 64 lowercase hexadecimal characters")
