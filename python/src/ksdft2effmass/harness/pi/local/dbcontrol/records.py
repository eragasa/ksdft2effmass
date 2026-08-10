"""Immutable request and result records for project-local control actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import CONTROL_DATABASE_PATH


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationRequest:
    """Explicit repository and destination for one control-state migration."""

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH

    def __post_init__(self) -> None:
        if (
            not isinstance(self.repository_root, Path)
            or not self.repository_root.is_absolute()
        ):
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if not isinstance(self.database_path, Path) or self.database_path.is_absolute():
            raise ValueError("database_path must be repository-relative")


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
