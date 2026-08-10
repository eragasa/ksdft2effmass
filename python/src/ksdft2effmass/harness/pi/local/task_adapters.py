"""Compatibility adapters for selected Task and chain records."""

from __future__ import annotations

import json
import re
from typing import Any

from .. import ChainView, ResourcePath, TaskReference
from ._parsing import (
    as_bool,
    as_str,
    failure,
    parse_object,
    strings,
    success,
)
from .models import AdaptationResult, LocalIssue
from .task_model import HarnessTaskDeserializer


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


_TASK_V1_FIELDS = frozenset(
    {
        "schema_version",
        "task_id",
        "title",
        "status",
        "parent_task_id",
        "task_prerequisite_ids",
        "external_prerequisite_ids",
        "explicit_activation_required",
        "objective",
        "authority_reference_paths",
        "authorized_scope",
        "completion_criteria",
        "exclusions",
        "intake_path",
        "archived_source",
    }
)
_IDENTIFIER = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")
_RESOURCE_PATH = re.compile(
    r"^(?!/)(?!.*(?:^|/)\.{1,2}(?:/|$))(?!.*//)(?!.*\\)"
    r"[^\x00-\x1f/]+(?:/[^\x00-\x1f/]+)*$"
)


def _strict_strings(value: object, field: str) -> tuple[str, ...]:
    values = strings(value, field)
    if (
        type(value) is not list
        or list(values) != value
        or len(set(values)) != len(values)
    ):
        raise ValueError(f"{field} must be unique and sorted")
    return values


def _task_record_values(
    task: dict[str, Any],
) -> tuple[str, tuple[str, ...], tuple[str, ...], str, bool]:
    """Validate one complete project-local JSON Task and return view fields."""
    if task.get("schema_version") in {2, 3}:
        payload = (json.dumps(task, ensure_ascii=False) + "\n").encode("utf-8")
        model = HarnessTaskDeserializer().execute(payload)
        return (
            model.task_id,
            model.task_prerequisite_ids,
            model.external_prerequisite_ids,
            model.status,
            model.explicit_activation_required,
        )
    missing = _TASK_V1_FIELDS - set(task)
    unknown = set(task) - _TASK_V1_FIELDS
    if missing:
        raise ValueError(f"JSON Task is missing {sorted(missing)[0]}")
    if unknown:
        raise ValueError(f"JSON Task has unknown field {sorted(unknown)[0]}")
    if type(task["schema_version"]) is not int or task["schema_version"] != 1:
        raise ValueError("schema_version must equal integer 1, 2, or 3")

    task_id = as_str(task["task_id"], "task_id")
    if _IDENTIFIER.fullmatch(task_id) is None:
        raise ValueError("task_id must be a version-1 identifier")
    parent = task["parent_task_id"]
    if parent is not None:
        parent = as_str(parent, "parent_task_id")
        if _IDENTIFIER.fullmatch(parent) is None or parent == task_id:
            raise ValueError("parent_task_id must be a distinct version-1 identifier")

    task_deps = _strict_strings(task["task_prerequisite_ids"], "task_prerequisite_ids")
    external = _strict_strings(
        task["external_prerequisite_ids"], "external_prerequisite_ids"
    )
    if task_id in {*task_deps, *external}:
        raise ValueError("Task cannot depend on itself")
    if set(task_deps) & set(external):
        raise ValueError("Task and external prerequisites must be disjoint")

    authority_paths = _strict_strings(
        task["authority_reference_paths"], "authority_reference_paths"
    )
    intake_path = task["intake_path"]
    paths = (
        authority_paths
        if intake_path is None
        else (*authority_paths, as_str(intake_path, "intake_path"))
    )
    for path in paths:
        if _RESOURCE_PATH.fullmatch(path) is None:
            raise ValueError("Task resource paths must be canonical relative paths")
    archived_source = task["archived_source"]
    if archived_source is not None:
        if type(archived_source) is not dict or set(archived_source) != {
            "path",
            "sha256",
        }:
            raise ValueError("archived_source must be a closed object or null")
        archive_path = as_str(archived_source["path"], "archived_source path")
        digest = as_str(archived_source["sha256"], "archived_source sha256")
        if (
            _RESOURCE_PATH.fullmatch(archive_path) is None
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            raise ValueError(
                "archived_source must contain a canonical path and SHA-256"
            )
    for field in ("authorized_scope", "completion_criteria", "exclusions"):
        values = strings(task[field], field)
        if not values:
            raise ValueError(f"{field} must not be empty")
    as_str(task["title"], "title")
    as_str(task["objective"], "objective")
    status = as_str(task["status"], "status")
    explicit = as_bool(
        task["explicit_activation_required"], "explicit_activation_required"
    )
    return task_id, task_deps, external, status, explicit


class TaskRecordAdapter:
    """Bind selected Markdown or JSON Task bytes to exact chain references.

    JSON-backed Tasks own their identity, status, separated prerequisite kinds,
    and explicit-activation requirement. Their chain entries may contain only
    chain-owned reference information; duplicated Task-owned fields fail closed.
    Markdown-backed bootstrap Tasks retain the legacy chain-owned adaptation.
    The ActionObject performs no repository discovery, persistence, or Task
    activation.
    """

    __slots__ = ()

    def execute(
        self,
        task_documents: tuple[tuple[ResourcePath, bytes], ...],
        chain_bytes: bytes,
        activation_bytes: bytes,
    ) -> AdaptationResult:
        """Return normalized Task references for one explicit chain selection.

        Parameters
        ----------
        task_documents
            Exact ``(resource_path, Task_bytes)`` pairs. Paths ending in
            ``.json`` use the retained Task JSON contracts; other paths use the
            bounded Markdown compatibility contract.
        chain_bytes
            Exact JSON bytes containing the selected ``task_sequence`` and
            chain-owned activation fields.
        activation_bytes
            Exact retained activation JSON bytes used by the compatibility
            result.

        Returns
        -------
        AdaptationResult
            A Task-identity-sorted tuple on success, or deterministic local
            diagnostics when Task, chain, or activation records disagree.

        Raises
        ------
        TypeError
            If the outer Task collection or an entry has the wrong semantic
            type.
        """
        if type(task_documents) is not tuple:
            raise TypeError("task_documents must be a tuple")
        chain, issue = parse_object(chain_bytes, "chain")
        if issue is not None:
            return failure(issue)
        activation, issue = parse_object(activation_bytes, "activation")
        if issue is not None:
            return failure(issue)
        assert chain is not None and activation is not None
        supplied = {}
        for path, payload in task_documents:
            if type(path) is not str or type(payload) is not bytes:
                raise TypeError("task document entries must be (str, bytes)")
            if path.endswith(".json"):
                document, issue = parse_object(payload, path)
                if issue is not None:
                    return failure(issue)
                supplied[path] = document
            else:
                try:
                    text = payload.decode("utf-8")
                except UnicodeDecodeError as exc:
                    return _invalid("TASK", path, exc)
                if not text.startswith("# ") or "Status:" not in text:
                    return failure(
                        LocalIssue(
                            "PIHL.TASK.INVALID", path, "missing title or Status field"
                        )
                    )
                supplied[path] = None
        try:
            entries = chain["task_sequence"]
            if type(entries) is not list:
                raise TypeError("task_sequence must be an array")
            activated = activation.get(
                "activated_task", activation.get("task", activation.get("task_id"))
            )
            result = []
            ids = {as_str(x.get("id"), "task id") for x in entries if type(x) is dict}
            json_selected = any(document is not None for document in supplied.values())
            chain_active = chain.get("active_task")
            if chain_active is not None:
                chain_active = as_str(chain_active, "active_task")
            chain_activated_ids = (
                _strict_strings(
                    chain.get("explicitly_activated_task_ids"),
                    "explicitly_activated_task_ids",
                )
                if json_selected
                else ()
            )
            if any(value not in ids for value in chain_activated_ids):
                raise ValueError("explicit activation names a nonmember Task")
            for item in entries:
                if type(item) is not dict:
                    raise TypeError("task entry must be an object")
                task_id = as_str(item["id"], "task id")
                record = as_str(item["record"], "task record")
                if record not in supplied:
                    raise ValueError(f"missing selected task bytes for {record}")
                task_document = supplied[record]
                if task_document is not None:
                    forbidden = {
                        "status",
                        "prerequisites",
                        "parent_task_id",
                        "task_prerequisite_ids",
                        "external_prerequisite_ids",
                        "superseded_by_task_ids",
                        "explicit_activation_required",
                    } & set(item)
                    if forbidden:
                        raise ValueError(
                            "JSON Task fields are duplicated in chain entry"
                        )
                    record_id, task_deps, external, status, explicit = (
                        _task_record_values(task_document)
                    )
                    if record_id != task_id:
                        raise ValueError("JSON Task identity differs from chain entry")
                    if (status == "active") != (chain_active == task_id):
                        raise ValueError(
                            "JSON Task status conflicts with chain active_task"
                        )
                    activation_count = chain_activated_ids.count(task_id)
                    if status == "active" and explicit and activation_count != 1:
                        raise ValueError("active JSON Task lacks explicit activation")
                    if not explicit and activation_count:
                        raise ValueError("JSON Task has unexpected explicit activation")
                else:
                    task_dep_list: list[str] = []
                    external_list: list[str] = []
                    for dep in item.get("prerequisites", []):
                        name = as_str(dep, "prerequisite").split(":", 1)[0]
                        (task_dep_list if name in ids else external_list).append(
                            dep if name not in ids else name
                        )
                    task_deps = tuple(task_dep_list)
                    external = tuple(external_list)
                    status = as_str(item["status"], "status")
                    explicit = task_id in {"H1", "H2", "H3", "H4", "H5"}
                result.append(
                    TaskReference(
                        1,
                        task_id,
                        record,
                        tuple(sorted(task_deps)),
                        tuple(sorted(external)),
                        status,
                        explicit,
                    )
                )
            if activated not in {None, *(x.task_id for x in result)}:
                raise ValueError("activation selects an unknown task")
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("TASK", "chain", exc)
        return success(tuple(sorted(result, key=lambda value: value.task_id)))


class ChainRecordAdapter:
    """Normalize one selected chain using already adapted Task records.

    The caller owns input selection and Task adaptation. This ActionObject
    constructs a generic chain view without reading repository state or
    authorizing execution.
    """

    __slots__ = ()

    def execute(
        self,
        chain_bytes: bytes,
        task_records: tuple[TaskReference, ...],
        activation_bytes: bytes,
    ) -> AdaptationResult:
        """Build a generic chain view without reading repository state.

        Parameters
        ----------
        chain_bytes
            Exact project-local chain JSON bytes.
        task_records
            Already adapted generic Task references for the chain.
        activation_bytes
            Exact retained activation JSON bytes.

        Returns
        -------
        AdaptationResult
            A generic chain view on success, or deterministic local diagnostics
            for malformed or incompatible bytes.
        """
        chain, issue = parse_object(chain_bytes, "chain")
        if issue is not None:
            return failure(issue)
        activation, issue = parse_object(activation_bytes, "activation")
        if issue is not None:
            return failure(issue)
        assert chain is not None and activation is not None
        try:
            active = chain.get("active_task")
            activated = activation.get(
                "activated_task", activation.get("task", activation.get("task_id"))
            )
            view = ChainView(
                1,
                as_str(chain.get("name"), "chain name"),
                active,
                task_records,
                () if activated is None else (as_str(activated, "activated task"),),
                as_bool(
                    chain["production_execution_authorized"], "production authorization"
                ),
                as_bool(
                    chain["package_publication_authorized"], "publication authorization"
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("CHAIN", "chain", exc)
        return success(view)
