"""Private canonical source-input resolution for maintained control state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ....configuration import HarnessConfiguration
from ..conformance_inputs import _PythonConformanceInputResolver
from ..dbcontrol.records import _HarnessProjectionRequest
from ..input_selection import _RepositoryInputSelector
from .configuration_inputs import _HarnessConfigurationInputResolver


@dataclass(frozen=True, slots=True)
class _HarnessProjectionInputs:
    """Exact immutable canonical request resolved from maintained source authority."""

    request: _HarnessProjectionRequest


class _HarnessProjectionInputResolver:
    """Resolve the canonical source documents into one projection request."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _HarnessProjectionInputs:
        """Resolve exact configuration bytes and construct the maintained request."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        root = repository_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        selector = _RepositoryInputSelector()
        configuration: HarnessConfiguration = (
            _HarnessConfigurationInputResolver().execute(root).configuration
        )
        conformance = _PythonConformanceInputResolver().execute(
            root,
            pyproject_path=Path(configuration.python_conformance.pyproject_path),
            test_root_path=Path(configuration.python_conformance.test_root),
            profile_path=Path(configuration.python_conformance.profile_matrix_path),
            migration_path=Path(configuration.python_conformance.migration_map_path),
        )
        for relative in (
            Path(configuration.resources.project_profile_path),
            Path(configuration.resources.generic_manifest_path),
            Path(configuration.resources.local_manifest_path),
        ):
            selector.file(root, relative, subject="configured control input")
        for relative in (
            Path(configuration.resources.generic_root),
            Path(configuration.resources.local_root),
            Path(configuration.catalogs.task_root),
            *(Path(path) for path in configuration.catalogs.agent_roots),
            *(Path(path) for path in configuration.catalogs.checkpoint_roots),
            *(Path(path) for path in configuration.catalogs.skill_roots),
        ):
            selector.directory(root, relative)
        task_root = root / configuration.catalogs.task_root
        task_paths = tuple(sorted(task_root.glob("*.json")))
        if not task_paths or any(path.is_symlink() for path in task_paths):
            raise ValueError("canonical Task catalog must contain regular JSON files")
        return _HarnessProjectionInputs(
            _HarnessProjectionRequest(
                root,
                harness_configuration=configuration,
                evidence_module_paths=conformance.module_paths,
            )
        )
