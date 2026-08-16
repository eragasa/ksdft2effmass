"""Private immutable records for project-local projection actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...configuration import PiHarnessConfiguration
from .constants import CONTROL_DATABASE_PATH


@dataclass(frozen=True, slots=True)
class _HarnessProjectionRequest:
    """Explicit inputs for one projection synchronization.

    During synchronization, authoritative Python test sources and canonical evidence
    declarations are observed once into an immutable in-memory corpus.
    Validation and ingestion reuse that corpus and its source identities.

    The maintained SQLite database, deterministic SQL recovery export,
    projection manifest, generated module inventory, and other generated files
    are corpus-derived projections. The generated module inventory is not the
    primary evidence authority.

    ``evidence_module_paths`` selects the authoritative Python sources.
    ``evidence_profile_matrix_path`` and ``evidence_migration_path`` select the
    canonical profile policy and predecessor declarations. An empty evidence corpus
    preserves bounded noncanonical behavior for isolated synchronization callers.

    The five resource fields select one explicit project profile, generic and
    local manifests, and their roots. They are supplied together for canonical
    maintained construction. An omitted resource corpus preserves bounded
    noncanonical compatibility without ambient resource discovery.

    ``pi_harness_configuration`` supplies the already-deserialized project-settings
    subset used by agent projection. Its default empty value preserves bounded
    noncanonical requests without file or runtime discovery.
    """

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH
    evidence_profile_matrix_path: Path | None = None
    evidence_module_paths: tuple[Path, ...] = ()
    evidence_migration_path: Path | None = None
    resource_profile_path: Path | None = None
    generic_resource_manifest_path: Path | None = None
    generic_resource_root_path: Path | None = None
    local_resource_manifest_path: Path | None = None
    local_resource_root_path: Path | None = None
    pi_harness_configuration: PiHarnessConfiguration = PiHarnessConfiguration(1, ())

    def __post_init__(self) -> None:
        if type(self.pi_harness_configuration) is not PiHarnessConfiguration:
            raise TypeError("pi_harness_configuration must be PiHarnessConfiguration")
        if (
            not isinstance(self.repository_root, Path)
            or not self.repository_root.is_absolute()
        ):
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if not isinstance(self.database_path, Path) or self.database_path.is_absolute():
            raise ValueError("database_path must be repository-relative")
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
        if profile_path is not None and not self.evidence_module_paths:
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
class _HarnessProjectionSyncResult:
    """Immutable summary of synchronized structured projection state."""

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
class _HarnessProjectionVerificationFinding:
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
        if type(self.code) is not str:
            raise TypeError("finding code must be str")
        if not self.code or self.code not in _VERIFICATION_FINDING_CODES:
            raise ValueError("unsupported control verification finding code")
        if self.path is not None and type(self.path) is not str:
            raise TypeError("finding path must be str or None")
        if self.path == "":
            raise ValueError("finding path must be nonempty when present")
        if type(self.message) is not str:
            raise TypeError("finding message must be str")
        if not self.message:
            raise ValueError("finding message must be nonempty")


@dataclass(frozen=True, slots=True)
class _HarnessProjectionVerificationResult:
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
    findings: tuple[_HarnessProjectionVerificationFinding, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "integrity_check",
            "semantic_digest",
            "reconstructed_semantic_digest",
            "raw_database_sha256",
            "reconstructed_database_sha256",
        ):
            if type(getattr(self, name)) is not str:
                raise TypeError(f"{name} must be str")
        if type(self.foreign_key_issue_count) is not int:
            raise TypeError("foreign_key_issue_count must be int")
        if self.foreign_key_issue_count < 0:
            raise ValueError("foreign_key_issue_count must be nonnegative")
        for name in (
            "projections_identical",
            "schema_version_agrees",
            "sql_identical",
            "manifest_identical",
        ):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be bool")
        if type(self.findings) is not tuple or any(
            type(item) is not _HarnessProjectionVerificationFinding
            for item in self.findings
        ):
            raise TypeError("findings must contain verification findings")
        key = lambda item: (item.code, item.path or "", item.message)  # noqa: E731
        if self.findings != tuple(sorted(set(self.findings), key=key)):
            raise ValueError("findings must be unique and deterministically sorted")
        represented_agreement = (
            self.integrity_check == "ok"
            and self.foreign_key_issue_count == 0
            and self.semantic_digest == self.reconstructed_semantic_digest
            and self.projections_identical
            and self.schema_version_agrees
            and self.sql_identical
            and self.manifest_identical
        )
        if represented_agreement != (not self.findings):
            raise ValueError("findings must agree with represented verification state")
