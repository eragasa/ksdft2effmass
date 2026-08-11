"""Explicit field mapping for checkpoint wire records."""

from __future__ import annotations

from typing import Any

from .records import _WireValueDecoder


class _CheckpointRecordSerializer:
    """Own the explicit checkpoint-record wire mapping."""

    __slots__ = ("_values",)

    def __init__(self) -> None:
        self._values = _WireValueDecoder()

    def encode(self, record: object) -> dict[str, object]:
        from ..checkpoints import CheckpointRecord

        if type(record) is not CheckpointRecord:
            raise TypeError("record must be CheckpointRecord")
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

    def decode(self, obj: dict[str, Any]) -> object:
        from ..checkpoints import CheckpointRecord

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
        self._values.require_fields(obj, expected)
        return CheckpointRecord(
            obj["schema_version"],
            obj["checkpoint_id"],
            obj["task_id"],
            obj["episode_id"],
            obj["status"],
            obj["decision_class"],
            obj["created_at"],
            obj["question"],
            self._values.freeze(obj["options"]),
            obj["human_response"],
            obj["normalized_decision"],
            obj["resolved_at"],
            obj["authorized_scope"],
            self._values.freeze(obj["record_paths"]),
            obj["resumption_status"],
        )
