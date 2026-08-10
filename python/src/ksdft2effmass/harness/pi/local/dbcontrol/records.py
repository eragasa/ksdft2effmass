"""Immutable request and result records for project-local control actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import CONTROL_DATABASE_PATH


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationRequest:
    """Explicit inputs for one control-state migration.

    ``evidence_module_ownership_path`` optionally selects a repository-relative
    Python-conformance ownership document.  When omitted, migration preserves
    the compatibility behavior of reading the generated module inventory.
    """

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH
    evidence_module_ownership_path: Path | None = None

    def __post_init__(self) -> None:
        if (
            not isinstance(self.repository_root, Path)
            or not self.repository_root.is_absolute()
        ):
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if not isinstance(self.database_path, Path) or self.database_path.is_absolute():
            raise ValueError("database_path must be repository-relative")
        ownership_path = self.evidence_module_ownership_path
        if ownership_path is not None and not isinstance(ownership_path, Path):
            raise TypeError(
                "evidence_module_ownership_path must be a pathlib.Path or None"
            )
        for name, path in (
            ("database_path", self.database_path),
            ("evidence_module_ownership_path", ownership_path),
        ):
            if path is not None and (
                path == Path(".") or ".." in path.parts or path.is_absolute()
            ):
                raise ValueError(
                    f"{name} must be a root-confined repository-relative path"
                )


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationResult:
    """Immutable summary of migrated structured control state."""

    schema_version: int
    semantic_digest: str
    counts: tuple[tuple[str, int], ...]
    unresolved_naming_issues: tuple[str, ...]
    projection_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HarnessControlVerificationResult:
    """Immutable deterministic reconstruction and integrity result."""

    integrity_check: str
    foreign_key_issue_count: int
    semantic_digest: str
    reconstructed_semantic_digest: str
    raw_database_sha256: str
    reconstructed_database_sha256: str
    projections_identical: bool
