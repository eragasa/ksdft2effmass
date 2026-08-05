"""Root-confined checksum records and validation."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .identity import (
    ArtifactIdentity,
    ResourcePath,
    _require_path,
    _require_tuple,
    _require_version,
)
from .resources import _confined_file
from .validation import ValidationResult, _issue, _result


@dataclass(frozen=True, slots=True)
class ChecksumEntry:
    """Expected exact byte identity for one root-relative regular file."""

    schema_version: int
    path: ResourcePath
    content_identity: ArtifactIdentity

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_path(self.path, "path")
        if type(self.content_identity) is not ArtifactIdentity:
            raise TypeError("content_identity must be ArtifactIdentity")


@dataclass(frozen=True, slots=True)
class ChecksumManifest:
    """Strictly path-sorted nonempty checksum entry set."""

    schema_version: int
    entries: tuple[ChecksumEntry, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_tuple(self.entries, "entries")
        if not self.entries or any(type(e) is not ChecksumEntry for e in self.entries):
            raise TypeError("entries must be nonempty ChecksumEntry tuple")
        paths = tuple(e.path for e in self.entries)
        if paths != tuple(sorted(paths)) or len(set(paths)) != len(paths):
            raise ValueError("entries must be unique and path-sorted")


class ValidateChecksumManifest:
    """Compare declared identities below one explicit root without repair."""

    __slots__ = ()

    def execute(self, root: Path, manifest: ChecksumManifest) -> ValidationResult:
        if not isinstance(root, Path) or type(manifest) is not ChecksumManifest:
            raise TypeError("root/manifest has wrong type")
        if not root.is_absolute() or not root.exists() or not root.is_dir():
            return _result(
                (_issue("PIH.PATH.ROOT_INVALID", "Explicit checksum root is invalid."),)
            )
        issues = []
        for entry in manifest.entries:
            path, problem = _confined_file(root, entry.path)
            if problem is not None:
                code = (
                    "PIH.CHECKSUM.FILE_MISSING"
                    if problem.code == "PIH.PATH.MISSING"
                    else problem.code
                )
                issues.append(
                    _issue(
                        code,
                        "Checksum entry file is unavailable."
                        if code == "PIH.CHECKSUM.FILE_MISSING"
                        else problem.message,
                        path=entry.path,
                    )
                )
                continue
            if path is None:
                raise AssertionError("successful confinement must return a path")
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                issues.append(
                    _issue(
                        "PIH.CHECKSUM.FILE_MISSING",
                        "Checksum entry file became unavailable.",
                        path=entry.path,
                    )
                )
                continue
            if digest != entry.content_identity.digest:
                issues.append(
                    _issue(
                        "PIH.CHECKSUM.HASH_MISMATCH",
                        "Checksum entry bytes differ.",
                        path=entry.path,
                    )
                )
        return _result(tuple(issues))
