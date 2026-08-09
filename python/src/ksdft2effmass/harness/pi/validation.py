"""Structured diagnostics and strict JSON wire actions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias

from .identity import (
    ArtifactIdentity,
    DiagnosticPath,
    HarnessInternalError,
    Identifier,
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)

if TYPE_CHECKING:
    from .chains import ChainView, TaskReference
    from .checkpoints import CheckpointRecord
    from .checksums import ChecksumEntry, ChecksumManifest
    from .evidence import EvidenceIdentifierOccurrence
    from .ownership import AgentDescriptorView, OwnershipManifestView, OwnershipScope
    from .profiles import ProjectProfile
    from .resources import ResourceManifest, ResourceReference, SkillDescriptor

_ISSUE_CODES = frozenset(
    """PIH.WIRE.INVALID_UTF8 PIH.WIRE.INVALID_JSON PIH.WIRE.DUPLICATE_KEY PIH.WIRE.UNKNOWN_FIELD PIH.WIRE.MISSING_FIELD PIH.WIRE.INVALID_TYPE PIH.WIRE.INVALID_VALUE PIH.WIRE.UNSUPPORTED_VERSION PIH.ID.EMPTY PIH.ID.INVALID_ASCII PIH.ID.DUPLICATE PIH.PATH.EMPTY PIH.PATH.ABSOLUTE PIH.PATH.INVALID_SEGMENT PIH.PATH.INVALID_CHARACTER PIH.PATH.NONCANONICAL_UNICODE PIH.PATH.WINDOWS_SYNTAX PIH.PATH.CASE_MISMATCH PIH.PATH.ESCAPE PIH.PATH.SYMLINK PIH.PATH.MISSING PIH.PATH.NOT_FILE PIH.PATH.ROOT_INVALID PIH.ARTIFACT.ALGORITHM_UNSUPPORTED PIH.ARTIFACT.DIGEST_INVALID PIH.ARTIFACT.HASH_MISMATCH PIH.RESOURCE.MANIFEST_MISMATCH PIH.RESOURCE.DUPLICATE_ID PIH.RESOURCE.DUPLICATE_PATH PIH.RESOURCE.MISSING_DEPENDENCY PIH.RESOURCE.DEPENDENCY_CYCLE PIH.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY PIH.RESOURCE.OVERLAY_REPLACEMENT PIH.RESOURCE.KIND_UNSUPPORTED PIH.RESOURCE.VERSION_INCOMPATIBLE PIH.RESOURCE.NOT_FOUND PIH.RESOURCE.AMBIGUOUS_SELECTION PIH.PROFILE.IDENTITY_MISMATCH PIH.PROFILE.CONTRACT_INCOMPATIBLE PIH.PROFILE.POLICY_REFERENCE_UNKNOWN PIH.PROFILE.VOCABULARY_OVERLAP PIH.PROFILE.EXTENSION_UNSUPPORTED PIH.SKILL.DUPLICATE_ID PIH.SKILL.ENTRY_MISSING PIH.SKILL.ENTRY_KIND_INVALID PIH.SKILL.CLOSURE_INCOMPLETE PIH.SKILL.POLICY_INCOMPATIBLE PIH.SKILL.BEHAVIOR_INCOMPATIBLE PIH.OWNERSHIP.TASK_MISMATCH PIH.OWNERSHIP.AGENT_MISMATCH PIH.OWNERSHIP.ROLE_DUPLICATE PIH.OWNERSHIP.PATH_OVERLAP PIH.OWNERSHIP.REVIEWER_NOT_INDEPENDENT PIH.OWNERSHIP.COMPLETION_INVALID PIH.OWNERSHIP.PROFILE_UNSUPPORTED PIH.CHECKPOINT.DUPLICATE_ID PIH.CHECKPOINT.TASK_UNKNOWN PIH.CHECKPOINT.STATUS_UNKNOWN PIH.CHECKPOINT.STATUS_CONFLICT PIH.CHECKPOINT.DECISION_UNKNOWN PIH.CHECKPOINT.RESOLUTION_CONFLICT PIH.CHECKPOINT.STATE_CONTRADICTION PIH.CHECKPOINT.DECISION_DUPLICATE PIH.CHAIN.TASK_DUPLICATE PIH.CHAIN.PREREQUISITE_MISSING PIH.CHAIN.PREREQUISITE_CYCLE PIH.CHAIN.ACTIVE_CONTRADICTION PIH.CHAIN.ACTIVATION_MISSING PIH.CHAIN.ACTIVATION_UNEXPECTED PIH.CHAIN.STATUS_UNKNOWN PIH.TASK_STATE.CHAIN_INVALID PIH.TASK_STATE.TASK_MISSING PIH.TASK_STATE.REFERENCE_INVALID PIH.TASK_STATE.REFERENCE_CONFLICT PIH.TASK_STATE.OWNERSHIP_INVALID PIH.EVIDENCE.SOURCE_INVALID PIH.EVIDENCE.ID_INVALID PIH.EVIDENCE.ID_DUPLICATE PIH.EVIDENCE.NAMESPACE_UNDECLARED PIH.EVIDENCE.MARKER_UNDECLARED PIH.EVIDENCE.RANGE_CONFLICT PIH.EVIDENCE.PROTECTED_GAP PIH.CHECKSUM.ENTRY_DUPLICATE PIH.CHECKSUM.FILE_MISSING PIH.CHECKSUM.HASH_MISMATCH""".split()  # noqa: E501 - closed registry
)
_SEVERITY_RANK = {"ERROR": 0, "WARNING": 1, "INFO": 2}


def _issue_key(issue: ValidationIssue) -> tuple[object, ...]:
    return (
        _SEVERITY_RANK[issue.severity],
        issue.code,
        (0, "") if issue.subject_id is None else (1, issue.subject_id),
        (0, b"") if issue.path is None else (1, issue.path.encode()),
        issue.related_ids,
        tuple(ord(c) for c in issue.message),
    )


def _result(issues: tuple[ValidationIssue, ...] = ()) -> ValidationResult:
    ordered = tuple(sorted(set(issues), key=_issue_key))
    status = (
        "FAIL"
        if any(i.severity == "ERROR" for i in ordered)
        else "WARN"
        if any(i.severity == "WARNING" for i in ordered)
        else "PASS"
    )
    return ValidationResult(1, status, ordered)


def _issue(
    code: str,
    message: str,
    subject_id: str | None = None,
    path: str | None = None,
    related_ids: tuple[str, ...] = (),
) -> ValidationIssue:
    return ValidationIssue(
        1,
        code,
        "WARNING" if code == "PIH.EVIDENCE.PROTECTED_GAP" else "ERROR",
        subject_id,
        path,
        related_ids,
        message,
    )


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One registered expected-invalidity finding."""

    schema_version: int
    code: Identifier
    severity: str
    subject_id: Identifier | None
    path: DiagnosticPath | None
    related_ids: tuple[Identifier, ...]
    message: str

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.code, "code")
        if self.code not in _ISSUE_CODES:
            raise ValueError("code is not registered")
        _require_builtin_str(self.severity, "severity")
        if self.severity not in _SEVERITY_RANK:
            raise ValueError("invalid severity")
        expected = "WARNING" if self.code == "PIH.EVIDENCE.PROTECTED_GAP" else "ERROR"
        if self.severity != expected:
            raise ValueError("severity does not match the registered code")
        if self.subject_id is not None:
            _require_identifier(self.subject_id, "subject_id")
        if self.path is not None:
            _require_path(self.path, "path")
        _require_tuple(self.related_ids, "related_ids")
        for value in self.related_ids:
            _require_identifier(value, "related_ids item")
        _require_sorted_unique(self.related_ids, "related_ids")
        _require_builtin_str(self.message, "message")


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Deterministically ordered aggregate structural result."""

    schema_version: int
    status: str
    issues: tuple[ValidationIssue, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_builtin_str(self.status, "status")
        if self.status not in {"PASS", "WARN", "FAIL"}:
            raise ValueError("invalid status")
        _require_tuple(self.issues, "issues")
        if any(type(i) is not ValidationIssue for i in self.issues):
            raise TypeError("issues must contain ValidationIssue values")
        if tuple(sorted(self.issues, key=_issue_key)) != self.issues:
            raise ValueError("issues are not deterministically sorted")
        keys = [
            (i.severity, i.code, i.subject_id, i.path, i.related_ids)
            for i in self.issues
        ]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate machine finding")
        actual = (
            "FAIL"
            if any(i.severity == "ERROR" for i in self.issues)
            else "WARN"
            if any(i.severity == "WARNING" for i in self.issues)
            else "PASS"
        )
        if self.status != actual:
            raise ValueError("status does not agree with issues")


if TYPE_CHECKING:
    HarnessWireRecord: TypeAlias = (  # noqa: UP040
        ArtifactIdentity
        | ResourceReference
        | ResourceManifest
        | ProjectProfile
        | SkillDescriptor
        | OwnershipScope
        | AgentDescriptorView
        | OwnershipManifestView
        | CheckpointRecord
        | TaskReference
        | ChainView
        | ChecksumEntry
        | ChecksumManifest
        | EvidenceIdentifierOccurrence
        | ValidationIssue
        | ValidationResult
    )
else:
    # Package initialization replaces this temporary alias after all record
    # modules exist; future annotations prevent early circular evaluation.
    HarnessWireRecord: TypeAlias = object  # noqa: UP040


@dataclass(frozen=True, slots=True)
class ProjectProfileLoadResult:
    profile: ProjectProfile | None
    validation: ValidationResult

    def __post_init__(self) -> None:
        from .profiles import ProjectProfile

        if self.profile is not None and type(self.profile) is not ProjectProfile:
            raise TypeError("profile has wrong type")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.profile is not None:
            raise ValueError("failed result must not contain a profile")


@dataclass(frozen=True, slots=True, eq=False)
class ResourceResolutionResult:
    resolved_path: Path | None
    reference: ResourceReference | None
    validation: ValidationResult

    def __post_init__(self) -> None:
        from .resources import ResourceReference

        if self.resolved_path is not None and not isinstance(self.resolved_path, Path):
            raise TypeError("resolved_path must be pathlib.Path")
        if self.reference is not None and type(self.reference) is not ResourceReference:
            raise TypeError("reference has wrong type")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and (
            self.resolved_path is not None or self.reference is not None
        ):
            raise ValueError("failed result must not contain selection")


@dataclass(frozen=True, slots=True)
class ChainEvaluationResult:
    active_task_ids: tuple[Identifier, ...]
    blocked_task_ids: tuple[Identifier, ...]
    ready_task_ids: tuple[Identifier, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        for name in ("active_task_ids", "blocked_task_ids", "ready_task_ids"):
            values = getattr(self, name)
            _require_tuple(values, name)
            for value in values:
                _require_identifier(value, name)
            _require_sorted_unique(values, name)
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and any(
            (self.active_task_ids, self.blocked_task_ids, self.ready_task_ids)
        ):
            raise ValueError("failed result must have empty facts")


@dataclass(frozen=True, slots=True)
class EvidenceAuditResult:
    occurrences: tuple[EvidenceIdentifierOccurrence, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        from .evidence import EvidenceIdentifierOccurrence

        _require_tuple(self.occurrences, "occurrences")
        if any(type(x) is not EvidenceIdentifierOccurrence for x in self.occurrences):
            raise TypeError("occurrences have wrong type")
        if (
            tuple(
                sorted(self.occurrences, key=lambda x: (x.evidence_id, x.path, x.line))
            )
            != self.occurrences
        ):
            raise ValueError("occurrences are not sorted")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.occurrences:
            raise ValueError("failed result must have empty occurrences")


@dataclass(frozen=True, slots=True)
class JsonSerializationResult:
    payload: bytes | None
    content_identity: ArtifactIdentity | None
    validation: ValidationResult

    def __post_init__(self) -> None:
        if self.payload is not None and type(self.payload) is not bytes:
            raise TypeError("payload must be bytes")
        if (
            self.content_identity is not None
            and type(self.content_identity) is not ArtifactIdentity
        ):
            raise TypeError("content_identity has wrong type")
        if (self.payload is None) != (self.content_identity is None):
            raise ValueError("payload and identity must be jointly present")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.payload is not None:
            raise ValueError("failed result must have no payload")


@dataclass(frozen=True, slots=True)
class JsonDeserializationResult:
    record: HarnessWireRecord | None
    validation: ValidationResult

    def __post_init__(self) -> None:
        if self.record is not None and not _is_wire_record(self.record):
            raise TypeError("record is outside HarnessWireRecord")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.record is not None:
            raise ValueError("failed result must have no record")


class WireRecordKind(str, Enum):  # noqa: UP042 - accepted API specifies Enum
    """Closed public-JSON record kind."""

    ArtifactIdentity = "ArtifactIdentity"
    ResourceReference = "ResourceReference"
    ResourceManifest = "ResourceManifest"
    ProjectProfile = "ProjectProfile"
    SkillDescriptor = "SkillDescriptor"
    OwnershipScope = "OwnershipScope"
    AgentDescriptorView = "AgentDescriptorView"
    OwnershipManifestView = "OwnershipManifestView"
    CheckpointRecord = "CheckpointRecord"
    TaskReference = "TaskReference"
    ChainView = "ChainView"
    ChecksumEntry = "ChecksumEntry"
    ChecksumManifest = "ChecksumManifest"
    EvidenceIdentifierOccurrence = "EvidenceIdentifierOccurrence"
    ValidationIssue = "ValidationIssue"
    ValidationResult = "ValidationResult"


def _artifact_identity_object(value: ArtifactIdentity) -> dict[str, object]:
    return {
        "schema_version": value.schema_version,
        "algorithm": value.algorithm,
        "digest": value.digest,
    }


def _validation_issue_object(value: ValidationIssue) -> dict[str, object]:
    return {
        "schema_version": value.schema_version,
        "code": value.code,
        "severity": value.severity,
        "subject_id": value.subject_id,
        "path": value.path,
        "related_ids": list(value.related_ids),
        "message": value.message,
    }


def _wire_object(record: HarnessWireRecord) -> dict[str, object]:
    """Return the fixed wire object for one member of the closed union."""
    from .chains import ChainView, TaskReference
    from .checkpoints import CheckpointRecord
    from .checksums import ChecksumEntry, ChecksumManifest
    from .evidence import EvidenceIdentifierOccurrence
    from .ownership import AgentDescriptorView, OwnershipManifestView, OwnershipScope
    from .profiles import ProjectProfile
    from .resources import ResourceManifest, ResourceReference, SkillDescriptor

    if type(record) is ArtifactIdentity:
        return _artifact_identity_object(record)
    if type(record) is ResourceReference:
        return {
            "schema_version": record.schema_version,
            "resource_id": record.resource_id,
            "resource_kind": record.resource_kind,
            "format_version": record.format_version,
            "path": record.path,
            "content_identity": _artifact_identity_object(record.content_identity),
            "dependency_ids": list(record.dependency_ids),
        }
    if type(record) is ResourceManifest:
        return {
            "schema_version": record.schema_version,
            "manifest_id": record.manifest_id,
            "manifest_version": record.manifest_version,
            "layer": record.layer,
            "extends_manifest_id": record.extends_manifest_id,
            "resources": [_wire_object(value) for value in record.resources],
        }
    if type(record) is ProjectProfile:
        return {
            "schema_version": record.schema_version,
            "profile_id": record.profile_id,
            "public_contract_version": record.public_contract_version,
            "generic_manifest_id": record.generic_manifest_id,
            "generic_manifest_version": record.generic_manifest_version,
            "local_manifest_id": record.local_manifest_id,
            "local_manifest_version": record.local_manifest_version,
            "overlay_policy": record.overlay_policy,
            "policy_reference_ids": list(record.policy_reference_ids),
            "supported_resource_formats": [
                list(value) for value in record.supported_resource_formats
            ],
            "supported_skill_behaviors": [
                list(value) for value in record.supported_skill_behaviors
            ],
            "evidence_namespace_rules": [
                list(value) for value in record.evidence_namespace_rules
            ],
            "evidence_scope_rules": [
                [
                    _wire_object(scope),
                    marker,
                    list(prefixes),
                ]
                for scope, marker, prefixes in record.evidence_scope_rules
            ],
            "protected_unowned_functions": [
                list(value) for value in record.protected_unowned_functions
            ],
            "pytest_markers": list(record.pytest_markers),
            "filename_policy_id": record.filename_policy_id,
            "checkpoint_unresolved_statuses": list(
                record.checkpoint_unresolved_statuses
            ),
            "checkpoint_resolved_statuses": list(record.checkpoint_resolved_statuses),
            "task_active_statuses": list(record.task_active_statuses),
            "task_blocked_statuses": list(record.task_blocked_statuses),
            "task_satisfied_statuses": list(record.task_satisfied_statuses),
            "compatibility_adapter_version": record.compatibility_adapter_version,
            "local_extension_ids": list(record.local_extension_ids),
        }
    if type(record) is SkillDescriptor:
        return {
            "schema_version": record.schema_version,
            "skill_id": record.skill_id,
            "behavior_version": record.behavior_version,
            "entry_resource_id": record.entry_resource_id,
            "trigger_capability_ids": list(record.trigger_capability_ids),
            "required_resource_ids": list(record.required_resource_ids),
            "side_effect_class": record.side_effect_class,
            "authorization_policy_id": record.authorization_policy_id,
            "retry_policy": record.retry_policy,
            "termination_policy": record.termination_policy,
        }
    if type(record) is OwnershipScope:
        return {
            "schema_version": record.schema_version,
            "path": record.path,
            "scope_kind": record.scope_kind,
        }
    if type(record) is AgentDescriptorView:
        return {
            "schema_version": record.schema_version,
            "agent_id": record.agent_id,
            "acceptance_role": record.acceptance_role,
        }
    if type(record) is OwnershipManifestView:
        return {
            "schema_version": record.schema_version,
            "task_id": record.task_id,
            "task_record_path": record.task_record_path,
            "writers": [
                [role, agent, [_wire_object(scope) for scope in scopes]]
                for role, agent, scopes in record.writers
            ],
            "reviewers": [list(value) for value in record.reviewers],
            "completion_validator_path": record.completion_validator_path,
            "completion_command": list(record.completion_command),
            "orchestration_profile_id": record.orchestration_profile_id,
        }
    if type(record) is CheckpointRecord:
        return {
            "schema_version": record.schema_version,
            "checkpoint_id": record.checkpoint_id,
            "task_id": record.task_id,
            "episode_id": record.episode_id,
            "status": record.status,
            "decision_class": record.decision_class,
            "created_at": record.created_at,
            "question": record.question,
            "options": [list(value) for value in record.options],
            "human_response": record.human_response,
            "normalized_decision": record.normalized_decision,
            "resolved_at": record.resolved_at,
            "authorized_scope": record.authorized_scope,
            "record_paths": list(record.record_paths),
            "resumption_status": record.resumption_status,
        }
    if type(record) is TaskReference:
        return {
            "schema_version": record.schema_version,
            "task_id": record.task_id,
            "record_path": record.record_path,
            "task_prerequisite_ids": list(record.task_prerequisite_ids),
            "external_prerequisite_ids": list(record.external_prerequisite_ids),
            "status": record.status,
            "explicit_activation_required": record.explicit_activation_required,
        }
    if type(record) is ChainView:
        return {
            "schema_version": record.schema_version,
            "chain_id": record.chain_id,
            "active_task_id": record.active_task_id,
            "tasks": [_wire_object(value) for value in record.tasks],
            "explicitly_activated_task_ids": list(record.explicitly_activated_task_ids),
            "production_execution_authorized": record.production_execution_authorized,
            "package_publication_authorized": record.package_publication_authorized,
        }
    if type(record) is ChecksumEntry:
        return {
            "schema_version": record.schema_version,
            "path": record.path,
            "content_identity": _artifact_identity_object(record.content_identity),
        }
    if type(record) is ChecksumManifest:
        return {
            "schema_version": record.schema_version,
            "entries": [_wire_object(value) for value in record.entries],
        }
    if type(record) is EvidenceIdentifierOccurrence:
        return {
            "schema_version": record.schema_version,
            "evidence_id": record.evidence_id,
            "path": record.path,
            "line": record.line,
        }
    if type(record) is ValidationIssue:
        return _validation_issue_object(record)
    if type(record) is ValidationResult:
        return {
            "schema_version": record.schema_version,
            "status": record.status,
            "issues": [_validation_issue_object(value) for value in record.issues],
        }
    raise TypeError("record is outside HarnessWireRecord")


def _is_wire_record(value: object) -> bool:
    try:
        _wire_object(value)  # type: ignore[arg-type]
    except TypeError:
        return False
    return True


class JsonRecordSerializer:
    """Serialize a closed wire record as canonical JSON plus LF."""

    __slots__ = ()

    def execute(self, record: HarnessWireRecord) -> JsonSerializationResult:
        if not _is_wire_record(record):
            raise TypeError("record is outside HarnessWireRecord")
        try:
            payload = (
                json.dumps(
                    _wire_object(record),
                    ensure_ascii=False,
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")
        except (UnicodeError, ValueError, TypeError) as exc:
            raise HarnessInternalError("JsonRecordSerializer", str(exc)) from exc
        identity = ArtifactIdentity(1, "sha256", hashlib.sha256(payload).hexdigest())
        return JsonSerializationResult(payload, identity, _result())


class _DuplicateKey(ValueError):
    pass


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _freeze(value: Any) -> Any:
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _record_object(value: Any) -> dict[str, Any]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise TypeError("nested wire record must be an object")
    return value


def _require_fields(obj: dict[str, object], expected: tuple[str, ...]) -> None:
    unknown = set(obj) - set(expected)
    missing = set(expected) - set(obj)
    if unknown:
        raise KeyError("unknown:" + sorted(unknown)[0])
    if missing:
        raise KeyError("missing:" + sorted(missing)[0])


def _array(value: Any, field: str) -> list[Any]:
    if type(value) is not list:
        raise TypeError(f"{field} must be a JSON array")
    return value


def _construct(kind: WireRecordKind, obj: dict[str, Any]) -> Any:
    """Construct one explicitly selected member of the closed wire union."""
    from .chains import ChainView, TaskReference
    from .checkpoints import CheckpointRecord
    from .checksums import ChecksumEntry, ChecksumManifest
    from .evidence import EvidenceIdentifierOccurrence
    from .ownership import AgentDescriptorView, OwnershipManifestView, OwnershipScope
    from .profiles import ProjectProfile
    from .resources import ResourceManifest, ResourceReference, SkillDescriptor

    if kind is WireRecordKind.ArtifactIdentity:
        _require_fields(obj, ("schema_version", "algorithm", "digest"))
        return ArtifactIdentity(obj["schema_version"], obj["algorithm"], obj["digest"])
    if kind is WireRecordKind.ResourceReference:
        _require_fields(
            obj,
            (
                "schema_version",
                "resource_id",
                "resource_kind",
                "format_version",
                "path",
                "content_identity",
                "dependency_ids",
            ),
        )
        identity = _construct(
            WireRecordKind.ArtifactIdentity, _record_object(obj["content_identity"])
        )
        if type(identity) is not ArtifactIdentity:
            raise AssertionError("artifact constructor returned wrong kind")
        return ResourceReference(
            obj["schema_version"],
            obj["resource_id"],
            obj["resource_kind"],
            obj["format_version"],
            obj["path"],
            identity,
            _freeze(obj["dependency_ids"]),
        )
    if kind is WireRecordKind.ResourceManifest:
        _require_fields(
            obj,
            (
                "schema_version",
                "manifest_id",
                "manifest_version",
                "layer",
                "extends_manifest_id",
                "resources",
            ),
        )
        resources = tuple(
            _construct(WireRecordKind.ResourceReference, _record_object(value))
            for value in _array(obj["resources"], "resources")
        )
        return ResourceManifest(
            obj["schema_version"],
            obj["manifest_id"],
            obj["manifest_version"],
            obj["layer"],
            obj["extends_manifest_id"],
            resources,
        )
    if kind is WireRecordKind.ProjectProfile:
        expected: tuple[str, ...] = (
            "schema_version",
            "profile_id",
            "public_contract_version",
            "generic_manifest_id",
            "generic_manifest_version",
            "local_manifest_id",
            "local_manifest_version",
            "overlay_policy",
            "policy_reference_ids",
            "supported_resource_formats",
            "supported_skill_behaviors",
            "evidence_namespace_rules",
            "evidence_scope_rules",
            "protected_unowned_functions",
            "pytest_markers",
            "filename_policy_id",
            "checkpoint_unresolved_statuses",
            "checkpoint_resolved_statuses",
            "task_active_statuses",
            "task_blocked_statuses",
            "task_satisfied_statuses",
            "compatibility_adapter_version",
            "local_extension_ids",
        )
        _require_fields(obj, expected)
        scope_rules = []
        for raw_rule in _array(obj["evidence_scope_rules"], "evidence_scope_rules"):
            rule = _array(raw_rule, "evidence_scope_rule")
            if len(rule) != 3:
                raise TypeError("evidence_scope_rule must contain three values")
            scope = _construct(WireRecordKind.OwnershipScope, _record_object(rule[0]))
            if type(scope) is not OwnershipScope:
                raise AssertionError("scope constructor returned wrong kind")
            scope_rules.append((scope, rule[1], _freeze(rule[2])))
        return ProjectProfile(
            obj["schema_version"],
            obj["profile_id"],
            obj["public_contract_version"],
            obj["generic_manifest_id"],
            obj["generic_manifest_version"],
            obj["local_manifest_id"],
            obj["local_manifest_version"],
            obj["overlay_policy"],
            _freeze(obj["policy_reference_ids"]),
            _freeze(obj["supported_resource_formats"]),
            _freeze(obj["supported_skill_behaviors"]),
            _freeze(obj["evidence_namespace_rules"]),
            tuple(scope_rules),
            _freeze(obj["protected_unowned_functions"]),
            _freeze(obj["pytest_markers"]),
            obj["filename_policy_id"],
            _freeze(obj["checkpoint_unresolved_statuses"]),
            _freeze(obj["checkpoint_resolved_statuses"]),
            _freeze(obj["task_active_statuses"]),
            _freeze(obj["task_blocked_statuses"]),
            _freeze(obj["task_satisfied_statuses"]),
            obj["compatibility_adapter_version"],
            _freeze(obj["local_extension_ids"]),
        )
    if kind is WireRecordKind.SkillDescriptor:
        expected = (
            "schema_version",
            "skill_id",
            "behavior_version",
            "entry_resource_id",
            "trigger_capability_ids",
            "required_resource_ids",
            "side_effect_class",
            "authorization_policy_id",
            "retry_policy",
            "termination_policy",
        )
        _require_fields(obj, expected)
        return SkillDescriptor(
            obj["schema_version"],
            obj["skill_id"],
            obj["behavior_version"],
            obj["entry_resource_id"],
            _freeze(obj["trigger_capability_ids"]),
            _freeze(obj["required_resource_ids"]),
            obj["side_effect_class"],
            obj["authorization_policy_id"],
            obj["retry_policy"],
            obj["termination_policy"],
        )
    if kind is WireRecordKind.OwnershipScope:
        _require_fields(obj, ("schema_version", "path", "scope_kind"))
        return OwnershipScope(obj["schema_version"], obj["path"], obj["scope_kind"])
    if kind is WireRecordKind.AgentDescriptorView:
        _require_fields(obj, ("schema_version", "agent_id", "acceptance_role"))
        return AgentDescriptorView(
            obj["schema_version"], obj["agent_id"], obj["acceptance_role"]
        )
    if kind is WireRecordKind.OwnershipManifestView:
        expected = (
            "schema_version",
            "task_id",
            "task_record_path",
            "writers",
            "reviewers",
            "completion_validator_path",
            "completion_command",
            "orchestration_profile_id",
        )
        _require_fields(obj, expected)
        writers = []
        for raw_writer in _array(obj["writers"], "writers"):
            writer = _array(raw_writer, "writer")
            if len(writer) != 3:
                raise TypeError("writer must contain three values")
            scopes = tuple(
                _construct(WireRecordKind.OwnershipScope, _record_object(value))
                for value in _array(writer[2], "owned_scopes")
            )
            writers.append((writer[0], writer[1], scopes))
        return OwnershipManifestView(
            obj["schema_version"],
            obj["task_id"],
            obj["task_record_path"],
            tuple(writers),
            _freeze(obj["reviewers"]),
            obj["completion_validator_path"],
            _freeze(obj["completion_command"]),
            obj["orchestration_profile_id"],
        )
    if kind is WireRecordKind.CheckpointRecord:
        expected = (
            "schema_version",
            "checkpoint_id",
            "task_id",
            "episode_id",
            "status",
            "decision_class",
            "created_at",
            "question",
            "options",
            "human_response",
            "normalized_decision",
            "resolved_at",
            "authorized_scope",
            "record_paths",
            "resumption_status",
        )
        _require_fields(obj, expected)
        return CheckpointRecord(
            obj["schema_version"],
            obj["checkpoint_id"],
            obj["task_id"],
            obj["episode_id"],
            obj["status"],
            obj["decision_class"],
            obj["created_at"],
            obj["question"],
            _freeze(obj["options"]),
            obj["human_response"],
            obj["normalized_decision"],
            obj["resolved_at"],
            obj["authorized_scope"],
            _freeze(obj["record_paths"]),
            obj["resumption_status"],
        )
    if kind is WireRecordKind.TaskReference:
        expected = (
            "schema_version",
            "task_id",
            "record_path",
            "task_prerequisite_ids",
            "external_prerequisite_ids",
            "status",
            "explicit_activation_required",
        )
        _require_fields(obj, expected)
        return TaskReference(
            obj["schema_version"],
            obj["task_id"],
            obj["record_path"],
            _freeze(obj["task_prerequisite_ids"]),
            _freeze(obj["external_prerequisite_ids"]),
            obj["status"],
            obj["explicit_activation_required"],
        )
    if kind is WireRecordKind.ChainView:
        expected = (
            "schema_version",
            "chain_id",
            "active_task_id",
            "tasks",
            "explicitly_activated_task_ids",
            "production_execution_authorized",
            "package_publication_authorized",
        )
        _require_fields(obj, expected)
        tasks = tuple(
            _construct(WireRecordKind.TaskReference, _record_object(value))
            for value in _array(obj["tasks"], "tasks")
        )
        return ChainView(
            obj["schema_version"],
            obj["chain_id"],
            obj["active_task_id"],
            tasks,
            _freeze(obj["explicitly_activated_task_ids"]),
            obj["production_execution_authorized"],
            obj["package_publication_authorized"],
        )
    if kind is WireRecordKind.ChecksumEntry:
        _require_fields(obj, ("schema_version", "path", "content_identity"))
        identity = _construct(
            WireRecordKind.ArtifactIdentity, _record_object(obj["content_identity"])
        )
        if type(identity) is not ArtifactIdentity:
            raise AssertionError("artifact constructor returned wrong kind")
        return ChecksumEntry(obj["schema_version"], obj["path"], identity)
    if kind is WireRecordKind.ChecksumManifest:
        _require_fields(obj, ("schema_version", "entries"))
        entries = tuple(
            _construct(WireRecordKind.ChecksumEntry, _record_object(value))
            for value in _array(obj["entries"], "entries")
        )
        return ChecksumManifest(obj["schema_version"], entries)
    if kind is WireRecordKind.EvidenceIdentifierOccurrence:
        _require_fields(obj, ("schema_version", "evidence_id", "path", "line"))
        return EvidenceIdentifierOccurrence(
            obj["schema_version"], obj["evidence_id"], obj["path"], obj["line"]
        )
    if kind is WireRecordKind.ValidationIssue:
        expected = (
            "schema_version",
            "code",
            "severity",
            "subject_id",
            "path",
            "related_ids",
            "message",
        )
        _require_fields(obj, expected)
        return ValidationIssue(
            obj["schema_version"],
            obj["code"],
            obj["severity"],
            obj["subject_id"],
            obj["path"],
            _freeze(obj["related_ids"]),
            obj["message"],
        )
    if kind is WireRecordKind.ValidationResult:
        _require_fields(obj, ("schema_version", "status", "issues"))
        issues = tuple(
            _construct(WireRecordKind.ValidationIssue, _record_object(value))
            for value in _array(obj["issues"], "issues")
        )
        return ValidationResult(obj["schema_version"], obj["status"], issues)
    raise AssertionError("WireRecordKind is not exhaustively handled")


class JsonRecordDeserializer:
    """Strictly decode caller-selected wire JSON without kind inference."""

    __slots__ = ()

    def execute(
        self, record_kind: WireRecordKind, payload: bytes
    ) -> JsonDeserializationResult:
        if type(record_kind) is not WireRecordKind:
            raise TypeError("record_kind must be WireRecordKind")
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            return JsonDeserializationResult(
                None,
                _result(
                    (_issue("PIH.WIRE.INVALID_UTF8", "Payload is not valid UTF-8."),)
                ),
            )
        if text.startswith("\ufeff"):
            return JsonDeserializationResult(
                None,
                _result(
                    (_issue("PIH.WIRE.INVALID_JSON", "A UTF-8 BOM is prohibited."),)
                ),
            )
        try:
            obj = json.loads(
                text,
                object_pairs_hook=_pairs,
                parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)),
            )
        except _DuplicateKey as exc:
            return JsonDeserializationResult(
                None,
                _result(
                    (_issue("PIH.WIRE.DUPLICATE_KEY", f"Duplicate JSON key: {exc}."),)
                ),
            )
        except json.JSONDecodeError, ValueError:
            return JsonDeserializationResult(
                None,
                _result(
                    (
                        _issue(
                            "PIH.WIRE.INVALID_JSON",
                            "Payload is not strict RFC 8259 JSON.",
                        ),
                    )
                ),
            )
        if type(obj) is not dict:
            return JsonDeserializationResult(
                None,
                _result(
                    (
                        _issue(
                            "PIH.WIRE.INVALID_TYPE",
                            "Top-level JSON value must be an object.",
                        ),
                    )
                ),
            )
        try:
            record = _construct(record_kind, obj)
        except KeyError as exc:
            tag = str(exc.args[0])
            code = (
                "PIH.WIRE.UNKNOWN_FIELD"
                if tag.startswith("unknown:")
                else "PIH.WIRE.MISSING_FIELD"
            )
            return JsonDeserializationResult(
                None, _result((_issue(code, tag.replace(":", " field: ", 1) + "."),))
            )
        except TypeError as exc:
            return JsonDeserializationResult(
                None, _result((_issue("PIH.WIRE.INVALID_TYPE", str(exc)),))
            )
        except ValueError as exc:
            detail = str(exc)
            registered = detail.split(":", 1)[0]
            if registered in _ISSUE_CODES:
                code = registered
            elif "schema_version" in detail:
                code = "PIH.WIRE.UNSUPPORTED_VERSION"
            else:
                code = "PIH.WIRE.INVALID_VALUE"
            return JsonDeserializationResult(None, _result((_issue(code, detail),)))
        return JsonDeserializationResult(record, _result())
