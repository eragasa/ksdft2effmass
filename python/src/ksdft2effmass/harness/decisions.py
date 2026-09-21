"""Immutable development decisions and explicit legacy checkpoint adaptation.

The records preserve external human input and source provenance. They grant no
operation authority. Serialization uses the dependency-free canonical Harness JSON
profile. Legacy adaptation preserves decision meaning but may normalize or omit path
metadata that the canonical contract cannot represent.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from urllib.parse import urlsplit

from ._contract import (
    canonical_bytes,
    closed,
    require_digest,
    require_identifier,
    require_path,
    require_str,
    require_timestamp,
    require_tuple,
    require_uint64,
    sha256,
    strict_json,
)


@dataclass(frozen=True, slots=True)
class DevelopmentDecisionOption:
    """One offered development-decision option in preserved source order."""

    option_id: str
    summary: str
    consequence: str | None

    def __post_init__(self) -> None:
        require_identifier(self.option_id, "option_id")
        require_str(self.summary, "summary")
        if self.consequence is not None:
            require_str(self.consequence, "consequence")


@dataclass(frozen=True, slots=True)
class DevelopmentDecisionSourceProvenance:
    """Identity and exact-byte provenance of one decision source artifact."""

    schema_version: int
    source_family: str
    source_schema_version: str
    source_artifact_identity: str
    source_path: str
    source_byte_count: int
    adapter_version: str
    legacy_checkpoint_id: str | None
    legacy_status: str | None

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        if self.source_family not in {"legacy_checkpoint", "development_decision"}:
            raise ValueError("source_family is not supported")
        require_identifier(self.source_schema_version, "source_schema_version")
        require_digest(self.source_artifact_identity, "source_artifact_identity")
        require_path(self.source_path, "source_path")
        require_uint64(self.source_byte_count, "source_byte_count")
        require_identifier(self.adapter_version, "adapter_version")
        if self.source_family == "legacy_checkpoint":
            require_identifier(self.legacy_checkpoint_id, "legacy_checkpoint_id")
            require_identifier(self.legacy_status, "legacy_status")
        elif self.legacy_checkpoint_id is not None or self.legacy_status is not None:
            raise ValueError("native provenance requires null legacy fields")


@dataclass(frozen=True, slots=True)
class DevelopmentDecisionAuthoritativeReference:
    """One exact authoritative path or HTTPS URI declaration.

    Parameters
    ----------
    reference_kind
        ``"resource_path"`` for a repository-relative file or legacy directory
        declaration, or ``"https_uri"`` for an absolute HTTPS URI.
    value
        Exact declaration. Resource directory declarations may retain one trailing
        slash. HTTPS URI text is preserved without normalization.
    """

    reference_kind: str
    value: str

    def __post_init__(self) -> None:
        if self.reference_kind == "resource_path":
            candidate = self.value[:-1] if self.value.endswith("/") else self.value
            require_path(candidate, "authoritative reference value")
        elif self.reference_kind == "https_uri":
            require_str(self.value, "authoritative reference value")
            parsed = urlsplit(self.value)
            if (
                parsed.scheme != "https"
                or not parsed.netloc
                or parsed.username is not None
                or parsed.password is not None
                or any(
                    character.isspace()
                    or ord(character) < 32
                    or 127 <= ord(character) <= 159
                    for character in self.value
                )
                or "\\" in self.value
            ):
                raise ValueError("https_uri value must be an absolute HTTPS URI")
            try:
                _port = parsed.port
            except ValueError as error:
                raise ValueError("https_uri value contains an invalid port") from error
        else:
            raise ValueError("reference_kind is not supported")


@dataclass(frozen=True, slots=True)
class DevelopmentDecision:
    """Represent one immutable unresolved or resolved development decision.

    All optional wire fields remain explicit.  Successor records identify the same
    predecessor through both predecessor fields.  Legacy values retain unavailable
    authority identity rather than inventing authority facts.
    """

    schema_version: int
    decision_id: str
    state: str
    decision_class: str | None
    task_id: str | None
    episode_id: str | None
    created_at: str | None
    question: str | None
    options: tuple[DevelopmentDecisionOption, ...]
    recommendation: str | None
    blocked_scope: str | None
    safe_scope: str | None
    declared_authoritative_references: tuple[
        DevelopmentDecisionAuthoritativeReference, ...
    ]
    response_source_identity: str | None
    authority_identity_status: str
    authority_identity: str | None
    response: str | None
    normalized_outcome: str | None
    selected_option_id: str | None
    resolved_at: str | None
    declared_scope: str | None
    record_paths: tuple[str, ...]
    resumption_status: str | None
    predecessor_decision_id: str | None
    supersedes_decision_id: str | None
    source_provenance: DevelopmentDecisionSourceProvenance

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 2:
            raise ValueError("schema_version must equal 2")
        require_identifier(self.decision_id, "decision_id")
        if self.state not in {"unresolved", "resolved"}:
            raise ValueError("state must be unresolved or resolved")
        for name in ("decision_class", "task_id", "episode_id"):
            value = getattr(self, name)
            if value is not None:
                require_identifier(value, name)
        for name in ("created_at", "resolved_at"):
            value = getattr(self, name)
            if value is not None:
                require_timestamp(value, name)
        for name in (
            "question",
            "recommendation",
            "blocked_scope",
            "safe_scope",
            "response",
            "normalized_outcome",
            "declared_scope",
            "resumption_status",
        ):
            value = getattr(self, name)
            if value is not None:
                require_str(value, name)
        require_tuple(self.options, "options", nonempty=True)
        if any(
            type(option) is not DevelopmentDecisionOption for option in self.options
        ):
            raise TypeError("options must contain DevelopmentDecisionOption")
        option_ids = tuple(option.option_id for option in self.options)
        if len(option_ids) != len(set(option_ids)):
            raise ValueError("option IDs must be unique")
        declared = require_tuple(
            self.declared_authoritative_references,
            "declared_authoritative_references",
        )
        if any(
            type(value) is not DevelopmentDecisionAuthoritativeReference
            for value in declared
        ):
            raise TypeError(
                "declared_authoritative_references must contain "
                "DevelopmentDecisionAuthoritativeReference"
            )
        if len(declared) != len(set(declared)):
            raise ValueError("declared_authoritative_references must be unique")
        records = require_tuple(self.record_paths, "record_paths")
        for value in records:
            require_path(value, "record_paths item")
        if len(records) != len(set(records)):
            raise ValueError("record_paths must be unique")
        if self.authority_identity_status not in {"available", "unavailable_legacy"}:
            raise ValueError("authority_identity_status is not supported")
        if self.authority_identity_status == "available":
            require_identifier(
                self.response_source_identity, "response_source_identity"
            )
            require_identifier(self.authority_identity, "authority_identity")
        elif (
            self.response_source_identity is not None
            or self.authority_identity is not None
        ):
            raise ValueError(
                "unavailable legacy identity requires both identities null"
            )
        if self.state == "unresolved":
            inactive = (
                self.response,
                self.normalized_outcome,
                self.selected_option_id,
                self.resolved_at,
                self.declared_scope,
            )
            if any(value is not None for value in inactive):
                raise ValueError("unresolved decision resolution fields must be null")
        else:
            for name in (
                "response",
                "normalized_outcome",
                "resolved_at",
                "declared_scope",
            ):
                if getattr(self, name) is None:
                    raise ValueError(f"resolved decision requires {name}")
        if (
            self.selected_option_id is not None
            and self.selected_option_id not in option_ids
        ):
            raise ValueError("selected_option_id must name an offered option")
        predecessors = (self.predecessor_decision_id, self.supersedes_decision_id)
        if (predecessors[0] is None) != (predecessors[1] is None) or (
            predecessors[0] is not None and predecessors[0] != predecessors[1]
        ):
            raise ValueError(
                "predecessor and supersedes identities must be null or equal"
            )
        if predecessors[0] == self.decision_id:
            raise ValueError("a decision may not supersede itself")
        if type(self.source_provenance) is not DevelopmentDecisionSourceProvenance:
            raise TypeError(
                "source_provenance must be DevelopmentDecisionSourceProvenance"
            )
        expected_status = (
            "unavailable_legacy"
            if self.source_provenance.source_family == "legacy_checkpoint"
            else "available"
        )
        if self.authority_identity_status != expected_status:
            raise ValueError("authority identity status must agree with source family")


class DevelopmentDecisionSerializer:
    """Serialize, deserialize, and one-way adapt the exact decision wire contract."""

    __slots__ = ()

    def execute(self, decision: DevelopmentDecision) -> bytes:
        """Return canonical version-2 bytes for ``decision``."""
        if type(decision) is not DevelopmentDecision:
            raise TypeError("decision must be DevelopmentDecision")
        return canonical_bytes(decision)

    serialize = execute

    def deserialize(self, payload: bytes) -> DevelopmentDecision:
        """Decode canonical decision bytes, rejecting all noncanonical payloads."""
        value = strict_json(payload)
        result = self._from_wire(value)
        if canonical_bytes(result) != payload:
            raise ValueError("decision payload is not canonical Harness JSON")
        return result

    def adapt_legacy(
        self,
        payload: bytes,
        *,
        decision_id: str,
        source_path: str,
        predecessor_decision_id: str | None = None,
        adapter_version: str = "legacy-checkpoint-v2-lossy",
    ) -> DevelopmentDecision:
        """Map exact legacy checkpoint bytes to a canonical successor value.

        ``decision_id`` is explicit migration-manifest input. Decision fields,
        repository-relative authority declarations, and HTTPS references are retained
        without treating historical scope as authorization. Repository directory
        record paths lose a trailing slash. Absolute external authority and record
        paths are omitted because canonical paths represent repository-relative
        resources only. Exact source hash and byte count remain in provenance; source
        bytes are not embedded.
        """
        require_identifier(decision_id, "decision_id")
        require_path(source_path, "source_path")
        value = strict_json(payload)
        keys = {
            "checkpoint_id",
            "task_id",
            "episode_id",
            "status",
            "decision_class",
            "created_at",
            "question",
            "options",
            "recommendation",
            "blocked_scope",
            "safe_scope",
            "authoritative_files",
            "human_response",
            "normalized_decision",
            "resolved_at",
            "authorized_scope",
            "record_paths",
            "resumption_status",
        }
        source = closed(value, keys, "legacy checkpoint")
        status = source["status"]
        require_identifier(status, "status")
        response = source["human_response"]
        state = "resolved" if response is not None else "unresolved"
        options_value = source["options"]
        if type(options_value) is not list:
            raise TypeError("options must be a JSON array")
        for option in options_value:
            closed(option, {"id", "summary", "consequence"}, "legacy option")
        options = tuple(
            DevelopmentDecisionOption(
                option["id"], option["summary"], option["consequence"]
            )
            for option in options_value
        )
        # Legacy normalized text is not separate evidence that one offered option was
        # selected. Preserve it verbatim but do not infer a selected option identity.
        selected = None
        provenance = DevelopmentDecisionSourceProvenance(
            1,
            "legacy_checkpoint",
            "1",
            sha256(payload),
            source_path,
            len(payload),
            adapter_version,
            source["checkpoint_id"],
            status,
        )
        references = source["authoritative_files"]
        records = source["record_paths"]
        if type(references) is not list or type(records) is not list:
            raise TypeError("legacy path fields must be JSON arrays")
        declared_references = self._adapt_authoritative_references(references)
        return DevelopmentDecision(
            2,
            decision_id,
            state,
            source["decision_class"],
            source["task_id"],
            source["episode_id"],
            source["created_at"],
            source["question"],
            options,
            source["recommendation"],
            source["blocked_scope"],
            source["safe_scope"],
            declared_references,
            None,
            "unavailable_legacy",
            None,
            response if state == "resolved" else None,
            source["normalized_decision"] if state == "resolved" else None,
            selected,
            source["resolved_at"] if state == "resolved" else None,
            source["authorized_scope"] if state == "resolved" else None,
            self._adapt_record_paths(records),
            source["resumption_status"],
            predecessor_decision_id,
            predecessor_decision_id,
            provenance,
        )

    @staticmethod
    def _adapt_authoritative_references(
        values: list[object],
    ) -> tuple[DevelopmentDecisionAuthoritativeReference, ...]:
        """Retain canonical repository paths and HTTPS references in source order."""
        retained: list[DevelopmentDecisionAuthoritativeReference] = []
        for value in values:
            if type(value) is not str:
                raise TypeError(
                    "legacy authoritative_files must contain built-in strings"
                )
            if value.startswith("/"):
                continue
            reference = DevelopmentDecisionAuthoritativeReference(
                "https_uri" if value.startswith("https://") else "resource_path",
                value,
            )
            if reference not in retained:
                retained.append(reference)
        return tuple(retained)

    @staticmethod
    def _adapt_record_paths(values: list[object]) -> tuple[str, ...]:
        """Apply the declared lossy policy to legacy record-path metadata."""
        retained: list[str] = []
        for value in values:
            if type(value) is not str:
                raise TypeError("legacy record_paths must contain built-in strings")
            if value.startswith("/"):
                continue
            candidate = value[:-1] if value.endswith("/") else value
            require_path(candidate, "legacy record_paths item")
            if candidate not in retained:
                retained.append(candidate)
        return tuple(retained)

    @staticmethod
    def _from_wire(value: object) -> DevelopmentDecision:
        expected = {field.name for field in fields(DevelopmentDecision)}
        data = closed(value, expected, "development decision")
        options = data["options"]
        if type(options) is not list:
            raise TypeError("options must be a JSON array")
        option_fields = {field.name for field in fields(DevelopmentDecisionOption)}
        data["options"] = tuple(
            DevelopmentDecisionOption(**closed(item, option_fields, "decision option"))
            for item in options
        )
        references = data["declared_authoritative_references"]
        if type(references) is not list:
            raise TypeError("declared_authoritative_references must be a JSON array")
        reference_fields = {
            field.name for field in fields(DevelopmentDecisionAuthoritativeReference)
        }
        data["declared_authoritative_references"] = tuple(
            DevelopmentDecisionAuthoritativeReference(
                **closed(item, reference_fields, "authoritative reference")
            )
            for item in references
        )
        if type(data["record_paths"]) is not list:
            raise TypeError("record_paths must be a JSON array")
        data["record_paths"] = tuple(data["record_paths"])
        provenance_fields = {
            field.name for field in fields(DevelopmentDecisionSourceProvenance)
        }
        data["source_provenance"] = DevelopmentDecisionSourceProvenance(
            **closed(data["source_provenance"], provenance_fields, "source provenance")
        )
        return DevelopmentDecision(**data)
