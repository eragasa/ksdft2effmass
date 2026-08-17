"""Private complete candidate generation for project-local harness control state.

The builder coordinates accepted domain and persistence owners. It writes only beneath
one caller-owned temporary workspace and has no maintained publication authority.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from ...configuration import PiHarnessAgentDefinitionResolver
from ...conformance.python import (
    PythonConformanceRequest,
    PythonConformanceValidator,
    PythonModuleSource,
)
from ...conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ...conformance.python.migration import _PythonEvidencePredecessorRule
from ...conformance.python.model import PythonTestModuleModel
from ..dbcontrol.constants import _GENERATOR_ID, CONTROL_SCHEMA_VERSION
from ..dbcontrol.database import _ControlDatabase
from ..dbcontrol.encoding import _ControlEncoding
from ..dbcontrol.ingestion import _RepositoryControlIngestor
from ..dbcontrol.projections import _ControlProjector
from ..dbcontrol.records import _HarnessProjectionRequest
from ..dbcontrol.resources import _ControlResourceCorpus, _ControlResourceCorpusBuilder
from ..dbcontrol.schema import _SCHEMA
from ..input_selection import _RepositoryInputSelector


@dataclass(frozen=True, slots=True)
class _HarnessProjectionGeneration:
    """Immutable descriptor of artifacts owned by one temporary workspace lifetime.

    The descriptor is immutable. The referenced files are temporary external
    artifacts and are not claimed to be deeply immutable. Their workspace owner must
    retain the workspace while consuming the descriptor and owns its cleanup.
    """

    workspace_root: Path
    database_path: Path
    artifacts: tuple[tuple[Path, Path], ...]
    schema_version: int
    semantic_digest: str
    counts: tuple[tuple[str, int], ...]
    unresolved_naming_issues: tuple[str, ...]
    projection_paths: tuple[str, ...]


class _HarnessProjectionGenerationBuilder:
    """Construct and validate one complete nonauthoritative control candidate."""

    __slots__ = ()

    @staticmethod
    def _candidate_path(workspace_root: Path, relative: Path) -> Path:
        """Confine one candidate output before directory creation or writing."""
        if relative.is_absolute() or relative == Path(".") or ".." in relative.parts:
            raise ValueError(f"candidate output path is not confined: {relative}")
        resolved_workspace = workspace_root.resolve(strict=True)
        try:
            candidate = (resolved_workspace / relative).resolve(strict=False)
            candidate.relative_to(resolved_workspace)
        except (OSError, RuntimeError, ValueError) as exc:
            raise ValueError(
                f"candidate output path is not confined: {relative}"
            ) from exc
        return candidate

    @staticmethod
    def _canonical_evidence_corpus(
        request: _HarnessProjectionRequest,
    ) -> tuple[
        tuple[Mapping[str, Any], ...],
        tuple[PythonTestModuleModel, ...],
        tuple[tuple[str, str], ...],
    ]:
        """Build canonical evidence inputs from source, policy, and migration map."""
        selector = _RepositoryInputSelector()
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
            entry: dict[str, Any] = {
                "path": model.path,
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
        validation_request = PythonConformanceRequest(
            tuple(sources),
            "<source-embedded-module-declarations>",
            ownership_payload,
            migration_path=request.evidence_migration_path.as_posix(),
            migration_payload=migration_payload,
            profile_path=request.evidence_profile_matrix_path.as_posix(),
            profile_payload=profile_path.read_bytes(),
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
        request: _HarnessProjectionRequest,
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

    def execute(
        self, request: _HarnessProjectionRequest, workspace_root: Path
    ) -> _HarnessProjectionGeneration:
        """Build complete candidate artifacts beneath ``workspace_root``."""
        if type(request) is not _HarnessProjectionRequest:
            raise TypeError("request must be _HarnessProjectionRequest")
        if (
            not isinstance(workspace_root, Path)
            or not workspace_root.is_absolute()
            or not workspace_root.is_dir()
        ):
            raise ValueError("workspace_root must be an absolute existing directory")
        root = request.repository_root
        configuration = request.harness_configuration
        agent_roots = (
            tuple(Path(path) for path in configuration.catalogs.agent_roots)
            if configuration is not None
            else (Path(".pi/agents"),)
        )
        agent_resolver = PiHarnessAgentDefinitionResolver()
        agent_paths = sorted(
            (
                path
                for agent_root in agent_roots
                for path in (root / agent_root).glob("*.md")
            ),
            key=lambda item: item.relative_to(root).as_posix(),
        )
        agent_definitions = tuple(
            agent_resolver.execute(
                path.relative_to(root).as_posix(),
                path.read_bytes(),
                request.pi_harness_configuration,
            )
            for path in agent_paths
        )
        module_inventory, evidence_models, evidence_predecessors = (
            self._canonical_evidence_corpus(request)
        )
        resource_corpus = self._canonical_resource_corpus(request)
        candidate_database = self._candidate_path(workspace_root, request.database_path)
        candidate_database.parent.mkdir(parents=True, exist_ok=True)
        _ControlDatabase.reconstruct(candidate_database, (_SCHEMA + "\n").encode())
        connection = sqlite3.connect(candidate_database)
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
                    (
                        "evidence_inventory_test_root",
                        configuration.python_conformance.test_root
                        if configuration is not None
                        else "python/tests",
                    ),
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
                agent_definitions,
                task_root=(
                    Path(configuration.catalogs.task_root)
                    if configuration is not None
                    else Path("harness/tasks")
                ),
                skill_roots=(
                    tuple(Path(path) for path in configuration.catalogs.skill_roots)
                    if configuration is not None
                    else (Path(".agents/skills"), Path(".pi/skills"))
                ),
                checkpoint_roots=(
                    tuple(
                        Path(path) for path in configuration.catalogs.checkpoint_roots
                    )
                    if configuration is not None
                    else (Path(".pi/checkpoints"),)
                ),
                test_root=(
                    Path(configuration.python_conformance.test_root)
                    if configuration is not None
                    else Path("python/tests")
                ),
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
                task_root=(
                    Path(configuration.catalogs.task_root)
                    if configuration is not None
                    else Path("harness/tasks")
                ),
                database_path=request.database_path,
                resource_manifest_paths=(
                    request.generic_resource_manifest_path,
                    request.local_resource_manifest_path,
                )
                if request.generic_resource_manifest_path is not None
                and request.local_resource_manifest_path is not None
                else (
                    Path("harness/pi/resource-manifest.json"),
                    Path("harness/local/resource-manifest.json"),
                ),
                resource_roots=(
                    request.generic_resource_root_path,
                    request.local_resource_root_path,
                )
                if request.generic_resource_root_path is not None
                and request.local_resource_root_path is not None
                else (Path("harness/pi"), Path("harness/local")),
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
                "INSERT INTO harness_metadata VALUES (?,?)",
                ("semantic_digest", digest),
            )
            connection.commit()
            digest = database.semantic_digest()
            connection.execute(
                "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
                (digest,),
            )
            connection.commit()
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
        sql_path = (
            Path(configuration.persistence.sql_export_path)
            if configuration is not None
            else Path("harness/state/harness-control.sql")
        )
        manifest_path = (
            Path(configuration.persistence.projection_manifest_path)
            if configuration is not None
            else Path("harness/state/projection-manifest.json")
        )
        manifest_bytes = _ControlProjector.projection_manifest_bytes(
            control_schema_version=CONTROL_SCHEMA_VERSION,
            semantic_database_digest=final_digest,
            sql_path=sql_path,
            sql_bytes=sql_bytes,
            projections=projections,
            unresolved_naming_issues=tuple(sorted(unresolved)),
        )
        _ControlDatabase.reconstruct(candidate_database, sql_bytes)
        payloads: dict[Path, bytes] = {
            request.database_path: candidate_database.read_bytes(),
            sql_path: sql_bytes,
            manifest_path: manifest_bytes,
            **{
                Path(path): payload
                for path, (_kind, payload) in sorted(projections.items())
            },
        }
        confined_candidates = {
            relative: self._candidate_path(workspace_root, relative)
            for relative in payloads
        }
        artifacts: list[tuple[Path, Path]] = []
        for relative, payload in sorted(
            payloads.items(), key=lambda item: item[0].as_posix()
        ):
            candidate = confined_candidates[relative]
            candidate.parent.mkdir(parents=True, exist_ok=True)
            if candidate != candidate_database:
                candidate.write_bytes(payload)
            artifacts.append((relative, candidate))
        return _HarnessProjectionGeneration(
            workspace_root,
            candidate_database,
            tuple(artifacts),
            CONTROL_SCHEMA_VERSION,
            final_digest,
            counts,
            tuple(sorted(unresolved)),
            tuple(sorted(projections)),
        )

    def validate(self, generation: _HarnessProjectionGeneration) -> None:
        """Validate one complete candidate before comparison or publication."""
        if type(generation) is not _HarnessProjectionGeneration:
            raise TypeError("generation must be _HarnessProjectionGeneration")
        expected = {relative for relative, _candidate in generation.artifacts}
        if len(expected) != len(generation.artifacts):
            raise RuntimeError("candidate generation contains duplicate output paths")
        for relative, candidate in generation.artifacts:
            if not candidate.is_file():
                raise RuntimeError(f"candidate artifact is missing: {relative}")
            candidate.resolve().relative_to(generation.workspace_root.resolve())
        with sqlite3.connect(generation.database_path) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            foreign_keys = tuple(connection.execute("PRAGMA foreign_key_check"))
            schema_version = connection.execute(
                "SELECT value FROM harness_metadata WHERE key='control_schema_version'"
            ).fetchone()
            stored_digest = connection.execute(
                "SELECT value FROM harness_metadata WHERE key='semantic_digest'"
            ).fetchone()
            semantic_digest = _ControlDatabase(connection).normalized_semantic_digest()
        if integrity != "ok" or foreign_keys:
            raise RuntimeError("candidate database integrity validation failed")
        if schema_version != (str(generation.schema_version),):
            raise RuntimeError("candidate database schema version disagrees")
        if stored_digest != (generation.semantic_digest,):
            raise RuntimeError("candidate stored semantic digest disagrees")
        if semantic_digest != generation.semantic_digest:
            raise RuntimeError("candidate database semantic content disagrees")
