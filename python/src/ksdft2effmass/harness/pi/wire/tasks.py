"""Explicit field mappings for Task and chain wire records."""

from __future__ import annotations

from typing import Any, cast

from .records import _WireValueDecoder


class _TaskWireSerializer:
    """Own the explicit Task-reference and chain wire mappings."""

    __slots__ = ("_values",)

    def __init__(self) -> None:
        self._values = _WireValueDecoder()

    def encode(self, record: object) -> dict[str, object]:
        from ..chains import ChainView, TaskReference

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
                "tasks": [self.encode(value) for value in record.tasks],
                "explicitly_activated_task_ids": list(
                    record.explicitly_activated_task_ids
                ),
                "production_execution_authorized": (
                    record.production_execution_authorized
                ),
                "package_publication_authorized": record.package_publication_authorized,
            }
        raise TypeError("record is outside Task wire records")

    def decode(self, kind_name: str, obj: dict[str, Any]) -> object:
        from ..chains import ChainView, TaskReference

        if kind_name == "TaskReference":
            expected = (
                "schema_version",
                "task_id",
                "record_path",
                "task_prerequisite_ids",
                "external_prerequisite_ids",
                "status",
                "explicit_activation_required",
            )
            self._values.require_fields(obj, expected)
            return TaskReference(
                obj["schema_version"],
                obj["task_id"],
                obj["record_path"],
                self._values.freeze(obj["task_prerequisite_ids"]),
                self._values.freeze(obj["external_prerequisite_ids"]),
                obj["status"],
                obj["explicit_activation_required"],
            )
        if kind_name == "ChainView":
            expected = (
                "schema_version",
                "chain_id",
                "active_task_id",
                "tasks",
                "explicitly_activated_task_ids",
                "production_execution_authorized",
                "package_publication_authorized",
            )
            self._values.require_fields(obj, expected)
            tasks = cast(
                tuple[TaskReference, ...],
                tuple(
                    self.decode("TaskReference", self._values.record_object(value))
                    for value in self._values.array(obj["tasks"], "tasks")
                ),
            )
            return ChainView(
                obj["schema_version"],
                obj["chain_id"],
                obj["active_task_id"],
                tasks,
                self._values.freeze(obj["explicitly_activated_task_ids"]),
                obj["production_execution_authorized"],
                obj["package_publication_authorized"],
            )
        raise AssertionError("Task wire kind is not exhaustively handled")
