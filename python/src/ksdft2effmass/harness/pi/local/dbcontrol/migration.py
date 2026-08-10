"""Thin orchestration for repository-specific control migration."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

from ...evidence.python_conformance import (
    PythonConformanceRequest,
    PythonConformanceValidator,
    PythonModuleSource,
)
from .constants import (
    _GENERATOR_ID,
    CONTROL_SCHEMA_VERSION,
    CONTROL_SQL_PATH,
    PROJECTION_MANIFEST_PATH,
)
from .database import _ControlDatabase
from .encoding import _ControlEncoding
from .ingestion import _RepositoryControlIngestor
from .projections import _ControlProjector
from .records import HarnessControlMigrationRequest, HarnessControlMigrationResult
from .schema import _SCHEMA


class HarnessControlMigrator:
    """Migrate file-backed control catalogs into one authoritative SQLite database."""

    __slots__ = ()

    @staticmethod
    def _repository_file(root: Path, relative: Path) -> Path:
        """Resolve one explicit regular file without escaping ``root``."""
        resolved_root = root.resolve()
        try:
            resolved = (resolved_root / relative).resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            raise ValueError(
                f"repository-relative input is not root-confined: {relative}"
            ) from exc
        if not resolved.is_file():
            raise ValueError(
                f"repository-relative input is not a regular file: {relative}"
            )
        return resolved

    @classmethod
    def _evidence_module_ownership(
        cls, request: HarnessControlMigrationRequest
    ) -> tuple[Mapping[str, Any], ...] | None:
        """Load and conformance-check the optional explicit ownership snapshot."""
        relative = request.evidence_module_ownership_path
        if relative is None:
            return None
        ownership_path = cls._repository_file(request.repository_root, relative)
        payload = ownership_path.read_bytes()
        profile_path = request.evidence_profile_matrix_path
        profile_payload: bytes | None = None
        if profile_path is not None:
            profile_payload = cls._repository_file(
                request.repository_root, profile_path
            ).read_bytes()
        try:
            document = json.loads(payload.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "evidence-module ownership input must be valid UTF-8 JSON"
            ) from exc
        raw_modules = document.get("modules") if isinstance(document, dict) else None
        if not isinstance(raw_modules, list):
            raise ValueError("evidence-module ownership input requires a modules list")
        if not raw_modules:
            if document != {"schema_version": 1, "modules": []}:
                raise ValueError(
                    "empty evidence-module ownership input has invalid schema"
                )
            return ()
        sources: list[PythonModuleSource] = []
        for index, entry in enumerate(raw_modules):
            raw_path = entry.get("path") if isinstance(entry, dict) else None
            if not isinstance(raw_path, str) or not raw_path:
                raise ValueError(
                    f"evidence-module ownership modules[{index}].path is invalid"
                )
            module_relative = Path(raw_path)
            if (
                module_relative.is_absolute()
                or ".." in module_relative.parts
                or len(module_relative.parts) < 3
                or module_relative.parts[:2] != ("python", "tests")
                or module_relative.suffix != ".py"
            ):
                message = (
                    "evidence-module ownership path is outside python/tests: "
                    f"{raw_path}"
                )
                raise ValueError(message)
            source_path = cls._repository_file(request.repository_root, module_relative)
            sources.append(PythonModuleSource(raw_path, source_path.read_bytes()))
        result = PythonConformanceValidator().execute(
            PythonConformanceRequest(
                tuple(sources),
                relative.as_posix(),
                payload,
                profile_path=profile_path.as_posix()
                if profile_path is not None
                else None,
                profile_payload=profile_payload,
            )
        )
        if result.status != "PASS":
            codes = ", ".join(sorted({finding.code for finding in result.findings}))
            raise ValueError(
                f"evidence-module ownership input is nonconforming: {codes}"
            )
        return tuple(MappingProxyType(dict(entry)) for entry in raw_modules)

    @staticmethod
    def _publish_generation(
        outputs: Mapping[Path, bytes], database_path: Path, semantic_digest: str
    ) -> None:
        """Stage, verify, and publish one generation with rollback on failure.

        Publication uses same-directory atomic replacements for individual files.
        It does not claim filesystem-level multi-file atomicity: if one replacement
        fails, retained backups restore every previously published output before the
        error is returned.
        """
        destinations = tuple(sorted(outputs, key=lambda path: path.as_posix()))
        staged = {
            destination: destination.with_name(
                f".{destination.name}.harness-control-staged"
            )
            for destination in destinations
        }
        backups = {
            destination: destination.with_name(
                f".{destination.name}.harness-control-backup"
            )
            for destination in destinations
        }
        existed = {destination: destination.exists() for destination in destinations}
        staged_database = staged[database_path]
        database_sidecars = tuple(
            Path(str(staged_database) + suffix)
            for suffix in ("-wal", "-shm", "-journal")
        )
        temporary_paths = (
            *staged.values(),
            *backups.values(),
            *database_sidecars,
        )
        try:
            for destination in destinations:
                destination.parent.mkdir(parents=True, exist_ok=True)
                staged[destination].unlink(missing_ok=True)
                backups[destination].unlink(missing_ok=True)
                staged[destination].write_bytes(outputs[destination])
            for destination in destinations:
                if staged[destination].read_bytes() != outputs[destination]:
                    raise RuntimeError(
                        f"staged output verification failed: {destination}"
                    )
            with sqlite3.connect(staged_database) as connection:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                foreign_keys = list(connection.execute("PRAGMA foreign_key_check"))
                stored_digest = connection.execute(
                    "SELECT value FROM harness_metadata WHERE key='semantic_digest'"
                ).fetchone()
            if integrity != "ok" or foreign_keys or stored_digest != (semantic_digest,):
                raise RuntimeError("staged authoritative database verification failed")
            for path in database_sidecars:
                path.unlink(missing_ok=True)
        except Exception:
            for path in temporary_paths:
                path.unlink(missing_ok=True)
            raise
        try:
            for destination in destinations:
                if existed[destination]:
                    destination.replace(backups[destination])
            for destination in destinations:
                staged[destination].replace(destination)
        except Exception as publish_error:
            try:
                for destination in reversed(destinations):
                    if backups[destination].exists():
                        destination.unlink(missing_ok=True)
                        backups[destination].replace(destination)
                    elif not existed[destination]:
                        destination.unlink(missing_ok=True)
            except Exception as rollback_error:
                raise RuntimeError(
                    "control generation publication and rollback both failed"
                ) from rollback_error
            raise RuntimeError(
                "control generation publication failed; previous generation restored"
            ) from publish_error
        finally:
            for path in temporary_paths:
                path.unlink(missing_ok=True)

    def execute(
        self, request: HarnessControlMigrationRequest
    ) -> HarnessControlMigrationResult:
        """Create the database, SQL recovery text, and projections."""
        if type(request) is not HarnessControlMigrationRequest:
            raise TypeError("request must be HarnessControlMigrationRequest")
        root = request.repository_root
        module_inventory = self._evidence_module_ownership(request)
        database_path = root / request.database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        working = database_path.with_suffix(".building.sqlite3")
        _ControlDatabase.reconstruct(working, (_SCHEMA + "\n").encode())
        connection = sqlite3.connect(working)
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA defer_foreign_keys=ON")
        unresolved: list[str] = []
        try:
            connection.executemany(
                "INSERT INTO harness_metadata VALUES (?,?)",
                (
                    ("control_schema_version", str(CONTROL_SCHEMA_VERSION)),
                    ("identifier_convention", "lowercase-dotted-kebab-segments"),
                    (
                        "runtime_observation_database",
                        ".pi/cache/harness-observations.sqlite3",
                    ),
                    ("telemetry_status", "deferred-inactive"),
                ),
            )
            ingestor = _RepositoryControlIngestor(
                connection, root, unresolved, module_inventory
            )
            ingestor.execute()
            connection.commit()
            projector = _ControlProjector(connection, ingestor.evidence_profiles)
            projections = projector.render_all()
            for path, (kind, payload) in sorted(projections.items()):
                connection.execute(
                    "INSERT INTO projection_record VALUES (?,?,?,?,?)",
                    (
                        path,
                        kind,
                        _ControlEncoding.sha256(payload),
                        len(payload),
                        _GENERATOR_ID,
                    ),
                )
            connection.commit()
            database = _ControlDatabase(connection)
            digest = database.semantic_digest()
            connection.execute(
                "INSERT INTO harness_metadata VALUES (?,?)", ("semantic_digest", digest)
            )
            connection.commit()
            digest = database.semantic_digest()
            connection.execute(
                "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
                (digest,),
            )
            connection.commit()
            # The digest field is excluded from identity comparison by normalizing it.
            final_digest = database.normalized_semantic_digest()
            connection.execute(
                "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
                (final_digest,),
            )
            connection.commit()
            sql_bytes = database.deterministic_sql_export()
            counts = database.catalog_counts()
        finally:
            connection.close()
        manifest_bytes = _ControlProjector.projection_manifest_bytes(
            control_schema_version=CONTROL_SCHEMA_VERSION,
            semantic_database_digest=final_digest,
            sql_path=CONTROL_SQL_PATH,
            sql_bytes=sql_bytes,
            projections=projections,
            unresolved_naming_issues=tuple(sorted(unresolved)),
        )
        _ControlDatabase.reconstruct(working, sql_bytes)
        outputs = {
            database_path: working.read_bytes(),
            root / CONTROL_SQL_PATH: sql_bytes,
            root / PROJECTION_MANIFEST_PATH: manifest_bytes,
            **{
                root / path: payload
                for path, (_kind, payload) in sorted(projections.items())
            },
        }
        try:
            self._publish_generation(outputs, database_path, final_digest)
        finally:
            working.unlink(missing_ok=True)
        return HarnessControlMigrationResult(
            CONTROL_SCHEMA_VERSION,
            final_digest,
            counts,
            tuple(sorted(unresolved)),
            tuple(sorted(projections)),
        )
