"""Root-confined file access for durable task-state inspection."""

from __future__ import annotations

from pathlib import Path

from ..identity import Identifier, _require_path
from ..validation import ValidationIssue, _issue


class _InspectionFiles:
    """Track exact root-confined paths inspected by one action execution."""

    __slots__ = ("inspected", "issues", "missing", "read", "root", "task_id")

    def __init__(self, root: Path, task_id: Identifier) -> None:
        self.root = root
        self.task_id = task_id
        self.issues: list[ValidationIssue] = []
        self.inspected: set[str] = set()
        self.read: set[str] = set()
        self.missing: set[str] = set()

    @staticmethod
    def _path_code(exc: ValueError) -> str:
        code = str(exc).split(":", 1)[0]
        return (
            code if code.startswith("PIH.PATH.") else "PIH.TASK_STATE.REFERENCE_INVALID"
        )

    def root_is_valid(self) -> bool:
        """Return whether the caller-selected root is canonical and nonsymlinked."""
        try:
            return (
                self.root.exists()
                and self.root.is_dir()
                and not self.root.is_symlink()
                and self.root.resolve(strict=True) == self.root
            )
        except OSError:
            return False

    def inspect(self, path: str) -> bytes | None:
        """Read one exact declared file without following symlinks."""
        self.inspected.add(path)
        try:
            _require_path(path, "referenced path")
        except ValueError as exc:
            self.issues.append(
                _issue(self._path_code(exc), str(exc), self.task_id, path=None)
            )
            return None

        current = self.root
        for part in path.split("/"):
            current = current / part
            if current.is_symlink():
                self.issues.append(
                    _issue(
                        "PIH.PATH.SYMLINK",
                        "Referenced path contains a symlink.",
                        self.task_id,
                        path,
                    )
                )
                return None
            if not current.exists():
                self.missing.add(path)
                self.issues.append(
                    _issue(
                        "PIH.PATH.MISSING",
                        "Referenced durable file is missing.",
                        self.task_id,
                        path,
                    )
                )
                return None

        if not current.is_file():
            self.issues.append(
                _issue(
                    "PIH.PATH.NOT_FILE",
                    "Referenced durable path is not a regular file.",
                    self.task_id,
                    path,
                )
            )
            return None
        try:
            payload = current.read_bytes()
        except OSError as exc:
            self.issues.append(
                _issue(
                    "PIH.TASK_STATE.REFERENCE_INVALID",
                    f"Referenced durable file could not be read: {exc}.",
                    self.task_id,
                    path,
                )
            )
            return None
        self.read.add(path)
        return payload
