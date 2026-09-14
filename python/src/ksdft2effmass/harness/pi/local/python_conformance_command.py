"""Complete explicit-file operation for Python evidence conformance commands."""

from __future__ import annotations

import json
from pathlib import Path

from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)
from ksdft2effmass.harness.pi.conformance.python.migration import (
    _PythonEvidenceMigrationRule,
)
from ksdft2effmass.harness.pi.conformance.python.model import PythonTestModuleModel
from ksdft2effmass.harness.pi.conformance.python.parser import PythonTestModuleParser


class _PythonConformanceCommandValidator:
    """Build and execute one conformance request from explicit command inputs."""

    __slots__ = ()

    def execute(
        self,
        paths: tuple[Path, ...],
        ownership_path: Path | None,
        migration_path: Path | None,
        profile_path: Path | None,
    ) -> PythonConformanceResult:
        """Return conformance for exact modules and optional metadata files."""
        migration_payload, migration_error = (
            self._read(migration_path) if migration_path is not None else (None, None)
        )
        migration = (
            _PythonEvidenceMigrationRule().execute(
                migration_path.as_posix(), migration_payload, migration_error
            )
            if migration_path is not None
            else None
        )
        legacy_test_owner_paths = frozenset(
            ()
            if migration is None
            else migration.activated_legacy_test_owner_paths(
                tuple(path.as_posix() for path in paths)
            )
        )
        parsed_models: tuple[PythonTestModuleModel, ...] = ()
        if ownership_path is not None:
            if ownership_path.as_posix().endswith("module-inventory.json"):
                raise ValueError("generated module inventory is projection-only")
            ownership_payload, ownership_error = self._read(ownership_path)
            rendered_ownership_path = ownership_path.as_posix()
            source_inputs = tuple(self._source(path) for path in paths)
        else:
            entries: list[dict[str, str]] = []
            models = []
            sources = []
            for path in paths:
                payload = path.read_bytes()
                rendered_path = path.as_posix()
                parser = (
                    PythonTestModuleParser.execute
                    if rendered_path in legacy_test_owner_paths
                    else PythonTestModuleParser.execute_with_test_owner
                )
                model = parser(rendered_path, payload)
                models.append(model)
                sources.append(PythonModuleSource(path.as_posix(), payload))
                entry: dict[str, str] = {
                    "path": path.as_posix(),
                    "mode": model.ownership_kind,
                    "evidence_class": model.evidence_class,
                    "evidence_profile": model.evidence_profile,
                }
                owner_key = (
                    "sut" if model.ownership_kind == "class_owned" else "artifact"
                )
                entry[owner_key] = model.owner_subject
                entries.append(entry)
            ownership_payload = json.dumps(
                {"schema_version": 1, "modules": entries}, separators=(",", ":")
            ).encode()
            ownership_error = None
            rendered_ownership_path = "<source-embedded-module-declarations>"
            parsed_models = tuple(models)
            source_inputs = tuple(sources)
        profile_payload, profile_error = (
            self._read(profile_path) if profile_path is not None else (None, None)
        )
        request = PythonConformanceRequest(
            source_inputs,
            rendered_ownership_path,
            ownership_payload,
            ownership_error,
            migration_path.as_posix() if migration_path is not None else None,
            migration_payload,
            migration_error,
            profile_path.as_posix() if profile_path is not None else None,
            profile_payload,
            profile_error,
            _parsed_models=parsed_models,
        )
        return PythonConformanceValidator().execute(request)

    @staticmethod
    def _read(path: Path) -> tuple[bytes | None, str | None]:
        """Read one exact command input without raising an expected I/O error."""
        try:
            return path.read_bytes(), None
        except OSError as exc:
            return None, str(exc)

    @classmethod
    def _source(cls, path: Path) -> PythonModuleSource:
        """Adapt one explicit path to the typed conformance source record."""
        rendered = path.as_posix()
        if not path.is_file() or path.is_symlink():
            return PythonModuleSource(rendered, None, False)
        payload, error = cls._read(path)
        return PythonModuleSource(rendered, payload, True, error)
