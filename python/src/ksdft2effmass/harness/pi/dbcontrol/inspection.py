"""Orchestration for one bounded durable task-state inspection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..validation import ValidationResult, _issue, _result
from .database import _TaskStateDatabaseReader
from .documents import _PARSE_ERRORS, _TaskStateDocumentParser
from .files import _InspectionFiles

_CONTROL_DATABASE_PATH = "harness/state/harness-control.sqlite3"


@dataclass(frozen=True, slots=True)
class _TaskStateQueryResult:
    """Project-neutral SQLite result used by the public Task-state action."""

    task_status: str | None
    active_task_id: str | None
    task_record_path: str | None
    ownership_manifest_path: str | None
    completion_validator_path: str | None
    completion_command: tuple[str, ...]
    writers: tuple[tuple[str, str], ...]
    reviewers: tuple[tuple[str, str], ...]
    artifact_paths: tuple[str, ...]
    run_record_paths: tuple[str, ...]
    handoff_record_paths: tuple[str, ...]
    durable_run_record_status: str
    durable_handoff_record_status: str
    inspected_paths: tuple[str, ...]
    read_paths: tuple[str, ...]
    limitations: tuple[str, ...]
    validation: ValidationResult


class _TaskStateQuery:
    """Own one bounded Task-state inspection execution."""

    __slots__ = ("chain_path", "repository_root", "task_id")

    def __init__(self, repository_root: Path, chain_path: str, task_id: str) -> None:
        self.repository_root = repository_root
        self.chain_path = chain_path
        self.task_id = task_id

    @staticmethod
    def _record_status(paths: tuple[str, ...], missing: set[str]) -> str:
        if not paths:
            return "not_declared"
        return "declared_missing" if set(paths) & missing else "inspected"

    def execute(self) -> _TaskStateQueryResult:
        """Inspect one exact Task without importing its public ActionObject owner."""
        repository_root = self.repository_root
        chain_path = self.chain_path
        task_id = self.task_id
        parser = _TaskStateDocumentParser()
        files = _InspectionFiles(repository_root, task_id)
        root_valid = files.root_is_valid()
        if not root_valid:
            files.issues.append(
                _issue(
                    "PIH.PATH.ROOT_INVALID",
                    "repository_root must be an existing canonical nonsymlink "
                    "directory.",
                    task_id,
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

        chain_payload = files.inspect(chain_path) if root_valid else None
        selected_task = None
        if chain_payload is not None:
            chain = parser._parse_chain(
                chain_payload,
                task_id,
                chain_path,
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
                task_payload = files.inspect(task_record_path)
                if task_payload is not None and task_record_path.endswith(".json"):
                    try:
                        task_status = parser._parse_json_task(task_payload, task_id)
                    except _PARSE_ERRORS as exc:
                        files.issues.append(
                            _issue(
                                "PIH.TASK_STATE.REFERENCE_INVALID",
                                f"JSON Task state is malformed: {exc}.",
                                task_id,
                                task_record_path,
                            )
                        )
            if ownership_path is not None:
                ownership_payload = files.inspect(ownership_path)
                if ownership_payload is not None:
                    try:
                        ownership = parser._parse_ownership(
                            ownership_payload,
                            task_id,
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
                                task_id,
                                ownership_path,
                            )
                        )
            for path in tuple(
                sorted(set((*artifact_paths, *run_paths, *handoff_paths)))
            ):
                files.inspect(path)

        control_database = repository_root / _CONTROL_DATABASE_PATH
        if control_database.is_file() and not control_database.is_symlink():
            files.inspect(_CONTROL_DATABASE_PATH)
            database_state = _TaskStateDatabaseReader(control_database).read(task_id)
            if database_state is None:
                files.issues.append(
                    _issue(
                        "PIH.TASK_STATE.REFERENCE_INVALID",
                        "The authoritative control database does not contain the "
                        "selected Task.",
                        task_id,
                        _CONTROL_DATABASE_PATH,
                    )
                )
            else:
                database_status, database_active = database_state
                if task_status is not None and task_status != database_status:
                    files.issues.append(
                        _issue(
                            "PIH.TASK_STATE.REFERENCE_INVALID",
                            "Projected Task status disagrees with authoritative "
                            "SQLite state.",
                            task_id,
                            task_record_path,
                        )
                    )
                task_status = database_status
                if database_active:
                    active_task = task_id
                elif active_task == task_id:
                    files.issues.append(
                        _issue(
                            "PIH.TASK_STATE.REFERENCE_INVALID",
                            "Chain activation disagrees with authoritative SQLite "
                            "state.",
                            task_id,
                            chain_path,
                        )
                    )

        limitations = {
            "Interactive runtime execution and reviewer-launch counts are outside "
            "declared repository state and were not inspected.",
            "Only the authoritative control database, chain, and exact durable paths "
            "declared by the selected task and ownership manifest were inspected.",
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

        return _TaskStateQueryResult(
            task_status,
            active_task,
            task_record_path,
            ownership_path,
            completion_path,
            completion_command,
            writers,
            reviewers,
            artifact_paths,
            run_paths,
            handoff_paths,
            self._record_status(run_paths, files.missing),
            self._record_status(handoff_paths, files.missing),
            tuple(sorted(files.inspected)),
            tuple(sorted(files.read)),
            tuple(sorted(limitations)),
            _result(tuple(files.issues)),
        )
