"""Structured diagnostics and strict JSON wire actions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias, cast

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
    from .evidence import IdentifierOccurrence
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
        | IdentifierOccurrence
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
        if self.record is not None and not self._is_wire_record(self.record):
            raise TypeError("record is outside HarnessWireRecord")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.record is not None:
            raise ValueError("failed result must have no record")

    @staticmethod
    def _is_wire_record(value: object) -> bool:
        """Return whether a result record belongs to the closed wire union."""
        from .wire.dispatch import _WireRecordDispatcher

        return _WireRecordDispatcher().supports(value)


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
    IdentifierOccurrence = "IdentifierOccurrence"
    ValidationIssue = "ValidationIssue"
    ValidationResult = "ValidationResult"


class JsonRecordSerializer:
    """Serialize a closed wire record as canonical JSON plus LF."""

    __slots__ = ()

    def execute(self, record: HarnessWireRecord) -> JsonSerializationResult:
        from .wire.canonical_json import _CanonicalJsonSerializer
        from .wire.dispatch import _WireRecordDispatcher

        dispatcher = _WireRecordDispatcher()
        if not dispatcher.supports(record):
            raise TypeError("record is outside HarnessWireRecord")
        try:
            payload = _CanonicalJsonSerializer().encode(dispatcher.encode(record))
        except (UnicodeError, ValueError, TypeError) as exc:
            raise HarnessInternalError("JsonRecordSerializer", str(exc)) from exc
        identity = ArtifactIdentity(1, "sha256", hashlib.sha256(payload).hexdigest())
        return JsonSerializationResult(payload, identity, _result())


class JsonRecordDeserializer:
    """Strictly decode caller-selected wire JSON without kind inference."""

    __slots__ = ()

    def execute(
        self, record_kind: WireRecordKind, payload: bytes
    ) -> JsonDeserializationResult:
        from .wire.canonical_json import _CanonicalJsonSerializer, _DuplicateKey
        from .wire.dispatch import _WireRecordDispatcher

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
            obj = _CanonicalJsonSerializer().decode(text)
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
            record = _WireRecordDispatcher().decode(record_kind.value, obj)
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
        return JsonDeserializationResult(cast(HarnessWireRecord, record), _result())
