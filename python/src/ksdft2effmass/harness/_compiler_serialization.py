"""Strict canonical serialization owned by the development-harness compiler.

The serializer converts only the compiler's closed nominal records into a closed
recursive JSON representation. It does not inspect arbitrary dataclasses, mappings,
or software objects and performs no parsing, I/O, persistence, or validation.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .decisions import (
    DevelopmentDecision,
    DevelopmentDecisionOption,
    DevelopmentDecisionSourceProvenance,
)
from .pi import (
    ArtifactIdentity,
    PiHarnessAgentDefinition,
    ResourceManifest,
    ResourceReference,
    SkillDescriptor,
)
from .pi.conformance.python import PythonModuleSource
from .task import ArchivedTaskSource, HarnessTask
from .task_selection import DevelopmentTaskSelection

if TYPE_CHECKING:
    from .compiler import (
        HarnessCapabilityCatalog,
        HarnessEvidenceCatalog,
        HarnessParsedValue,
        HarnessResourceCatalog,
        HarnessSourceContract,
        HarnessSourceIdentity,
        HarnessSourceRecord,
        HarnessSourceSnapshot,
        HarnessState,
    )
    from .task import HarnessTaskRegistry


@dataclass(frozen=True, slots=True)
class _JsonArray:
    values: tuple[_JsonValue, ...]


@dataclass(frozen=True, slots=True)
class _JsonMember:
    name: str
    value: _JsonValue


@dataclass(frozen=True, slots=True)
class _JsonObject:
    members: tuple[_JsonMember, ...]


type _JsonValue = None | bool | int | str | _JsonArray | _JsonObject


class _CanonicalJsonSerializer:
    """Encode the closed compiler JSON representation to canonical UTF-8 bytes."""

    __slots__ = ()

    def execute(self, value: _JsonValue) -> bytes:
        """Return NFC, key-sorted, insignificant-whitespace-free JSON bytes."""
        return self._encode(value).encode("utf-8")

    def _encode(self, value: _JsonValue) -> str:
        if value is None:
            return "null"
        if type(value) is bool:
            return "true" if value else "false"
        if type(value) is int:
            return str(value)
        if type(value) is str:
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError("canonical JSON strings must use NFC")
            return json.dumps(
                value, ensure_ascii=False, allow_nan=False, separators=(",", ":")
            )
        if type(value) is _JsonArray:
            return "[" + ",".join(self._encode(item) for item in value.values) + "]"
        if not isinstance(value, _JsonObject):
            raise TypeError("value is outside the closed JSON representation")
        members = tuple(
            sorted(value.members, key=lambda member: member.name.encode("utf-8"))
        )
        names = tuple(member.name for member in members)
        if len(names) != len(set(names)):
            raise ValueError("canonical JSON object member names must be unique")
        return (
            "{"
            + ",".join(
                self._encode(member.name) + ":" + self._encode(member.value)
                for member in members
            )
            + "}"
        )


class _HarnessCompilerSerializer:
    """Serialize exact compiler contracts and semantic values without type erasure."""

    __slots__ = ()

    def source_contract_identity(self, contract: HarnessSourceContract) -> str:
        """Return the domain-separated identity of one exact source contract."""
        families = _JsonArray(
            tuple(
                self._object(
                    ("family", item.family.value),
                    (
                        "catalog_roots",
                        self._strings(
                            tuple(root.as_posix() for root in item.catalog_roots)
                        ),
                    ),
                    (
                        "source_paths",
                        self._strings(
                            tuple(path.as_posix() for path in item.source_paths)
                        ),
                    ),
                    ("format_version", item.format_version),
                    ("minimum_count", item.minimum_count),
                )
                for item in contract.families
            )
        )
        bindings = _JsonArray(
            tuple(
                self._object(
                    ("source_path", item.source_path.as_posix()),
                    ("decision_id", item.decision_id),
                    ("predecessor_decision_id", item.predecessor_decision_id),
                    ("adapter_version", item.adapter_version),
                )
                for item in contract.legacy_decision_bindings
            )
        )
        payload = self._bytes(
            self._object(
                ("schema_version", contract.schema_version),
                ("families", families),
                ("symlink_policy", contract.symlink_policy),
                ("legacy_decision_bindings", bindings),
            )
        )
        return self._identity("ksdft2effmass.harness.source-contract.v1", payload)

    def source_snapshot_identity(
        self,
        source_contract_identity: str,
        records: tuple[HarnessSourceRecord, ...],
    ) -> str:
        """Return the domain-separated identity of one closed source observation."""
        payload = self._bytes(
            self._object(
                ("schema_version", 1),
                ("source_contract_identity", source_contract_identity),
                (
                    "records",
                    _JsonArray(tuple(self._source_record(item) for item in records)),
                ),
            )
        )
        return self._identity("ksdft2effmass.harness.source-snapshot.v1", payload)

    def capability_catalog_identity(
        self,
        model_version: int,
        normalization_version: str,
        capabilities: tuple[SkillDescriptor, ...],
        agent_definitions: tuple[PiHarnessAgentDefinition, ...],
    ) -> str:
        """Return the semantic identity of one capability catalog."""
        payload = self._bytes(
            self._object(
                ("model_version", model_version),
                ("normalization_version", normalization_version),
                (
                    "capabilities",
                    _JsonArray(tuple(self._skill(value) for value in capabilities)),
                ),
                (
                    "agent_definitions",
                    _JsonArray(
                        tuple(self._agent(value) for value in agent_definitions)
                    ),
                ),
            )
        )
        return self._identity("ksdft2effmass.harness.capability-catalog.v1", payload)

    def resource_catalog_identity(
        self,
        model_version: int,
        normalization_version: str,
        resources: tuple[ResourceManifest, ...],
    ) -> str:
        """Return the semantic identity of one resource catalog."""
        payload = self._bytes(
            self._object(
                ("model_version", model_version),
                ("normalization_version", normalization_version),
                (
                    "resources",
                    _JsonArray(
                        tuple(self._resource_manifest(value) for value in resources)
                    ),
                ),
            )
        )
        return self._identity("ksdft2effmass.harness.resource-catalog.v1", payload)

    def evidence_catalog_identity(
        self,
        model_version: int,
        normalization_version: str,
        evidence: tuple[PythonModuleSource, ...],
        source_identities: tuple[HarnessSourceIdentity, ...],
    ) -> str:
        """Return identity of exact Python source paths, bytes, and identities."""
        payload = self._bytes(
            self._object(
                ("model_version", model_version),
                ("normalization_version", normalization_version),
                (
                    "sources",
                    _JsonArray(
                        tuple(
                            self._evidence(value, identity)
                            for value, identity in zip(
                                evidence, source_identities, strict=True
                            )
                        )
                    ),
                ),
            )
        )
        return self._identity("ksdft2effmass.harness.evidence-catalog.v1", payload)

    def state_identity(self, state: HarnessState) -> str:
        """Return the semantic identity of one complete selected source state."""
        return self.state_identity_components(
            state.identity.model_version,
            state.normalization_version,
            state.tasks,
            state.selection,
            state.decisions,
            state.capabilities,
            state.resources,
            state.evidence,
        )

    def state_identity_components(
        self,
        model_version: int,
        normalization_version: str,
        tasks: HarnessTaskRegistry,
        selection: DevelopmentTaskSelection,
        decisions: tuple[DevelopmentDecision, ...],
        capabilities: HarnessCapabilityCatalog,
        resources: HarnessResourceCatalog,
        evidence: HarnessEvidenceCatalog,
    ) -> str:
        """Return state identity from exact normalized semantic components."""
        payload = self._bytes(
            self._object(
                ("model_version", model_version),
                ("normalization_version", normalization_version),
                (
                    "tasks",
                    _JsonArray(tuple(self._task(value) for value in tasks.tasks)),
                ),
                ("selection", self._selection(selection)),
                (
                    "decisions",
                    _JsonArray(tuple(self._decision(value) for value in decisions)),
                ),
                ("capabilities", self._capability_catalog(capabilities)),
                ("resources", self._resource_catalog(resources)),
                ("evidence", self._evidence_catalog(evidence)),
            )
        )
        return self._identity("ksdft2effmass.harness.state.v1", payload)

    def snapshot_is_consistent(self, snapshot: HarnessSourceSnapshot) -> bool:
        """Return whether a snapshot's derived identity agrees with its exact fields."""
        return snapshot.snapshot_identity == self.source_snapshot_identity(
            snapshot.source_contract_identity, snapshot.records
        )

    def _capability_catalog(self, catalog: HarnessCapabilityCatalog) -> _JsonObject:
        return self._object(
            ("model_version", catalog.model_version),
            ("normalization_version", catalog.normalization_version),
            (
                "capabilities",
                _JsonArray(tuple(self._skill(value) for value in catalog.capabilities)),
            ),
            (
                "agent_definitions",
                _JsonArray(
                    tuple(self._agent(value) for value in catalog.agent_definitions)
                ),
            ),
        )

    def _resource_catalog(self, catalog: HarnessResourceCatalog) -> _JsonObject:
        return self._object(
            ("model_version", catalog.model_version),
            ("normalization_version", catalog.normalization_version),
            (
                "resources",
                _JsonArray(
                    tuple(self._resource_manifest(value) for value in catalog.resources)
                ),
            ),
        )

    def _evidence_catalog(self, catalog: HarnessEvidenceCatalog) -> _JsonObject:
        return self._object(
            ("model_version", catalog.model_version),
            ("normalization_version", catalog.normalization_version),
            (
                "sources",
                _JsonArray(
                    tuple(
                        self._evidence(value, identity)
                        for value, identity in zip(
                            catalog.evidence, catalog.source_identities, strict=True
                        )
                    )
                ),
            ),
        )

    def _source_identity(self, value: HarnessSourceIdentity) -> _JsonObject:
        return self._object(
            ("family", value.family.value),
            ("relative_path", value.relative_path.as_posix()),
            ("format_version", value.format_version),
            ("sha256", value.sha256),
            ("byte_count", value.byte_count),
        )

    def _source_record(self, record: HarnessSourceRecord) -> _JsonObject:
        return self._object(
            ("identity", self._source_identity(record.identity)),
            ("value", self._source_value(record.value, record.identity)),
        )

    def _source_value(
        self, value: HarnessParsedValue, identity: HarnessSourceIdentity
    ) -> _JsonObject:
        if type(value) is HarnessTask:
            return self._typed_value("task", self._task(value))
        if type(value) is DevelopmentTaskSelection:
            return self._typed_value("task_selection", self._selection(value))
        if type(value) is DevelopmentDecision:
            return self._typed_value("development_decision", self._decision(value))
        if type(value) is SkillDescriptor:
            return self._typed_value("capability", self._skill(value))
        if type(value) is ResourceManifest:
            return self._typed_value("resource", self._resource_manifest(value))
        if type(value) is PiHarnessAgentDefinition:
            return self._typed_value("agent_definition", self._source_agent(value))
        if type(value) is PythonModuleSource:
            return self._typed_value("evidence", self._evidence(value, identity))
        raise TypeError("source record contains an unsupported parsed value")

    def _typed_value(self, kind: str, value: _JsonObject) -> _JsonObject:
        return self._object(("kind", kind), ("value", value))

    def _task(self, value: HarnessTask) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("task_id", value.task_id),
            ("title", value.title),
            ("status", value.status),
            ("status_detail", value.status_detail),
            ("parent_task_id", value.parent_task_id),
            ("task_prerequisite_ids", self._strings(value.task_prerequisite_ids)),
            (
                "external_prerequisite_ids",
                self._strings(value.external_prerequisite_ids),
            ),
            ("superseded_by_task_ids", self._strings(value.superseded_by_task_ids)),
            ("explicit_activation_required", value.explicit_activation_required),
            ("objective", value.objective),
            (
                "authority_reference_paths",
                self._strings(value.authority_reference_paths),
            ),
            ("authorized_scope", self._strings(value.authorized_scope)),
            ("completion_criteria", self._strings(value.completion_criteria)),
            ("exclusions", self._strings(value.exclusions)),
            ("intake_path", value.intake_path),
            ("archived_source", self._archived_task_source(value.archived_source)),
            ("documentation_path", value.documentation_path),
        )

    def _archived_task_source(
        self, value: ArchivedTaskSource | None
    ) -> _JsonObject | None:
        if value is None:
            return None
        return self._object(("path", value.path), ("sha256", value.sha256))

    def _selection(self, value: DevelopmentTaskSelection) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("active_task_id", value.active_task_id),
            (
                "explicit_activation_receipt_ids",
                self._strings(value.explicit_activation_receipt_ids),
            ),
            ("automatic_successor_activation", value.automatic_successor_activation),
        )

    def _decision(self, value: DevelopmentDecision) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("decision_id", value.decision_id),
            ("state", value.state),
            ("decision_class", value.decision_class),
            ("task_id", value.task_id),
            ("episode_id", value.episode_id),
            ("created_at", value.created_at),
            ("question", value.question),
            (
                "options",
                _JsonArray(
                    tuple(self._decision_option(item) for item in value.options)
                ),
            ),
            ("recommendation", value.recommendation),
            ("blocked_scope", value.blocked_scope),
            ("safe_scope", value.safe_scope),
            (
                "declared_authoritative_paths",
                self._strings(value.declared_authoritative_paths),
            ),
            ("response_source_identity", value.response_source_identity),
            ("authority_identity_status", value.authority_identity_status),
            ("authority_identity", value.authority_identity),
            ("response", value.response),
            ("normalized_outcome", value.normalized_outcome),
            ("selected_option_id", value.selected_option_id),
            ("resolved_at", value.resolved_at),
            ("declared_scope", value.declared_scope),
            ("record_paths", self._strings(value.record_paths)),
            ("resumption_status", value.resumption_status),
            ("predecessor_decision_id", value.predecessor_decision_id),
            ("supersedes_decision_id", value.supersedes_decision_id),
            (
                "source_provenance",
                self._decision_source_provenance(value.source_provenance),
            ),
        )

    def _decision_source_provenance(
        self, value: DevelopmentDecisionSourceProvenance
    ) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("source_family", value.source_family),
            ("source_schema_version", value.source_schema_version),
            ("source_artifact_identity", value.source_artifact_identity),
            ("source_path", value.source_path),
            ("source_byte_count", value.source_byte_count),
            ("adapter_version", value.adapter_version),
            ("legacy_checkpoint_id", value.legacy_checkpoint_id),
            ("legacy_status", value.legacy_status),
        )

    def _decision_option(self, value: DevelopmentDecisionOption) -> _JsonObject:
        return self._object(
            ("option_id", value.option_id),
            ("summary", value.summary),
            ("consequence", value.consequence),
        )

    def _skill(self, value: SkillDescriptor) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("skill_id", value.skill_id),
            ("behavior_version", value.behavior_version),
            ("entry_resource_id", value.entry_resource_id),
            ("trigger_capability_ids", self._strings(value.trigger_capability_ids)),
            ("required_resource_ids", self._strings(value.required_resource_ids)),
            ("side_effect_class", value.side_effect_class),
            ("authorization_policy_id", value.authorization_policy_id),
            ("retry_policy", value.retry_policy),
            ("termination_policy", value.termination_policy),
        )

    def _artifact_identity(self, value: ArtifactIdentity) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("algorithm", value.algorithm),
            ("digest", value.digest),
        )

    def _resource_reference(self, value: ResourceReference) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("resource_id", value.resource_id),
            ("resource_kind", value.resource_kind),
            ("format_version", value.format_version),
            ("path", value.path),
            ("content_identity", self._artifact_identity(value.content_identity)),
            ("dependency_ids", self._strings(value.dependency_ids)),
        )

    def _resource_manifest(self, value: ResourceManifest) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("manifest_id", value.manifest_id),
            ("manifest_version", value.manifest_version),
            ("layer", value.layer),
            ("extends_manifest_id", value.extends_manifest_id),
            (
                "resources",
                _JsonArray(
                    tuple(self._resource_reference(item) for item in value.resources)
                ),
            ),
        )

    def _agent(self, value: PiHarnessAgentDefinition) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("name", value.name),
            ("package", value.package),
            ("runtime_name", value.runtime_name),
            ("acceptance_role", value.acceptance_role),
            ("selected_skills", self._strings(value.selected_skills)),
            ("enabled", value.enabled),
        )

    def _source_agent(self, value: PiHarnessAgentDefinition) -> _JsonObject:
        return self._object(
            ("schema_version", value.schema_version),
            ("name", value.name),
            ("package", value.package),
            ("runtime_name", value.runtime_name),
            ("source_path", value.source_path),
            ("source_identity", self._artifact_identity(value.source_identity)),
            ("acceptance_role", value.acceptance_role),
            ("selected_skills", self._strings(value.selected_skills)),
            ("enabled", value.enabled),
        )

    def _evidence(
        self, value: PythonModuleSource, identity: HarnessSourceIdentity
    ) -> _JsonObject:
        if value.payload is None:
            raise ValueError("loaded evidence source requires exact payload bytes")
        return self._object(
            ("path", value.path),
            ("payload_hex", value.payload.hex()),
            ("source_identity", self._source_identity(identity)),
        )

    @staticmethod
    def _strings(values: tuple[str, ...]) -> _JsonArray:
        return _JsonArray(values)

    @staticmethod
    def _object(*members: tuple[str, _JsonValue]) -> _JsonObject:
        return _JsonObject(tuple(_JsonMember(name, value) for name, value in members))

    @staticmethod
    def _identity(domain: str, payload: bytes) -> str:
        framed = (
            domain.encode("ascii") + b"\x00" + len(payload).to_bytes(8, "big") + payload
        )
        return hashlib.sha256(framed).hexdigest()

    @staticmethod
    def _bytes(value: _JsonValue) -> bytes:
        return _CanonicalJsonSerializer().execute(value)
