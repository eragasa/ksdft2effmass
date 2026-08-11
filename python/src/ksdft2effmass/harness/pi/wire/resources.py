"""Explicit field mappings for resource and profile wire records."""

from __future__ import annotations

from typing import Any, cast

from .human_review import _ReviewOwnershipWireSerializer
from .records import _CommonWireRecordSerializer, _WireValueDecoder


class _ResourceWireSerializer:
    """Own explicit resource and project-profile wire mappings."""

    __slots__ = ("_common_codec", "_review_codec", "_values")

    def __init__(
        self,
        common_codec: _CommonWireRecordSerializer,
        review_codec: _ReviewOwnershipWireSerializer,
    ) -> None:
        self._common_codec = common_codec
        self._review_codec = review_codec
        self._values = _WireValueDecoder()

    def encode(self, record: object) -> dict[str, object]:
        from ..profiles import ProjectProfile
        from ..resources import ResourceManifest, ResourceReference, SkillDescriptor

        if type(record) is ResourceReference:
            return {
                "schema_version": record.schema_version,
                "resource_id": record.resource_id,
                "resource_kind": record.resource_kind,
                "format_version": record.format_version,
                "path": record.path,
                "content_identity": self._common_codec._encode_artifact_identity(
                    record.content_identity
                ),
                "dependency_ids": list(record.dependency_ids),
            }
        if type(record) is ResourceManifest:
            return {
                "schema_version": record.schema_version,
                "manifest_id": record.manifest_id,
                "manifest_version": record.manifest_version,
                "layer": record.layer,
                "extends_manifest_id": record.extends_manifest_id,
                "resources": [self.encode(value) for value in record.resources],
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
                    [self._review_codec.encode(scope), marker, list(prefixes)]
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
                "checkpoint_resolved_statuses": list(
                    record.checkpoint_resolved_statuses
                ),
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
        raise TypeError("record is outside resource wire records")

    def decode(self, kind_name: str, obj: dict[str, Any]) -> object:
        from ..ownership import OwnershipScope
        from ..profiles import ProjectProfile
        from ..resources import ResourceManifest, ResourceReference, SkillDescriptor

        if kind_name == "ResourceReference":
            expected: tuple[str, ...] = (
                "schema_version",
                "resource_id",
                "resource_kind",
                "format_version",
                "path",
                "content_identity",
                "dependency_ids",
            )
            self._values.require_fields(obj, expected)
            identity = self._common_codec._decode_artifact_identity(
                self._values.record_object(obj["content_identity"])
            )
            return ResourceReference(
                obj["schema_version"],
                obj["resource_id"],
                obj["resource_kind"],
                obj["format_version"],
                obj["path"],
                identity,
                self._values.freeze(obj["dependency_ids"]),
            )
        if kind_name == "ResourceManifest":
            expected = (
                "schema_version",
                "manifest_id",
                "manifest_version",
                "layer",
                "extends_manifest_id",
                "resources",
            )
            self._values.require_fields(obj, expected)
            resources = cast(
                tuple[ResourceReference, ...],
                tuple(
                    self.decode(
                        "ResourceReference", self._values.record_object(value)
                    )
                    for value in self._values.array(obj["resources"], "resources")
                ),
            )
            return ResourceManifest(
                obj["schema_version"],
                obj["manifest_id"],
                obj["manifest_version"],
                obj["layer"],
                obj["extends_manifest_id"],
                resources,
            )
        if kind_name == "ProjectProfile":
            expected = (
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
            self._values.require_fields(obj, expected)
            scope_rules = []
            for raw_rule in self._values.array(
                obj["evidence_scope_rules"], "evidence_scope_rules"
            ):
                rule = self._values.array(raw_rule, "evidence_scope_rule")
                if len(rule) != 3:
                    raise TypeError("evidence_scope_rule must contain three values")
                scope = self._review_codec.decode(
                    "OwnershipScope", self._values.record_object(rule[0])
                )
                if type(scope) is not OwnershipScope:
                    raise AssertionError("scope constructor returned wrong kind")
                scope_rules.append((scope, rule[1], self._values.freeze(rule[2])))
            return ProjectProfile(
                obj["schema_version"],
                obj["profile_id"],
                obj["public_contract_version"],
                obj["generic_manifest_id"],
                obj["generic_manifest_version"],
                obj["local_manifest_id"],
                obj["local_manifest_version"],
                obj["overlay_policy"],
                self._values.freeze(obj["policy_reference_ids"]),
                self._values.freeze(obj["supported_resource_formats"]),
                self._values.freeze(obj["supported_skill_behaviors"]),
                self._values.freeze(obj["evidence_namespace_rules"]),
                tuple(scope_rules),
                self._values.freeze(obj["protected_unowned_functions"]),
                self._values.freeze(obj["pytest_markers"]),
                obj["filename_policy_id"],
                self._values.freeze(obj["checkpoint_unresolved_statuses"]),
                self._values.freeze(obj["checkpoint_resolved_statuses"]),
                self._values.freeze(obj["task_active_statuses"]),
                self._values.freeze(obj["task_blocked_statuses"]),
                self._values.freeze(obj["task_satisfied_statuses"]),
                obj["compatibility_adapter_version"],
                self._values.freeze(obj["local_extension_ids"]),
            )
        if kind_name == "SkillDescriptor":
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
            self._values.require_fields(obj, expected)
            return SkillDescriptor(
                obj["schema_version"],
                obj["skill_id"],
                obj["behavior_version"],
                obj["entry_resource_id"],
                self._values.freeze(obj["trigger_capability_ids"]),
                self._values.freeze(obj["required_resource_ids"]),
                obj["side_effect_class"],
                obj["authorization_policy_id"],
                obj["retry_policy"],
                obj["termination_policy"],
            )
        raise AssertionError("resource wire kind is not exhaustively handled")
