"""Orchestration for one bounded durable task-state inspection."""

from __future__ import annotations

from ._task_state_documents import _PARSE_ERRORS, _parse_chain, _parse_ownership
from ._task_state_files import _InspectionFiles
from .task_state import (
    TaskStateInspectionRequest,
    TaskStateInspectionResult,
)
from .validation import _issue, _result


def _record_status(paths: tuple[str, ...], missing: set[str]) -> str:
    if not paths:
        return "not_declared"
    return "declared_missing" if set(paths) & missing else "inspected"


def _inspect_task_state(
    request: TaskStateInspectionRequest,
) -> TaskStateInspectionResult:
    files = _InspectionFiles(request.repository_root, request.task_id)
    root_valid = files.root_is_valid()
    if not root_valid:
        files.issues.append(
            _issue(
                "PIH.PATH.ROOT_INVALID",
                "repository_root must be an existing canonical nonsymlink directory.",
                request.task_id,
            )
        )

    task_status: str | None = None
    active_task: str | None = None
    task_record_path: str | None = None
    ownership_path: str | None = None
    completion_path: str | None = None
    completion_command: tuple[str, ...] = ()
    writers: tuple[tuple[str, str], ...] = ()
    reviewers: tuple[tuple[str, str], ...] = ()
    artifact_paths: tuple[str, ...] = ()
    run_paths: tuple[str, ...] = ()
    handoff_paths: tuple[str, ...] = ()

    chain_payload = files.inspect(request.chain_path) if root_valid else None
    selected_task = None
    if chain_payload is not None:
        chain = _parse_chain(
            chain_payload,
            request.task_id,
            request.chain_path,
            files.issues,
        )
        active_task = chain.active_task
        selected_task = chain.selected_task
        if selected_task is not None:
            task_status = selected_task.status
            task_record_path = selected_task.task_record_path
            ownership_path = selected_task.ownership_path
            artifact_paths = selected_task.artifact_paths
            run_paths = selected_task.run_paths
            handoff_paths = selected_task.handoff_paths

    if selected_task is not None:
        if task_record_path is not None:
            files.inspect(task_record_path)
        if ownership_path is not None:
            ownership_payload = files.inspect(ownership_path)
            if ownership_payload is not None:
                try:
                    ownership = _parse_ownership(
                        ownership_payload,
                        request.task_id,
                        task_record_path,
                        ownership_path,
                        files.issues,
                    )
                    completion_path = ownership.completion_path
                    completion_command = ownership.completion_command
                    writers = ownership.writers
                    reviewers = ownership.reviewers
                    files.inspect(completion_path)
                except _PARSE_ERRORS as exc:
                    files.issues.append(
                        _issue(
                            "PIH.TASK_STATE.OWNERSHIP_INVALID",
                            f"Ownership state is malformed: {exc}.",
                            request.task_id,
                            ownership_path,
                        )
                    )
        for path in tuple(sorted(set((*artifact_paths, *run_paths, *handoff_paths)))):
            files.inspect(path)

    limitations = {
        "Interactive runtime execution and reviewer-launch counts are outside "
        "declared repository state and were not inspected.",
        "Only the chain and exact durable paths declared by the selected task "
        "and ownership manifest were inspected.",
    }
    if selected_task is not None and task_record_path is None:
        limitations.add("No task record is declared by the selected chain entry.")
    if selected_task is not None and ownership_path is None:
        limitations.add(
            "No ownership manifest is declared by the selected chain entry."
        )
    if not run_paths:
        limitations.add(
            "No durable run record is declared by the selected chain entry."
        )
    if not handoff_paths:
        limitations.add(
            "No durable handoff record is declared by the selected chain entry."
        )

    return TaskStateInspectionResult(
        1,
        request.repository_root,
        request.task_id,
        task_status,
        active_task,
        request.chain_path,
        task_record_path,
        ownership_path,
        completion_path,
        completion_command,
        writers,
        reviewers,
        artifact_paths,
        run_paths,
        handoff_paths,
        _record_status(run_paths, files.missing),
        _record_status(handoff_paths, files.missing),
        tuple(sorted(files.inspected)),
        tuple(sorted(files.read)),
        tuple(sorted(limitations)),
        _result(tuple(files.issues)),
    )
