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

    The five resource fields select one explicit project profile, generic and
    local manifests, and their roots. They are supplied together for canonical
    maintained construction. An omitted resource corpus preserves bounded
    noncanonical compatibility without ambient resource discovery.
    """

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH
    evidence_module_ownership_path: Path | None = None
    evidence_profile_matrix_path: Path | None = None
    evidence_module_paths: tuple[Path, ...] = ()
    evidence_migration_path: Path | None = None
    resource_profile_path: Path | None = None
    generic_resource_manifest_path: Path | None = None
    generic_resource_root_path: Path | None = None
    local_resource_manifest_path: Path | None = None
    local_resource_root_path: Path | None = None

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
        resource_paths = (
            self.resource_profile_path,
            self.generic_resource_manifest_path,
            self.generic_resource_root_path,
            self.local_resource_manifest_path,
            self.local_resource_root_path,
        )
        if any(
            path is not None and not isinstance(path, Path) for path in resource_paths
        ):
            raise TypeError("resource inputs must be pathlib.Path values or None")
        if any(path is not None for path in resource_paths) and any(
            path is None for path in resource_paths
        ):
            raise ValueError("canonical resource inputs must be supplied together")
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
            ("resource_profile_path", self.resource_profile_path),
            ("generic_resource_manifest_path", self.generic_resource_manifest_path),
            ("generic_resource_root_path", self.generic_resource_root_path),
            ("local_resource_manifest_path", self.local_resource_manifest_path),
            ("local_resource_root_path", self.local_resource_root_path),
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


_VERIFICATION_FINDING_CODES = {
    "changed_artifact",
    "foreign_key_failure",
    "integrity_failure",
    "missing_artifact",
    "schema_disagreement",
    "semantic_disagreement",
    "source_input_failure",
    "unexpected_artifact",
}


@dataclass(frozen=True, slots=True)
class HarnessControlVerificationFinding:
    """One deterministic maintained-control disagreement.

    Parameters
    ----------
    code
        Closed structural disagreement identity.
    path
        Repository-relative affected path, or ``None`` for database-wide facts.
    message
        Stable human-readable explanation without runtime or timing data.
    """

    code: str
    path: str | None
    message: str

    def __post_init__(self) -> None:
        if type(self.code) is not str or self.code not in _VERIFICATION_FINDING_CODES:
            raise ValueError("unsupported control verification finding code")
        if self.path is not None and (type(self.path) is not str or not self.path):
            raise TypeError("finding path must be a nonempty str or None")
        if type(self.message) is not str or not self.message:
            raise TypeError("finding message must be a nonempty str")


@dataclass(frozen=True, slots=True)
class HarnessControlVerificationResult:
    """Immutable deterministic source-aware control verification result.

    Raw SQLite hashes are diagnostic only. Conformance is determined from integrity,
    foreign keys, schema version, normalized logical table content, canonical SQL,
    and exact publisher-owned projections.
    """

    integrity_check: str
    foreign_key_issue_count: int
    semantic_digest: str
    reconstructed_semantic_digest: str
    raw_database_sha256: str
    reconstructed_database_sha256: str
    projections_identical: bool
    schema_version_agrees: bool = True
    sql_identical: bool = True
    manifest_identical: bool = True
    findings: tuple[HarnessControlVerificationFinding, ...] = ()

    def __post_init__(self) -> None:
        if type(self.foreign_key_issue_count) is not int:
            raise TypeError("foreign_key_issue_count must be int")
        for name in (
            "projections_identical",
            "schema_version_agrees",
            "sql_identical",
            "manifest_identical",
        ):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be bool")
        if type(self.findings) is not tuple or any(
            type(item) is not HarnessControlVerificationFinding
            for item in self.findings
        ):
            raise TypeError("findings must contain verification findings")
        key = lambda item: (item.code, item.path or "", item.message)  # noqa: E731
        if self.findings != tuple(sorted(set(self.findings), key=key)):
            raise ValueError("findings must be unique and deterministically sorted")
