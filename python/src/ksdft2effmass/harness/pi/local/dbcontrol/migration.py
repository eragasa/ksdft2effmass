"""Thin orchestration for repository-specific control migration."""

from __future__ import annotations

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
from ...evidence.python_conformance.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ...evidence.python_conformance.migration import _PythonEvidencePredecessorRule
from ...evidence.python_conformance.model import PythonTestModuleModel
from .constants import (
    _GENERATOR_ID,
    CONTROL_SCHEMA_VERSION,
    CONTROL_SQL_PATH,
    PROJECTION_MANIFEST_PATH,
)
from .database import _ControlDatabase
from .encoding import _ControlEncoding
from .ingestion import _RepositoryControlIngestor
from .input_files import _ControlInputFileSelector
from .projections import _ControlProjector
from .records import HarnessControlMigrationRequest, HarnessControlMigrationResult
from .resources import _ControlResourceCorpus, _ControlResourceCorpusBuilder
from .schema import _SCHEMA


class HarnessControlMigrator:
    """Migrate file-backed control catalogs into one authoritative SQLite database."""

    __slots__ = ()

    @staticmethod
    def _canonical_evidence_corpus(
        request: HarnessControlMigrationRequest,
    ) -> tuple[
        tuple[Mapping[str, Any], ...],
        tuple[PythonTestModuleModel, ...],
        tuple[tuple[str, str], ...],
    ]:
        """Build canonical evidence inputs from source, policy, and migration map."""
        selector = _ControlInputFileSelector()
        if request.evidence_module_ownership_path is not None:
            selector.file(
                request.repository_root, request.evidence_module_ownership_path
            )
            raise ValueError(
                "generated or external module inventories are projection-only"
            )
        if not request.evidence_module_paths:
            return (), (), ()
        assert request.evidence_profile_matrix_path is not None
        assert request.evidence_migration_path is not None
        profile_path = selector.file(
            request.repository_root, request.evidence_profile_matrix_path
        )
        migration_path = selector.file(
            request.repository_root, request.evidence_migration_path
        )
        sources: list[PythonModuleSource] = []
        inputs: list[_PythonTestModuleInput] = []
        for relative in request.evidence_module_paths:
            path = selector.file(request.repository_root, relative)
            payload = path.read_bytes()
            raw_path = relative.as_posix()
            sources.append(PythonModuleSource(raw_path, payload))
            inputs.append(_PythonTestModuleInput(raw_path, payload))
        corpus = _PythonTestModuleCorpusBuilder().execute(tuple(inputs))
        if corpus.failures:
            raise SyntaxError(corpus.failures[0].message)
        models = list(corpus.models)
        modules: list[dict[str, Any]] = []
        for model in models:
            raw_path = model.path
            entry: dict[str, Any] = {
                "path": raw_path,
                "mode": model.ownership_kind,
                "evidence_class": model.evidence_class,
                "evidence_profile": model.evidence_profile,
            }
            entry["sut" if model.ownership_kind == "class_owned" else "artifact"] = (
                model.owner_subject
            )
            modules.append(entry)
        ownership_payload = _ControlEncoding.canonical_json_bytes(
            {"schema_version": 1, "modules": modules}
        )
        migration_payload = migration_path.read_bytes()
        profile_payload = profile_path.read_bytes()
        validation_request = PythonConformanceRequest(
            tuple(sources),
            "<source-embedded-module-declarations>",
            ownership_payload,
            migration_path=request.evidence_migration_path.as_posix(),
            migration_payload=migration_payload,
            profile_path=request.evidence_profile_matrix_path.as_posix(),
            profile_payload=profile_payload,
            _parsed_models=tuple(models),
        )
        result = PythonConformanceValidator()._execute(validation_request, corpus)
        if result.status != "PASS":
            codes = ", ".join(sorted({item.code for item in result.findings}))
            raise ValueError(f"canonical evidence inputs are nonconforming: {codes}")
        predecessors = (
            _PythonEvidencePredecessorRule()
            .execute(
                request.evidence_migration_path.as_posix(), migration_payload, None
            )
            .pairs
        )
        return (
            tuple(MappingProxyType(item) for item in modules),
            tuple(models),
            predecessors,
        )

    @staticmethod
    def _canonical_resource_corpus(
        request: HarnessControlMigrationRequest,
    ) -> _ControlResourceCorpus | None:
        """Build canonical resources only from the request's explicit paths."""
        if request.resource_profile_path is None:
            return None
        assert request.generic_resource_manifest_path is not None
        assert request.generic_resource_root_path is not None
        assert request.local_resource_manifest_path is not None
        assert request.local_resource_root_path is not None
        return _ControlResourceCorpusBuilder().execute(
            request.repository_root,
            request.resource_profile_path,
            request.generic_resource_manifest_path,
            request.generic_resource_root_path,
            request.local_resource_manifest_path,
            request.local_resource_root_path,
        )

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
        module_inventory, evidence_models, evidence_predecessors = (
            self._canonical_evidence_corpus(request)
        )
        resource_corpus = self._canonical_resource_corpus(request)
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
                    ("evidence_inventory_baseline_collected_node_count", "2383"),
                    ("evidence_inventory_baseline_module_count", "182"),
                    (
                        "evidence_inventory_baseline_revision",
                        "1a0c8ac35aa3e9bf3bdd6d11ba8afaf68c5bed06",
                    ),
                    ("evidence_inventory_test_root", "python/tests"),
                ),
            )
            ingestor = _RepositoryControlIngestor(
                connection,
                root,
                unresolved,
                module_inventory,
                evidence_models,
                evidence_predecessors,
                resource_corpus,
            )
            ingestor.execute()
            connection.commit()
            projector = _ControlProjector(
                connection,
                ingestor.evidence_profiles,
                None
                if resource_corpus is None
                else (
                    resource_corpus.generic_manifest,
                    resource_corpus.local_manifest,
                ),
            )
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
