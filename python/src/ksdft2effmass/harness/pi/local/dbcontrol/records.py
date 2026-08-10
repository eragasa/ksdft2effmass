"""Immutable request and result records for project-local control actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import CONTROL_DATABASE_PATH


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationRequest:
    """Explicit inputs for one control-state migration.

    During migration, authoritative Python test sources and canonical evidence
    declarations are observed once into an immutable in-memory corpus.
    Validation and ingestion reuse that corpus and its source identities.

    The maintained SQLite database, deterministic SQL recovery export,
    projection manifest, generated module inventory, and other generated files
    are corpus-derived projections. The generated module inventory is not the
    primary evidence authority.

    ``evidence_module_paths`` selects the authoritative Python sources.
    ``evidence_profile_matrix_path`` and ``evidence_migration_path`` select the
    canonical profile policy and predecessor declarations. The retained
    ``evidence_module_ownership_path`` compatibility field is rejected by
    canonical corpus construction because generated or external ownership
    inventories are projections rather than evidence authority. An empty
    evidence corpus preserves bounded noncanonical compatibility for isolated
    migration callers.
    """

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH
    evidence_module_ownership_path: Path | None = None
    evidence_profile_matrix_path: Path | None = None
    evidence_module_paths: tuple[Path, ...] = ()
    evidence_migration_path: Path | None = None

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
        profile_path = self.evidence_profile_matrix_path
        if profile_path is not None and not isinstance(profile_path, Path):
            raise TypeError(
                "evidence_profile_matrix_path must be a pathlib.Path or None"
            )
        if type(self.evidence_module_paths) is not tuple or any(
            not isinstance(path, Path) for path in self.evidence_module_paths
        ):
            raise TypeError(
                "evidence_module_paths must be a tuple of pathlib.Path values"
            )
        if len(self.evidence_module_paths) != len(set(self.evidence_module_paths)):
            raise ValueError("evidence_module_paths must be unique")
        migration_path = self.evidence_migration_path
        if migration_path is not None and not isinstance(migration_path, Path):
            raise TypeError("evidence_migration_path must be a pathlib.Path or None")
        if (
            profile_path is not None
            and not self.evidence_module_paths
            and ownership_path is None
        ):
            raise ValueError(
                "evidence_profile_matrix_path requires evidence_module_paths"
            )
        if self.evidence_module_paths and (
            profile_path is None or migration_path is None
        ):
            raise ValueError(
                "evidence_module_paths require explicit profile and migration inputs"
            )
        for name, path in (
            ("database_path", self.database_path),
            ("evidence_module_ownership_path", ownership_path),
            ("evidence_profile_matrix_path", profile_path),
            ("evidence_migration_path", migration_path),
            *(("evidence_module_paths", path) for path in self.evidence_module_paths),
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
