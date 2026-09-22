"""Explicit, root-confined Task catalog observations for local control consumers.

These private values retain the actual source path and decoded schema-3 Task.
Discovery never classifies by Task-ID prefix, renames identities, grants authority,
or falls back to another root. Filesystem checks do not eliminate access races.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...configuration import HarnessCatalogConfiguration, _HarnessResourcePathValidator
from ...task import HarnessTask, HarnessTaskDeserializer
from .input_selection import _RepositoryInputSelector


@dataclass(frozen=True, slots=True)
class _TaskCatalogSource:
    """Immutable association between a Task and its actual relative source path."""

    source_path: str
    task: HarnessTask

    def __post_init__(self) -> None:
        if type(self.source_path) is not str:
            raise TypeError("source_path must be a built-in string")
        if type(self.task) is not HarnessTask:
            raise TypeError("task must be HarnessTask")
        _HarnessResourcePathValidator().execute(self.source_path, "source_path")
        path = Path(self.source_path)
        if (
            not self.source_path
            or path.is_absolute()
            or ".." in path.parts
            or path.as_posix() != self.source_path
        ):
            raise ValueError("Task source path must be relative and normalized")
        if path.name != f"{self.task.task_id}.json":
            raise ValueError(
                "authoritative Task identity must equal its source filename: "
                + path.name
            )


class _TaskCatalogReadFailure(ValueError):
    """Retain the exact source path of one failed Task observation."""

    def __init__(self, source_path: str, message: str) -> None:
        super().__init__(message)
        self.source_path = source_path


class _TaskCatalogReader:
    """Read explicitly selected catalogs, rejecting aliases and duplicate identities."""

    __slots__ = ()

    @staticmethod
    def configured_roots(catalogs: HarnessCatalogConfiguration) -> tuple[Path, ...]:
        tasks = catalogs.task_catalog
        return (
            Path(tasks.research_root),
            Path(tasks.simulation_root),
            Path(tasks.software_root),
        )

    def execute(
        self, root: Path, roots: tuple[Path, ...]
    ) -> tuple[_TaskCatalogSource, ...]:
        if not isinstance(root, Path):
            raise TypeError("repository root must be pathlib.Path")
        if not root.is_absolute():
            raise ValueError("repository root must be absolute")
        if type(roots) is not tuple or any(
            not isinstance(path, Path) for path in roots
        ):
            raise TypeError("catalog roots must be an explicit tuple of paths")
        if not roots:
            raise ValueError("at least one explicit Task catalog root is required")
        root = root.resolve(strict=True)
        selector = _RepositoryInputSelector()
        sources: list[_TaskCatalogSource] = []
        identities: set[str] = set()
        folded_paths: set[str] = set()
        directories: list[Path] = []
        for relative in roots:
            if (
                relative.is_absolute()
                or relative == Path(".")
                or ".." in relative.parts
            ):
                raise ValueError("Task catalog roots must be repository-relative")
            current = root
            for part in relative.parts:
                current /= part
                if current.is_symlink():
                    raise ValueError("Task catalog roots must not traverse symlinks")
            directory = selector.directory(root, relative)
            if any(
                directory.samefile(other)
                or directory in other.parents
                or other in directory.parents
                for other in directories
            ):
                raise ValueError("Task catalog roots overlap or alias")
            directories.append(directory)
            for path in sorted(directory.glob("*.json")):
                if path.is_symlink() or not path.is_file():
                    raise ValueError("Task catalogs must contain regular JSON files")
                source_path = path.relative_to(root).as_posix()
                selected = selector.file(root, Path(source_path), subject="Task record")
                try:
                    task = HarnessTaskDeserializer().execute(selected.read_bytes())
                    source = _TaskCatalogSource(source_path, task)
                except (OSError, TypeError, ValueError) as exc:
                    raise _TaskCatalogReadFailure(source_path, str(exc)) from exc
                if task.task_id in identities:
                    raise ValueError(
                        f"duplicate Task identity across catalogs: {task.task_id}"
                    )
                if source_path.casefold() in folded_paths:
                    raise ValueError(
                        "Task source paths must not have case-folded aliases"
                    )
                identities.add(task.task_id)
                folded_paths.add(source_path.casefold())
                sources.append(source)
        if not sources:
            raise ValueError("the complete Task catalog must be nonempty")
        return tuple(sorted(sources, key=lambda source: source.source_path))
