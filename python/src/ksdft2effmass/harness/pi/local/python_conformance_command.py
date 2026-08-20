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
from ksdft2effmass.harness.pi.conformance.python.model import PythonTestModuleModel
from ksdft2effmass.harness.pi.conformance.python.parser import parse_module


def _read(path: Path) -> tuple[bytes | None, str | None]:
    try:
        return path.read_bytes(), None
    except OSError as exc:
        return None, str(exc)


def _source(path: Path) -> PythonModuleSource:
    rendered = path.as_posix()
    if not path.is_file() or path.is_symlink():
        return PythonModuleSource(rendered, None, False)
    payload, error = _read(path)
    return PythonModuleSource(rendered, payload, True, error)


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
        parsed_models: tuple[PythonTestModuleModel, ...] = ()
        if ownership_path is not None:
            if ownership_path.as_posix().endswith("module-inventory.json"):
                raise ValueError("generated module inventory is projection-only")
            ownership_payload, ownership_error = _read(ownership_path)
            rendered_ownership_path = ownership_path.as_posix()
            source_inputs = tuple(_source(path) for path in paths)
        else:
            entries: list[dict[str, object]] = []
            models = []
            sources = []
            for path in paths:
                payload = path.read_bytes()
                model = parse_module(path.as_posix(), payload)
                models.append(model)
                sources.append(PythonModuleSource(path.as_posix(), payload))
                entry: dict[str, object] = {
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
        migration_payload, migration_error = (
            _read(migration_path) if migration_path is not None else (None, None)
        )
        profile_payload, profile_error = (
            _read(profile_path) if profile_path is not None else (None, None)
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
            parsed_models,
        )
        return PythonConformanceValidator().execute(request)
