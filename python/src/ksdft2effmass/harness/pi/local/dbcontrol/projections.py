"""Deterministic project-local projections from authoritative control state."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .constants import _GENERATOR_ID
from .encoding import _ControlEncoding


class _ControlProjector:
    """Own deterministic projections for one control connection."""

    __slots__ = ("connection",)

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def _task_payload(self, task_id: str) -> dict[str, Any]:
        connection = self.connection
        row = connection.execute(
            "SELECT * FROM task_definition WHERE task_id=?", (task_id,)
        ).fetchone()
        if row is None:
            raise KeyError(task_id)
        keys = [
            item[1] for item in connection.execute("PRAGMA table_info(task_definition)")
        ]
        task = dict(zip(keys, row, strict=True))
        state = connection.execute(
            "SELECT lifecycle_status FROM task_state WHERE task_id=?", (task_id,)
        ).fetchone()
        relationships = list(
            connection.execute(
                "SELECT target_task_id,relationship_kind FROM task_relationship "
                "WHERE source_task_id=? ORDER BY relationship_kind,target_task_id",
                (task_id,),
            )
        )
        text = {
            (kind, ordinal): value
            for kind, ordinal, value in connection.execute(
                "SELECT text_kind,ordinal,value FROM task_text WHERE task_id=? "
                "ORDER BY text_kind,ordinal",
                (task_id,),
            )
        }

        def values(kind: str) -> list[str]:
            return [value for (found, _), value in text.items() if found == kind]

        payload: dict[str, Any] = {
            "schema_version": task["schema_version"],
            "task_id": task_id,
            "title": task["title"],
            "status": state[0] if state else "inactive",
        }
        if task["schema_version"] >= 2:
            payload["status_detail"] = task["status_detail"]
        payload.update(
            {
                "parent_task_id": next(
                    (target for target, kind in relationships if kind == "child_of"),
                    None,
                ),
                "task_prerequisite_ids": sorted(
                    target for target, kind in relationships if kind == "depends_on"
                ),
                "external_prerequisite_ids": [
                    row[0]
                    for row in connection.execute(
                        "SELECT prerequisite_id FROM task_external_prerequisite "
                        "WHERE task_id=? ORDER BY ordinal",
                        (task_id,),
                    )
                ],
                "superseded_by_task_ids": sorted(
                    target for target, kind in relationships if kind == "superseded_by"
                ),
                "explicit_activation_required": bool(
                    task["explicit_activation_required"]
                ),
                "objective": task["objective"],
                "authority_reference_paths": values("authority_reference"),
                "authorized_scope": values("authorized_scope"),
                "completion_criteria": values("completion_criterion"),
                "exclusions": values("exclusion"),
                "intake_path": task["intake_path"],
                "archived_source": None
                if task["archive_path"] is None
                else {"path": task["archive_path"], "sha256": task["archive_sha256"]},
            }
        )
        if task["schema_version"] == 2:
            payload.pop("superseded_by_task_ids")
        return payload

    def _task_markdown(
        self, task: dict[str, Any], previous_id: str | None, next_id: str | None
    ) -> bytes:
        nav = ["[Task index](index.md)"]
        if previous_id is not None:
            nav.append(f"[Previous](./{previous_id}.md)")
        if next_id is not None:
            nav.append(f"[Next](./{next_id}.md)")

        def bullets(values: list[str]) -> str:
            return "\n".join(f"- {value}" for value in values) if values else "None."

        relationships = []
        if task["parent_task_id"] is not None:
            relationships.append(f"- Parent: `{task['parent_task_id']}`")
        relationships.extend(
            f"- Depends on: `{item}`" for item in task["task_prerequisite_ids"]
        )
        relationships.extend(
            f"- External prerequisite: `{item}`"
            for item in task["external_prerequisite_ids"]
        )
        relationships.extend(
            f"- Superseded by: `{item}`"
            for item in task.get("superseded_by_task_ids", [])
        )
        archive = task["archived_source"]
        historical = (
            "No archived source."
            if archive is None
            else f"`{archive['path']}` (`sha256:{archive['sha256']}`)"
        )
        status_suffix = (
            ": " + task["status_detail"] if task.get("status_detail") else ""
        )
        text = (
            "<!-- Generated from SQLite control state; do not edit. -->\n"
            f"# {task['title']}\n\n"
            f"{' · '.join(nav)}\n\n"
            "## Status\n\n"
            f"`{task['status']}`{status_suffix}\n\n"
            "## Objective\n\n"
            f"{task['objective']}\n\n"
            "## Parent and prerequisites\n\n"
            f"{chr(10).join(relationships) if relationships else 'None.'}\n\n"
            "## Authority references\n\n"
            f"{bullets(task['authority_reference_paths'])}\n\n"
            "## Authorized scope\n\n"
            f"{bullets(task['authorized_scope'])}\n\n"
            "## Completion criteria\n\n"
            f"{bullets(task['completion_criteria'])}\n\n"
            "## Exclusions\n\n"
            f"{bullets(task['exclusions'])}\n\n"
            "## Historical source\n\n"
            f"{historical}\n"
        )
        return text.encode()

    def render_all(self) -> dict[str, tuple[str, bytes]]:
        connection = self.connection
        ids = [
            row[0]
            for row in connection.execute(
                "SELECT task_id FROM task_definition ORDER BY task_id"
            )
        ]
        result: dict[str, tuple[str, bytes]] = {}
        tasks = {task_id: self._task_payload(task_id) for task_id in ids}
        for index, task_id in enumerate(ids):
            result[f"harness/tasks/{task_id}.json"] = (
                "task-json",
                _ControlEncoding.json_bytes(tasks[task_id]),
            )
            result[f"docs/harness/tasks/{task_id}.md"] = (
                "task-markdown",
                self._task_markdown(
                    tasks[task_id],
                    ids[index - 1] if index else None,
                    ids[index + 1] if index + 1 < len(ids) else None,
                ),
            )
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
            "generated_from": "harness/state/harness-control.sqlite3",
            "nodes": [{"task_id": task_id} for task_id in ids],
            "edges": edges,
        }
        result["harness/task-graph.json"] = (
            "task-graph-json",
            _ControlEncoding.json_bytes(graph),
        )
        lines = [
            "<!-- Generated from harness/state/harness-control.sqlite3; "
            "do not edit. -->",
            "# Harness Tasks",
            "",
        ]
        lines.extend(
            f"- [`{task_id}`]({task_id}.md) — {tasks[task_id]['title']} "
            f"(`{tasks[task_id]['status']}`)"
            for task_id in ids
        )
        result["docs/harness/tasks/index.md"] = (
            "task-index-markdown",
            ("\n".join(lines) + "\n").encode(),
        )
        for layer, path, manifest_id, version, extends in (
            (
                "generic",
                "harness/pi/resource-manifest.json",
                "pih.generic.resources",
                5,
                None,
            ),
            (
                "project_local",
                "harness/local/resource-manifest.json",
                "ksdft2effmass.local.resources",
                11,
                "pih.generic.resources",
            ),
        ):
            resources = []
            for (
                resource_id,
                kind,
                source_path,
                digest,
                format_version,
            ) in connection.execute(
                "SELECT resource_id,resource_kind,source_path,sha256,format_version "
                "FROM resource_definition WHERE layer=? ORDER BY resource_id",
                (layer,),
            ):
                prefix = "harness/pi/" if layer == "generic" else "harness/local/"
                dependencies = [
                    row[0]
                    for row in connection.execute(
                        "SELECT prerequisite_resource_id FROM resource_dependency "
                        "WHERE dependent_resource_id=? "
                        "ORDER BY prerequisite_resource_id",
                        (resource_id,),
                    )
                ]
                resources.append(
                    {
                        "content_identity": {
                            "algorithm": "sha256",
                            "digest": digest,
                            "schema_version": 1,
                        },
                        "dependency_ids": dependencies,
                        "format_version": format_version,
                        "path": source_path.removeprefix(prefix),
                        "resource_id": resource_id,
                        "resource_kind": kind,
                        "schema_version": 1,
                    }
                )
            manifest = {
                "extends_manifest_id": extends,
                "layer": "generic" if layer == "generic" else "local",
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
        ) in connection.execute(
            "SELECT source_path,sha256,ownership_kind,owner_subject,evidence_class "
            "FROM test_module ORDER BY source_path"
        ):
            entry = {
                "conformance_status": "conforming",
                "content_sha256": digest,
                "evidence_class": evidence_class.replace("-", "_"),
                "mode": ownership,
                "path": source_path,
            }
            entry["sut" if ownership == "class_owned" else "artifact"] = subject
            modules.append(entry)
        node_count = int(
            connection.execute("SELECT COUNT(*) FROM test_node").fetchone()[0]
        )
        inventory = {
            "baseline_collected_node_count": 2383,
            "baseline_module_count": 182,
            "baseline_revision": "1a0c8ac35aa3e9bf3bdd6d11ba8afaf68c5bed06",
            "expected_collected_node_count": node_count,
            "expected_module_count": len(modules),
            "modules": modules,
            "schema_version": 1,
            "test_root": "python/tests",
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
