"""Strict version-1 JSON serialization for provenance public records.

Canonical output uses compact, lexicographically sorted object keys, UTF-8
Unicode characters, and exactly one trailing line feed.  Input is strict:
duplicate or unknown keys, a byte-order mark, non-finite numbers, malformed JSON,
Unicode surrogate code points, and invalid record invariants are rejected.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .actions import (
    ArtifactIdentityVerificationResult,
    CorrelationIssue,
    ExecutionCorrelationResult,
)
from .records import (
    ArtifactIdentity,
    ArtifactLocation,
    ArtifactLocationKind,
    ArtifactReference,
    ArtifactSpecification,
    LineageKind,
    LineageRelation,
    ManifestState,
    ProvenanceRecord,
    RunManifest,
)
from .tools import (
    CapabilityKind,
    DeclaredCapability,
    ExternalExecutionFailure,
    ExternalExecutionRequest,
    ExternalExecutionResult,
    ExternalExecutionStatus,
    ExternalFailureCode,
    ExternalFailureStage,
    ExternalToolIdentity,
    ExternalToolSpecification,
    InstallationObservation,
    VerificationObservation,
    VerificationStatus,
)

_SCHEMA_VERSION = 1

JsonRecord = (
    ArtifactIdentity
    | ArtifactSpecification
    | ArtifactReference
    | ArtifactLocation
    | RunManifest
    | ProvenanceRecord
    | LineageRelation
    | ExternalToolIdentity
    | ExternalToolSpecification
    | DeclaredCapability
    | InstallationObservation
    | VerificationObservation
    | ExternalExecutionRequest
    | ExternalExecutionResult
    | ExternalExecutionFailure
    | ArtifactIdentityVerificationResult
    | ExecutionCorrelationResult
)
"""Public record types admitted by :class:`ProvenanceJsonSerializer`."""


class ProvenanceJsonError(ValueError):
    """Strict JSON decoding or version-1 wire-contract failure.

    Raised when JSON syntax, duplicate or unknown keys, Unicode, numeric forms,
    discriminators, enums, field invariants, or supported record types violate
    the public version-1 contract.  The exception reports no partial record and
    performs no recovery or input/output.
    """


class _DuplicateKeyError(ValueError):
    """Internal signal used by the strict object-pairs decoder."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object while rejecting duplicate member names."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> Any:
    """Reject JavaScript-style non-finite constants accepted by ``json``."""
    raise ProvenanceJsonError(f"non-finite JSON number is prohibited: {value}")


def _check_json_scalars(value: Any) -> None:
    """Recursively reject surrogates and every floating-point JSON number."""
    if type(value) is str:
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ProvenanceJsonError("Unicode surrogate code points are prohibited")
    elif type(value) is float:
        raise ProvenanceJsonError("floating-point JSON numbers are prohibited")
    elif type(value) is list:
        for item in value:
            _check_json_scalars(item)
    elif type(value) is dict:
        for key, item in value.items():
            _check_json_scalars(key)
            _check_json_scalars(item)


def _expect_object(value: Any, context: str) -> dict[str, Any]:
    """Require a JSON object at a documented record boundary."""
    if type(value) is not dict:
        raise ProvenanceJsonError(f"{context} must be a JSON object")
    return value


def _expect_fields(
    value: Any, context: str, required: set[str], optional: set[str] | None = None
) -> dict[str, Any]:
    """Require an object with exactly its versioned member vocabulary."""
    obj = _expect_object(value, context)
    allowed = required | (optional or set())
    unknown = set(obj) - allowed
    missing = required - set(obj)
    if unknown:
        raise ProvenanceJsonError(
            f"{context} contains unknown keys: {', '.join(sorted(unknown))}"
        )
    if missing:
        raise ProvenanceJsonError(
            f"{context} is missing keys: {', '.join(sorted(missing))}"
        )
    return obj


def _expect_list(value: Any, context: str) -> list[Any]:
    """Require a JSON array without coercing strings or other iterables."""
    if type(value) is not list:
        raise ProvenanceJsonError(f"{context} must be a JSON array")
    return value


def _base(record_type: str) -> dict[str, Any]:
    """Create the fixed version discriminator members."""
    return {"record_type": record_type, "schema_version": _SCHEMA_VERSION}


def _identity_to_data(value: ArtifactIdentity) -> dict[str, Any]:
    """Represent an artifact identity as nested JSON data."""
    return {
        "artifact_id": value.artifact_id,
        "byte_size": value.byte_size,
        "sha256": value.sha256,
    }


def _specification_to_data(value: ArtifactSpecification) -> dict[str, Any]:
    """Represent an artifact specification as nested JSON data."""
    return {
        "format": value.format,
        "logical_path": value.logical_path,
        "retention_policy": value.retention_policy,
        "semantic_role": value.semantic_role,
    }


def _to_data(value: JsonRecord) -> dict[str, Any]:
    """Explicitly map every supported record to its version-1 wire object."""
    if isinstance(value, ArtifactIdentity):
        return _base("artifact_identity") | _identity_to_data(value)
    if isinstance(value, ArtifactSpecification):
        return _base("artifact_specification") | _specification_to_data(value)
    if isinstance(value, ArtifactReference):
        return _base("artifact_reference") | {
            "identity": _identity_to_data(value.identity),
            "producer_manifest_id": value.producer_manifest_id,
            "specification": _specification_to_data(value.specification),
        }
    if isinstance(value, ArtifactLocation):
        return _base("artifact_location") | {
            "artifact_id": value.artifact_id,
            "external_descriptor_id": value.external_descriptor_id,
            "kind": value.kind.value,
            "path": value.path,
            "root_id": value.root_id,
        }
    if isinstance(value, RunManifest):
        return _base("run_manifest") | {
            "dependency_manifest_ids": list(value.dependency_manifest_ids),
            "finished_at": value.finished_at,
            "input_artifact_ids": list(value.input_artifact_ids),
            "manifest_id": value.manifest_id,
            "output_artifact_ids": list(value.output_artifact_ids),
            "specification_id": value.specification_id,
            "started_at": value.started_at,
            "state": value.state.value,
        }
    if isinstance(value, ProvenanceRecord):
        return _base("provenance_record") | {
            "artifact_ids": list(value.artifact_ids),
            "manifest_id": value.manifest_id,
            "parent_provenance_ids": list(value.parent_provenance_ids),
            "provenance_id": value.provenance_id,
        }
    if isinstance(value, LineageRelation):
        return _base("lineage_relation") | {
            "child_id": value.child_id,
            "kind": value.kind.value,
            "lineage_id": value.lineage_id,
            "parent_id": value.parent_id,
            "provenance_id": value.provenance_id,
        }
    if isinstance(value, ExternalToolIdentity):
        return _base("external_tool_identity") | {
            "implementation_family": value.implementation_family,
            "tool_id": value.tool_id,
        }
    if isinstance(value, ExternalToolSpecification):
        return _base("external_tool_specification") | {
            "executable_or_package_id": value.executable_or_package_id,
            "requested_version": value.requested_version,
            "specification_id": value.specification_id,
            "tool_id": value.tool_id,
        }
    if isinstance(value, DeclaredCapability):
        return _base("declared_capability") | {
            "capability_id": value.capability_id,
            "kind": value.kind.value,
            "name": value.name,
            "specification_version": value.specification_version,
            "tool_id": value.tool_id,
        }
    if isinstance(value, InstallationObservation):
        return _base("installation_observation") | {
            "environment_record_id": value.environment_record_id,
            "executable_or_package_id": value.executable_or_package_id,
            "executable_sha256": value.executable_sha256,
            "installation_id": value.installation_id,
            "observed_version": value.observed_version,
            "provenance_id": value.provenance_id,
            "specification_id": value.specification_id,
            "tool_id": value.tool_id,
        }
    if isinstance(value, VerificationObservation):
        return _base("verification_observation") | {
            "capability_id": value.capability_id,
            "evidence_artifact_ids": list(value.evidence_artifact_ids),
            "installation_id": value.installation_id,
            "provenance_id": value.provenance_id,
            "status": value.status.value,
            "verification_id": value.verification_id,
        }
    if isinstance(value, ExternalExecutionRequest):
        return _base("external_execution_request") | {
            "authorization_id": value.authorization_id,
            "capability_id": value.capability_id,
            "correlation_id": value.correlation_id,
            "attempt_id": value.attempt_id,
            "retry_parent_request_id": value.retry_parent_request_id,
            "expected_output_roles": list(value.expected_output_roles),
            "input_artifact_ids": list(value.input_artifact_ids),
            "installation_id": value.installation_id,
            "provenance_id": value.provenance_id,
            "request_id": value.request_id,
            "tool_id": value.tool_id,
        }
    if isinstance(value, ExternalExecutionResult):
        return _base("external_execution_result") | {
            "attempt_id": value.attempt_id,
            "correlation_id": value.correlation_id,
            "manifest_id": value.manifest_id,
            "output_artifact_ids": list(value.output_artifact_ids),
            "provenance_id": value.provenance_id,
            "request_id": value.request_id,
            "result_id": value.result_id,
            "status": value.status.value,
        }
    if isinstance(value, ExternalExecutionFailure):
        return _base("external_execution_failure") | {
            "attempt_id": value.attempt_id,
            "code": value.code.value,
            "correlation_id": value.correlation_id,
            "diagnostic_paths": list(value.diagnostic_paths),
            "failure_id": value.failure_id,
            "provenance_id": value.provenance_id,
            "request_id": value.request_id,
            "stage": value.stage.value,
        }
    if isinstance(value, ArtifactIdentityVerificationResult):
        return _base("artifact_identity_verification_result") | {
            "artifact_id": value.artifact_id,
            "expected_byte_size": value.expected_byte_size,
            "expected_sha256": value.expected_sha256,
            "observed_byte_size": value.observed_byte_size,
            "observed_sha256": value.observed_sha256,
        }
    if isinstance(value, ExecutionCorrelationResult):
        return _base("execution_correlation_result") | {
            "issues": [issue.value for issue in value.issues],
            "outcome_id": value.outcome_id,
            "request_id": value.request_id,
        }
    raise TypeError(f"unsupported provenance JSON record: {type(value).__name__}")


def _identity_from_data(value: Any, context: str = "identity") -> ArtifactIdentity:
    """Construct an artifact identity from an exact nested object."""
    obj = _expect_fields(value, context, {"artifact_id", "byte_size", "sha256"})
    return ArtifactIdentity(
        artifact_id=obj["artifact_id"],
        sha256=obj["sha256"],
        byte_size=obj["byte_size"],
    )


def _specification_from_data(
    value: Any, context: str = "specification"
) -> ArtifactSpecification:
    """Construct an artifact specification from an exact nested object."""
    obj = _expect_fields(
        value,
        context,
        {"format", "logical_path", "retention_policy", "semantic_role"},
    )
    return ArtifactSpecification(
        logical_path=obj["logical_path"],
        format=obj["format"],
        semantic_role=obj["semantic_role"],
        retention_policy=obj["retention_policy"],
    )


def _enum(enum_type: type[Any], value: Any, context: str) -> Any:
    """Construct an exact string-valued enum with a public contract error."""
    if type(value) is not str:
        raise ProvenanceJsonError(f"{context} must be a built-in string enum value")
    try:
        return enum_type(value)
    except ValueError as error:
        raise ProvenanceJsonError(f"unsupported {context}: {value}") from error


def _from_data(value: Any) -> JsonRecord:
    """Explicitly construct one supported record from strict decoded JSON."""
    root = _expect_object(value, "root")
    if "record_type" not in root or "schema_version" not in root:
        raise ProvenanceJsonError("root requires record_type and schema_version")
    if type(root["schema_version"]) is not int or root["schema_version"] != 1:
        raise ProvenanceJsonError("schema_version must be built-in integer 1")
    if type(root["record_type"]) is not str:
        raise ProvenanceJsonError("record_type must be a built-in string")
    record_type = root["record_type"]
    common = {"record_type", "schema_version"}
    if record_type == "artifact_identity":
        obj = _expect_fields(
            root, "artifact_identity", common | {"artifact_id", "byte_size", "sha256"}
        )
        return _identity_from_data(
            {key: obj[key] for key in ("artifact_id", "byte_size", "sha256")}
        )
    if record_type == "artifact_specification":
        fields = {"format", "logical_path", "retention_policy", "semantic_role"}
        obj = _expect_fields(root, "artifact_specification", common | fields)
        return _specification_from_data({key: obj[key] for key in fields})
    if record_type == "artifact_reference":
        obj = _expect_fields(
            root,
            "artifact_reference",
            common | {"identity", "producer_manifest_id", "specification"},
        )
        return ArtifactReference(
            identity=_identity_from_data(obj["identity"]),
            specification=_specification_from_data(obj["specification"]),
            producer_manifest_id=obj["producer_manifest_id"],
        )
    if record_type == "artifact_location":
        fields = {"artifact_id", "external_descriptor_id", "kind", "path", "root_id"}
        obj = _expect_fields(root, "artifact_location", common | fields)
        return ArtifactLocation(
            artifact_id=obj["artifact_id"],
            kind=_enum(ArtifactLocationKind, obj["kind"], "kind"),
            root_id=obj["root_id"],
            path=obj["path"],
            external_descriptor_id=obj["external_descriptor_id"],
        )
    if record_type == "run_manifest":
        fields = {
            "dependency_manifest_ids",
            "finished_at",
            "input_artifact_ids",
            "manifest_id",
            "output_artifact_ids",
            "specification_id",
            "started_at",
            "state",
        }
        obj = _expect_fields(root, "run_manifest", common | fields)
        return RunManifest(
            manifest_id=obj["manifest_id"],
            specification_id=obj["specification_id"],
            input_artifact_ids=tuple(
                _expect_list(obj["input_artifact_ids"], "input_artifact_ids")
            ),
            started_at=obj["started_at"],
            finished_at=obj["finished_at"],
            output_artifact_ids=tuple(
                _expect_list(obj["output_artifact_ids"], "output_artifact_ids")
            ),
            dependency_manifest_ids=tuple(
                _expect_list(obj["dependency_manifest_ids"], "dependency_manifest_ids")
            ),
            state=_enum(ManifestState, obj["state"], "state"),
        )
    if record_type == "provenance_record":
        fields = {
            "artifact_ids",
            "manifest_id",
            "parent_provenance_ids",
            "provenance_id",
        }
        obj = _expect_fields(root, "provenance_record", common | fields)
        return ProvenanceRecord(
            obj["provenance_id"],
            obj["manifest_id"],
            tuple(_expect_list(obj["parent_provenance_ids"], "parent_provenance_ids")),
            tuple(_expect_list(obj["artifact_ids"], "artifact_ids")),
        )
    if record_type == "lineage_relation":
        fields = {"child_id", "kind", "lineage_id", "parent_id", "provenance_id"}
        obj = _expect_fields(root, "lineage_relation", common | fields)
        return LineageRelation(
            obj["lineage_id"],
            obj["parent_id"],
            obj["child_id"],
            _enum(LineageKind, obj["kind"], "kind"),
            obj["provenance_id"],
        )
    if record_type == "external_tool_identity":
        obj = _expect_fields(
            root,
            "external_tool_identity",
            common | {"implementation_family", "tool_id"},
        )
        return ExternalToolIdentity(obj["tool_id"], obj["implementation_family"])
    if record_type == "external_tool_specification":
        fields = {
            "executable_or_package_id",
            "requested_version",
            "specification_id",
            "tool_id",
        }
        obj = _expect_fields(root, "external_tool_specification", common | fields)
        return ExternalToolSpecification(
            obj["specification_id"],
            obj["tool_id"],
            obj["requested_version"],
            obj["executable_or_package_id"],
        )
    if record_type == "declared_capability":
        fields = {"capability_id", "kind", "name", "specification_version", "tool_id"}
        obj = _expect_fields(root, "declared_capability", common | fields)
        return DeclaredCapability(
            obj["capability_id"],
            obj["tool_id"],
            _enum(CapabilityKind, obj["kind"], "kind"),
            obj["name"],
            obj["specification_version"],
        )
    if record_type == "installation_observation":
        fields = {
            "environment_record_id",
            "executable_or_package_id",
            "executable_sha256",
            "installation_id",
            "observed_version",
            "provenance_id",
            "specification_id",
            "tool_id",
        }
        obj = _expect_fields(root, "installation_observation", common | fields)
        return InstallationObservation(
            obj["installation_id"],
            obj["specification_id"],
            obj["tool_id"],
            obj["observed_version"],
            obj["executable_or_package_id"],
            obj["executable_sha256"],
            obj["environment_record_id"],
            obj["provenance_id"],
        )
    if record_type == "verification_observation":
        fields = {
            "capability_id",
            "evidence_artifact_ids",
            "installation_id",
            "provenance_id",
            "status",
            "verification_id",
        }
        obj = _expect_fields(root, "verification_observation", common | fields)
        return VerificationObservation(
            obj["verification_id"],
            obj["installation_id"],
            obj["capability_id"],
            _enum(VerificationStatus, obj["status"], "status"),
            tuple(_expect_list(obj["evidence_artifact_ids"], "evidence_artifact_ids")),
            obj["provenance_id"],
        )
    if record_type == "external_execution_request":
        fields = {
            "attempt_id",
            "authorization_id",
            "capability_id",
            "correlation_id",
            "expected_output_roles",
            "input_artifact_ids",
            "installation_id",
            "provenance_id",
            "request_id",
            "retry_parent_request_id",
            "tool_id",
        }
        obj = _expect_fields(root, "external_execution_request", common | fields)
        return ExternalExecutionRequest(
            obj["request_id"],
            obj["correlation_id"],
            obj["attempt_id"],
            obj["retry_parent_request_id"],
            obj["tool_id"],
            obj["capability_id"],
            obj["installation_id"],
            obj["authorization_id"],
            tuple(_expect_list(obj["input_artifact_ids"], "input_artifact_ids")),
            tuple(_expect_list(obj["expected_output_roles"], "expected_output_roles")),
            obj["provenance_id"],
        )
    if record_type == "external_execution_result":
        fields = {
            "attempt_id",
            "correlation_id",
            "manifest_id",
            "output_artifact_ids",
            "provenance_id",
            "request_id",
            "result_id",
            "status",
        }
        obj = _expect_fields(root, "external_execution_result", common | fields)
        return ExternalExecutionResult(
            obj["result_id"],
            obj["request_id"],
            obj["correlation_id"],
            obj["attempt_id"],
            _enum(ExternalExecutionStatus, obj["status"], "status"),
            tuple(_expect_list(obj["output_artifact_ids"], "output_artifact_ids")),
            obj["manifest_id"],
            obj["provenance_id"],
        )
    if record_type == "external_execution_failure":
        fields = {
            "attempt_id",
            "code",
            "correlation_id",
            "diagnostic_paths",
            "failure_id",
            "provenance_id",
            "request_id",
            "stage",
        }
        obj = _expect_fields(root, "external_execution_failure", common | fields)
        return ExternalExecutionFailure(
            obj["failure_id"],
            obj["request_id"],
            obj["correlation_id"],
            obj["attempt_id"],
            _enum(ExternalFailureStage, obj["stage"], "stage"),
            _enum(ExternalFailureCode, obj["code"], "code"),
            tuple(_expect_list(obj["diagnostic_paths"], "diagnostic_paths")),
            obj["provenance_id"],
        )
    if record_type == "artifact_identity_verification_result":
        fields = {
            "artifact_id",
            "expected_byte_size",
            "expected_sha256",
            "observed_byte_size",
            "observed_sha256",
        }
        obj = _expect_fields(
            root, "artifact_identity_verification_result", common | fields
        )
        return ArtifactIdentityVerificationResult(
            obj["artifact_id"],
            obj["expected_sha256"],
            obj["observed_sha256"],
            obj["expected_byte_size"],
            obj["observed_byte_size"],
        )
    if record_type == "execution_correlation_result":
        fields = {"issues", "outcome_id", "request_id"}
        obj = _expect_fields(root, "execution_correlation_result", common | fields)
        issues = tuple(
            _enum(CorrelationIssue, issue, "issues item")
            for issue in _expect_list(obj["issues"], "issues")
        )
        return ExecutionCorrelationResult(
            obj["request_id"],
            obj["outcome_id"],
            issues,
        )
    raise ProvenanceJsonError(f"unsupported record_type: {record_type}")


@dataclass(frozen=True, slots=True)
class ProvenanceJsonSerializer:
    """Stateless strict serializer ActionObject for the version-1 wire contract.

    Methods
    -------
    serialize(record)
        Produce canonical compact JSON text with one trailing line feed.
    deserialize(text)
        Strictly decode exactly one supported version-1 record.
    """

    def serialize(self, record: JsonRecord) -> str:
        """Serialize one supported immutable record to canonical JSON text.

        Parameters
        ----------
        record
            Supported provenance DataObject or ResultObject.

        Returns
        -------
        str
            Compact sorted-key JSON containing no non-finite values and ending
            with exactly one line feed.

        Raises
        ------
        TypeError
            If ``record`` is not an explicitly supported public record.
        """
        data = _to_data(record)
        text = json.dumps(
            data,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        # Encoding is checked even though the Python API returns text, so output
        # is guaranteed to be representable as the specified UTF-8 wire bytes.
        text.encode("utf-8", errors="strict")
        return text + "\n"

    def deserialize(self, text: str) -> JsonRecord:
        """Deserialize one strict version-1 JSON record.

        Parameters
        ----------
        text
            JSON text with no BOM.  A final line feed is accepted but not
            required on input.

        Returns
        -------
        JsonRecord
            The exact public immutable record selected by ``record_type``.

        Raises
        ------
        TypeError
            If ``text`` is not a string.
        ProvenanceJsonError
            If JSON syntax, Unicode, keys, version, enums, field types, or record
            invariants violate the strict version-1 contract.
        """
        if type(text) is not str:
            raise TypeError("text must be a built-in str")
        if text.startswith("\ufeff"):
            raise ProvenanceJsonError("a Unicode byte-order mark is prohibited")
        try:
            value = json.loads(
                text,
                object_pairs_hook=_strict_object,
                parse_constant=_reject_constant,
            )
            _check_json_scalars(value)
            return _from_data(value)
        except ProvenanceJsonError:
            raise
        except (
            _DuplicateKeyError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ) as error:
            raise ProvenanceJsonError(str(error)) from error
