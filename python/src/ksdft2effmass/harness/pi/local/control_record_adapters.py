"""Compatibility adapters for selected checkpoint and agent control records."""

from __future__ import annotations

import re

from .. import AgentDescriptorView, CheckpointRecord, ResourcePath
from ._parsing import as_str, failure, parse_object, require_fields, strings, success
from .models import AdaptationResult, LocalIssue


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


def _options(value: object) -> tuple[tuple[str, str, str | None], ...]:
    if type(value) is not list:
        raise TypeError("options must be an array")
    result = []
    for item in value:
        if type(item) is not dict:
            raise TypeError("option must be an object")
        result.append(
            (
                as_str(item.get("id"), "option id"),
                str(item.get("summary", "")),
                item.get("consequence"),
            )
        )
    return tuple(result)


class CheckpointRecordAdapter:
    """Normalize caller-selected checkpoint JSON documents.

    The ActionObject adapts exact caller-supplied bytes into generic immutable
    checkpoint records. It performs no discovery, persistence, checkpoint
    resolution, or task resumption.
    """

    __slots__ = ()

    def execute(
        self, checkpoint_documents: tuple[tuple[ResourcePath, bytes], ...]
    ) -> AdaptationResult:
        """Adapt path/byte pairs into checkpoint records sorted by identity.

        Parameters
        ----------
        checkpoint_documents
            Exact ``(resource_path, JSON_bytes)`` pairs selected by the caller.

        Returns
        -------
        AdaptationResult
            A checkpoint-identity-sorted tuple on success, or deterministic
            local diagnostics on invalid input.

        Raises
        ------
        TypeError
            If ``checkpoint_documents`` is not a built-in tuple.
        """
        if type(checkpoint_documents) is not tuple:
            raise TypeError("checkpoint_documents must be a tuple")
        records = []
        for path, payload in checkpoint_documents:
            obj, issue = parse_object(payload, path)
            if issue is not None:
                return failure(issue)
            assert obj is not None
            required = {"checkpoint_id", "status", "options", "record_paths"}
            if (issue := require_fields(obj, required, path)) is not None:
                return failure(issue)
            try:
                records.append(
                    CheckpointRecord(
                        1,
                        as_str(obj["checkpoint_id"], "checkpoint_id"),
                        obj.get("task_id"),
                        obj.get("episode_id"),
                        as_str(obj["status"], "status"),
                        obj.get("decision_class"),
                        obj.get("created_at"),
                        obj.get("question"),
                        _options(obj["options"]),
                        obj.get("human_response"),
                        obj.get("normalized_decision"),
                        obj.get("resolved_at"),
                        obj.get("authorized_scope"),
                        tuple(
                            sorted(
                                path.rstrip("/")
                                for path in strings(obj["record_paths"], "record_paths")
                            )
                        ),
                        (
                            None
                            if obj.get("resumption_status") is None
                            else "resumed"
                            if obj.get("status")
                            in {"resolved", "cancelled", "superseded"}
                            else "blocked"
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                return _invalid("CHECKPOINT", path, exc)
        return success(tuple(sorted(records, key=lambda value: value.checkpoint_id)))


class AgentRecordAdapter:
    """Extract generic agent identities from selected Markdown front matter.

    The ActionObject reads only caller-supplied bytes and represents the
    ``name`` and ``acceptanceRole`` fields. It does not discover, launch, or
    authorize an agent.
    """

    __slots__ = ()

    def execute(
        self, agent_documents: tuple[tuple[ResourcePath, bytes], ...]
    ) -> AdaptationResult:
        """Adapt agent Markdown front matter into sorted generic views.

        Parameters
        ----------
        agent_documents
            Exact ``(resource_path, Markdown_bytes)`` pairs selected by the
            caller.

        Returns
        -------
        AdaptationResult
            An agent-identity-sorted tuple on success, or deterministic local
            diagnostics when required front matter is absent or invalid.
        """
        records = []
        for path, payload in agent_documents:
            try:
                text = payload.decode("utf-8")
                name = re.search(r"(?m)^name:\s*(\S+)\s*$", text)
                role = re.search(r"(?m)^acceptanceRole:\s*(\S+)\s*$", text)
                if name is None or role is None:
                    raise ValueError("missing name or acceptanceRole")
                records.append(AgentDescriptorView(1, name.group(1), role.group(1)))
            except (UnicodeDecodeError, TypeError, ValueError) as exc:
                return _invalid("AGENT", path, exc)
        return success(tuple(sorted(records, key=lambda value: value.agent_id)))
