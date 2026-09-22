"""Deterministic project-local projections from authoritative control state."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from ....task import ArchivedTaskSource, HarnessTask, HarnessTaskSerializer
from ...resources import ResourceManifest
from ..task_catalog import _TaskCatalogSource
from .constants import _GENERATOR_ID
from .encoding import _ControlEncoding

type _SqlValue = str | int | float | bytes | None
type _SqlRow = tuple[_SqlValue, ...]


class _ControlProjector:
    """Own deterministic projections for one control connection."""

    __slots__ = (
        "connection",
        "evidence_profiles",
        "resource_manifests",
        "task_roots",
        "database_path",
        "resource_manifest_paths",
        "resource_roots",
    )

    def __init__(
        self,
        connection: sqlite3.Connection,
        evidence_profiles: Mapping[str, str] | None = None,
        resource_manifests: tuple[ResourceManifest, ResourceManifest] | None = None,
        *,
        task_roots: tuple[Path, ...] = (),
        database_path: Path = Path("harness/state/harness-control.sqlite3"),
        resource_manifest_paths: tuple[Path, Path] = (
            Path("harness/pi/resource-manifest.json"),
            Path("harness/local/resource-manifest.json"),
        ),
        resource_roots: tuple[Path, Path] = (
            Path("harness/pi"),
            Path("harness/local"),
        ),
    ) -> None:
        self.connection = connection
        self.evidence_profiles = dict(evidence_profiles or {})
        self.resource_manifests = resource_manifests
        self.task_roots = task_roots
        self.database_path = database_path
        self.resource_manifest_paths = resource_manifest_paths
        self.resource_roots = resource_roots

    def _rows(
        self, statement: str, parameters: tuple[_SqlValue, ...] = ()
    ) -> tuple[_SqlRow, ...]:
        return cast(
            tuple[_SqlRow, ...], tuple(self.connection.execute(statement, parameters))
        )

    @staticmethod
    def _text(value: _SqlValue) -> str:
        if type(value) is not str:
            raise TypeError("Task projection text must be a built-in string")
        return value

    def _optional_text(self, value: _SqlValue) -> str | None:
        return None if value is None else self._text(value)

    @staticmethod
    def _integer(value: _SqlValue) -> int:
        if type(value) is not int:
            raise TypeError("Task projection integer must exclude booleans")
        return value

    def _task_text(self, task_id: str, kind: str) -> tuple[str, ...]:
        return tuple(
            self._text(row[0])
            for row in self._rows(
                "SELECT value FROM task_text WHERE task_id=? AND text_kind=? "
                "ORDER BY ordinal",
                (task_id, kind),
            )
        )

    def _task_source(self, task_id: str) -> _TaskCatalogSource:
        rows = self._rows(
            "SELECT schema_version,title,objective,source_path,status_detail,"
            "explicit_activation_required,intake_path,archive_path,archive_sha256,"
            "documentation_path FROM task_definition WHERE task_id=?",
            (task_id,),
        )
        if len(rows) != 1:
            raise ValueError("Task definition must exist exactly once")
        row = rows[0]
        states = self._rows(
            "SELECT lifecycle_status FROM task_state WHERE task_id=?", (task_id,)
        )
        if len(states) != 1:
            raise ValueError("Task projection requires its represented lifecycle state")
        relationships = tuple(
            (self._text(value[0]), self._text(value[1]))
            for value in self._rows(
                "SELECT target_task_id,relationship_kind FROM task_relationship "
                "WHERE source_task_id=? ORDER BY relationship_kind,target_task_id",
                (task_id,),
            )
        )
        if any(
            kind not in {"child_of", "depends_on", "superseded_by"}
            for _, kind in relationships
        ):
            raise ValueError("unsupported Task relationship in projection")
        parents = tuple(target for target, kind in relationships if kind == "child_of")
        if len(parents) > 1:
            raise ValueError("Task projection cannot have multiple parents")
        flag = self._integer(row[5])
        if flag not in (0, 1):
            raise ValueError("Task activation flag must be represented as zero or one")
        archived_path = self._optional_text(row[7])
        archived_digest = self._optional_text(row[8])
        if (archived_path is None) != (archived_digest is None):
            raise ValueError("archive path and digest must be jointly present")
        archived = None
        if archived_path is not None and archived_digest is not None:
            archived = ArchivedTaskSource(archived_path, archived_digest)
        task = HarnessTask(
            self._integer(row[0]),
            task_id,
            self._text(row[1]),
            self._text(states[0][0]),
            self._optional_text(row[4]),
            parents[0] if parents else None,
            tuple(target for target, kind in relationships if kind == "depends_on"),
            tuple(
                self._text(value[0])
                for value in self._rows(
                    "SELECT prerequisite_id FROM task_external_prerequisite "
                    "WHERE task_id=? ORDER BY ordinal",
                    (task_id,),
                )
            ),
            tuple(target for target, kind in relationships if kind == "superseded_by"),
            bool(flag),
            self._text(row[2]),
            self._task_text(task_id, "authority_reference"),
            self._task_text(task_id, "authorized_scope"),
            self._task_text(task_id, "completion_criterion"),
            self._task_text(task_id, "exclusion"),
            self._optional_text(row[6]),
            archived,
            self._optional_text(row[9]),
        )
        source = _TaskCatalogSource(self._text(row[3]), task)
        if Path(source.source_path).parent not in self.task_roots:
            raise ValueError("stored Task source path is outside the selected catalogs")
        return source

    def render_all(self) -> dict[str, tuple[str, bytes]]:
        connection = self.connection
        ids = [
            self._text(row[0])
            for row in self._rows(
                "SELECT task_id FROM task_definition ORDER BY task_id"
            )
        ]
        result: dict[str, tuple[str, bytes]] = {}
        serializer = HarnessTaskSerializer()
        for task_id in ids:
            source = self._task_source(task_id)
            result[source.source_path] = ("task-json", serializer.execute(source.task))
        edges = [
            {"source": source, "target": target, "kind": kind}
            for source, target, kind in connection.execute(
                "SELECT source_task_id,target_task_id,relationship_kind "
                "FROM task_relationship ORDER BY relationship_kind,source_task_id,"
                "target_task_id"
            )
        ]
        graph = {
            "schema_version": 2,
            "generated_from": self.database_path.as_posix(),
            "nodes": [{"task_id": task_id} for task_id in ids],
            "edges": edges,
        }
        result["harness/task-graph.json"] = (
            "task-graph-json",
            _ControlEncoding.json_bytes(graph),
        )
        default_manifests = (
            (
                "generic",
                "harness/pi/resource-manifest.json",
                "pih.generic.resources",
                6,
                None,
            ),
            (
                "project_local",
                "harness/local/resource-manifest.json",
                "ksdft2effmass.local.resources",
                12,
                "pih.generic.resources",
            ),
        )
        selected_manifests = self.resource_manifests
        for index, manifest_defaults in enumerate(default_manifests):
            layer, _default_path, default_id, default_version, default_extends = (
                manifest_defaults
            )
            path = self.resource_manifest_paths[index].as_posix()
            selected = None if selected_manifests is None else selected_manifests[index]
            manifest_id = default_id if selected is None else selected.manifest_id
            version = default_version if selected is None else selected.manifest_version
            extends = (
                default_extends if selected is None else selected.extends_manifest_id
            )
            manifest_layer = (
                ("generic" if layer == "generic" else "local")
                if selected is None
                else selected.layer
            )
            declared = (
                {}
                if selected is None
                else {resource.resource_id: resource for resource in selected.resources}
            )
            resources = []
            rows = connection.execute(
                "SELECT resource_id,resource_kind,source_path,sha256,format_version "
                "FROM resource_definition WHERE layer=? ORDER BY resource_id",
                (layer,),
            )
            for resource_id, kind, source_path, digest, format_version in rows:
                dependencies = [
                    row[0]
                    for row in connection.execute(
                        "SELECT prerequisite_resource_id FROM resource_dependency "
                        "WHERE dependent_resource_id=? "
                        "ORDER BY prerequisite_resource_id",
                        (resource_id,),
                    )
                ]
                reference = declared.get(resource_id)
                prefix = self.resource_roots[index].as_posix() + "/"
                resources.append(
                    {
                        "content_identity": {
                            "algorithm": "sha256",
                            "digest": digest,
                            "schema_version": 1,
                        },
                        "dependency_ids": dependencies,
                        "format_version": format_version,
                        "path": (
                            source_path.removeprefix(prefix)
                            if reference is None
                            else reference.path
                        ),
                        "resource_id": resource_id,
                        "resource_kind": kind,
                        "schema_version": 1,
                    }
                )
            manifest = {
                "extends_manifest_id": extends,
                "layer": manifest_layer,
                "manifest_id": manifest_id,
                "manifest_version": version,
                "resources": resources,
                "schema_version": 1,
            }
            result[path] = (
                "resource-manifest-json",
                _ControlEncoding.canonical_json_bytes(manifest),
            )
        modules = []
        for (
            source_path,
            digest,
            ownership,
            subject,
            evidence_class,
            evidence_profile,
        ) in connection.execute(
            "SELECT source_path,sha256,ownership_kind,owner_subject,"
            "evidence_class,evidence_profile FROM test_module ORDER BY source_path"
        ):
            entry = {
                "conformance_status": "conforming",
                "content_sha256": digest,
                "evidence_class": evidence_class.replace("-", "_"),
                "mode": ownership,
                "path": source_path,
            }
            entry["sut" if ownership == "class_owned" else "artifact"] = subject
            entry["evidence_profile"] = evidence_profile
            modules.append(entry)
        node_count = int(
            connection.execute("SELECT COUNT(*) FROM test_node").fetchone()[0]
        )
        metadata = dict(connection.execute("SELECT key,value FROM harness_metadata"))
        inventory = {
            "baseline_collected_node_count": int(
                metadata.get("evidence_inventory_baseline_collected_node_count", "2383")
            ),
            "baseline_module_count": int(
                metadata.get("evidence_inventory_baseline_module_count", "182")
            ),
            "baseline_revision": metadata.get(
                "evidence_inventory_baseline_revision",
                "1a0c8ac35aa3e9bf3bdd6d11ba8afaf68c5bed06",
            ),
            "expected_collected_node_count": node_count,
            "expected_module_count": len(modules),
            "modules": modules,
            "schema_version": 1,
            "test_root": metadata.get("evidence_inventory_test_root", "python/tests"),
        }
        result[".pi/evidence/python-conformance/module-inventory.json"] = (
            "evidence-module-inventory-json",
            _ControlEncoding.json_bytes(inventory),
        )
        return result

    @classmethod
    def projection_manifest_bytes(
        cls,
        *,
        control_schema_version: int,
        semantic_database_digest: str,
        sql_path: Path,
        sql_bytes: bytes,
        projections: Mapping[str, tuple[str, bytes]],
        unresolved_naming_issues: tuple[str, ...],
    ) -> bytes:
        """Return the exact projection-manifest wire representation."""
        manifest = {
            "schema_version": 1,
            "control_schema_version": control_schema_version,
            "semantic_database_digest": semantic_database_digest,
            "sql_export": {
                "path": sql_path.as_posix(),
                "sha256": _ControlEncoding.sha256(sql_bytes),
                "byte_count": len(sql_bytes),
            },
            "projections": [
                {
                    "path": path,
                    "projection_kind": kind,
                    "sha256": _ControlEncoding.sha256(payload),
                    "byte_count": len(payload),
                    "generating_action": _GENERATOR_ID,
                }
                for path, (kind, payload) in sorted(projections.items())
            ],
            "unresolved_naming_issues": sorted(unresolved_naming_issues),
        }
        return _ControlEncoding.json_bytes(manifest)
