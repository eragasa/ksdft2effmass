"""Orchestration for one explicit-input durable Task-state inspection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..validation import ValidationResult, _issue, _result
from .documents import _PARSE_ERRORS, _TaskStateDocumentParser
from .files import _InspectionFiles


@dataclass(frozen=True, slots=True)
class _TaskStateQueryResult:
    """Private result projected by the public Task-state ActionObject."""

    task_status: str | None
    selected_task_id: str | None
    completion_validator_path: str | None
    completion_command: tuple[str, ...]
    writers: tuple[tuple[str, str], ...]
    reviewers: tuple[tuple[str, str], ...]
    inspected_paths: tuple[str, ...]
    read_paths: tuple[str, ...]
    limitations: tuple[str, ...]
    validation: ValidationResult


class _TaskStateQuery:
    """Own one bounded inspection over exact caller-supplied inputs."""

    __slots__ = (
        "ownership_manifest_path",
        "repository_root",
        "selection_path",
        "task_id",
        "task_path",
    )

    def __init__(
        self,
        repository_root: Path,
        task_path: str,
        selection_path: str,
        task_id: str,
        ownership_manifest_path: str | None,
    ) -> None:
        self.repository_root = repository_root
        self.task_path = task_path
        self.selection_path = selection_path
        self.task_id = task_id
        self.ownership_manifest_path = ownership_manifest_path

    def execute(self) -> _TaskStateQueryResult:
        """Inspect Task, selection, and optional ownership without discovery."""
        parser = _TaskStateDocumentParser()
        files = _InspectionFiles(self.repository_root, self.task_id)
        root_valid = files.root_is_valid()
        if not root_valid:
            files.issues.append(
                _issue(
                    "PIH.PATH.ROOT_INVALID",
                    "repository_root must be an existing canonical nonsymlink "
                    "directory.",
                    self.task_id,
                )
            )

        task_status: str | None = None
        selected_task_id: str | None = None
        completion_path: str | None = None
        completion_command: tuple[str, ...] = ()
        writers: tuple[tuple[str, str], ...] = ()
        reviewers: tuple[tuple[str, str], ...] = ()

        if root_valid:
            task_payload = files.inspect(self.task_path)
            if task_payload is not None:
                try:
                    task_status = parser.parse_task(task_payload, self.task_id).status
                except _PARSE_ERRORS as exc:
                    files.issues.append(
                        _issue(
                            "PIH.TASK_STATE.REFERENCE_INVALID",
                            f"Canonical Task state is malformed: {exc}.",
                            self.task_id,
                            self.task_path,
                        )
                    )

            selection_payload = files.inspect(self.selection_path)
            if selection_payload is not None:
                try:
                    selected_task_id = parser.parse_selection(
                        selection_payload
                    ).selected_task_id
                except _PARSE_ERRORS as exc:
                    files.issues.append(
                        _issue(
                            "PIH.TASK_STATE.REFERENCE_INVALID",
                            f"Development Task selection is malformed: {exc}.",
                            self.task_id,
                            self.selection_path,
                        )
                    )

            if self.ownership_manifest_path is not None:
                ownership_payload = files.inspect(self.ownership_manifest_path)
                if ownership_payload is not None:
                    try:
                        ownership = parser.parse_ownership(
                            ownership_payload,
                            self.task_id,
                            self.task_path,
                            self.ownership_manifest_path,
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
                                self.task_id,
                                self.ownership_manifest_path,
                            )
                        )

        limitations = {
            "Authority, operation execution, runtime history, and reviewer launches "
            "were not inspected.",
            "Only the exact Task, selection, and optional operation-scoped ownership "
            "inputs were inspected.",
        }
        if self.ownership_manifest_path is None:
            limitations.add("No operation-scoped ownership manifest was supplied.")

        return _TaskStateQueryResult(
            task_status,
            selected_task_id,
            completion_path,
            completion_command,
            writers,
            reviewers,
            tuple(sorted(files.inspected)),
            tuple(sorted(files.read)),
            tuple(sorted(limitations)),
            _result(tuple(files.issues)),
        )
