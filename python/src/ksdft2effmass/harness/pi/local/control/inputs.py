"""Private canonical source-input resolution for maintained control state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...configuration import PiHarnessConfigurationDeserializer
from ..conformance_inputs import _PythonConformanceInputResolver
from ..dbcontrol.records import _HarnessProjectionRequest
from ..input_selection import _RepositoryInputSelector

_PROJECT_SETTINGS = Path(".pi/settings.json")
_RESOURCE_PROFILE = Path("harness/local/profiles/ksdft2effmass-v2.json")
_GENERIC_MANIFEST = Path("harness/pi/resource-manifest.json")
_GENERIC_ROOT = Path("harness/pi")
_LOCAL_MANIFEST = Path("harness/local/resource-manifest.json")
_LOCAL_ROOT = Path("harness/local")


@dataclass(frozen=True, slots=True)
class _HarnessProjectionInputs:
    """Exact immutable canonical request resolved from maintained source authority."""

    request: _HarnessProjectionRequest


class _HarnessProjectionInputResolver:
    """Resolve the frozen R2.7 canonical-input map without generated authority."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _HarnessProjectionInputs:
        """Return the exact canonical maintained control-generation request."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        root = repository_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        selector = _RepositoryInputSelector()
        conformance = _PythonConformanceInputResolver().execute(root)
        fixed_files = (
            _PROJECT_SETTINGS,
            _RESOURCE_PROFILE,
            _GENERIC_MANIFEST,
            _LOCAL_MANIFEST,
        )
        for fixed_relative in fixed_files:
            selector.file(root, fixed_relative, subject="canonical control input")
        selector.directory(root, _GENERIC_ROOT)
        selector.directory(root, _LOCAL_ROOT)
        for root_relative in (
            Path("harness/tasks"),
            Path(".pi/agents"),
            Path(".pi/checkpoints"),
            Path(".pi/skills"),
            Path(".agents/skills"),
        ):
            selector.directory(root, root_relative)
        task_paths = tuple(sorted((root / "harness/tasks").glob("*.json")))
        if not task_paths or any(path.is_symlink() for path in task_paths):
            raise ValueError("canonical Task catalog must contain regular JSON files")
        pi_configuration = PiHarnessConfigurationDeserializer().execute(
            selector.file(root, _PROJECT_SETTINGS, subject="configuration").read_bytes()
        )
        request = _HarnessProjectionRequest(
            root,
            evidence_profile_matrix_path=conformance.profile_path,
            evidence_module_paths=conformance.module_paths,
            evidence_migration_path=conformance.migration_path,
            resource_profile_path=_RESOURCE_PROFILE,
            generic_resource_manifest_path=_GENERIC_MANIFEST,
            generic_resource_root_path=_GENERIC_ROOT,
            local_resource_manifest_path=_LOCAL_MANIFEST,
            local_resource_root_path=_LOCAL_ROOT,
            pi_harness_configuration=pi_configuration,
        )
        return _HarnessProjectionInputs(request)
