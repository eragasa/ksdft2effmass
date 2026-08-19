"""Immutable development decisions and lossless legacy checkpoint adaptation.

The records preserve external human input and source provenance.  They grant no
operation authority.  Serialization uses the dependency-free canonical Harness JSON
profile; adaptation consumes exact legacy bytes and never rewrites the source.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

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


def _require_declared_path(value: object, name: str) -> str:
    """Validate one preserved legacy file or directory declaration."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    candidate = value[:-1] if value.endswith("/") else value
    require_path(candidate, name)
    return value


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
    declared_authoritative_paths: tuple[str, ...]
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
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
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
            self.declared_authoritative_paths, "declared_authoritative_paths"
        )
        for value in declared:
            _require_declared_path(value, "declared_authoritative_paths item")
        records = require_tuple(self.record_paths, "record_paths")
        for value in records:
            require_path(value, "record_paths item")
        for name, values in (
            ("declared_authoritative_paths", declared),
            ("record_paths", records),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{name} must be unique")
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
        """Return canonical version-1 bytes for ``decision``."""
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
        adapter_version: str = "legacy-checkpoint-v1",
    ) -> DevelopmentDecision:
        """Losslessly map exact legacy checkpoint bytes to a successor value.

        ``decision_id`` is explicit migration-manifest input.  The method copies all
        legacy fields and records exact-byte identity without interpreting response
        text or treating historical scope as authorization.
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
        state = "resolved" if status == "resolved" else "unresolved"
        if state == "unresolved" and response is not None:
            raise ValueError("non-resolved legacy status with response is ambiguous")
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
        paths = source["authoritative_files"]
        records = source["record_paths"]
        if type(paths) is not list or type(records) is not list:
            raise TypeError("legacy path fields must be JSON arrays")
        return DevelopmentDecision(
            1,
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
            tuple(paths),
            None,
            "unavailable_legacy",
            None,
            response if state == "resolved" else None,
            source["normalized_decision"] if state == "resolved" else None,
            selected,
            source["resolved_at"] if state == "resolved" else None,
            source["authorized_scope"] if state == "resolved" else None,
            tuple(records),
            source["resumption_status"],
            predecessor_decision_id,
            predecessor_decision_id,
            provenance,
        )

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
        for name in ("declared_authoritative_paths", "record_paths"):
            if type(data[name]) is not list:
                raise TypeError(f"{name} must be a JSON array")
            data[name] = tuple(data[name])
        provenance_fields = {
            field.name for field in fields(DevelopmentDecisionSourceProvenance)
        }
        data["source_provenance"] = DevelopmentDecisionSourceProvenance(
            **closed(data["source_provenance"], provenance_fields, "source provenance")
        )
        return DevelopmentDecision(**data)
