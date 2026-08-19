"""Default-unsigned Task gating and optional signed development authority.

This module represents only public verification material and deterministic outcomes.
It performs no signing, discovery, persistence, reservation, target effect, credential
access, or ambient authority selection.  The optional ``cryptography`` import occurs
only when a Task explicitly requires signed authority.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from importlib import import_module
from typing import Any, ClassVar, cast

from ._contract import (
    b64_decode,
    canonical_bytes,
    closed,
    derived_identity,
    identity_from_fields,
    require_canonical,
    require_digest,
    require_identifier,
    require_path,
    require_str,
    require_tuple,
    require_uint64,
    sha256,
    strict_json,
)

_CONFIG_DOMAIN = "ksdft2effmass-development-task-signature-configuration"
_TASK_REVISION_DOMAIN = "ksdft2effmass-development-configured-task-revision"
_REQUIREMENT_DOMAIN = "ksdft2effmass-development-task-signature-requirement-result"
_TRUST_DOMAIN = "ksdft2effmass-development-trust-configuration"
_PIN_DOMAIN = "ksdft2effmass-development-trust-configuration-pin"
_SOURCE_DOMAIN = "ksdft2effmass-development-authority-source"
_RECORD_DOMAIN = "ksdft2effmass-development-authority-record"
_RECEIPT_DOMAIN = "ksdft2effmass-development-authority-receipt"
_CONTEXT_DOMAIN = "ksdft2effmass-development-authority-context"
_INPUT_DOMAIN = "ksdft2effmass-development-operation-authorization-input"
_RESULT_DOMAIN = "ksdft2effmass-development-operation-authorization-result"
_CANONICALIZATION = "harness-canonical-json-v1"
_RECORD_KINDS = {
    "authority_policy",
    "task_authorization",
    "review_authorization",
    "promotion_authorization",
    "eligibility_reference",
    "authorization_use",
    "revocation",
}


def _version(value: object) -> None:
    if type(value) is not int:
        raise TypeError("schema_version must be an int excluding bool")
    if value != 1:
        raise ValueError("schema_version must equal 1")


def _optional_identifier(value: object, name: str) -> None:
    if value is not None:
        require_identifier(value, name)


def _optional_digest(value: object, name: str) -> None:
    if value is not None:
        require_digest(value, name)


def _diagnostics(
    values: tuple[DevelopmentAuthorityDiagnostic, ...], *, nonempty: bool = False
) -> None:
    require_tuple(values, "diagnostics", nonempty=nonempty)
    if any(type(value) is not DevelopmentAuthorityDiagnostic for value in values):
        raise TypeError("diagnostics must contain DevelopmentAuthorityDiagnostic")

    def key(value: DevelopmentAuthorityDiagnostic) -> tuple[str, str, str]:
        return (value.code, value.subject_identity or "", value.detail)

    if values != tuple(sorted(set(values), key=key)):
        raise ValueError("diagnostics must be canonical")


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityDiagnostic:
    """One deterministic authority diagnostic."""

    code: str
    subject_identity: str | None
    detail: str

    def __post_init__(self) -> None:
        require_identifier(self.code, "code")
        _optional_identifier(self.subject_identity, "subject_identity")
        require_str(self.detail, "detail")


@dataclass(frozen=True, slots=True)
class DevelopmentTaskSignatureConfiguration:
    """Repository-derived signature requirement for one exact Task record."""

    schema_version: int
    configuration_identity: str
    task_id: str
    task_record_identity: str
    signature_requirement: str

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.configuration_identity, "configuration_identity")
        require_identifier(self.task_id, "task_id")
        require_digest(self.task_record_identity, "task_record_identity")
        if self.signature_requirement not in {"not_required", "required"}:
            raise ValueError("invalid signature_requirement")


@dataclass(frozen=True, slots=True)
class DevelopmentTaskSignatureRequirementResult:
    """Closed outcome of resolving one exact Task signature requirement."""

    schema_version: int
    result_identity: str
    status: str
    task_id: str
    task_revision: str
    signature_requirement: str | None
    configuration_identity: str | None
    source: str | None
    diagnostics: tuple[DevelopmentAuthorityDiagnostic, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.result_identity, "result_identity")
        if self.status not in {"resolved", "error"}:
            raise ValueError("invalid requirement result status")
        require_identifier(self.task_id, "task_id")
        require_digest(self.task_revision, "task_revision")
        _optional_digest(self.configuration_identity, "configuration_identity")
        _diagnostics(self.diagnostics, nonempty=self.status == "error")
        if self.status == "resolved":
            if (
                self.signature_requirement not in {"not_required", "required"}
                or self.source not in {"default", "explicit"}
                or self.diagnostics
            ):
                raise ValueError("invalid resolved requirement result")
            if self.source == "default" and (
                self.signature_requirement != "not_required"
                or self.configuration_identity is not None
            ):
                raise ValueError("default result must be unsigned and unconfigured")
            if self.source == "explicit" and self.configuration_identity is None:
                raise ValueError("explicit result requires configuration_identity")
        elif any(
            value is not None
            for value in (
                self.signature_requirement,
                self.configuration_identity,
                self.source,
            )
        ):
            raise ValueError("error outcome fields must be null")


@dataclass(frozen=True, slots=True)
class DevelopmentTrustAnchor:
    """One public Ed25519 verification anchor; private material is unrepresentable."""

    schema_version: int
    anchor_id: str
    key_id: str
    mechanism: str
    public_key_encoding: str
    public_key_bytes: bytes
    issuer_authority_identity: str
    state: str

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_identifier(self.anchor_id, "anchor_id")
        require_digest(self.key_id, "key_id")
        if self.mechanism != "ed25519" or self.public_key_encoding != "raw-base64url":
            raise ValueError("unsupported public-key mechanism or encoding")
        if type(self.public_key_bytes) is not bytes or len(self.public_key_bytes) != 32:
            raise TypeError("public_key_bytes must be exactly 32 bytes")
        expected = sha256(
            b"ksdft2effmass-development-authority-key\x00v1\x00" + self.public_key_bytes
        )
        if self.key_id != expected:
            raise ValueError("key_id does not identify public_key_bytes")
        require_identifier(self.issuer_authority_identity, "issuer_authority_identity")
        if self.state not in {"enabled", "disabled"}:
            raise ValueError("invalid anchor state")


@dataclass(frozen=True, slots=True)
class DevelopmentIssuerAnchorBinding:
    """Threshold and allowed kinds for one issuer's enabled anchors."""

    issuer_authority_identity: str
    allowed_record_kinds: tuple[str, ...]
    anchor_ids: tuple[str, ...]
    threshold: int

    def __post_init__(self) -> None:
        require_identifier(self.issuer_authority_identity, "issuer_authority_identity")
        require_canonical(
            self.allowed_record_kinds, "allowed_record_kinds", nonempty=True
        )
        if not set(self.allowed_record_kinds) <= _RECORD_KINDS:
            raise ValueError("unknown allowed record kind")
        require_canonical(self.anchor_ids, "anchor_ids", nonempty=True)
        require_uint64(self.threshold, "threshold", positive=True)
        if self.threshold > len(self.anchor_ids):
            raise ValueError("threshold exceeds anchor count")


@dataclass(frozen=True, slots=True)
class DevelopmentTrustConfiguration:
    """Protected trust configuration pinned independently of candidate state."""

    schema_version: int
    configuration_identity: str
    configuration_revision: int
    predecessor_configuration_identity: str | None
    trust_domain: str
    accepted_payload_schema_version: int
    accepted_envelope_schema_version: int
    accepted_canonicalization_version: str
    accepted_source_modes: tuple[str, ...]
    accepted_head_artifact_identity: str
    required_ancestor_payload_identity: str
    minimum_snapshot_sequence: int
    anchors: tuple[DevelopmentTrustAnchor, ...]
    issuer_anchor_bindings: tuple[DevelopmentIssuerAnchorBinding, ...]
    resolver_policy_version: str

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.configuration_identity, "configuration_identity")
        require_uint64(self.configuration_revision, "configuration_revision")
        _optional_digest(
            self.predecessor_configuration_identity,
            "predecessor_configuration_identity",
        )
        if (self.configuration_revision == 0) != (
            self.predecessor_configuration_identity is None
        ):
            raise ValueError("configuration predecessor rule failed")
        require_identifier(self.trust_domain, "trust_domain")
        if (
            self.accepted_payload_schema_version != 1
            or type(self.accepted_payload_schema_version) is not int
        ):
            raise ValueError("accepted_payload_schema_version must equal 1")
        if (
            self.accepted_envelope_schema_version != 1
            or type(self.accepted_envelope_schema_version) is not int
        ):
            raise ValueError("accepted_envelope_schema_version must equal 1")
        if self.accepted_canonicalization_version != _CANONICALIZATION:
            raise ValueError("unsupported canonicalization")
        require_canonical(
            self.accepted_source_modes, "accepted_source_modes", nonempty=True
        )
        if not set(self.accepted_source_modes) <= {"local", "ci"}:
            raise ValueError("unknown source mode")
        require_digest(
            self.accepted_head_artifact_identity, "accepted_head_artifact_identity"
        )
        require_digest(
            self.required_ancestor_payload_identity,
            "required_ancestor_payload_identity",
        )
        require_uint64(self.minimum_snapshot_sequence, "minimum_snapshot_sequence")
        require_tuple(self.anchors, "anchors", nonempty=True)
        require_tuple(
            self.issuer_anchor_bindings, "issuer_anchor_bindings", nonempty=True
        )
        if any(type(value) is not DevelopmentTrustAnchor for value in self.anchors):
            raise TypeError("anchors has wrong member type")
        if tuple(a.anchor_id for a in self.anchors) != tuple(
            sorted({a.anchor_id for a in self.anchors})
        ):
            raise ValueError("anchors must be canonical by anchor_id")
        if any(
            type(value) is not DevelopmentIssuerAnchorBinding
            for value in self.issuer_anchor_bindings
        ):
            raise TypeError("issuer_anchor_bindings has wrong member type")
        if tuple(
            b.issuer_authority_identity for b in self.issuer_anchor_bindings
        ) != tuple(
            sorted({b.issuer_authority_identity for b in self.issuer_anchor_bindings})
        ):
            raise ValueError("issuer bindings must be canonical")
        anchor_map = {a.anchor_id: a for a in self.anchors}
        for binding in self.issuer_anchor_bindings:
            enabled = [anchor_map.get(a) for a in binding.anchor_ids]
            if any(
                a is None
                or a.issuer_authority_identity != binding.issuer_authority_identity
                for a in enabled
            ):
                raise ValueError(
                    "issuer binding names unavailable or wrong-issuer anchor"
                )
            if (
                sum(a.state == "enabled" for a in enabled if a is not None)
                < binding.threshold
            ):
                raise ValueError("issuer binding threshold lacks enabled anchors")
        require_identifier(self.resolver_policy_version, "resolver_policy_version")


@dataclass(frozen=True, slots=True)
class DevelopmentTrustConfigurationPin:
    """Independently authenticated anti-rollback trust-configuration pin."""

    schema_version: int
    pin_identity: str
    current_configuration_identity: str
    minimum_configuration_revision: int
    source_authority_identity: str
    authentication_receipt_identity: str

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.pin_identity, "pin_identity")
        require_digest(
            self.current_configuration_identity, "current_configuration_identity"
        )
        require_uint64(
            self.minimum_configuration_revision, "minimum_configuration_revision"
        )
        require_identifier(self.source_authority_identity, "source_authority_identity")
        require_identifier(
            self.authentication_receipt_identity, "authentication_receipt_identity"
        )


@dataclass(frozen=True, slots=True)
class DevelopmentAuthoritySnapshotSource:
    """Bounded explicit local or CI signed-snapshot source descriptor."""

    schema_version: int
    source_descriptor_identity: str
    mode: str
    source_reference_identity: str
    expected_head_artifact_identity: str
    maximum_snapshot_count: int
    maximum_aggregate_byte_count: int

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.source_descriptor_identity, "source_descriptor_identity")
        if self.mode not in {"local", "ci"}:
            raise ValueError("invalid source mode")
        require_identifier(self.source_reference_identity, "source_reference_identity")
        require_digest(
            self.expected_head_artifact_identity, "expected_head_artifact_identity"
        )
        require_uint64(
            self.maximum_snapshot_count, "maximum_snapshot_count", positive=True
        )
        require_uint64(
            self.maximum_aggregate_byte_count,
            "maximum_aggregate_byte_count",
            positive=True,
        )


@dataclass(frozen=True, slots=True)
class DevelopmentTaskOperationBinding:
    """Exact immutable Task-operation grant/request binding."""

    binding_kind: str
    signature_requirement_result_identity: str
    repository_root_identity: str
    source_snapshot_identity: str
    harness_state_identity: str
    selection_revision: str
    task_id: str
    task_revision: str
    starting_revision: str
    candidate_revision: str
    operation_id: str
    attempt_id: str
    idempotency_id: str
    operation_kind: str
    permitted_paths: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    architecture_policy_identity: str
    validator_profile_identity: str

    def __post_init__(self) -> None:
        if self.binding_kind != "task":
            raise ValueError("binding_kind must be task")
        for name in ("signature_requirement_result_identity",):
            require_digest(getattr(self, name), name)
        for name in (
            "repository_root_identity",
            "source_snapshot_identity",
            "harness_state_identity",
            "selection_revision",
            "task_id",
            "task_revision",
            "starting_revision",
            "candidate_revision",
            "operation_id",
            "attempt_id",
            "idempotency_id",
            "architecture_policy_identity",
            "validator_profile_identity",
        ):
            require_identifier(getattr(self, name), name)
        if self.operation_kind not in {
            "planning",
            "implementation_planning",
            "implementation",
            "verification",
            "administrative_closeout",
            "repository_mutation",
        }:
            raise ValueError("invalid task operation_kind")
        require_canonical(self.permitted_paths, "permitted_paths")
        for path in self.permitted_paths:
            require_path(path, "permitted_paths item")
        require_canonical(self.requirement_ids, "requirement_ids")
        for item in self.requirement_ids:
            require_identifier(item, "requirement_ids item")


@dataclass(frozen=True, slots=True)
class DevelopmentReviewOperationBinding:
    """Exact review operation binding including review subject and result."""

    binding_kind: str
    signature_requirement_result_identity: str
    repository_root_identity: str
    source_snapshot_identity: str
    harness_state_identity: str
    selection_revision: str
    task_id: str
    task_revision: str
    starting_revision: str
    candidate_revision: str
    operation_id: str
    attempt_id: str
    idempotency_id: str
    operation_kind: str
    permitted_paths: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    architecture_policy_identity: str
    validator_profile_identity: str
    review_subject_identity: str
    review_result_identity: str

    def __post_init__(self) -> None:
        values = {
            field.name: getattr(self, field.name)
            for field in fields(DevelopmentTaskOperationBinding)
        }
        values["binding_kind"] = "task"
        values["operation_kind"] = "verification"
        DevelopmentTaskOperationBinding(**values)
        if self.binding_kind != "review" or self.operation_kind != "review":
            raise ValueError("review binding kind and operation_kind must be review")
        require_identifier(self.review_subject_identity, "review_subject_identity")
        require_identifier(self.review_result_identity, "review_result_identity")


@dataclass(frozen=True, slots=True)
class DevelopmentPromotionOperationBinding:
    """Exact promotion, activation, or rollback operation binding."""

    binding_kind: str
    signature_requirement_result_identity: str
    repository_root_identity: str
    source_snapshot_identity: str
    harness_state_identity: str
    selection_revision: str
    task_id: str
    task_revision: str
    starting_revision: str
    candidate_revision: str
    operation_id: str
    attempt_id: str
    idempotency_id: str
    operation_kind: str
    permitted_paths: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    architecture_policy_identity: str
    validator_profile_identity: str
    decision_identity: str
    candidate_composition_identity: str
    predecessor_composition_identity: str
    target_identity: str

    def __post_init__(self) -> None:
        values = {
            field.name: getattr(self, field.name)
            for field in fields(DevelopmentTaskOperationBinding)
        }
        values["binding_kind"] = "task"
        values["operation_kind"] = "verification"
        DevelopmentTaskOperationBinding(**values)
        if self.binding_kind != "promotion" or self.operation_kind not in {
            "promotion",
            "activation",
            "rollback",
        }:
            raise ValueError("invalid promotion binding")
        for name in (
            "decision_identity",
            "candidate_composition_identity",
            "predecessor_composition_identity",
            "target_identity",
        ):
            require_identifier(getattr(self, name), name)


OperationBinding = (
    DevelopmentTaskOperationBinding
    | DevelopmentReviewOperationBinding
    | DevelopmentPromotionOperationBinding
)


def _common_record(value: Any, kind: str) -> None:
    _version(value.schema_version)
    require_identifier(value.record_id, "record_id")
    require_digest(value.record_content_identity, "record_content_identity")
    require_uint64(value.record_ordinal, "record_ordinal")
    _optional_digest(
        value.previous_record_content_identity, "previous_record_content_identity"
    )
    if (value.record_ordinal == 0) != (value.previous_record_content_identity is None):
        raise ValueError("record predecessor rule failed")
    if value.record_kind != kind:
        raise ValueError(f"record_kind must be {kind}")
    require_identifier(value.issuer_authority_identity, "issuer_authority_identity")
    _optional_digest(value.governing_policy_identity, "governing_policy_identity")
    if kind == "authority_policy" and value.record_ordinal == 0:
        if value.governing_policy_identity is not None:
            raise ValueError("genesis policy governing identity must be null")
    elif value.governing_policy_identity is None:
        raise ValueError("non-genesis record requires governing policy")


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityPolicy:
    """Closed ledger authority-policy record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    policy_revision: int
    policy_document_identity: str

    def __post_init__(self) -> None:
        _common_record(self, "authority_policy")
        require_uint64(self.policy_revision, "policy_revision")
        require_identifier(self.policy_document_identity, "policy_document_identity")


@dataclass(frozen=True, slots=True)
class DevelopmentTaskAuthorization:
    """Single-use exact Task-operation authorization record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    authorization_id: str
    operation_binding: DevelopmentTaskOperationBinding
    use_limit: int

    def __post_init__(self) -> None:
        _common_record(self, "task_authorization")
        require_identifier(self.authorization_id, "authorization_id")
        if type(self.operation_binding) is not DevelopmentTaskOperationBinding:
            raise TypeError("wrong operation binding")
        if self.use_limit != 1 or type(self.use_limit) is not int:
            raise ValueError("use_limit must equal 1")


@dataclass(frozen=True, slots=True)
class DevelopmentReviewAuthorization:
    """Single-use exact review authorization record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    authorization_id: str
    operation_binding: DevelopmentReviewOperationBinding
    use_limit: int

    def __post_init__(self) -> None:
        _common_record(self, "review_authorization")
        require_identifier(self.authorization_id, "authorization_id")
        if type(self.operation_binding) is not DevelopmentReviewOperationBinding:
            raise TypeError("wrong operation binding")
        if self.use_limit != 1 or type(self.use_limit) is not int:
            raise ValueError("use_limit must equal 1")


@dataclass(frozen=True, slots=True)
class DevelopmentPromotionAuthorization:
    """Single-use exact promotion authorization record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    authorization_id: str
    operation_binding: DevelopmentPromotionOperationBinding
    use_limit: int

    def __post_init__(self) -> None:
        _common_record(self, "promotion_authorization")
        require_identifier(self.authorization_id, "authorization_id")
        if type(self.operation_binding) is not DevelopmentPromotionOperationBinding:
            raise TypeError("wrong operation binding")
        if self.use_limit != 1 or type(self.use_limit) is not int:
            raise ValueError("use_limit must equal 1")


@dataclass(frozen=True, slots=True)
class DevelopmentEligibilityReference:
    """Closed eligibility-reference ledger record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    eligibility_result_identity: str
    subject_identity: str

    def __post_init__(self) -> None:
        _common_record(self, "eligibility_reference")
        require_identifier(
            self.eligibility_result_identity, "eligibility_result_identity"
        )
        require_identifier(self.subject_identity, "subject_identity")


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorizationUse:
    """Immutable evidence that one exact-attempt authorization was consumed."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    authorization_id: str
    operation_id: str
    attempt_id: str
    idempotency_id: str
    operation_receipt_identity: str

    def __post_init__(self) -> None:
        _common_record(self, "authorization_use")
        for name in (
            "authorization_id",
            "operation_id",
            "attempt_id",
            "idempotency_id",
            "operation_receipt_identity",
        ):
            require_identifier(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorizationRevocation:
    """Immutable revocation of an earlier authorization record."""

    schema_version: int
    record_id: str
    record_content_identity: str
    record_ordinal: int
    previous_record_content_identity: str | None
    record_kind: str
    issuer_authority_identity: str
    governing_policy_identity: str | None
    target_authorization_record_id: str
    reason_code: str
    replacement_authorization_record_id: str | None

    def __post_init__(self) -> None:
        _common_record(self, "revocation")
        require_identifier(
            self.target_authorization_record_id, "target_authorization_record_id"
        )
        require_identifier(self.reason_code, "reason_code")
        _optional_identifier(
            self.replacement_authorization_record_id,
            "replacement_authorization_record_id",
        )


DevelopmentAuthorityRecord = (
    DevelopmentAuthorityPolicy
    | DevelopmentTaskAuthorization
    | DevelopmentReviewAuthorization
    | DevelopmentPromotionAuthorization
    | DevelopmentEligibilityReference
    | DevelopmentAuthorizationUse
    | DevelopmentAuthorizationRevocation
)


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityLedgerSnapshot:
    """Complete immutable authority record history at one sequence."""

    schema_version: int
    ledger_id: str
    snapshot_sequence: int
    predecessor_payload_identity: str | None
    first_record_ordinal: int
    last_record_ordinal: int
    governing_policy_identity: str
    records: tuple[DevelopmentAuthorityRecord, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_identifier(self.ledger_id, "ledger_id")
        require_uint64(self.snapshot_sequence, "snapshot_sequence")
        _optional_digest(
            self.predecessor_payload_identity, "predecessor_payload_identity"
        )
        if (self.snapshot_sequence == 0) != (self.predecessor_payload_identity is None):
            raise ValueError("snapshot predecessor rule failed")
        if self.first_record_ordinal != 0 or type(self.first_record_ordinal) is not int:
            raise ValueError("first_record_ordinal must equal 0")
        require_uint64(self.last_record_ordinal, "last_record_ordinal")
        require_digest(self.governing_policy_identity, "governing_policy_identity")
        require_tuple(self.records, "records", nonempty=True)
        if self.last_record_ordinal != len(self.records) - 1 or tuple(
            r.record_ordinal for r in self.records
        ) != tuple(range(len(self.records))):
            raise ValueError("snapshot record ordinals must be complete")

    @property
    def payload_identity(self) -> str:
        """SHA-256 identity of exact canonical snapshot bytes."""
        return sha256(canonical_bytes(self))


@dataclass(frozen=True, slots=True)
class DevelopmentSignatureEntry:
    """One Ed25519 signature over the framed canonical snapshot payload."""

    mechanism: str
    key_id: str
    signature_encoding: str
    signature_bytes: bytes

    def __post_init__(self) -> None:
        if self.mechanism != "ed25519" or self.signature_encoding != "raw-base64url":
            raise ValueError("unsupported signature mechanism or encoding")
        require_digest(self.key_id, "key_id")
        if type(self.signature_bytes) is not bytes or len(self.signature_bytes) != 64:
            raise TypeError("signature_bytes must be exactly 64 bytes")


@dataclass(frozen=True, slots=True)
class DevelopmentSignedAuthoritySnapshot:
    """Canonical snapshot bytes and strictly ordered public signatures."""

    schema_version: int
    canonicalization_version: str
    payload_encoding: str
    payload_bytes: bytes
    signatures: tuple[DevelopmentSignatureEntry, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        if (
            self.canonicalization_version != _CANONICALIZATION
            or self.payload_encoding != "base64url-no-padding"
        ):
            raise ValueError("unsupported envelope encoding")
        if type(self.payload_bytes) is not bytes:
            raise TypeError("payload_bytes must be bytes")
        require_tuple(self.signatures, "signatures", nonempty=True)
        if any(type(s) is not DevelopmentSignatureEntry for s in self.signatures):
            raise TypeError("signatures has wrong member type")
        if tuple(s.key_id for s in self.signatures) != tuple(
            sorted({s.key_id for s in self.signatures})
        ):
            raise ValueError("signatures must be canonical by unique key_id")

    @property
    def artifact_identity(self) -> str:
        """SHA-256 identity of exact canonical envelope bytes."""
        return sha256(canonical_bytes(self))


_STATUS_FIELDS = (
    "source_status",
    "configuration_status",
    "content_status",
    "signature_status",
    "threshold_status",
    "snapshot_chain_status",
    "record_chain_status",
    "reference_closure_status",
    "issuer_policy_status",
    "accepted_head_status",
)


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityReconstructionReceipt:
    """Detailed deterministic evidence for context reconstruction."""

    schema_version: int
    receipt_identity: str
    source_descriptor_identity: str
    mode: str
    trust_configuration_pin_identity: str
    trust_configuration_identity: str
    trust_configuration_revision: int
    requested_head_artifact_identity: str
    observed_head_artifact_identity: str | None
    head_payload_identity: str | None
    head_snapshot_sequence: int | None
    verified_snapshot_count: int
    canonicalization_version: str
    resolver_version: str
    source_status: str
    configuration_status: str
    content_status: str
    signature_status: str
    threshold_status: str
    snapshot_chain_status: str
    record_chain_status: str
    reference_closure_status: str
    issuer_policy_status: str
    accepted_head_status: str
    verified_key_ids: tuple[str, ...]
    diagnostics: tuple[DevelopmentAuthorityDiagnostic, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.receipt_identity, "receipt_identity")
        require_digest(self.source_descriptor_identity, "source_descriptor_identity")
        if self.mode not in {"local", "ci"}:
            raise ValueError("invalid receipt mode")
        for name in (
            "trust_configuration_pin_identity",
            "trust_configuration_identity",
            "requested_head_artifact_identity",
        ):
            require_digest(getattr(self, name), name)
        require_uint64(
            self.trust_configuration_revision, "trust_configuration_revision"
        )
        _optional_digest(
            self.observed_head_artifact_identity, "observed_head_artifact_identity"
        )
        _optional_digest(self.head_payload_identity, "head_payload_identity")
        if self.head_snapshot_sequence is not None:
            require_uint64(self.head_snapshot_sequence, "head_snapshot_sequence")
        require_uint64(self.verified_snapshot_count, "verified_snapshot_count")
        if self.canonicalization_version != _CANONICALIZATION:
            raise ValueError("unsupported canonicalization")
        require_identifier(self.resolver_version, "resolver_version")
        for name in _STATUS_FIELDS:
            if getattr(self, name) not in {"passed", "failed", "not_reached"}:
                raise ValueError(f"invalid {name}")
        require_canonical(self.verified_key_ids, "verified_key_ids")
        _diagnostics(self.diagnostics)


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityContext:
    """Candidate-independent verified authority context."""

    schema_version: int
    context_identity: str
    trust_configuration_pin_identity: str
    trust_configuration_identity: str
    trust_configuration_revision: int
    source_descriptor_identity: str
    head_artifact_identity: str
    head_payload_identity: str
    ledger_id: str
    snapshot_sequence: int
    predecessor_payload_identity: str | None
    first_record_ordinal: int
    last_record_ordinal: int
    record_head_identity: str
    governing_policy_identity: str
    receipt_identity: str
    records: tuple[DevelopmentAuthorityRecord, ...]
    resolver_version: str

    def __post_init__(self) -> None:
        _version(self.schema_version)
        for name in (
            "context_identity",
            "trust_configuration_pin_identity",
            "trust_configuration_identity",
            "source_descriptor_identity",
            "head_artifact_identity",
            "head_payload_identity",
            "record_head_identity",
            "governing_policy_identity",
            "receipt_identity",
        ):
            require_digest(getattr(self, name), name)
        require_uint64(
            self.trust_configuration_revision, "trust_configuration_revision"
        )
        require_identifier(self.ledger_id, "ledger_id")
        require_uint64(self.snapshot_sequence, "snapshot_sequence")
        _optional_digest(
            self.predecessor_payload_identity, "predecessor_payload_identity"
        )
        if (self.snapshot_sequence == 0) != (
            self.predecessor_payload_identity is None
        ):
            raise ValueError("context snapshot predecessor rule failed")
        if self.first_record_ordinal != 0 or type(self.first_record_ordinal) is not int:
            raise ValueError("first_record_ordinal must equal 0")
        require_uint64(self.last_record_ordinal, "last_record_ordinal")
        require_tuple(self.records, "records", nonempty=True)
        if self.last_record_ordinal != len(self.records) - 1:
            raise ValueError("last_record_ordinal must match records")
        require_identifier(self.resolver_version, "resolver_version")


@dataclass(frozen=True, slots=True)
class DevelopmentAuthorityContextResolutionResult:
    """Closed resolved/failed authority-context outcome."""

    schema_version: int
    status: str
    receipt: DevelopmentAuthorityReconstructionReceipt
    context: DevelopmentAuthorityContext | None

    def __post_init__(self) -> None:
        _version(self.schema_version)
        if self.status not in {"resolved", "failed"}:
            raise ValueError("invalid resolution status")
        if type(self.receipt) is not DevelopmentAuthorityReconstructionReceipt:
            raise TypeError("receipt has wrong type")
        if self.status == "resolved":
            if (
                type(self.context) is not DevelopmentAuthorityContext
                or any(
                    getattr(self.receipt, name) != "passed" for name in _STATUS_FIELDS
                )
                or self.receipt.diagnostics
            ):
                raise ValueError(
                    "resolved result requires context, passed statuses, "
                    "and no diagnostics"
                )
        elif (
            self.context is not None
            or "failed" not in {getattr(self.receipt, name) for name in _STATUS_FIELDS}
            or not self.receipt.diagnostics
        ):
            raise ValueError(
                "failed result requires no context, a failure, and diagnostics"
            )


@dataclass(frozen=True, slots=True)
class DevelopmentOperationAuthorizationInput:
    """Exact operation request; it is never itself a grant."""

    schema_version: int
    input_identity: str
    operation_binding: OperationBinding

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.input_identity, "input_identity")
        if type(self.operation_binding) not in {
            DevelopmentTaskOperationBinding,
            DevelopmentReviewOperationBinding,
            DevelopmentPromotionOperationBinding,
        }:
            raise TypeError("operation_binding has wrong type")


@dataclass(frozen=True, slots=True)
class DevelopmentOperationAuthorizationResult:
    """Closed unsigned-default, authorized, denied, or error outcome."""

    schema_version: int
    result_identity: str
    status: str
    input: DevelopmentOperationAuthorizationInput
    requested_signature_requirement_result_identity: str
    observed_signature_requirement_result_identity: str | None
    context_identity: str | None
    authorization_id: str | None
    authorization_record_content_identity: str | None
    authorizer_version: str
    diagnostics: tuple[DevelopmentAuthorityDiagnostic, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        require_digest(self.result_identity, "result_identity")
        if self.status not in {
            "signature_not_required",
            "authorized",
            "denied",
            "error",
        }:
            raise ValueError("invalid authorization status")
        if type(self.input) is not DevelopmentOperationAuthorizationInput:
            raise TypeError("input has wrong type")
        require_digest(
            self.requested_signature_requirement_result_identity, "requested identity"
        )
        _optional_digest(
            self.observed_signature_requirement_result_identity, "observed identity"
        )
        _optional_digest(self.context_identity, "context_identity")
        _optional_identifier(self.authorization_id, "authorization_id")
        _optional_digest(
            self.authorization_record_content_identity,
            "authorization_record_content_identity",
        )
        require_identifier(self.authorizer_version, "authorizer_version")
        _diagnostics(self.diagnostics, nonempty=self.status in {"denied", "error"})
        if (
            self.requested_signature_requirement_result_identity
            != self.input.operation_binding.signature_requirement_result_identity
        ):
            raise ValueError("requested identity does not match operation binding")
        if (
            self.status != "error"
            and self.observed_signature_requirement_result_identity
            != self.requested_signature_requirement_result_identity
        ):
            raise ValueError("non-error result requires exact observed identity")
        if self.status == "signature_not_required" and (
            self.diagnostics
            or any(
                v is not None
                for v in (
                    self.context_identity,
                    self.authorization_id,
                    self.authorization_record_content_identity,
                )
            )
        ):
            raise ValueError("unsigned result must be clean and identify no authority")
        if self.status == "authorized" and (
            self.diagnostics
            or any(
                v is None
                for v in (
                    self.context_identity,
                    self.authorization_id,
                    self.authorization_record_content_identity,
                )
            )
        ):
            raise ValueError(
                "authorized result requires clean context and authorization identities"
            )
        if self.status == "denied" and self.context_identity is None:
            raise ValueError("denied result requires a reliable context identity")
        if self.status in {"denied", "error"} and any(
            v is not None
            for v in (self.authorization_id, self.authorization_record_content_identity)
        ):
            raise ValueError("non-authorized result must not identify authorization")


class DevelopmentTaskSignatureRequirementResolver:
    """Resolve the exact configured Task revision without touching cryptography."""

    __slots__ = ()
    version: ClassVar[str] = "development-signature-requirement-resolver-v1"

    def execute(
        self,
        *,
        task_id: str,
        task_record_identity: str,
        expected_task_revision: str,
        configuration: DevelopmentTaskSignatureConfiguration | None = None,
    ) -> DevelopmentTaskSignatureRequirementResult:
        """Return default unsigned, explicit, or fail-closed mismatch outcome."""
        require_identifier(task_id, "task_id")
        require_digest(task_record_identity, "task_record_identity")
        require_digest(expected_task_revision, "expected_task_revision")
        diagnostic: DevelopmentAuthorityDiagnostic | None = None
        config_identity: str | None = None
        requirement: str | None = "not_required"
        source: str | None = "default"
        if configuration is not None:
            if type(configuration) is not DevelopmentTaskSignatureConfiguration:
                raise TypeError("configuration has wrong type")
            config_identity = configuration.configuration_identity
            requirement = configuration.signature_requirement
            source = "explicit"
            if (
                configuration.task_id != task_id
                or configuration.task_record_identity != task_record_identity
                or derived_identity(
                    _CONFIG_DOMAIN, configuration, "configuration_identity"
                )
                != configuration.configuration_identity
            ):
                diagnostic = DevelopmentAuthorityDiagnostic(
                    "AUTH.CONFIGURATION_MISMATCH",
                    task_id,
                    "signature configuration does not match the exact Task",
                )
        revision_body = {
            "schema_version": 1,
            "task_record_identity": task_record_identity,
            "signature_configuration_identity": config_identity,
            "signature_requirement": requirement,
        }
        actual_revision = identity_from_fields(_TASK_REVISION_DOMAIN, revision_body)
        if diagnostic is None and actual_revision != expected_task_revision:
            diagnostic = DevelopmentAuthorityDiagnostic(
                "AUTH.TASK_REVISION_MISMATCH",
                task_id,
                "configured Task revision does not match caller input",
            )
        if diagnostic is not None:
            body: dict[str, object] = {
                "schema_version": 1,
                "result_identity": None,
                "status": "error",
                "task_id": task_id,
                "task_revision": expected_task_revision,
                "signature_requirement": None,
                "configuration_identity": None,
                "source": None,
                "diagnostics": (diagnostic,),
            }
        else:
            body = {
                "schema_version": 1,
                "result_identity": None,
                "status": "resolved",
                "task_id": task_id,
                "task_revision": expected_task_revision,
                "signature_requirement": requirement,
                "configuration_identity": config_identity,
                "source": source,
                "diagnostics": (),
            }
        body["result_identity"] = identity_from_fields(_REQUIREMENT_DOMAIN, body)
        return DevelopmentTaskSignatureRequirementResult(**cast(Any, body))


def _resolution_is_internally_consistent(
    resolution: DevelopmentAuthorityContextResolutionResult,
) -> bool:
    """Return whether one successful resolver result is self-consistent."""
    if resolution.status != "resolved" or resolution.context is None:
        return False
    receipt = resolution.receipt
    context = resolution.context
    if (
        derived_identity(_RECEIPT_DOMAIN, receipt, "receipt_identity")
        != receipt.receipt_identity
        or derived_identity(_CONTEXT_DOMAIN, context, "context_identity")
        != context.context_identity
        or context.receipt_identity != receipt.receipt_identity
        or any(getattr(receipt, name) != "passed" for name in _STATUS_FIELDS)
        or receipt.diagnostics
    ):
        return False
    shared = (
        (
            context.trust_configuration_pin_identity,
            receipt.trust_configuration_pin_identity,
        ),
        (context.trust_configuration_identity, receipt.trust_configuration_identity),
        (context.trust_configuration_revision, receipt.trust_configuration_revision),
        (context.source_descriptor_identity, receipt.source_descriptor_identity),
        (context.head_artifact_identity, receipt.observed_head_artifact_identity),
        (context.head_payload_identity, receipt.head_payload_identity),
        (context.snapshot_sequence, receipt.head_snapshot_sequence),
        (context.resolver_version, receipt.resolver_version),
    )
    if any(actual != observed for actual, observed in shared):
        return False
    try:
        reconstructed_head = DevelopmentAuthorityLedgerSnapshot(
            1,
            context.ledger_id,
            context.snapshot_sequence,
            context.predecessor_payload_identity,
            context.first_record_ordinal,
            context.last_record_ordinal,
            context.governing_policy_identity,
            context.records,
        )
    except (TypeError, ValueError):
        return False
    if reconstructed_head.payload_identity != context.head_payload_identity:
        return False
    previous: str | None = None
    seen_record_ids: set[str] = set()
    seen_authorization_ids: set[str] = set()
    for ordinal, record in enumerate(context.records):
        if (
            record.record_ordinal != ordinal
            or record.previous_record_content_identity != previous
            or record.record_id in seen_record_ids
            or derived_identity(_RECORD_DOMAIN, record, "record_content_identity")
            != record.record_content_identity
        ):
            return False
        seen_record_ids.add(record.record_id)
        if isinstance(
            record,
            (
                DevelopmentTaskAuthorization,
                DevelopmentReviewAuthorization,
                DevelopmentPromotionAuthorization,
            ),
        ):
            if record.authorization_id in seen_authorization_ids:
                return False
            seen_authorization_ids.add(record.authorization_id)
        previous = record.record_content_identity
    return (
        previous == context.record_head_identity
        and context.records[-1].record_content_identity == context.record_head_identity
    )


class DevelopmentOperationAuthorizer:
    """Match one exact operation against an already resolved authority context."""

    __slots__ = ()
    version: ClassVar[str] = "development-operation-authorizer-v1"

    def execute(
        self,
        operation_input: DevelopmentOperationAuthorizationInput,
        signature_requirement: DevelopmentTaskSignatureRequirementResult,
        context_resolution: DevelopmentAuthorityContextResolutionResult | None = None,
    ) -> DevelopmentOperationAuthorizationResult:
        """Return a bound unsigned, authorized, denied, or fail-closed result.

        Signed mode accepts only the complete successful resolver result, not a
        caller-assembled context value. Receipt and context identities and their
        shared reconstruction fields are independently rechecked before matching.
        """
        if (
            type(operation_input) is not DevelopmentOperationAuthorizationInput
            or type(signature_requirement)
            is not DevelopmentTaskSignatureRequirementResult
        ):
            raise TypeError("authorizer inputs have wrong type")
        binding = operation_input.operation_binding
        requested = binding.signature_requirement_result_identity
        diagnostics: tuple[DevelopmentAuthorityDiagnostic, ...] = ()
        status = "error"
        context_id = None
        authorization_id = None
        record_identity = None
        input_identity_valid = (
            derived_identity(_INPUT_DOMAIN, operation_input, "input_identity")
            == operation_input.input_identity
        )
        requirement_identity_valid = (
            derived_identity(
                _REQUIREMENT_DOMAIN, signature_requirement, "result_identity"
            )
            == signature_requirement.result_identity
        )
        if (
            not input_identity_valid
            or not requirement_identity_valid
            or signature_requirement.result_identity != requested
            or signature_requirement.status != "resolved"
            or signature_requirement.task_id != binding.task_id
            or signature_requirement.task_revision != binding.task_revision
        ):
            diagnostics = (
                DevelopmentAuthorityDiagnostic(
                    "AUTH.REQUIREMENT_MISMATCH",
                    operation_input.input_identity,
                    "operation or signature requirement identity and Task binding "
                    "is unavailable or mismatched",
                ),
            )
        elif signature_requirement.signature_requirement == "not_required":
            if context_resolution is not None:
                diagnostics = (
                    DevelopmentAuthorityDiagnostic(
                        "AUTH.UNEXPECTED_CONTEXT",
                        operation_input.input_identity,
                        "unsigned operation must not consume authority context",
                    ),
                )
            else:
                status = "signature_not_required"
        elif context_resolution is None:
            diagnostics = (
                DevelopmentAuthorityDiagnostic(
                    "AUTH.CONTEXT_REQUIRED",
                    operation_input.input_identity,
                    "required signed authority resolution is unavailable",
                ),
            )
        elif (
            type(context_resolution) is not DevelopmentAuthorityContextResolutionResult
        ):
            raise TypeError("context_resolution has wrong type")
        elif not _resolution_is_internally_consistent(context_resolution):
            diagnostics = (
                DevelopmentAuthorityDiagnostic(
                    "AUTH.CONTEXT_INCONSISTENT",
                    operation_input.input_identity,
                    "authority resolution receipt or context identity is inconsistent",
                ),
            )
        else:
            context = cast(DevelopmentAuthorityContext, context_resolution.context)
            context_id = context.context_identity
            authorizations = [
                record
                for record in context.records
                if isinstance(
                    record,
                    (
                        DevelopmentTaskAuthorization,
                        DevelopmentReviewAuthorization,
                        DevelopmentPromotionAuthorization,
                    ),
                )
                and record.operation_binding == operation_input.operation_binding
            ]
            revoked = {
                record.target_authorization_record_id
                for record in context.records
                if isinstance(record, DevelopmentAuthorizationRevocation)
            }
            used = {
                record.authorization_id
                for record in context.records
                if isinstance(record, DevelopmentAuthorizationUse)
            }
            valid = [
                record
                for record in authorizations
                if record.record_id not in revoked
                and record.authorization_id not in used
            ]
            if len(valid) == 1:
                status = "authorized"
                authorization_id = valid[0].authorization_id
                record_identity = valid[0].record_content_identity
            else:
                status = "denied"
                diagnostics = (
                    DevelopmentAuthorityDiagnostic(
                        "AUTH.NO_EXACT_UNUSED_GRANT",
                        operation_input.input_identity,
                        "no unique exact unrevoked unused authorization exists",
                    ),
                )
        body: dict[str, object] = {
            "schema_version": 1,
            "result_identity": None,
            "status": status,
            "input": operation_input,
            "requested_signature_requirement_result_identity": requested,
            "observed_signature_requirement_result_identity": (
                signature_requirement.result_identity
            ),
            "context_identity": context_id,
            "authorization_id": authorization_id,
            "authorization_record_content_identity": record_identity,
            "authorizer_version": self.version,
            "diagnostics": diagnostics,
        }
        body["result_identity"] = identity_from_fields(_RESULT_DOMAIN, body)
        return DevelopmentOperationAuthorizationResult(**cast(Any, body))


# Strict serializer mechanics. Each serializer exposes execute/serialize and typed
# deserialization methods; no record owns wire or persistence behavior.
class _Serializer:
    __slots__ = ()

    def execute(self, value: object) -> bytes:
        return canonical_bytes(value)

    serialize = execute

    @staticmethod
    def _decode(payload: bytes) -> Any:
        value = strict_json(payload)
        if canonical_bytes(value) != payload:
            raise ValueError("payload is not canonical Harness JSON")
        return value


def _record_from_wire(value: object) -> DevelopmentAuthorityRecord:
    if type(value) is not dict:
        raise TypeError("record must be a JSON object")
    kinds: dict[str, type[Any]] = {
        "authority_policy": DevelopmentAuthorityPolicy,
        "task_authorization": DevelopmentTaskAuthorization,
        "review_authorization": DevelopmentReviewAuthorization,
        "promotion_authorization": DevelopmentPromotionAuthorization,
        "eligibility_reference": DevelopmentEligibilityReference,
        "authorization_use": DevelopmentAuthorizationUse,
        "revocation": DevelopmentAuthorizationRevocation,
    }
    cls = kinds.get(cast(str, value.get("record_kind")))
    if cls is None:
        raise ValueError("unknown record_kind")
    data = closed(value, {field.name for field in fields(cls)}, "authority record")
    if "operation_binding" in data:
        data["operation_binding"] = _binding_from_wire(data["operation_binding"])
    return cls(**data)


def _binding_from_wire(value: object) -> OperationBinding:
    if type(value) is not dict:
        raise TypeError("operation binding must be a JSON object")
    classes = {
        "task": DevelopmentTaskOperationBinding,
        "review": DevelopmentReviewOperationBinding,
        "promotion": DevelopmentPromotionOperationBinding,
    }
    cls = classes.get(cast(str, value.get("binding_kind")))
    if cls is None:
        raise ValueError("unknown binding_kind")
    data = closed(value, {field.name for field in fields(cls)}, "operation binding")
    for name in ("permitted_paths", "requirement_ids"):
        if type(data[name]) is not list:
            raise TypeError(f"{name} must be a JSON array")
        data[name] = tuple(data[name])
    return cls(**data)


class DevelopmentTaskSignatureConfigurationSerializer(_Serializer):
    """Strict Task signature-configuration and requirement-result serializer."""

    def deserialize_configuration(
        self, payload: bytes
    ) -> DevelopmentTaskSignatureConfiguration:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentTaskSignatureConfiguration)},
            "signature configuration",
        )
        return DevelopmentTaskSignatureConfiguration(**value)

    def deserialize_result(
        self, payload: bytes
    ) -> DevelopmentTaskSignatureRequirementResult:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentTaskSignatureRequirementResult)},
            "requirement result",
        )
        value["diagnostics"] = _diagnostics_from_wire(value["diagnostics"])
        return DevelopmentTaskSignatureRequirementResult(**value)


class DevelopmentTrustConfigurationSerializer(_Serializer):
    """Strict protected trust, pin, and source-descriptor serializer."""

    def deserialize_configuration(
        self, payload: bytes
    ) -> DevelopmentTrustConfiguration:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentTrustConfiguration)},
            "trust configuration",
        )
        for name in ("accepted_source_modes",):
            value[name] = tuple(value[name])
        value["anchors"] = tuple(_anchor_from_wire(v) for v in value["anchors"])
        value["issuer_anchor_bindings"] = tuple(
            _binding_policy_from_wire(v) for v in value["issuer_anchor_bindings"]
        )
        return DevelopmentTrustConfiguration(**value)

    def deserialize_pin(self, payload: bytes) -> DevelopmentTrustConfigurationPin:
        return DevelopmentTrustConfigurationPin(
            **closed(
                self._decode(payload),
                {f.name for f in fields(DevelopmentTrustConfigurationPin)},
                "trust pin",
            )
        )

    def deserialize_source(self, payload: bytes) -> DevelopmentAuthoritySnapshotSource:
        return DevelopmentAuthoritySnapshotSource(
            **closed(
                self._decode(payload),
                {f.name for f in fields(DevelopmentAuthoritySnapshotSource)},
                "snapshot source",
            )
        )


def _anchor_from_wire(value: object) -> DevelopmentTrustAnchor:
    data = closed(
        value, {f.name for f in fields(DevelopmentTrustAnchor)}, "trust anchor"
    )
    data["public_key_bytes"] = b64_decode(
        data["public_key_bytes"], "public_key_bytes", 32
    )
    return DevelopmentTrustAnchor(**data)


def _binding_policy_from_wire(value: object) -> DevelopmentIssuerAnchorBinding:
    data = closed(
        value,
        {f.name for f in fields(DevelopmentIssuerAnchorBinding)},
        "issuer binding",
    )
    data["allowed_record_kinds"] = tuple(data["allowed_record_kinds"])
    data["anchor_ids"] = tuple(data["anchor_ids"])
    return DevelopmentIssuerAnchorBinding(**data)


def _diagnostics_from_wire(value: object) -> tuple[DevelopmentAuthorityDiagnostic, ...]:
    if type(value) is not list:
        raise TypeError("diagnostics must be a JSON array")
    return tuple(
        DevelopmentAuthorityDiagnostic(
            **closed(v, {"code", "subject_identity", "detail"}, "diagnostic")
        )
        for v in value
    )


class DevelopmentSignedAuthoritySnapshotSerializer(_Serializer):
    """Strict authority records, snapshots, signatures, and envelopes serializer."""

    def deserialize_snapshot(
        self, payload: bytes
    ) -> DevelopmentAuthorityLedgerSnapshot:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentAuthorityLedgerSnapshot)},
            "snapshot",
        )
        value["records"] = tuple(_record_from_wire(v) for v in value["records"])
        return DevelopmentAuthorityLedgerSnapshot(**value)

    def deserialize_envelope(
        self, payload: bytes
    ) -> DevelopmentSignedAuthoritySnapshot:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentSignedAuthoritySnapshot)},
            "signed snapshot",
        )
        value["payload_bytes"] = b64_decode_arbitrary(
            value["payload_bytes"], "payload_bytes"
        )
        value["signatures"] = tuple(
            _signature_from_wire(v) for v in value["signatures"]
        )
        result = DevelopmentSignedAuthoritySnapshot(**value)
        if canonical_bytes(result) != payload:
            raise ValueError("envelope is not canonical")
        return result


def b64_decode_arbitrary(value: object, name: str) -> bytes:
    import base64

    text = require_str(value, name)
    if "=" in text:
        raise ValueError(f"{name} must be unpadded")
    try:
        result = base64.b64decode(
            text + "=" * (-len(text) % 4), altchars=b"-_", validate=True
        )
    except Exception as exc:
        raise ValueError(f"{name} must be canonical base64url") from exc
    from ._contract import b64_encode

    if b64_encode(result) != text:
        raise ValueError(f"{name} must be canonical base64url")
    return result


def _signature_from_wire(value: object) -> DevelopmentSignatureEntry:
    data = closed(
        value, {f.name for f in fields(DevelopmentSignatureEntry)}, "signature"
    )
    data["signature_bytes"] = b64_decode(data["signature_bytes"], "signature_bytes", 64)
    return DevelopmentSignatureEntry(**data)


class DevelopmentAuthorityResolutionSerializer(_Serializer):
    """Strict reconstruction receipt, context, and result serializer."""

    _owned_types = (
        DevelopmentAuthorityReconstructionReceipt,
        DevelopmentAuthorityContext,
        DevelopmentAuthorityContextResolutionResult,
    )

    def execute(self, value: object) -> bytes:
        """Serialize only one resolution-family value to canonical bytes."""
        if type(value) not in self._owned_types:
            raise TypeError("value must be an authority resolution-family value")
        return canonical_bytes(value)

    serialize = execute

    def deserialize_receipt(
        self, payload: bytes
    ) -> DevelopmentAuthorityReconstructionReceipt:
        """Deserialize one exact canonical reconstruction receipt."""
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentAuthorityReconstructionReceipt)},
            "reconstruction receipt",
        )
        value["verified_key_ids"] = _string_tuple_from_wire(
            value["verified_key_ids"], "verified_key_ids"
        )
        value["diagnostics"] = _diagnostics_from_wire(value["diagnostics"])
        result = DevelopmentAuthorityReconstructionReceipt(**value)
        _require_exact_typed_payload(result, payload, "reconstruction receipt")
        return result

    def deserialize_context(self, payload: bytes) -> DevelopmentAuthorityContext:
        """Deserialize one exact canonical authority context."""
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentAuthorityContext)},
            "authority context",
        )
        records = value["records"]
        if type(records) is not list:
            raise TypeError("records must be a JSON array")
        value["records"] = tuple(_record_from_wire(item) for item in records)
        result = DevelopmentAuthorityContext(**value)
        _require_exact_typed_payload(result, payload, "authority context")
        return result

    def deserialize_result(
        self, payload: bytes
    ) -> DevelopmentAuthorityContextResolutionResult:
        """Deserialize one exact canonical closed context-resolution result."""
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentAuthorityContextResolutionResult)},
            "context resolution result",
        )
        value["receipt"] = _receipt_from_wire(value["receipt"])
        if value["context"] is not None:
            value["context"] = _context_from_wire(value["context"])
        result = DevelopmentAuthorityContextResolutionResult(**value)
        _require_exact_typed_payload(result, payload, "context resolution result")
        return result


class DevelopmentOperationAuthorizationSerializer(_Serializer):
    """Strict operation input and closed authorization-result serializer."""

    _owned_types = (
        DevelopmentOperationAuthorizationInput,
        DevelopmentOperationAuthorizationResult,
    )

    def execute(self, value: object) -> bytes:
        """Serialize only one operation-authorization-family value."""
        if type(value) not in self._owned_types:
            raise TypeError("value must be an operation authorization-family value")
        return canonical_bytes(value)

    serialize = execute

    def deserialize_input(
        self, payload: bytes
    ) -> DevelopmentOperationAuthorizationInput:
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentOperationAuthorizationInput)},
            "authorization input",
        )
        value["operation_binding"] = _binding_from_wire(value["operation_binding"])
        result = DevelopmentOperationAuthorizationInput(**value)
        _require_exact_typed_payload(result, payload, "authorization input")
        return result

    def deserialize_result(
        self, payload: bytes
    ) -> DevelopmentOperationAuthorizationResult:
        """Deserialize one exact canonical closed authorization result."""
        value = closed(
            self._decode(payload),
            {f.name for f in fields(DevelopmentOperationAuthorizationResult)},
            "authorization result",
        )
        value["input"] = _operation_input_from_wire(value["input"])
        value["diagnostics"] = _diagnostics_from_wire(value["diagnostics"])
        result = DevelopmentOperationAuthorizationResult(**value)
        _require_exact_typed_payload(result, payload, "authorization result")
        return result


def _string_tuple_from_wire(value: object, name: str) -> tuple[str, ...]:
    if type(value) is not list:
        raise TypeError(f"{name} must be a JSON array")
    if any(type(item) is not str for item in value):
        raise TypeError(f"{name} must contain strings")
    return tuple(value)


def _receipt_from_wire(value: object) -> DevelopmentAuthorityReconstructionReceipt:
    payload = canonical_bytes(value)
    return DevelopmentAuthorityResolutionSerializer().deserialize_receipt(payload)


def _context_from_wire(value: object) -> DevelopmentAuthorityContext:
    payload = canonical_bytes(value)
    return DevelopmentAuthorityResolutionSerializer().deserialize_context(payload)


def _operation_input_from_wire(value: object) -> DevelopmentOperationAuthorizationInput:
    payload = canonical_bytes(value)
    return DevelopmentOperationAuthorizationSerializer().deserialize_input(payload)


def _require_exact_typed_payload(value: object, payload: bytes, name: str) -> None:
    if canonical_bytes(value) != payload:
        raise ValueError(f"{name} is not canonical for its typed value")


class DevelopmentAuthorityContextResolver:
    """Fail-closed verifier for one bounded explicitly supplied signed ledger chain."""

    __slots__ = ()
    version: ClassVar[str] = "development-authority-context-resolver-v1"

    def execute(
        self,
        pin: DevelopmentTrustConfigurationPin,
        configuration: DevelopmentTrustConfiguration,
        source: DevelopmentAuthoritySnapshotSource,
        envelope_bytes: tuple[bytes, ...],
    ) -> DevelopmentAuthorityContextResolutionResult:
        """Authenticate and reconstruct one exact candidate-independent context."""
        if (
            type(pin) is not DevelopmentTrustConfigurationPin
            or type(configuration) is not DevelopmentTrustConfiguration
            or type(source) is not DevelopmentAuthoritySnapshotSource
        ):
            raise TypeError("resolver inputs have wrong type")
        require_tuple(envelope_bytes, "envelope_bytes", nonempty=True)
        diagnostics: list[DevelopmentAuthorityDiagnostic] = []
        envelopes: list[DevelopmentSignedAuthoritySnapshot] = []
        snapshots: list[DevelopmentAuthorityLedgerSnapshot] = []
        verified_keys_by_envelope: list[set[str]] = []
        statuses = {name: "not_reached" for name in _STATUS_FIELDS}
        observed = None
        head_payload = None
        sequence = None

        def fail(code: str, detail: str, status: str) -> None:
            statuses[status] = "failed"
            diagnostics.append(
                DevelopmentAuthorityDiagnostic(
                    code, source.source_reference_identity, detail
                )
            )

        if (
            derived_identity(_PIN_DOMAIN, pin, "pin_identity") != pin.pin_identity
            or derived_identity(_TRUST_DOMAIN, configuration, "configuration_identity")
            != configuration.configuration_identity
            or pin.current_configuration_identity
            != configuration.configuration_identity
            or configuration.configuration_revision < pin.minimum_configuration_revision
        ):
            fail(
                "AUTH.TRUST_CONFIGURATION",
                "protected trust configuration or pin mismatch",
                "configuration_status",
            )
        else:
            statuses["configuration_status"] = "passed"
        if statuses["configuration_status"] == "passed":
            if (
                derived_identity(_SOURCE_DOMAIN, source, "source_descriptor_identity")
                != source.source_descriptor_identity
                or source.mode not in configuration.accepted_source_modes
                or source.expected_head_artifact_identity
                != configuration.accepted_head_artifact_identity
                or len(envelope_bytes) > source.maximum_snapshot_count
                or sum(len(v) for v in envelope_bytes)
                > source.maximum_aggregate_byte_count
            ):
                fail(
                    "AUTH.SOURCE_BOUNDARY",
                    "source descriptor, mode, head, or bounds mismatch",
                    "source_status",
                )
            else:
                statuses["source_status"] = "passed"
        if statuses["source_status"] == "passed":
            serializer = DevelopmentSignedAuthoritySnapshotSerializer()
            try:
                for raw in envelope_bytes:
                    envelope = serializer.deserialize_envelope(raw)
                    snapshot = serializer.deserialize_snapshot(envelope.payload_bytes)
                    envelopes.append(envelope)
                    snapshots.append(snapshot)
                statuses["content_status"] = "passed"
            except (TypeError, ValueError) as exc:
                fail("AUTH.CONTENT", str(exc), "content_status")
        if statuses["content_status"] == "passed":
            try:
                exceptions_module = import_module("cryptography.exceptions")
                ed25519_module = import_module(
                    "cryptography.hazmat.primitives.asymmetric.ed25519"
                )
                invalid_signature = exceptions_module.InvalidSignature
                public_key_type = ed25519_module.Ed25519PublicKey
            except ImportError:
                fail(
                    "AUTH.SIGNATURE_CAPABILITY_UNAVAILABLE",
                    "optional authority-signatures capability is unavailable",
                    "signature_status",
                )
            else:
                anchors = {
                    a.key_id: a for a in configuration.anchors if a.state == "enabled"
                }
                try:
                    for envelope, _snapshot in zip(envelopes, snapshots, strict=True):
                        preimage = (
                            b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
                            + len(envelope.payload_bytes).to_bytes(8, "big")
                            + envelope.payload_bytes
                        )
                        envelope_keys: set[str] = set()
                        for signature in envelope.signatures:
                            anchor = anchors.get(signature.key_id)
                            if anchor is None:
                                continue
                            public_key_type.from_public_bytes(
                                anchor.public_key_bytes
                            ).verify(signature.signature_bytes, preimage)
                            envelope_keys.add(signature.key_id)
                        if not envelope_keys:
                            raise ValueError(
                                "each envelope requires an enabled verified signer"
                            )
                        verified_keys_by_envelope.append(envelope_keys)
                    statuses["signature_status"] = "passed"
                except invalid_signature, ValueError:
                    fail(
                        "AUTH.INVALID_SIGNATURE",
                        "an envelope signature is invalid",
                        "signature_status",
                    )
        if statuses["signature_status"] == "passed":
            head = snapshots[-1]
            head_envelope = envelopes[-1]
            observed = head_envelope.artifact_identity
            head_payload = head.payload_identity
            sequence = head.snapshot_sequence
            # Only signatures over the accepted head may satisfy its record policy.
            # A key verified on an ancestor cannot be carried forward implicitly.
            head_verified_keys = verified_keys_by_envelope[-1]
            anchors_by_id = {a.anchor_id: a for a in configuration.anchors}
            bindings = {
                b.issuer_authority_identity: b
                for b in configuration.issuer_anchor_bindings
            }
            okay = True
            for record in head.records:
                binding = bindings.get(record.issuer_authority_identity)
                keys = (
                    {
                        anchors_by_id[a].key_id
                        for a in binding.anchor_ids
                        if a in anchors_by_id and anchors_by_id[a].state == "enabled"
                    }
                    if binding
                    else set()
                )
                if (
                    binding is None
                    or record.record_kind not in binding.allowed_record_kinds
                    or len(keys & head_verified_keys) < binding.threshold
                ):
                    okay = False
            if okay:
                statuses["threshold_status"] = "passed"
                statuses["issuer_policy_status"] = "passed"
            else:
                fail(
                    "AUTH.ISSUER_THRESHOLD",
                    "issuer binding or threshold failed",
                    "threshold_status",
                )
        if statuses["threshold_status"] == "passed":
            chain_ok = (
                snapshots[0].payload_identity
                == configuration.required_ancestor_payload_identity
            )
            for before, after in zip(snapshots, snapshots[1:], strict=False):
                chain_ok &= (
                    after.predecessor_payload_identity == before.payload_identity
                    and after.snapshot_sequence == before.snapshot_sequence + 1
                    and after.ledger_id == before.ledger_id
                    and after.records[: len(before.records)] == before.records
                )
            if chain_ok:
                statuses["snapshot_chain_status"] = "passed"
            else:
                fail(
                    "AUTH.SNAPSHOT_CHAIN",
                    "snapshot ancestry or prefix continuity failed",
                    "snapshot_chain_status",
                )
        if statuses["snapshot_chain_status"] == "passed":
            head = snapshots[-1]
            chain_ok = all(
                r.record_content_identity
                == derived_identity(_RECORD_DOMAIN, r, "record_content_identity")
                and (
                    i == 0
                    or r.previous_record_content_identity
                    == head.records[i - 1].record_content_identity
                )
                for i, r in enumerate(head.records)
            )
            if chain_ok:
                statuses["record_chain_status"] = "passed"
            else:
                fail(
                    "AUTH.RECORD_CHAIN",
                    "record content identity or predecessor failed",
                    "record_chain_status",
                )
        if statuses["record_chain_status"] == "passed":
            head = snapshots[-1]
            records_by_id: dict[str, DevelopmentAuthorityRecord] = {}
            policies_by_identity: dict[str, DevelopmentAuthorityPolicy] = {}
            authorizations_by_id: dict[
                str,
                DevelopmentTaskAuthorization
                | DevelopmentReviewAuthorization
                | DevelopmentPromotionAuthorization,
            ] = {}
            authorizations_by_record_id: dict[
                str,
                DevelopmentTaskAuthorization
                | DevelopmentReviewAuthorization
                | DevelopmentPromotionAuthorization,
            ] = {}
            use_keys: set[tuple[str, str, str, str]] = set()
            used_authorizations: set[str] = set()
            revoked_records: set[str] = set()
            closure = True
            for index, record in enumerate(head.records):
                # Record and authorization identities are globally unique.
                if record.record_id in records_by_id:
                    closure = False
                if index == 0:
                    closure &= (
                        type(record) is DevelopmentAuthorityPolicy
                        and record.governing_policy_identity is None
                    )
                else:
                    closure &= record.governing_policy_identity in policies_by_identity
                if isinstance(
                    record,
                    (
                        DevelopmentTaskAuthorization,
                        DevelopmentReviewAuthorization,
                        DevelopmentPromotionAuthorization,
                    ),
                ):
                    if record.authorization_id in authorizations_by_id:
                        closure = False
                    authorizations_by_id[record.authorization_id] = record
                    authorizations_by_record_id[record.record_id] = record
                elif isinstance(record, DevelopmentAuthorizationUse):
                    grant = authorizations_by_id.get(record.authorization_id)
                    key = (
                        record.authorization_id,
                        record.operation_id,
                        record.attempt_id,
                        record.idempotency_id,
                    )
                    closure &= (
                        grant is not None
                        and key not in use_keys
                        and record.authorization_id not in used_authorizations
                        and grant.operation_binding.operation_id == record.operation_id
                        and grant.operation_binding.attempt_id == record.attempt_id
                        and grant.operation_binding.idempotency_id
                        == record.idempotency_id
                    )
                    use_keys.add(key)
                    used_authorizations.add(record.authorization_id)
                elif isinstance(record, DevelopmentAuthorizationRevocation):
                    target = authorizations_by_record_id.get(
                        record.target_authorization_record_id
                    )
                    replacement = (
                        authorizations_by_record_id.get(
                            record.replacement_authorization_record_id
                        )
                        if record.replacement_authorization_record_id is not None
                        else None
                    )
                    closure &= (
                        target is not None
                        and record.target_authorization_record_id not in revoked_records
                        and (
                            record.replacement_authorization_record_id is None
                            or (
                                replacement is not None
                                and type(replacement) is type(target)
                                and replacement.record_id != target.record_id
                            )
                        )
                    )
                    revoked_records.add(record.target_authorization_record_id)
                records_by_id[record.record_id] = record
                if type(record) is DevelopmentAuthorityPolicy:
                    policies_by_identity[record.record_content_identity] = record
            closure &= (
                head.governing_policy_identity in policies_by_identity
                and head.records[0].record_content_identity in policies_by_identity
            )
            if closure:
                statuses["reference_closure_status"] = "passed"
            else:
                fail(
                    "AUTH.REFERENCE_CLOSURE",
                    "ledger genesis, policy, authorization, use, or revocation "
                    "closure failed",
                    "reference_closure_status",
                )
        if (
            statuses["reference_closure_status"] == "passed"
            and statuses["issuer_policy_status"] == "passed"
        ):
            if (
                observed
                == configuration.accepted_head_artifact_identity
                == source.expected_head_artifact_identity
                and snapshots[-1].snapshot_sequence
                >= configuration.minimum_snapshot_sequence
            ):
                statuses["accepted_head_status"] = "passed"
            else:
                fail(
                    "AUTH.ACCEPTED_HEAD",
                    "head identity or minimum sequence mismatch",
                    "accepted_head_status",
                )
        # Statuses skipped because an earlier gate failed remain not_reached.
        diagnostics_tuple = tuple(
            sorted(
                diagnostics, key=lambda d: (d.code, d.subject_identity or "", d.detail)
            )
        )
        receipt_body: dict[str, object] = {
            "schema_version": 1,
            "receipt_identity": None,
            "source_descriptor_identity": source.source_descriptor_identity,
            "mode": source.mode,
            "trust_configuration_pin_identity": pin.pin_identity,
            "trust_configuration_identity": configuration.configuration_identity,
            "trust_configuration_revision": configuration.configuration_revision,
            "requested_head_artifact_identity": source.expected_head_artifact_identity,
            "observed_head_artifact_identity": observed,
            "head_payload_identity": head_payload,
            "head_snapshot_sequence": sequence,
            "verified_snapshot_count": len(envelopes)
            if statuses["signature_status"] == "passed"
            else 0,
            "canonicalization_version": _CANONICALIZATION,
            "resolver_version": self.version,
            **statuses,
            "verified_key_ids": tuple(
                sorted(verified_keys_by_envelope[-1])
                if statuses["signature_status"] == "passed"
                else ()
            ),
            "diagnostics": diagnostics_tuple,
        }
        receipt_body["receipt_identity"] = identity_from_fields(
            _RECEIPT_DOMAIN, receipt_body
        )
        receipt = DevelopmentAuthorityReconstructionReceipt(**cast(Any, receipt_body))
        if all(statuses[name] == "passed" for name in _STATUS_FIELDS):
            head = snapshots[-1]
            context_body: dict[str, object] = {
                "schema_version": 1,
                "context_identity": None,
                "trust_configuration_pin_identity": pin.pin_identity,
                "trust_configuration_identity": configuration.configuration_identity,
                "trust_configuration_revision": configuration.configuration_revision,
                "source_descriptor_identity": source.source_descriptor_identity,
                "head_artifact_identity": observed,
                "head_payload_identity": head_payload,
                "ledger_id": head.ledger_id,
                "snapshot_sequence": head.snapshot_sequence,
                "predecessor_payload_identity": head.predecessor_payload_identity,
                "first_record_ordinal": head.first_record_ordinal,
                "last_record_ordinal": head.last_record_ordinal,
                "record_head_identity": head.records[-1].record_content_identity,
                "governing_policy_identity": head.governing_policy_identity,
                "receipt_identity": receipt.receipt_identity,
                "records": head.records,
                "resolver_version": self.version,
            }
            context_body["context_identity"] = identity_from_fields(
                _CONTEXT_DOMAIN, context_body
            )
            context = DevelopmentAuthorityContext(**cast(Any, context_body))
            return DevelopmentAuthorityContextResolutionResult(
                1, "resolved", receipt, context
            )
        return DevelopmentAuthorityContextResolutionResult(1, "failed", receipt, None)
