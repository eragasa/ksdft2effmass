"""Canonical project-local inputs for Python source conformance."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .input_selection import _RepositoryInputSelector

_PYTHON_CONFORMANCE_PROFILE = Path(
    "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
)
_PYTHON_CONFORMANCE_MIGRATION = Path(
    ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
)


@dataclass(frozen=True, slots=True)
class _PythonConformanceInputs:
    """Exact repository-relative source, profile, and migration inputs."""

    repository_root: Path
    profile_path: Path
    module_paths: tuple[Path, ...]
    migration_path: Path


class _PythonConformanceInputResolver:
    """Resolve canonical Python conformance inputs without projection coupling."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _PythonConformanceInputs:
        """Return exact maintained conformance paths beneath ``repository_root``."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        root = repository_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        selector = _RepositoryInputSelector()
        pyproject_relative = Path("python/pyproject.toml")
        pyproject = selector.file(root, pyproject_relative, subject="configuration")
        configuration = tomllib.loads(pyproject.read_text())
        try:
            testpaths = configuration["tool"]["pytest"]["ini_options"]["testpaths"]
        except (KeyError, TypeError) as exc:
            raise ValueError(
                "python/pyproject.toml lacks configured testpaths"
            ) from exc
        if testpaths != ["tests"]:
            raise ValueError("canonical Python conformance root must be exactly tests")
        test_root_relative = Path("python") / testpaths[0]
        test_root = selector.directory(root, test_root_relative)
        module_paths: list[Path] = []
        for path in sorted(
            test_root.rglob("test*.py"), key=lambda item: item.as_posix()
        ):
            if path.is_symlink() or not path.is_file():
                raise ValueError(
                    "canonical Python conformance modules must be regular files"
                )
            module_paths.append(Path(path.resolve().relative_to(root).as_posix()))
        if not module_paths:
            raise ValueError(
                "canonical Python conformance root contains no test modules"
            )
        selector.file(
            root, _PYTHON_CONFORMANCE_PROFILE, subject="Python conformance input"
        )
        selector.file(
            root, _PYTHON_CONFORMANCE_MIGRATION, subject="Python conformance input"
        )
        return _PythonConformanceInputs(
            root,
            _PYTHON_CONFORMANCE_PROFILE,
            tuple(module_paths),
            _PYTHON_CONFORMANCE_MIGRATION,
        )
