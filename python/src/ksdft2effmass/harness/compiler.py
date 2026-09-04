"""Deterministic loading and compilation of complete development-harness state.

The loader consumes one explicit root, closed source contract, and injected Pi
configuration.  It performs bounded local file reads without following symlinks.
The compiler is pure: it normalizes only the closed typed snapshot and returns one
complete state or a represented failure.  Neither action validates development
policy, grants authority, persists state, projects artifacts, or performs scientific
or protected execution.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Literal

from ._compiler_serialization import _HarnessCompilerSerializer
from .decisions import DevelopmentDecision, DevelopmentDecisionSerializer
from .pi import (
    JsonRecordDeserializer,
    PiHarnessAgentDefinition,
    PiHarnessAgentDefinitionResolver,
    PiHarnessConfiguration,
    ResourceManifest,
    SkillDescriptor,
    WireRecordKind,
)
from .pi.conformance.python import PythonModuleSource
from .task import HarnessTask, HarnessTaskDeserializer, HarnessTaskRegistry
from .task_selection import (
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionDeserializer,
)


class HarnessSourceFamily(StrEnum):
    """Closed canonical source-family order for compiler inputs."""

    TASK = "task"
    TASK_SELECTION = "task_selection"
    DEVELOPMENT_DECISION = "development_decision"
    CAPABILITY = "capability"
    RESOURCE = "resource"
    AGENT_DEFINITION = "agent_definition"
    EVIDENCE = "evidence"


class HarnessCompilerPhase(StrEnum):
    """Phase that owns one compiler diagnostic."""

    LOADING = "loading"
    COMPILATION = "compilation"


class HarnessDiagnosticSeverity(StrEnum):
    """Closed diagnostic severity vocabulary."""

    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class HarnessCompilerFailureCode(StrEnum):
    """Closed stable loader and compiler failure-code vocabulary."""

    INVALID_ROOT = "invalid_root"
    INVALID_SOURCE_CONTRACT = "invalid_source_contract"
    MISSING_SOURCE = "missing_source"
    UNEXPECTED_SOURCE = "unexpected_source"
    PATH_ESCAPE = "path_escape"
    CASE_MISMATCH = "case_mismatch"
    SYMLINK_REJECTED = "symlink_rejected"
    UNSUPPORTED_FILE_TYPE = "unsupported_file_type"
    READ_FAILURE = "read_failure"
    SOURCE_CHANGED = "source_changed"
    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DECODE_FAILURE = "decode_failure"
    UNSUPPORTED_FORMAT_VERSION = "unsupported_format_version"
    DUPLICATE_SOURCE_PATH = "duplicate_source_path"
    SOURCE_FAMILY_MISMATCH = "source_family_mismatch"
    DUPLICATE_CANONICAL_IDENTITY = "duplicate_canonical_identity"
    AMBIGUOUS_ALIAS = "ambiguous_alias"
    UNREPRESENTABLE_NORMALIZATION = "unrepresentable_normalization"
    INTERNAL_CONTRACT_VIOLATION = "internal_contract_violation"


class HarnessSourceLoadStatus(StrEnum):
    """Closed repository-load outcome status."""

    LOADED = "loaded"
    FAILED = "failed"


class HarnessCompilationStatus(StrEnum):
    """Closed compilation outcome status."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


_PATH_DRIVE = re.compile(r"^[A-Za-z]:")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_POINTER = re.compile(r"(?:|/(?:[^~]|~[01])*)\Z")
_MAX_SOURCE_BYTES = 16 * 1024 * 1024
_FAMILY_FORMAT_VERSIONS = {
    HarnessSourceFamily.TASK: 3,
    HarnessSourceFamily.TASK_SELECTION: 1,
    HarnessSourceFamily.DEVELOPMENT_DECISION: 1,
    HarnessSourceFamily.CAPABILITY: 1,
    HarnessSourceFamily.RESOURCE: 1,
    HarnessSourceFamily.AGENT_DEFINITION: 1,
    HarnessSourceFamily.EVIDENCE: 1,
}
_FAMILY_MINIMUM_COUNTS = {
    HarnessSourceFamily.TASK: 1,
    HarnessSourceFamily.TASK_SELECTION: 1,
    HarnessSourceFamily.DEVELOPMENT_DECISION: 0,
    HarnessSourceFamily.CAPABILITY: 1,
    HarnessSourceFamily.RESOURCE: 1,
    HarnessSourceFamily.AGENT_DEFINITION: 1,
    HarnessSourceFamily.EVIDENCE: 1,
}


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessLegacyDecisionBinding:
    """Explicit one-way adaptation inputs for one legacy checkpoint source.

    ``source_path`` is the exact repository-relative checkpoint path.
    ``decision_id`` and optional predecessor are caller-supplied identities and are
    never inferred from source text, file name, content identity, or ordering.
    """

    source_path: PurePosixPath
    decision_id: str
    predecessor_decision_id: str | None
    adapter_version: str

    def __post_init__(self) -> None:
        self._require_path(self.source_path, "source_path")
        for name, value in (
            ("decision_id", self.decision_id),
            ("adapter_version", self.adapter_version),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if self.predecessor_decision_id is not None:
            if type(self.predecessor_decision_id) is not str:
                raise TypeError(
                    "predecessor_decision_id must be a built-in str or None"
                )
            if not self.predecessor_decision_id:
                raise ValueError("predecessor_decision_id must be nonempty")

    @staticmethod
    def _require_path(value: PurePosixPath, field: str) -> None:
        if type(value) is not PurePosixPath:
            raise TypeError(f"{field} must be PurePosixPath")
        text = value.as_posix()
        if text in {"", "."} or value.is_absolute() or ".." in value.parts:
            raise ValueError(f"{field} must be a confined repository-relative path")
        if (
            unicodedata.normalize("NFC", text) != text
            or "\\" in text
            or _PATH_DRIVE.match(text)
        ):
            raise ValueError(f"{field} must be a normalized NFC POSIX path")


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceFamilyContract:
    """Closed selected source paths for one semantic family.

    ``catalog_roots`` permits the plural roots already owned by harness
    configuration. Paths and roots are NFC repository-relative POSIX paths sorted
    strictly by UTF-8 bytes. Every selected path must lie beneath one root.
    """

    family: HarnessSourceFamily
    catalog_roots: tuple[PurePosixPath, ...]
    source_paths: tuple[PurePosixPath, ...]
    format_version: int
    minimum_count: int

    def __post_init__(self) -> None:
        if type(self.family) is not HarnessSourceFamily:
            raise TypeError("family must be HarnessSourceFamily")
        if (
            type(self.catalog_roots) is not tuple
            or type(self.source_paths) is not tuple
        ):
            raise TypeError("catalog_roots and source_paths must be tuples")
        if not self.catalog_roots:
            raise ValueError("catalog_roots must be nonempty")
        for root in self.catalog_roots:
            HarnessLegacyDecisionBinding._require_path(root, "catalog_roots item")
        for path in self.source_paths:
            HarnessLegacyDecisionBinding._require_path(path, "source_paths item")
        root_keys = tuple(
            root.as_posix().encode("utf-8") for root in self.catalog_roots
        )
        path_keys = tuple(path.as_posix().encode("utf-8") for path in self.source_paths)
        if root_keys != tuple(sorted(set(root_keys))):
            raise ValueError("catalog_roots must be strictly UTF-8 sorted and unique")
        if path_keys != tuple(sorted(set(path_keys))):
            raise ValueError("source_paths must be strictly UTF-8 sorted and unique")
        if type(self.format_version) is not int or type(self.minimum_count) is not int:
            raise TypeError("format_version and minimum_count must be built-in ints")
        expected_version = _FAMILY_FORMAT_VERSIONS[self.family]
        expected_minimum = _FAMILY_MINIMUM_COUNTS[self.family]
        if self.format_version != expected_version:
            raise ValueError(
                f"{self.family.value} format_version must equal {expected_version}"
            )
        if self.minimum_count != expected_minimum:
            raise ValueError(
                f"{self.family.value} minimum_count must equal {expected_minimum}"
            )
        if len(self.source_paths) < expected_minimum:
            raise ValueError("source_paths does not satisfy the family minimum")
        if (
            self.family is HarnessSourceFamily.TASK_SELECTION
            and len(self.source_paths) != 1
        ):
            raise ValueError("task selection requires exactly one path")
        if any(
            not any(path.is_relative_to(root) for root in self.catalog_roots)
            for path in self.source_paths
        ):
            raise ValueError("every source path must be beneath a catalog root")


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceContract:
    """Explicit repository and complete source-family selection for one load."""

    schema_version: Literal[1]
    repository_root: Path
    families: tuple[HarnessSourceFamilyContract, ...]
    symlink_policy: Literal["reject"]
    legacy_decision_bindings: tuple[HarnessLegacyDecisionBinding, ...] = ()

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in int")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute() or ".." in self.repository_root.parts:
            raise ValueError("repository_root must be absolute without traversal")
        if type(self.families) is not tuple or any(
            type(item) is not HarnessSourceFamilyContract for item in self.families
        ):
            raise TypeError("families must contain HarnessSourceFamilyContract values")
        if tuple(item.family for item in self.families) != tuple(HarnessSourceFamily):
            raise ValueError("families must contain every family once in enum order")
        if self.symlink_policy != "reject":
            raise ValueError("symlink_policy must equal reject")
        if type(self.legacy_decision_bindings) is not tuple or any(
            type(item) is not HarnessLegacyDecisionBinding
            for item in self.legacy_decision_bindings
        ):
            raise TypeError("legacy_decision_bindings must contain exact bindings")
        paths = tuple(
            item.source_path.as_posix().encode("utf-8")
            for item in self.legacy_decision_bindings
        )
        if paths != tuple(sorted(set(paths))):
            raise ValueError("legacy_decision_bindings must be path-sorted and unique")
        decision_paths = set(self.families[2].source_paths)
        if any(
            binding.source_path not in decision_paths
            for binding in self.legacy_decision_bindings
        ):
            raise ValueError(
                "legacy decision binding must name a selected decision path"
            )

    @property
    def source_contract_identity(self) -> str:
        """Return the exact root-independent identity derived from this contract."""
        return _HarnessCompilerSerializer().source_contract_identity(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceIdentity:
    """Exact identity of one loaded repository source."""

    family: HarnessSourceFamily
    relative_path: PurePosixPath
    format_version: int
    sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.family) is not HarnessSourceFamily:
            raise TypeError("family must be HarnessSourceFamily")
        HarnessLegacyDecisionBinding._require_path(self.relative_path, "relative_path")
        if type(self.format_version) is not int or type(self.byte_count) is not int:
            raise TypeError("format_version and byte_count must be built-in ints")
        if self.format_version < 1 or self.byte_count < 0:
            raise ValueError(
                "format_version must be positive and byte_count nonnegative"
            )
        if type(self.sha256) is not str:
            raise TypeError("sha256 must be a built-in str")
        if _DIGEST.fullmatch(self.sha256) is None:
            raise ValueError("sha256 must be 64 lowercase hexadecimal characters")


type HarnessParsedValue = (
    HarnessTask
    | DevelopmentTaskSelection
    | DevelopmentDecision
    | SkillDescriptor
    | ResourceManifest
    | PiHarnessAgentDefinition
    | PythonModuleSource
)


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceProvenance:
    """Map one source location to one normalized aggregate location."""

    source_identity: HarnessSourceIdentity
    source_location: str
    normalized_location: str

    def __post_init__(self) -> None:
        if type(self.source_identity) is not HarnessSourceIdentity:
            raise TypeError("source_identity must be HarnessSourceIdentity")
        for name, value in (
            ("source_location", self.source_location),
            ("normalized_location", self.normalized_location),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _POINTER.fullmatch(value) is None:
                raise ValueError(f"{name} must be empty or an RFC 6901 pointer")

    @property
    def sort_key(self) -> tuple[str, bytes, str]:
        """Return canonical normalized/source/source-location order."""
        return (
            self.normalized_location,
            self.source_identity.relative_path.as_posix().encode("utf-8"),
            self.source_location,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceRecord:
    """One identity, typed decoded value, and its ordered provenance."""

    identity: HarnessSourceIdentity
    value: HarnessParsedValue
    provenance: tuple[HarnessSourceProvenance, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not HarnessSourceIdentity:
            raise TypeError("identity must be HarnessSourceIdentity")
        if type(self.value) not in HarnessSourceRecord._value_types():
            raise TypeError("value must belong to HarnessParsedValue")
        if type(self.provenance) is not tuple or any(
            type(item) is not HarnessSourceProvenance for item in self.provenance
        ):
            raise TypeError("provenance must contain HarnessSourceProvenance values")
        if any(item.source_identity != self.identity for item in self.provenance):
            raise ValueError("record provenance must name its identity")

    @staticmethod
    def _value_types() -> tuple[
        type[HarnessTask]
        | type[DevelopmentTaskSelection]
        | type[DevelopmentDecision]
        | type[SkillDescriptor]
        | type[ResourceManifest]
        | type[PiHarnessAgentDefinition]
        | type[PythonModuleSource],
        ...,
    ]:
        return (
            HarnessTask,
            DevelopmentTaskSelection,
            DevelopmentDecision,
            SkillDescriptor,
            ResourceManifest,
            PiHarnessAgentDefinition,
            PythonModuleSource,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceSnapshot:
    """Closed immutable source observation consumed by the pure compiler."""

    schema_version: Literal[1]
    snapshot_identity: str
    source_contract_identity: str
    identities: tuple[HarnessSourceIdentity, ...]
    records: tuple[HarnessSourceRecord, ...]
    provenance: tuple[HarnessSourceProvenance, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in int")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        for name, value in (
            ("snapshot_identity", self.snapshot_identity),
            ("source_contract_identity", self.source_contract_identity),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _DIGEST.fullmatch(value) is None:
                raise ValueError(f"{name} must be a SHA-256 digest")
        if type(self.identities) is not tuple or any(
            type(item) is not HarnessSourceIdentity for item in self.identities
        ):
            raise TypeError("identities must contain HarnessSourceIdentity values")
        if type(self.records) is not tuple or any(
            type(item) is not HarnessSourceRecord for item in self.records
        ):
            raise TypeError("records must contain HarnessSourceRecord values")
        if tuple(record.identity for record in self.records) != self.identities:
            raise ValueError("identities and records must be one-to-one and ordered")
        canonical_identities = tuple(
            sorted(
                self.identities,
                key=lambda item: (
                    tuple(HarnessSourceFamily).index(item.family),
                    item.relative_path.as_posix().encode("utf-8"),
                ),
            )
        )
        if self.identities != canonical_identities or len(set(self.identities)) != len(
            self.identities
        ):
            raise ValueError("source identities must be canonically ordered and unique")
        if type(self.provenance) is not tuple or any(
            type(item) is not HarnessSourceProvenance for item in self.provenance
        ):
            raise TypeError("provenance must contain HarnessSourceProvenance values")
        flattened = tuple(item for record in self.records for item in record.provenance)
        canonical_provenance = tuple(
            sorted(
                flattened,
                key=lambda item: (
                    item.normalized_location,
                    item.source_identity.relative_path.as_posix().encode("utf-8"),
                    item.source_location,
                ),
            )
        )
        if self.provenance != canonical_provenance:
            raise ValueError(
                "snapshot provenance must equal canonical record provenance closure"
            )
        if not _HarnessCompilerSerializer().snapshot_is_consistent(self):
            raise ValueError("snapshot_identity does not match snapshot semantics")

    @classmethod
    def create(
        cls,
        *,
        source_contract_identity: str,
        identities: tuple[HarnessSourceIdentity, ...],
        records: tuple[HarnessSourceRecord, ...],
        provenance: tuple[HarnessSourceProvenance, ...],
    ) -> HarnessSourceSnapshot:
        """Construct a snapshot with its exact derived identity."""
        identity = _HarnessCompilerSerializer().source_snapshot_identity(
            source_contract_identity, records
        )
        return cls(
            schema_version=1,
            snapshot_identity=identity,
            source_contract_identity=source_contract_identity,
            identities=identities,
            records=records,
            provenance=provenance,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessCompilerDiagnostic:
    """One deterministic sanitized loading or compilation diagnostic."""

    phase: HarnessCompilerPhase
    code: HarnessCompilerFailureCode
    severity: HarnessDiagnosticSeverity
    source_identity: HarnessSourceIdentity | None
    source_location: str | None
    normalized_identity: str | None
    expected: str
    observed: str
    claim_boundary: str

    def __post_init__(self) -> None:
        if (
            type(self.phase) is not HarnessCompilerPhase
            or type(self.code) is not HarnessCompilerFailureCode
            or type(self.severity) is not HarnessDiagnosticSeverity
        ):
            raise TypeError("phase, code, and severity must use their closed enums")
        if (
            self.source_identity is not None
            and type(self.source_identity) is not HarnessSourceIdentity
        ):
            raise TypeError("source_identity must be HarnessSourceIdentity or None")
        for name in ("source_location", "normalized_identity"):
            value = getattr(self, name)
            if value is not None and type(value) is not str:
                raise TypeError(f"{name} must be a built-in str or None")
        for name in ("expected", "observed", "claim_boundary"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or "\n" in value or "\r" in value:
                raise ValueError(f"{name} must be nonempty sanitized single-line text")

    @property
    def sort_key(self) -> tuple[str, bytes, str, str, str, str, str]:
        """Return the canonical diagnostic ordering key."""
        path = (
            b""
            if self.source_identity is None
            else self.source_identity.relative_path.as_posix().encode("utf-8")
        )
        return (
            self.phase.value,
            path,
            self.source_location or "",
            self.code.value,
            self.normalized_identity or "",
            self.expected,
            self.observed,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceLoadSucceeded:
    """Successful closed repository-load outcome."""

    status: Literal[HarnessSourceLoadStatus.LOADED]
    source_contract_identity: str
    loader_version: str
    snapshot: HarnessSourceSnapshot
    diagnostics: tuple[HarnessCompilerDiagnostic, ...]

    def __post_init__(self) -> None:
        if self.status is not HarnessSourceLoadStatus.LOADED:
            raise ValueError("status must be loaded")
        HarnessCompilerDiagnosticContract.validate_load_result(
            self.source_contract_identity, self.loader_version, self.diagnostics
        )
        if type(self.snapshot) is not HarnessSourceSnapshot:
            raise TypeError("snapshot must be HarnessSourceSnapshot")
        if self.snapshot.source_contract_identity != self.source_contract_identity:
            raise ValueError("snapshot and result contract identities must agree")
        if not _HarnessCompilerSerializer().snapshot_is_consistent(self.snapshot):
            raise ValueError("successful load requires an untampered snapshot identity")
        if any(
            item.severity is HarnessDiagnosticSeverity.BLOCKING
            for item in self.diagnostics
        ):
            raise ValueError("loaded result must not contain blocking diagnostics")


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessSourceLoadFailed:
    """Failed all-or-nothing repository-load outcome with no snapshot."""

    status: Literal[HarnessSourceLoadStatus.FAILED]
    source_contract_identity: str
    loader_version: str
    diagnostics: tuple[HarnessCompilerDiagnostic, ...]

    def __post_init__(self) -> None:
        if self.status is not HarnessSourceLoadStatus.FAILED:
            raise ValueError("status must be failed")
        HarnessCompilerDiagnosticContract.validate_load_result(
            self.source_contract_identity, self.loader_version, self.diagnostics
        )
        if not any(
            item.severity is HarnessDiagnosticSeverity.BLOCKING
            and item.phase is HarnessCompilerPhase.LOADING
            for item in self.diagnostics
        ):
            raise ValueError("failed load requires a blocking loading diagnostic")


type HarnessSourceLoadResult = HarnessSourceLoadSucceeded | HarnessSourceLoadFailed


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessCapabilityCatalog:
    """Canonical available skill and repository agent-definition values."""

    catalog_identity: str
    model_version: Literal[1]
    normalization_version: str
    capabilities: tuple[SkillDescriptor, ...]
    agent_definitions: tuple[PiHarnessAgentDefinition, ...]

    def __post_init__(self) -> None:
        HarnessCompilerDiagnosticContract.require_digest(
            self.catalog_identity, "catalog_identity"
        )
        HarnessCompilerDiagnosticContract.validate_model_and_normalization(
            self.model_version, self.normalization_version
        )
        if type(self.capabilities) is not tuple or any(
            type(item) is not SkillDescriptor for item in self.capabilities
        ):
            raise TypeError("capabilities must contain SkillDescriptor values")
        if type(self.agent_definitions) is not tuple or any(
            type(item) is not PiHarnessAgentDefinition
            for item in self.agent_definitions
        ):
            raise TypeError(
                "agent_definitions must contain PiHarnessAgentDefinition values"
            )
        if tuple(item.skill_id for item in self.capabilities) != tuple(
            sorted(
                (item.skill_id for item in self.capabilities),
                key=lambda value: value.encode("utf-8"),
            )
        ):
            raise ValueError("capabilities must be ordered by skill_id")
        if tuple(item.runtime_name for item in self.agent_definitions) != tuple(
            sorted(
                (item.runtime_name for item in self.agent_definitions),
                key=lambda value: value.encode("utf-8"),
            )
        ):
            raise ValueError("agent_definitions must be ordered by runtime_name")
        expected_identity = _HarnessCompilerSerializer().capability_catalog_identity(
            self.model_version,
            self.normalization_version,
            self.capabilities,
            self.agent_definitions,
        )
        if self.catalog_identity != expected_identity:
            raise ValueError("catalog_identity does not match capability semantics")

    @classmethod
    def create(
        cls,
        *,
        model_version: Literal[1],
        normalization_version: str,
        capabilities: tuple[SkillDescriptor, ...],
        agent_definitions: tuple[PiHarnessAgentDefinition, ...],
    ) -> HarnessCapabilityCatalog:
        """Construct a capability catalog with its exact derived identity."""
        identity = _HarnessCompilerSerializer().capability_catalog_identity(
            model_version, normalization_version, capabilities, agent_definitions
        )
        return cls(
            catalog_identity=identity,
            model_version=model_version,
            normalization_version=normalization_version,
            capabilities=capabilities,
            agent_definitions=agent_definitions,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessResourceCatalog:
    """Canonical resource-manifest catalog."""

    catalog_identity: str
    model_version: Literal[1]
    normalization_version: str
    resources: tuple[ResourceManifest, ...]

    def __post_init__(self) -> None:
        HarnessCompilerDiagnosticContract.require_digest(
            self.catalog_identity, "catalog_identity"
        )
        HarnessCompilerDiagnosticContract.validate_model_and_normalization(
            self.model_version, self.normalization_version
        )
        if type(self.resources) is not tuple or any(
            type(item) is not ResourceManifest for item in self.resources
        ):
            raise TypeError("resources must contain ResourceManifest values")
        if tuple(item.manifest_id for item in self.resources) != tuple(
            sorted(
                (item.manifest_id for item in self.resources),
                key=lambda value: value.encode("utf-8"),
            )
        ):
            raise ValueError("resources must be ordered by manifest_id")
        expected_identity = _HarnessCompilerSerializer().resource_catalog_identity(
            self.model_version, self.normalization_version, self.resources
        )
        if self.catalog_identity != expected_identity:
            raise ValueError("catalog_identity does not match resource semantics")

    @classmethod
    def create(
        cls,
        *,
        model_version: Literal[1],
        normalization_version: str,
        resources: tuple[ResourceManifest, ...],
    ) -> HarnessResourceCatalog:
        """Construct a resource catalog with its exact derived identity."""
        identity = _HarnessCompilerSerializer().resource_catalog_identity(
            model_version, normalization_version, resources
        )
        return cls(
            catalog_identity=identity,
            model_version=model_version,
            normalization_version=normalization_version,
            resources=resources,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessEvidenceCatalog:
    """Canonical exact Python module source catalog without semantic validation."""

    catalog_identity: str
    model_version: Literal[1]
    normalization_version: str
    evidence: tuple[PythonModuleSource, ...]
    source_identities: tuple[HarnessSourceIdentity, ...]

    def __post_init__(self) -> None:
        HarnessCompilerDiagnosticContract.require_digest(
            self.catalog_identity, "catalog_identity"
        )
        HarnessCompilerDiagnosticContract.validate_model_and_normalization(
            self.model_version, self.normalization_version
        )
        if type(self.evidence) is not tuple or any(
            type(item) is not PythonModuleSource for item in self.evidence
        ):
            raise TypeError("evidence must contain PythonModuleSource values")
        if tuple(item.path for item in self.evidence) != tuple(
            sorted(
                (item.path for item in self.evidence),
                key=lambda value: value.encode("utf-8"),
            )
        ):
            raise ValueError("evidence must be ordered by path")
        if type(self.source_identities) is not tuple or any(
            type(item) is not HarnessSourceIdentity for item in self.source_identities
        ):
            raise TypeError(
                "source_identities must contain HarnessSourceIdentity values"
            )
        if len(self.evidence) != len(self.source_identities) or any(
            identity.family is not HarnessSourceFamily.EVIDENCE
            or source.path != identity.relative_path.as_posix()
            or source.payload is None
            or hashlib.sha256(source.payload).hexdigest() != identity.sha256
            or len(source.payload) != identity.byte_count
            for source, identity in zip(
                self.evidence, self.source_identities, strict=True
            )
        ):
            raise ValueError("evidence sources and exact identities must agree")
        expected_identity = _HarnessCompilerSerializer().evidence_catalog_identity(
            self.model_version,
            self.normalization_version,
            self.evidence,
            self.source_identities,
        )
        if self.catalog_identity != expected_identity:
            raise ValueError(
                "catalog_identity does not match evidence source semantics"
            )

    @classmethod
    def create(
        cls,
        *,
        model_version: Literal[1],
        normalization_version: str,
        evidence: tuple[PythonModuleSource, ...],
        source_identities: tuple[HarnessSourceIdentity, ...],
    ) -> HarnessEvidenceCatalog:
        """Construct a source-level evidence catalog with exact derived identity."""
        identity = _HarnessCompilerSerializer().evidence_catalog_identity(
            model_version, normalization_version, evidence, source_identities
        )
        return cls(
            catalog_identity=identity,
            model_version=model_version,
            normalization_version=normalization_version,
            evidence=evidence,
            source_identities=source_identities,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessStateIdentity:
    """Versioned semantic identity of one normalized harness aggregate."""

    model_version: Literal[1]
    sha256: str

    def __post_init__(self) -> None:
        if type(self.model_version) is not int:
            raise TypeError("model_version must be a built-in int")
        if self.model_version != 1:
            raise ValueError("model_version must equal 1")
        HarnessCompilerDiagnosticContract.require_digest(self.sha256, "sha256")


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessState:
    """Complete immutable normalized development-harness aggregate."""

    identity: HarnessStateIdentity
    source_snapshot_identity: str
    normalization_version: str
    tasks: HarnessTaskRegistry
    selection: DevelopmentTaskSelection
    decisions: tuple[DevelopmentDecision, ...]
    capabilities: HarnessCapabilityCatalog
    resources: HarnessResourceCatalog
    evidence: HarnessEvidenceCatalog
    provenance: tuple[HarnessSourceProvenance, ...]

    def __post_init__(self) -> None:
        if (
            type(self.identity) is not HarnessStateIdentity
            or type(self.tasks) is not HarnessTaskRegistry
            or type(self.selection) is not DevelopmentTaskSelection
        ):
            raise TypeError("state identity, tasks, and selection have wrong types")
        HarnessCompilerDiagnosticContract.require_digest(
            self.source_snapshot_identity, "source_snapshot_identity"
        )
        HarnessCompilerDiagnosticContract.validate_version(
            self.normalization_version, "normalization_version"
        )
        expected = (
            (self.decisions, DevelopmentDecision),
            (self.provenance, HarnessSourceProvenance),
        )
        for values, kind in expected:
            if type(values) is not tuple or any(
                type(item) is not kind for item in values
            ):
                raise TypeError("state tuple contains a wrong value type")
        if (
            type(self.capabilities) is not HarnessCapabilityCatalog
            or type(self.resources) is not HarnessResourceCatalog
            or type(self.evidence) is not HarnessEvidenceCatalog
        ):
            raise TypeError("state catalog has a wrong type")
        catalog_versions = (
            (self.capabilities.model_version, self.capabilities.normalization_version),
            (self.resources.model_version, self.resources.normalization_version),
            (self.evidence.model_version, self.evidence.normalization_version),
        )
        if any(
            model != self.identity.model_version
            or normalization != self.normalization_version
            for model, normalization in catalog_versions
        ):
            raise ValueError(
                "state and catalog model/normalization versions must agree"
            )
        expected_identity = _HarnessCompilerSerializer().state_identity(self)
        if self.identity.sha256 != expected_identity:
            raise ValueError("state identity does not match state semantics")

    @classmethod
    def create(
        cls,
        *,
        source_snapshot_identity: str,
        normalization_version: str,
        tasks: HarnessTaskRegistry,
        selection: DevelopmentTaskSelection,
        decisions: tuple[DevelopmentDecision, ...],
        capabilities: HarnessCapabilityCatalog,
        resources: HarnessResourceCatalog,
        evidence: HarnessEvidenceCatalog,
        provenance: tuple[HarnessSourceProvenance, ...],
    ) -> HarnessState:
        """Construct complete selected source state with its exact derived identity."""
        serializer = _HarnessCompilerSerializer()
        digest = serializer.state_identity_components(
            1,
            normalization_version,
            tasks,
            selection,
            decisions,
            capabilities,
            resources,
            evidence,
        )
        return cls(
            identity=HarnessStateIdentity(model_version=1, sha256=digest),
            source_snapshot_identity=source_snapshot_identity,
            normalization_version=normalization_version,
            tasks=tasks,
            selection=selection,
            decisions=decisions,
            capabilities=capabilities,
            resources=resources,
            evidence=evidence,
            provenance=provenance,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessCompilationSucceeded:
    """Successful pure compilation with exactly one complete state."""

    status: Literal[HarnessCompilationStatus.SUCCEEDED]
    source_snapshot_identity: str
    compiler_version: str
    model_version: Literal[1]
    normalization_version: str
    diagnostics: tuple[HarnessCompilerDiagnostic, ...]
    state: HarnessState

    def __post_init__(self) -> None:
        if self.status is not HarnessCompilationStatus.SUCCEEDED:
            raise ValueError("status must be succeeded")
        HarnessCompilerDiagnosticContract.validate_compilation_result(
            self.source_snapshot_identity,
            self.compiler_version,
            self.model_version,
            self.normalization_version,
            self.diagnostics,
        )
        if type(self.state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        if (
            self.state.source_snapshot_identity != self.source_snapshot_identity
            or self.state.identity.model_version != self.model_version
            or self.state.normalization_version != self.normalization_version
        ):
            raise ValueError("successful compilation result bindings must agree")
        if any(
            item.severity is HarnessDiagnosticSeverity.BLOCKING
            for item in self.diagnostics
        ):
            raise ValueError(
                "successful compilation must not contain blocking diagnostics"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class HarnessCompilationFailed:
    """Failed pure compilation with diagnostics and no partial state."""

    status: Literal[HarnessCompilationStatus.FAILED]
    source_snapshot_identity: str
    compiler_version: str
    model_version: Literal[1]
    normalization_version: str
    diagnostics: tuple[HarnessCompilerDiagnostic, ...]

    def __post_init__(self) -> None:
        if self.status is not HarnessCompilationStatus.FAILED:
            raise ValueError("status must be failed")
        HarnessCompilerDiagnosticContract.validate_compilation_result(
            self.source_snapshot_identity,
            self.compiler_version,
            self.model_version,
            self.normalization_version,
            self.diagnostics,
        )
        if not any(
            item.severity is HarnessDiagnosticSeverity.BLOCKING
            and item.phase is HarnessCompilerPhase.COMPILATION
            for item in self.diagnostics
        ):
            raise ValueError(
                "failed compilation requires a blocking compilation diagnostic"
            )


type HarnessCompilationResult = HarnessCompilationSucceeded | HarnessCompilationFailed


class HarnessCompilerDiagnosticContract:
    """Own shared mechanical invariants and deterministic diagnostic construction."""

    __slots__ = ()

    @staticmethod
    def require_digest(value: str, field: str) -> None:
        if type(value) is not str:
            raise TypeError(f"{field} must be a built-in str")
        if _DIGEST.fullmatch(value) is None:
            raise ValueError(f"{field} must be a SHA-256 digest")

    @staticmethod
    def validate_load_result(
        contract_identity: str,
        version: str,
        diagnostics: tuple[HarnessCompilerDiagnostic, ...],
    ) -> None:
        HarnessCompilerDiagnosticContract.require_digest(
            contract_identity, "source_contract_identity"
        )
        HarnessCompilerDiagnosticContract.validate_version(version, "loader_version")
        HarnessCompilerDiagnosticContract.validate_diagnostics(diagnostics)

    @staticmethod
    def validate_compilation_result(
        snapshot_identity: str,
        compiler_version: str,
        model_version: int,
        normalization_version: str,
        diagnostics: tuple[HarnessCompilerDiagnostic, ...],
    ) -> None:
        HarnessCompilerDiagnosticContract.require_digest(
            snapshot_identity, "source_snapshot_identity"
        )
        HarnessCompilerDiagnosticContract.validate_version(
            compiler_version, "compiler_version"
        )
        HarnessCompilerDiagnosticContract.validate_version(
            normalization_version, "normalization_version"
        )
        if type(model_version) is not int:
            raise TypeError("model_version must be a built-in int")
        if model_version != 1:
            raise ValueError("model_version must equal 1")
        HarnessCompilerDiagnosticContract.validate_diagnostics(diagnostics)

    @staticmethod
    def validate_model_and_normalization(
        model_version: int, normalization_version: str
    ) -> None:
        """Validate the model and normalization versions shared by aggregates."""
        if type(model_version) is not int:
            raise TypeError("model_version must be a built-in int")
        if model_version != 1:
            raise ValueError("model_version must equal 1")
        HarnessCompilerDiagnosticContract.validate_version(
            normalization_version, "normalization_version"
        )

    @staticmethod
    def validate_version(value: str, field: str) -> None:
        if type(value) is not str:
            raise TypeError(f"{field} must be a built-in str")
        if not value or "\n" in value or "\r" in value:
            raise ValueError(f"{field} must be nonempty single-line text")

    @staticmethod
    def validate_diagnostics(value: tuple[HarnessCompilerDiagnostic, ...]) -> None:
        if type(value) is not tuple or any(
            type(item) is not HarnessCompilerDiagnostic for item in value
        ):
            raise TypeError("diagnostics must contain HarnessCompilerDiagnostic values")
        if value != tuple(sorted(value, key=lambda item: item.sort_key)):
            raise ValueError("diagnostics must be canonically ordered")

    @staticmethod
    def blocking(
        phase: HarnessCompilerPhase,
        code: HarnessCompilerFailureCode,
        identity: HarnessSourceIdentity | None,
        expected: str,
        observed: str,
    ) -> HarnessCompilerDiagnostic:
        return HarnessCompilerDiagnostic(
            phase=phase,
            code=code,
            severity=HarnessDiagnosticSeverity.BLOCKING,
            source_identity=identity,
            source_location=None,
            normalized_identity=None,
            expected=expected,
            observed=observed,
            claim_boundary=(
                "development-harness structural loading and compilation only"
            ),
        )


@dataclass(frozen=True, slots=True)
class _FilesystemMetadata:
    device: int
    inode: int
    size: int
    mtime_ns: int

    @classmethod
    def from_stat(cls, value: os.stat_result) -> _FilesystemMetadata:
        return cls(value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)


class _RepositoryDescriptor:
    """Own component-wise descriptor-relative repository observations."""

    __slots__ = ("_descriptor", "_root", "_root_metadata")

    def __init__(self, root: Path) -> None:
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        self._descriptor = os.open(root, flags)
        self._root = root
        self._root_metadata = _FilesystemMetadata.from_stat(os.fstat(self._descriptor))

    def close(self) -> None:
        """Close the retained repository descriptor."""
        os.close(self._descriptor)

    def root_is_stable(self) -> bool:
        """Return whether the explicit path still names the opened root directory."""
        try:
            current = _FilesystemMetadata.from_stat(
                self._root.stat(follow_symlinks=False)
            )
        except OSError:
            return False
        return current == self._root_metadata

    def read(
        self, relative: PurePosixPath
    ) -> tuple[bytes, _FilesystemMetadata] | HarnessCompilerFailureCode:
        """Read one selected file by exact-case no-follow component traversal."""
        parent_descriptor = self._open_directory(relative.parts[:-1])
        if isinstance(parent_descriptor, HarnessCompilerFailureCode):
            return parent_descriptor
        try:
            name = relative.parts[-1]
            case = self._exact_name(parent_descriptor, name)
            if case is not None:
                return case
            before_stat = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(before_stat.st_mode):
                return HarnessCompilerFailureCode.SYMLINK_REJECTED
            if not stat.S_ISREG(before_stat.st_mode):
                return HarnessCompilerFailureCode.UNSUPPORTED_FILE_TYPE
            before = _FilesystemMetadata.from_stat(before_stat)
            descriptor = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW,
                dir_fd=parent_descriptor,
            )
            try:
                chunks: list[bytes] = []
                count = 0
                while True:
                    chunk = os.read(
                        descriptor, min(65536, _MAX_SOURCE_BYTES + 1 - count)
                    )
                    if not chunk:
                        break
                    chunks.append(chunk)
                    count += len(chunk)
                    if count > _MAX_SOURCE_BYTES:
                        return HarnessCompilerFailureCode.READ_FAILURE
                after = _FilesystemMetadata.from_stat(os.fstat(descriptor))
            finally:
                os.close(descriptor)
            if before != after:
                return HarnessCompilerFailureCode.SOURCE_CHANGED
            return b"".join(chunks), after
        except FileNotFoundError:
            return HarnessCompilerFailureCode.MISSING_SOURCE
        except OSError:
            return HarnessCompilerFailureCode.READ_FAILURE
        finally:
            os.close(parent_descriptor)

    def metadata(
        self, relative: PurePosixPath
    ) -> _FilesystemMetadata | HarnessCompilerFailureCode:
        """Observe one selected path after loading through the same safe traversal."""
        parent_descriptor = self._open_directory(relative.parts[:-1])
        if isinstance(parent_descriptor, HarnessCompilerFailureCode):
            return parent_descriptor
        try:
            name = relative.parts[-1]
            case = self._exact_name(parent_descriptor, name)
            if case is not None:
                return case
            value = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(value.st_mode):
                return HarnessCompilerFailureCode.SYMLINK_REJECTED
            if not stat.S_ISREG(value.st_mode):
                return HarnessCompilerFailureCode.UNSUPPORTED_FILE_TYPE
            return _FilesystemMetadata.from_stat(value)
        except FileNotFoundError:
            return HarnessCompilerFailureCode.MISSING_SOURCE
        except OSError:
            return HarnessCompilerFailureCode.READ_FAILURE
        finally:
            os.close(parent_descriptor)

    def scan(
        self,
        roots: tuple[PurePosixPath, ...],
        selected: tuple[PurePosixPath, ...],
    ) -> (
        tuple[set[PurePosixPath], tuple[tuple[str, _FilesystemMetadata], ...]]
        | HarnessCompilerFailureCode
    ):
        """Observe selected existence and the complete stable catalog closure."""
        found: set[PurePosixPath] = set()
        closure: list[tuple[str, _FilesystemMetadata]] = []
        selected_set = set(selected)
        for root in roots:
            descriptor = self._open_directory(root.parts)
            if isinstance(descriptor, HarnessCompilerFailureCode):
                return descriptor
            try:
                failure = self._scan_directory(
                    descriptor, root, selected_set, found, closure
                )
                if failure is not None:
                    return failure
            finally:
                os.close(descriptor)
        return found, tuple(sorted(closure, key=lambda item: item[0].encode("utf-8")))

    def _scan_directory(
        self,
        descriptor: int,
        prefix: PurePosixPath,
        selected: set[PurePosixPath],
        found: set[PurePosixPath],
        closure: list[tuple[str, _FilesystemMetadata]],
    ) -> HarnessCompilerFailureCode | None:
        try:
            names = tuple(
                sorted(os.listdir(descriptor), key=lambda name: name.encode("utf-8"))
            )
            for name in names:
                if unicodedata.normalize("NFC", name) != name:
                    return HarnessCompilerFailureCode.CASE_MISMATCH
                value = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
                relative = prefix / name
                metadata = _FilesystemMetadata.from_stat(value)
                closure.append((relative.as_posix(), metadata))
                if stat.S_ISLNK(value.st_mode):
                    return HarnessCompilerFailureCode.SYMLINK_REJECTED
                if stat.S_ISDIR(value.st_mode):
                    child = os.open(
                        name,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=descriptor,
                    )
                    try:
                        failure = self._scan_directory(
                            child, relative, selected, found, closure
                        )
                        if failure is not None:
                            return failure
                    finally:
                        os.close(child)
                elif stat.S_ISREG(value.st_mode) and relative in selected:
                    found.add(relative)
                elif not stat.S_ISREG(value.st_mode):
                    return HarnessCompilerFailureCode.UNSUPPORTED_FILE_TYPE
        except OSError:
            return HarnessCompilerFailureCode.READ_FAILURE
        return None

    def _open_directory(
        self, components: tuple[str, ...]
    ) -> int | HarnessCompilerFailureCode:
        descriptor = os.dup(self._descriptor)
        try:
            for component in components:
                case = self._exact_name(descriptor, component)
                if case is not None:
                    os.close(descriptor)
                    return case
                value = os.stat(component, dir_fd=descriptor, follow_symlinks=False)
                if stat.S_ISLNK(value.st_mode):
                    os.close(descriptor)
                    return HarnessCompilerFailureCode.SYMLINK_REJECTED
                if not stat.S_ISDIR(value.st_mode):
                    os.close(descriptor)
                    return HarnessCompilerFailureCode.UNSUPPORTED_FILE_TYPE
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
                os.close(descriptor)
                descriptor = child
        except FileNotFoundError:
            os.close(descriptor)
            return HarnessCompilerFailureCode.MISSING_SOURCE
        except OSError:
            os.close(descriptor)
            return HarnessCompilerFailureCode.READ_FAILURE
        return descriptor

    @staticmethod
    def _exact_name(
        descriptor: int, expected: str
    ) -> HarnessCompilerFailureCode | None:
        try:
            names = os.listdir(descriptor)
        except OSError:
            return HarnessCompilerFailureCode.READ_FAILURE
        if expected in names:
            return None
        folded = expected.casefold()
        if any(name.casefold() == folded for name in names):
            return HarnessCompilerFailureCode.CASE_MISMATCH
        return HarnessCompilerFailureCode.MISSING_SOURCE


class HarnessRepositoryLoader:
    """Load one explicit complete source set from a local repository.

    Parameters
    ----------
    loader_version
        Nonempty single-line implementation version recorded on results.
    pi_configuration
        Exact resolved Pi subset injected solely for agent-definition decoding.

    Notes
    -----
    Each selected regular file is opened once with ``O_NOFOLLOW`` where available,
    read to a fixed 16 MiB safety bound, and checked before, during, and after family
    scans. Filesystem ordering is ignored. No current-directory, environment, Git,
    configuration-file, authority, or generated-artifact discovery occurs.
    """

    __slots__ = ("_loader_version", "_pi_configuration")

    def __init__(
        self, loader_version: str, pi_configuration: PiHarnessConfiguration
    ) -> None:
        HarnessCompilerDiagnosticContract.validate_version(
            loader_version, "loader_version"
        )
        if type(pi_configuration) is not PiHarnessConfiguration:
            raise TypeError("pi_configuration must be PiHarnessConfiguration")
        self._loader_version = loader_version
        self._pi_configuration = pi_configuration

    def execute(self, contract: HarnessSourceContract) -> HarnessSourceLoadResult:
        """Return one closed snapshot or a failed result with no snapshot."""
        if type(contract) is not HarnessSourceContract:
            raise TypeError("contract must be HarnessSourceContract")
        contract_identity = contract.source_contract_identity
        try:
            repository = _RepositoryDescriptor(contract.repository_root)
        except OSError:
            return self._failed(
                contract_identity,
                HarnessCompilerFailureCode.INVALID_ROOT,
                None,
                "openable nonsymlink directory with no-follow support",
                "root unavailable or unsupported",
            )
        try:
            return self._execute_open(contract, contract_identity, repository)
        finally:
            repository.close()

    def _execute_open(
        self,
        contract: HarnessSourceContract,
        contract_identity: str,
        repository: _RepositoryDescriptor,
    ) -> HarnessSourceLoadResult:
        records: list[HarnessSourceRecord] = []
        observed: list[
            tuple[PurePosixPath, _FilesystemMetadata, HarnessSourceIdentity]
        ] = []
        for family_contract in contract.families:
            scanned = repository.scan(
                family_contract.catalog_roots, family_contract.source_paths
            )
            if isinstance(scanned, HarnessCompilerFailureCode):
                return self._filesystem_failure(contract_identity, scanned, None)
            discovered, closure = scanned
            if discovered != set(family_contract.source_paths):
                return self._failed(
                    contract_identity,
                    HarnessCompilerFailureCode.MISSING_SOURCE,
                    None,
                    "every explicitly selected source exists",
                    "one or more selected sources are absent",
                )
            for relative_path in family_contract.source_paths:
                loaded = self._read_source(
                    repository, family_contract, relative_path, contract
                )
                if isinstance(loaded, HarnessCompilerDiagnostic):
                    return HarnessSourceLoadFailed(
                        status=HarnessSourceLoadStatus.FAILED,
                        source_contract_identity=contract_identity,
                        loader_version=self._loader_version,
                        diagnostics=(loaded,),
                    )
                record, metadata = loaded
                records.append(record)
                observed.append((relative_path, metadata, record.identity))
            rescanned = repository.scan(
                family_contract.catalog_roots, family_contract.source_paths
            )
            if isinstance(rescanned, HarnessCompilerFailureCode):
                return self._filesystem_failure(contract_identity, rescanned, None)
            rediscovered, reclosure = rescanned
            if rediscovered != discovered or reclosure != closure:
                return self._failed(
                    contract_identity,
                    HarnessCompilerFailureCode.SOURCE_CHANGED,
                    None,
                    "stable family path and metadata closure",
                    "family closure changed",
                )
        for relative, metadata, identity in observed:
            final = repository.metadata(relative)
            if isinstance(final, HarnessCompilerFailureCode) or final != metadata:
                return self._failed(
                    contract_identity,
                    HarnessCompilerFailureCode.SOURCE_CHANGED,
                    identity,
                    "stable source metadata",
                    "source metadata changed after load",
                )
        if not repository.root_is_stable():
            return self._failed(
                contract_identity,
                HarnessCompilerFailureCode.SOURCE_CHANGED,
                None,
                "stable explicit repository root identity",
                "repository root path changed during load",
            )
        ordered = tuple(
            sorted(
                records,
                key=lambda record: (
                    tuple(HarnessSourceFamily).index(record.identity.family),
                    record.identity.relative_path.as_posix().encode("utf-8"),
                ),
            )
        )
        identities = tuple(record.identity for record in ordered)
        provenance = tuple(
            sorted(
                (item for record in ordered for item in record.provenance),
                key=lambda item: item.sort_key,
            )
        )
        snapshot = HarnessSourceSnapshot.create(
            source_contract_identity=contract_identity,
            identities=identities,
            records=ordered,
            provenance=provenance,
        )
        return HarnessSourceLoadSucceeded(
            status=HarnessSourceLoadStatus.LOADED,
            source_contract_identity=contract_identity,
            loader_version=self._loader_version,
            snapshot=snapshot,
            diagnostics=(),
        )

    def _filesystem_failure(
        self,
        contract_identity: str,
        code: HarnessCompilerFailureCode,
        identity: HarnessSourceIdentity | None,
    ) -> HarnessSourceLoadFailed:
        expected = "exact-case nonsymlink confined regular source components"
        observed = "filesystem component violates the selected source contract"
        return self._failed(contract_identity, code, identity, expected, observed)

    def _failed(
        self,
        contract_identity: str,
        code: HarnessCompilerFailureCode,
        identity: HarnessSourceIdentity | None,
        expected: str,
        observed: str,
    ) -> HarnessSourceLoadFailed:
        diagnostic = HarnessCompilerDiagnosticContract.blocking(
            HarnessCompilerPhase.LOADING, code, identity, expected, observed
        )
        return HarnessSourceLoadFailed(
            status=HarnessSourceLoadStatus.FAILED,
            source_contract_identity=contract_identity,
            loader_version=self._loader_version,
            diagnostics=(diagnostic,),
        )

    def _read_source(
        self,
        repository: _RepositoryDescriptor,
        family: HarnessSourceFamilyContract,
        relative: PurePosixPath,
        contract: HarnessSourceContract,
    ) -> tuple[HarnessSourceRecord, _FilesystemMetadata] | HarnessCompilerDiagnostic:
        observed = repository.read(relative)
        if isinstance(observed, HarnessCompilerFailureCode):
            return HarnessCompilerDiagnosticContract.blocking(
                HarnessCompilerPhase.LOADING,
                observed,
                None,
                "exact-case nonsymlink confined stable regular source",
                "source component or read violates the selected contract",
            )
        payload, after = observed
        identity = HarnessSourceIdentity(
            family=family.family,
            relative_path=relative,
            format_version=family.format_version,
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
        )
        try:
            value = self._decode(identity, payload, contract)
        except TypeError, ValueError:
            return HarnessCompilerDiagnosticContract.blocking(
                HarnessCompilerPhase.LOADING,
                HarnessCompilerFailureCode.DECODE_FAILURE,
                identity,
                "valid typed source representation",
                "source decoding failed",
            )
        provenance = HarnessSourceProvenance(
            source_identity=identity,
            source_location="",
            normalized_location=self._normalized_location(identity, value),
        )
        return HarnessSourceRecord(
            identity=identity, value=value, provenance=(provenance,)
        ), after

    def _decode(
        self,
        identity: HarnessSourceIdentity,
        payload: bytes,
        contract: HarnessSourceContract,
    ) -> HarnessParsedValue:
        family = identity.family
        if family is HarnessSourceFamily.TASK:
            return HarnessTaskDeserializer().execute(payload)
        if family is HarnessSourceFamily.TASK_SELECTION:
            return DevelopmentTaskSelectionDeserializer().execute(payload)
        if family is HarnessSourceFamily.DEVELOPMENT_DECISION:
            binding = next(
                (
                    item
                    for item in contract.legacy_decision_bindings
                    if item.source_path == identity.relative_path
                ),
                None,
            )
            serializer = DevelopmentDecisionSerializer()
            if binding is None:
                return serializer.deserialize(payload)
            return serializer.adapt_legacy(
                payload,
                decision_id=binding.decision_id,
                source_path=identity.relative_path.as_posix(),
                predecessor_decision_id=binding.predecessor_decision_id,
                adapter_version=binding.adapter_version,
            )
        if family is HarnessSourceFamily.CAPABILITY:
            decoded = JsonRecordDeserializer().execute(
                WireRecordKind.SkillDescriptor, payload
            )
            if type(decoded.record) is not SkillDescriptor:
                raise ValueError("capability source did not decode as SkillDescriptor")
            return decoded.record
        if family is HarnessSourceFamily.RESOURCE:
            decoded = JsonRecordDeserializer().execute(
                WireRecordKind.ResourceManifest, payload
            )
            if type(decoded.record) is not ResourceManifest:
                raise ValueError("resource source did not decode as ResourceManifest")
            return decoded.record
        if family is HarnessSourceFamily.AGENT_DEFINITION:
            return PiHarnessAgentDefinitionResolver().execute(
                identity.relative_path.as_posix(), payload, self._pi_configuration
            )
        if family is HarnessSourceFamily.EVIDENCE:
            return PythonModuleSource(identity.relative_path.as_posix(), payload)
        raise ValueError("unsupported source family")

    def _normalized_location(
        self, identity: HarnessSourceIdentity, value: HarnessParsedValue
    ) -> str:
        locations = {
            HarnessSourceFamily.TASK: "/tasks",
            HarnessSourceFamily.TASK_SELECTION: "/selection",
            HarnessSourceFamily.DEVELOPMENT_DECISION: "/decisions",
            HarnessSourceFamily.CAPABILITY: "/capabilities/capabilities",
            HarnessSourceFamily.RESOURCE: "/resources",
            HarnessSourceFamily.AGENT_DEFINITION: "/capabilities/agent_definitions",
            HarnessSourceFamily.EVIDENCE: "/evidence",
        }
        return locations[identity.family]


class HarnessCompiler:
    """Pure deterministic compiler from one source snapshot to one harness state."""

    __slots__ = ("_compiler_version", "_normalization_version", "_model_version")

    def __init__(
        self,
        compiler_version: str,
        normalization_version: str,
        model_version: Literal[1] = 1,
    ) -> None:
        HarnessCompilerDiagnosticContract.validate_version(
            compiler_version, "compiler_version"
        )
        HarnessCompilerDiagnosticContract.validate_version(
            normalization_version, "normalization_version"
        )
        if type(model_version) is not int:
            raise TypeError("model_version must be a built-in int")
        if model_version != 1:
            raise ValueError("model_version must equal 1")
        self._compiler_version = compiler_version
        self._normalization_version = normalization_version
        self._model_version = model_version

    def execute(self, snapshot: HarnessSourceSnapshot) -> HarnessCompilationResult:
        """Compile ``snapshot`` without I/O, authority interpretation, or validation."""
        if type(snapshot) is not HarnessSourceSnapshot:
            raise TypeError("snapshot must be HarnessSourceSnapshot")
        if len(snapshot.identities) != len(set(snapshot.identities)):
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.DUPLICATE_SOURCE_PATH,
                "one record per source identity",
                "duplicate source identity",
            )
        unsupported = next(
            (
                record.identity
                for record in snapshot.records
                if record.identity.format_version
                != _FAMILY_FORMAT_VERSIONS[record.identity.family]
            ),
            None,
        )
        if unsupported is not None:
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.UNSUPPORTED_FORMAT_VERSION,
                "source identity format version equals the owning family version",
                "source identity declares an unsupported format version",
                unsupported,
            )
        wrong = next(
            (record for record in snapshot.records if not self._family_matches(record)),
            None,
        )
        if wrong is not None:
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.SOURCE_FAMILY_MISMATCH,
                "decoded value agrees with source family",
                "source family and value differ",
                wrong.identity,
            )
        mismatch = next(
            (
                record.identity
                for record in snapshot.records
                if self._record_identity_mismatch(record)
            ),
            None,
        )
        if mismatch is not None:
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.CONTENT_IDENTITY_MISMATCH,
                "decoded source-level value agrees with exact source identity",
                "decoded source-level value and source identity differ",
                mismatch,
            )
        tasks = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is HarnessTask
                ),
                key=lambda item: item.task_id.encode("utf-8"),
            )
        )
        selections = tuple(
            record.value
            for record in snapshot.records
            if type(record.value) is DevelopmentTaskSelection
        )
        decisions = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is DevelopmentDecision
                ),
                key=lambda item: (
                    (item.predecessor_decision_id or "").encode("utf-8"),
                    item.decision_id.encode("utf-8"),
                ),
            )
        )
        capabilities = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is SkillDescriptor
                ),
                key=lambda item: item.skill_id.encode("utf-8"),
            )
        )
        agents = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is PiHarnessAgentDefinition
                ),
                key=lambda item: item.runtime_name.encode("utf-8"),
            )
        )
        resources = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is ResourceManifest
                ),
                key=lambda item: item.manifest_id.encode("utf-8"),
            )
        )
        evidence = tuple(
            sorted(
                (
                    record.value
                    for record in snapshot.records
                    if type(record.value) is PythonModuleSource
                ),
                key=lambda item: item.path.encode("utf-8"),
            )
        )
        duplicates = self._duplicate_identity(
            tasks, decisions, capabilities, agents, resources, evidence
        )
        if duplicates:
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.DUPLICATE_CANONICAL_IDENTITY,
                "unique canonical identities",
                "duplicate canonical identity",
            )
        family_counts = {
            family: sum(record.identity.family is family for record in snapshot.records)
            for family in HarnessSourceFamily
        }
        required_families = tuple(
            family
            for family in HarnessSourceFamily
            if family is not HarnessSourceFamily.DEVELOPMENT_DECISION
        )
        if len(selections) != 1 or any(
            family_counts[family] < _FAMILY_MINIMUM_COUNTS[family]
            for family in required_families
        ):
            return self._failed(
                snapshot,
                HarnessCompilerFailureCode.UNREPRESENTABLE_NORMALIZATION,
                "every required family and exactly one selection",
                "required aggregate component absent",
            )
        evidence_record_values: list[HarnessSourceRecord] = []
        for record in snapshot.records:
            if isinstance(record.value, PythonModuleSource):
                evidence_record_values.append(record)
        evidence_records = tuple(
            sorted(
                evidence_record_values,
                key=lambda record: record.identity.relative_path.as_posix().encode(
                    "utf-8"
                ),
            )
        )
        evidence_identities = tuple(record.identity for record in evidence_records)
        capability_catalog = HarnessCapabilityCatalog.create(
            model_version=1,
            normalization_version=self._normalization_version,
            capabilities=capabilities,
            agent_definitions=agents,
        )
        resource_catalog = HarnessResourceCatalog.create(
            model_version=1,
            normalization_version=self._normalization_version,
            resources=resources,
        )
        evidence_catalog = HarnessEvidenceCatalog.create(
            model_version=1,
            normalization_version=self._normalization_version,
            evidence=evidence,
            source_identities=evidence_identities,
        )
        registry = HarnessTaskRegistry(1, tasks)
        state = HarnessState.create(
            source_snapshot_identity=snapshot.snapshot_identity,
            normalization_version=self._normalization_version,
            tasks=registry,
            selection=selections[0],
            decisions=decisions,
            capabilities=capability_catalog,
            resources=resource_catalog,
            evidence=evidence_catalog,
            provenance=self._state_provenance(
                snapshot.records,
                tasks,
                decisions,
                capabilities,
                agents,
                resources,
                evidence,
            ),
        )
        return HarnessCompilationSucceeded(
            status=HarnessCompilationStatus.SUCCEEDED,
            source_snapshot_identity=snapshot.snapshot_identity,
            compiler_version=self._compiler_version,
            model_version=1,
            normalization_version=self._normalization_version,
            diagnostics=(),
            state=state,
        )

    def _failed(
        self,
        snapshot: HarnessSourceSnapshot,
        code: HarnessCompilerFailureCode,
        expected: str,
        observed: str,
        identity: HarnessSourceIdentity | None = None,
    ) -> HarnessCompilationFailed:
        diagnostic = HarnessCompilerDiagnosticContract.blocking(
            HarnessCompilerPhase.COMPILATION, code, identity, expected, observed
        )
        return HarnessCompilationFailed(
            status=HarnessCompilationStatus.FAILED,
            source_snapshot_identity=snapshot.snapshot_identity,
            compiler_version=self._compiler_version,
            model_version=1,
            normalization_version=self._normalization_version,
            diagnostics=(diagnostic,),
        )

    def _family_matches(self, record: HarnessSourceRecord) -> bool:
        expected = {
            HarnessSourceFamily.TASK: HarnessTask,
            HarnessSourceFamily.TASK_SELECTION: DevelopmentTaskSelection,
            HarnessSourceFamily.DEVELOPMENT_DECISION: DevelopmentDecision,
            HarnessSourceFamily.CAPABILITY: SkillDescriptor,
            HarnessSourceFamily.RESOURCE: ResourceManifest,
            HarnessSourceFamily.AGENT_DEFINITION: PiHarnessAgentDefinition,
            HarnessSourceFamily.EVIDENCE: PythonModuleSource,
        }
        return type(record.value) is expected[record.identity.family]

    def _record_identity_mismatch(self, record: HarnessSourceRecord) -> bool:
        value = record.value
        if isinstance(value, PythonModuleSource):
            return (
                value.payload is None
                or value.path != record.identity.relative_path.as_posix()
                or hashlib.sha256(value.payload).hexdigest() != record.identity.sha256
                or len(value.payload) != record.identity.byte_count
            )
        if isinstance(value, PiHarnessAgentDefinition):
            return (
                value.source_path != record.identity.relative_path.as_posix()
                or value.source_identity.digest != record.identity.sha256
            )
        return False

    def _duplicate_identity(
        self,
        tasks: tuple[HarnessTask, ...],
        decisions: tuple[DevelopmentDecision, ...],
        capabilities: tuple[SkillDescriptor, ...],
        agents: tuple[PiHarnessAgentDefinition, ...],
        resources: tuple[ResourceManifest, ...],
        evidence: tuple[PythonModuleSource, ...],
    ) -> bool:
        groups = (
            tuple(item.task_id for item in tasks),
            tuple(item.decision_id for item in decisions),
            tuple(item.skill_id for item in capabilities),
            tuple(item.runtime_name for item in agents),
            tuple(item.manifest_id for item in resources),
            tuple(item.path for item in evidence),
        )
        return any(len(values) != len(set(values)) for values in groups)

    def _state_provenance(
        self,
        records: tuple[HarnessSourceRecord, ...],
        tasks: tuple[HarnessTask, ...],
        decisions: tuple[DevelopmentDecision, ...],
        capabilities: tuple[SkillDescriptor, ...],
        agents: tuple[PiHarnessAgentDefinition, ...],
        resources: tuple[ResourceManifest, ...],
        evidence: tuple[PythonModuleSource, ...],
    ) -> tuple[HarnessSourceProvenance, ...]:
        locations: dict[HarnessSourceIdentity, str] = {}
        for record in records:
            value = record.value
            if type(value) is HarnessTask:
                locations[record.identity] = f"/tasks/{tasks.index(value)}"
            elif type(value) is DevelopmentTaskSelection:
                locations[record.identity] = "/selection"
            elif type(value) is DevelopmentDecision:
                locations[record.identity] = f"/decisions/{decisions.index(value)}"
            elif type(value) is SkillDescriptor:
                locations[record.identity] = (
                    f"/capabilities/capabilities/{capabilities.index(value)}"
                )
            elif type(value) is PiHarnessAgentDefinition:
                locations[record.identity] = (
                    f"/capabilities/agent_definitions/{agents.index(value)}"
                )
            elif type(value) is ResourceManifest:
                locations[record.identity] = (
                    f"/resources/resources/{resources.index(value)}"
                )
            elif type(value) is PythonModuleSource:
                locations[record.identity] = (
                    f"/evidence/sources/{evidence.index(value)}"
                )
        provenance = tuple(
            HarnessSourceProvenance(
                source_identity=item.source_identity,
                source_location=item.source_location,
                normalized_location=locations[item.source_identity],
            )
            for record in records
            for item in record.provenance
        )
        return tuple(sorted(provenance, key=lambda item: item.sort_key))


__all__ = (
    "HarnessSourceFamily",
    "HarnessSourceFamilyContract",
    "HarnessLegacyDecisionBinding",
    "HarnessSourceContract",
    "HarnessSourceIdentity",
    "HarnessParsedValue",
    "HarnessSourceProvenance",
    "HarnessSourceRecord",
    "HarnessSourceSnapshot",
    "HarnessSourceLoadStatus",
    "HarnessSourceLoadSucceeded",
    "HarnessSourceLoadFailed",
    "HarnessSourceLoadResult",
    "HarnessCapabilityCatalog",
    "HarnessResourceCatalog",
    "HarnessEvidenceCatalog",
    "HarnessStateIdentity",
    "HarnessState",
    "HarnessCompilerPhase",
    "HarnessDiagnosticSeverity",
    "HarnessCompilerFailureCode",
    "HarnessCompilerDiagnostic",
    "HarnessCompilationStatus",
    "HarnessCompilationSucceeded",
    "HarnessCompilationFailed",
    "HarnessCompilationResult",
    "HarnessRepositoryLoader",
    "HarnessCompiler",
)
