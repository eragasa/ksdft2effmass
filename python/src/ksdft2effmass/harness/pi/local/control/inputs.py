"""Private canonical source-input resolution for maintained control state."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from ..dbcontrol.input_files import _ControlInputFileSelector
from ..dbcontrol.records import HarnessControlMigrationRequest

_EVIDENCE_PROFILE = Path(
    "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
)
_EVIDENCE_MIGRATION = Path(
    ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
)
_RESOURCE_PROFILE = Path("harness/local/profiles/ksdft2effmass-v2.json")
_GENERIC_MANIFEST = Path("harness/pi/resource-manifest.json")
_GENERIC_ROOT = Path("harness/pi")
_LOCAL_MANIFEST = Path("harness/local/resource-manifest.json")
_LOCAL_ROOT = Path("harness/local")


@dataclass(frozen=True, slots=True)
class _HarnessControlInputs:
    """Exact immutable canonical request resolved from maintained source authority."""

    request: HarnessControlMigrationRequest


class _HarnessControlInputResolver:
    """Resolve the frozen R2.7 canonical-input map without generated authority."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _HarnessControlInputs:
        """Return the exact canonical maintained control-generation request."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        root = repository_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        selector = _ControlInputFileSelector()
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
            raise ValueError("canonical Python evidence root must be exactly tests")
        test_root_relative = Path("python") / testpaths[0]
        test_root = selector.directory(root, test_root_relative)
        module_paths: list[Path] = []
        for path in sorted(
            test_root.rglob("test*.py"), key=lambda item: item.as_posix()
        ):
            if path.is_symlink() or not path.is_file():
                raise ValueError(
                    "canonical Python evidence modules must be regular files"
                )
            module_relative = path.resolve().relative_to(root).as_posix()
            module_paths.append(Path(module_relative))
        if not module_paths:
            raise ValueError("canonical Python evidence root contains no test modules")
        fixed_files = (
            _EVIDENCE_PROFILE,
            _EVIDENCE_MIGRATION,
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
        request = HarnessControlMigrationRequest(
            root,
            evidence_profile_matrix_path=_EVIDENCE_PROFILE,
            evidence_module_paths=tuple(module_paths),
            evidence_migration_path=_EVIDENCE_MIGRATION,
            resource_profile_path=_RESOURCE_PROFILE,
            generic_resource_manifest_path=_GENERIC_MANIFEST,
            generic_resource_root_path=_GENERIC_ROOT,
            local_resource_manifest_path=_LOCAL_MANIFEST,
            local_resource_root_path=_LOCAL_ROOT,
        )
        return _HarnessControlInputs(request)
