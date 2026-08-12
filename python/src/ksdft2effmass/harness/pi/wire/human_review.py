"""Explicit field mappings for review-ownership wire records."""

from __future__ import annotations

from typing import Any, cast

from .records import _WireValueDecoder


class _ReviewOwnershipWireSerializer:
    """Own explicit review-ownership wire mappings."""

    __slots__ = ("_values",)

    def __init__(self) -> None:
        self._values = _WireValueDecoder()

    def encode(self, record: object) -> dict[str, object]:
        from ..ownership import (
            AgentDescriptorView,
            OwnershipManifestView,
            OwnershipScope,
        )

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
                    [role, agent, [self.encode(scope) for scope in scopes]]
                    for role, agent, scopes in record.writers
                ],
                "reviewers": [list(value) for value in record.reviewers],
                "completion_validator_path": record.completion_validator_path,
                "completion_command": list(record.completion_command),
                "orchestration_profile_id": record.orchestration_profile_id,
            }
        raise TypeError("record is outside review-ownership wire records")

    def decode(self, kind_name: str, obj: dict[str, Any]) -> object:
        from ..ownership import (
            AgentDescriptorView,
            OwnershipManifestView,
            OwnershipScope,
        )

        if kind_name == "OwnershipScope":
            self._values.require_fields(obj, ("schema_version", "path", "scope_kind"))
            return OwnershipScope(obj["schema_version"], obj["path"], obj["scope_kind"])
        if kind_name == "AgentDescriptorView":
            self._values.require_fields(
                obj, ("schema_version", "agent_id", "acceptance_role")
            )
            return AgentDescriptorView(
                obj["schema_version"], obj["agent_id"], obj["acceptance_role"]
            )
        if kind_name == "OwnershipManifestView":
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
            self._values.require_fields(obj, expected)
            writers = []
            for raw_writer in self._values.array(obj["writers"], "writers"):
                writer = self._values.array(raw_writer, "writer")
                if len(writer) != 3:
                    raise TypeError("writer must contain three values")
                scopes = cast(
                    tuple[OwnershipScope, ...],
                    tuple(
                        self.decode("OwnershipScope", self._values.record_object(value))
                        for value in self._values.array(writer[2], "owned_scopes")
                    ),
                )
                writers.append((writer[0], writer[1], scopes))
            return OwnershipManifestView(
                obj["schema_version"],
                obj["task_id"],
                obj["task_record_path"],
                tuple(writers),
                self._values.freeze(obj["reviewers"]),
                obj["completion_validator_path"],
                self._values.freeze(obj["completion_command"]),
                obj["orchestration_profile_id"],
            )
        raise AssertionError("review-ownership wire kind is not exhaustively handled")
