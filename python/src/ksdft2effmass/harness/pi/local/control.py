"""Authoritative SQLite-hybrid harness control state.

This module owns the project-local persistence boundary for structured harness
control data. Human-authored source, test, agent, skill, resource, schema,
fixture, decision, and documentation files remain authoritative for their
content; this database records their identities, relationships, classifications,
and lifecycle state. Runtime observations and telemetry are excluded.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONTROL_SCHEMA_VERSION = 1
CONTROL_DATABASE_PATH = Path("harness/state/harness-control.sqlite3")
CONTROL_SQL_PATH = Path("harness/state/harness-control.sql")
PROJECTION_MANIFEST_PATH = Path("harness/state/projection-manifest.json")
_GENERATOR_ID = "harness.control.projection-generator.v1"
_EVIDENCE_CLASSES = {
    "software_verification": "software-verification",
    "numerical_verification": "numerical-verification",
    "scientific_validation": "scientific-validation",
    "uncertainty_quantification": "uncertainty-quantification",
}
_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+(?:-[a-z0-9]+)*)+$")
_EVIDENCE_ID = re.compile(r"(?m)^Evidence ID:\s*(\S+)\s*$")
_SCHEMA = r"""
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA page_size = 4096;
CREATE TABLE harness_metadata (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
) WITHOUT ROWID;
CREATE TABLE task_definition (
  task_id TEXT PRIMARY KEY,
  schema_version INTEGER NOT NULL CHECK(schema_version IN (1,2,3)),
  title TEXT NOT NULL,
  objective TEXT NOT NULL,
  source_path TEXT NOT NULL UNIQUE,
  status_detail TEXT,
  explicit_activation_required INTEGER NOT NULL CHECK(explicit_activation_required IN (0,1)),
  intake_path TEXT,
  archive_path TEXT,
  archive_sha256 TEXT CHECK(archive_sha256 IS NULL OR length(archive_sha256)=64)
) WITHOUT ROWID;
CREATE TABLE task_relationship (
  source_task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  target_task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  relationship_kind TEXT NOT NULL CHECK(relationship_kind IN ('child_of','depends_on','superseded_by','ordered_before')),
  PRIMARY KEY(source_task_id,target_task_id,relationship_kind),
  CHECK(source_task_id<>target_task_id)
) WITHOUT ROWID;
CREATE TABLE task_external_prerequisite (
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  prerequisite_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  PRIMARY KEY(task_id,prerequisite_id), UNIQUE(task_id,ordinal)
) WITHOUT ROWID;
CREATE TABLE task_text (
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  text_kind TEXT NOT NULL CHECK(text_kind IN ('authority_reference','authorized_scope','completion_criterion','exclusion')),
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  value TEXT NOT NULL,
  PRIMARY KEY(task_id,text_kind,ordinal), UNIQUE(task_id,text_kind,value)
) WITHOUT ROWID;
CREATE TABLE task_state (
  task_id TEXT PRIMARY KEY REFERENCES task_definition(task_id),
  lifecycle_status TEXT NOT NULL,
  is_active INTEGER NOT NULL CHECK(is_active IN (0,1)),
  automatic_successor_enabled INTEGER NOT NULL CHECK(automatic_successor_enabled IN (0,1))
) WITHOUT ROWID;
CREATE UNIQUE INDEX one_active_task ON task_state(is_active) WHERE is_active=1;
CREATE TABLE task_state_event (
  event_id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=0),
  lifecycle_status TEXT NOT NULL,
  event_kind TEXT NOT NULL CHECK(event_kind IN ('imported','activated','completed','superseded','deferred')),
  UNIQUE(task_id,event_ordinal)
) WITHOUT ROWID;
CREATE TABLE evidence_claim (
  evidence_id TEXT PRIMARY KEY,
  evidence_class TEXT NOT NULL CHECK(evidence_class IN ('software-verification','numerical-verification','scientific-validation','uncertainty-quantification')),
  claim_summary TEXT NOT NULL,
  naming_status TEXT NOT NULL CHECK(naming_status IN ('semantic','temporary-legacy'))
) WITHOUT ROWID;
CREATE TABLE evidence_alias (
  alias_id TEXT PRIMARY KEY,
  evidence_id TEXT NOT NULL REFERENCES evidence_claim(evidence_id),
  alias_kind TEXT NOT NULL CHECK(alias_kind='historical')
) WITHOUT ROWID;
CREATE TABLE test_module (
  module_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  ownership_kind TEXT NOT NULL CHECK(ownership_kind IN ('class_owned','artifact_owned')),
  owner_subject TEXT NOT NULL,
  evidence_class TEXT NOT NULL CHECK(evidence_class IN ('software-verification','numerical-verification','scientific-validation','uncertainty-quantification'))
) WITHOUT ROWID;
CREATE TABLE evidence_owner (
  evidence_id TEXT PRIMARY KEY REFERENCES evidence_claim(evidence_id),
  module_id TEXT NOT NULL REFERENCES test_module(module_id),
  owner_node_id TEXT NOT NULL UNIQUE,
  owner_kind TEXT NOT NULL CHECK(owner_kind IN ('test_function','artifact_test'))
) WITHOUT ROWID;
CREATE TABLE test_node (
  node_id TEXT PRIMARY KEY,
  module_id TEXT NOT NULL REFERENCES test_module(module_id),
  evidence_id TEXT REFERENCES evidence_claim(evidence_id),
  parameter_id TEXT,
  CHECK(parameter_id IS NULL OR parameter_id GLOB '[a-z0-9_]*')
) WITHOUT ROWID;
CREATE TABLE agent_definition (
  agent_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  lifecycle TEXT NOT NULL CHECK(lifecycle IN ('durable','historical')),
  access_class TEXT NOT NULL CHECK(access_class IN ('writer','read_only')),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE skill_definition (
  skill_id TEXT PRIMARY KEY,
  canonical_path TEXT NOT NULL,
  live_path TEXT NOT NULL UNIQUE,
  descriptor_path TEXT,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE agent_skill_route (
  agent_id TEXT NOT NULL REFERENCES agent_definition(agent_id),
  skill_id TEXT NOT NULL REFERENCES skill_definition(skill_id),
  PRIMARY KEY(agent_id,skill_id)
) WITHOUT ROWID;
CREATE TABLE resource_definition (
  resource_id TEXT PRIMARY KEY,
  layer TEXT NOT NULL CHECK(layer IN ('generic','project_local')),
  resource_kind TEXT NOT NULL,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  format_version INTEGER NOT NULL CHECK(format_version>0),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE resource_dependency (
  dependent_resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  prerequisite_resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  PRIMARY KEY(dependent_resource_id,prerequisite_resource_id),
  CHECK(dependent_resource_id<>prerequisite_resource_id)
) WITHOUT ROWID;
CREATE TABLE resource_profile_membership (
  profile_id TEXT NOT NULL,
  resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  PRIMARY KEY(profile_id,resource_id), UNIQUE(profile_id,ordinal)
) WITHOUT ROWID;
CREATE TABLE decision_reference (
  decision_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  related_task_id TEXT REFERENCES task_definition(task_id),
  disposition TEXT,
  resolution_state TEXT NOT NULL CHECK(resolution_state IN ('resolved','unresolved'))
) WITHOUT ROWID;
CREATE TABLE projection_record (
  projection_path TEXT PRIMARY KEY,
  projection_kind TEXT NOT NULL CHECK(projection_kind IN ('task-json','task-graph-json','task-index-markdown','task-markdown','resource-manifest-json','evidence-module-inventory-json')),
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  byte_count INTEGER NOT NULL CHECK(byte_count>=0),
  generating_action_id TEXT NOT NULL
) WITHOUT ROWID;
"""  # noqa: E501
_TABLE_ORDER = (
    "harness_metadata",
    "task_definition",
    "task_relationship",
    "task_external_prerequisite",
    "task_text",
    "task_state",
    "task_state_event",
    "evidence_claim",
    "evidence_alias",
    "test_module",
    "evidence_owner",
    "test_node",
    "agent_definition",
    "skill_definition",
    "agent_skill_route",
    "resource_definition",
    "resource_dependency",
    "resource_profile_membership",
    "decision_reference",
    "projection_record",
)


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationRequest:
    """Explicit repository and destination for one control-state migration."""

    repository_root: Path
    database_path: Path = CONTROL_DATABASE_PATH

    def __post_init__(self) -> None:
        if (
            not isinstance(self.repository_root, Path)
            or not self.repository_root.is_absolute()
        ):
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if not isinstance(self.database_path, Path) or self.database_path.is_absolute():
            raise ValueError("database_path must be repository-relative")


@dataclass(frozen=True, slots=True)
class HarnessControlMigrationResult:
    """Immutable summary of migrated structured control state."""

    schema_version: int
    semantic_digest: str
    counts: tuple[tuple[str, int], ...]
    unresolved_naming_issues: tuple[str, ...]
    projection_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HarnessControlVerificationResult:
    """Immutable deterministic reconstruction and integrity result."""

    integrity_check: str
    foreign_key_issue_count: int
    semantic_digest: str
    reconstructed_semantic_digest: str
    raw_database_sha256: str
    reconstructed_database_sha256: str
    projections_identical: bool


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def _canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode()


def _slug(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return re.sub(r"-+", "-", value) or "unnamed"


def _rows(connection: sqlite3.Connection, table: str) -> list[tuple[Any, ...]]:
    columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
    order = ",".join(f'"{name}"' for name in columns)
    return list(connection.execute(f'SELECT {order} FROM "{table}" ORDER BY {order}'))


def semantic_digest(connection: sqlite3.Connection) -> str:
    """Hash ordered logical table contents rather than SQLite file bytes."""
    tables = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_schema WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    payload = [(table, _rows(connection, table)) for table in tables]
    return _sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
    )


def _sql_literal(value: object) -> str:
    if value is None:
        return "NULL"
    if type(value) is int:
        return str(value)
    if type(value) is not str:
        raise TypeError(f"unsupported SQL literal {type(value).__name__}")
    return "'" + value.replace("'", "''") + "'"


def deterministic_sql_export(connection: sqlite3.Connection) -> bytes:
    """Return stable schema and ordered inserts for exact reconstruction."""
    schema_lines = _SCHEMA.strip().splitlines()
    pragma_lines = [line for line in schema_lines if line.startswith("PRAGMA ")]
    definition_lines = [line for line in schema_lines if not line.startswith("PRAGMA ")]
    lines = [
        "-- Generated from authoritative harness control state; do not edit.",
        *pragma_lines,
        "BEGIN IMMEDIATE;",
        *definition_lines,
    ]
    tables = _TABLE_ORDER
    for table in tables:
        columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
        names = ",".join(f'"{name}"' for name in columns)
        for row in _rows(connection, table):
            values = ",".join(_sql_literal(value) for value in row)
            lines.append(f'INSERT INTO "{table}" ({names}) VALUES ({values});')
    lines.extend(["COMMIT;", "PRAGMA wal_checkpoint(TRUNCATE);", ""])
    return "\n".join(lines).encode()


def _task_payload(connection: sqlite3.Connection, task_id: str) -> dict[str, Any]:
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
                (target for target, kind in relationships if kind == "child_of"), None
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
            "explicit_activation_required": bool(task["explicit_activation_required"]),
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
    task: dict[str, Any], previous_id: str | None, next_id: str | None
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
        f"- Superseded by: `{item}`" for item in task.get("superseded_by_task_ids", [])
    )
    archive = task["archived_source"]
    historical = (
        "No archived source."
        if archive is None
        else f"`{archive['path']}` (`sha256:{archive['sha256']}`)"
    )
    text = f"""<!-- Generated from SQLite control state; do not edit. -->
# {task["title"]}

{" · ".join(nav)}

## Status

`{task["status"]}`{": " + task["status_detail"] if task.get("status_detail") else ""}

## Objective

{task["objective"]}

## Parent and prerequisites

{chr(10).join(relationships) if relationships else "None."}

## Authority references

{bullets(task["authority_reference_paths"])}

## Authorized scope

{bullets(task["authorized_scope"])}

## Completion criteria

{bullets(task["completion_criteria"])}

## Exclusions

{bullets(task["exclusions"])}

## Historical source

{historical}
"""
    return text.encode()


def _projections(connection: sqlite3.Connection) -> dict[str, tuple[str, bytes]]:
    ids = [
        row[0]
        for row in connection.execute(
            "SELECT task_id FROM task_definition ORDER BY task_id"
        )
    ]
    result: dict[str, tuple[str, bytes]] = {}
    tasks = {task_id: _task_payload(connection, task_id) for task_id in ids}
    for index, task_id in enumerate(ids):
        result[f"harness/tasks/{task_id}.json"] = (
            "task-json",
            _json_bytes(tasks[task_id]),
        )
        result[f"docs/harness/tasks/{task_id}.md"] = (
            "task-markdown",
            _task_markdown(
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
    result["harness/task-graph.json"] = ("task-graph-json", _json_bytes(graph))
    lines = [
        "<!-- Generated from harness/state/harness-control.sqlite3; do not edit. -->",
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
                    "WHERE dependent_resource_id=? ORDER BY prerequisite_resource_id",
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
        result[path] = ("resource-manifest-json", _canonical_json_bytes(manifest))
    modules = []
    for source_path, digest, ownership, subject, evidence_class in connection.execute(
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
    node_count = int(connection.execute("SELECT COUNT(*) FROM test_node").fetchone()[0])
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
        _json_bytes(inventory),
    )
    return result


def _execute_script(path: Path, sql: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm", "-journal"):
        Path(str(path) + suffix).unlink(missing_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.executescript(sql.decode())
        connection.commit()
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        connection.close()


def _module_inventory(root: Path) -> list[dict[str, Any]]:
    path = root / ".pi/evidence/python-conformance/module-inventory.json"
    document = json.loads(path.read_text())
    return list(document["modules"])


def _canonical_evidence_id(module: dict[str, Any], function_name: str) -> str:
    path = Path(module["path"])
    parts = list(path.parts)
    try:
        start = parts.index("ksdft2effmass")
        domain = [_slug(item) for item in parts[start + 1 : -1]]
    except ValueError:
        domain = ["repository"]
    subject = _slug(path.stem.removeprefix("test__"))
    claim = ".".join(
        _slug(item) for item in function_name.removeprefix("test_").split("__")
    )
    prefix = _EVIDENCE_CLASSES[module["evidence_class"]]
    return ".".join((prefix, *(domain or ["root"]), subject, claim))


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


class HarnessControlMigrator:
    """Migrate file-backed control catalogs into one authoritative SQLite database."""

    __slots__ = ()

    def execute(
        self, request: HarnessControlMigrationRequest
    ) -> HarnessControlMigrationResult:
        """Create the database, SQL recovery text, and projections."""
        if type(request) is not HarnessControlMigrationRequest:
            raise TypeError("request must be HarnessControlMigrationRequest")
        root = request.repository_root
        database_path = root / request.database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        working = database_path.with_suffix(".building.sqlite3")
        _execute_script(working, (_SCHEMA + "\n").encode())
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
            self._migrate_tasks(connection, root)
            self._migrate_evidence(connection, root, unresolved)
            self._migrate_collected_nodes(connection, root, unresolved)
            self._migrate_agents_and_skills(connection, root)
            self._migrate_resources(connection, root)
            self._migrate_decisions(connection, root)
            connection.commit()
            projections = _projections(connection)
            for path, (kind, payload) in sorted(projections.items()):
                connection.execute(
                    "INSERT INTO projection_record VALUES (?,?,?,?,?)",
                    (path, kind, _sha256(payload), len(payload), _GENERATOR_ID),
                )
            connection.commit()
            digest = semantic_digest(connection)
            connection.execute(
                "INSERT INTO harness_metadata VALUES (?,?)", ("semantic_digest", digest)
            )
            connection.commit()
            digest = semantic_digest(connection)
            connection.execute(
                "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
                (digest,),
            )
            connection.commit()
            # The digest field is excluded from identity comparison by normalizing it.
            final_digest = _semantic_digest_normalized(connection)
            connection.execute(
                "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
                (final_digest,),
            )
            connection.commit()
            sql_bytes = deterministic_sql_export(connection)
        finally:
            connection.close()
        sql_path = root / CONTROL_SQL_PATH
        sql_path.write_bytes(sql_bytes)
        _execute_script(database_path, sql_bytes)
        working.unlink(missing_ok=True)
        for path, (_kind, payload) in sorted(projections.items()):
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        manifest = {
            "schema_version": 1,
            "control_schema_version": CONTROL_SCHEMA_VERSION,
            "semantic_database_digest": final_digest,
            "sql_export": {
                "path": CONTROL_SQL_PATH.as_posix(),
                "sha256": _sha256(sql_bytes),
                "byte_count": len(sql_bytes),
            },
            "projections": [
                {
                    "path": path,
                    "projection_kind": kind,
                    "sha256": _sha256(payload),
                    "byte_count": len(payload),
                    "generating_action": _GENERATOR_ID,
                }
                for path, (kind, payload) in sorted(projections.items())
            ],
            "unresolved_naming_issues": sorted(unresolved),
        }
        (root / PROJECTION_MANIFEST_PATH).write_bytes(_json_bytes(manifest))
        with sqlite3.connect(database_path) as final:
            counts = tuple(
                (
                    table,
                    int(final.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]),
                )
                for table in (
                    "task_definition",
                    "task_relationship",
                    "evidence_claim",
                    "evidence_alias",
                    "test_module",
                    "evidence_owner",
                    "test_node",
                    "agent_definition",
                    "skill_definition",
                    "resource_definition",
                    "decision_reference",
                    "projection_record",
                )
            )
        return HarnessControlMigrationResult(
            CONTROL_SCHEMA_VERSION,
            final_digest,
            counts,
            tuple(sorted(unresolved)),
            tuple(sorted(projections)),
        )

    @staticmethod
    def _migrate_tasks(connection: sqlite3.Connection, root: Path) -> None:
        task_paths = sorted(
            (root / "harness/tasks").glob("*.json"), key=lambda item: item.name
        )
        tasks: dict[str, dict[str, Any]] = {}
        for path in task_paths:
            task = json.loads(path.read_text())
            tasks[task["task_id"]] = task
        migration_id = "harness.simplification.round-2.sqlite-hybrid-cutover"
        tasks[migration_id] = {
            "schema_version": 3,
            "task_id": migration_id,
            "title": "Implement the complete SQLite-hybrid harness control cutover",
            "status": "completed",
            "status_detail": "bounded migration completed; no successor activated",
            "parent_task_id": None,
            "task_prerequisite_ids": ["harness.simplification.evidence.naming"],
            "external_prerequisite_ids": [],
            "superseded_by_task_ids": [],
            "explicit_activation_required": False,
            "objective": (
                "Consolidate structured harness control information in one tracked "
                "authoritative SQLite database while retaining executable code and "
                "human-authored content in ordinary files."
            ),
            "authority_reference_paths": ["AGENTS.md"],
            "authorized_scope": [
                "Migrate Tasks, evidence, tests, agents, skills, resources, "
                "decisions, and generated projection identities into the "
                "SQLite-hybrid control model."
            ],
            "completion_criteria": [
                "The deterministic database, SQL recovery representation, "
                "projections, reader cutover, and bounded validation agree."
            ],
            "exclusions": [
                "Runtime observations, telemetry, scientific calculations, protected "
                "execution, release actions, and successor activation remain excluded."
            ],
            "intake_path": None,
            "archived_source": None,
        }
        ids = set(tasks)
        for task_id, task in sorted(tasks.items()):
            archived = task.get("archived_source") or {}
            connection.execute(
                "INSERT INTO task_definition VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    task_id,
                    task["schema_version"],
                    task["title"],
                    task["objective"],
                    f"harness/tasks/{task_id}.json",
                    task.get("status_detail"),
                    int(task["explicit_activation_required"]),
                    task.get("intake_path"),
                    archived.get("path"),
                    archived.get("sha256"),
                ),
            )
            status = task["status"]
            connection.execute(
                "INSERT INTO task_state VALUES (?,?,?,?)",
                (task_id, status, int(status == "active"), 0),
            )
            event_kind = (
                "superseded"
                if "superseded" in status
                else "deferred"
                if "deferred" in status or status == "inactive"
                else "completed"
                if status != "active"
                else "activated"
            )
            connection.execute(
                "INSERT INTO task_state_event VALUES (?,?,?,?,?)",
                (
                    f"task-state.{_slug(task_id)}.imported",
                    task_id,
                    0,
                    status,
                    event_kind,
                ),
            )
            for kind, field in (
                ("authority_reference", "authority_reference_paths"),
                ("authorized_scope", "authorized_scope"),
                ("completion_criterion", "completion_criteria"),
                ("exclusion", "exclusions"),
            ):
                for index, value in enumerate(task[field]):
                    connection.execute(
                        "INSERT INTO task_text VALUES (?,?,?,?)",
                        (task_id, kind, index, value),
                    )
        for task_id, task in sorted(tasks.items()):
            if task.get("parent_task_id") in ids:
                connection.execute(
                    "INSERT INTO task_relationship VALUES (?,?,?)",
                    (task_id, task["parent_task_id"], "child_of"),
                )
            for dependency in task["task_prerequisite_ids"]:
                if dependency in ids:
                    connection.execute(
                        "INSERT INTO task_relationship VALUES (?,?,?)",
                        (task_id, dependency, "depends_on"),
                    )
            for index, dependency in enumerate(task["external_prerequisite_ids"]):
                connection.execute(
                    "INSERT INTO task_external_prerequisite VALUES (?,?,?)",
                    (task_id, dependency, index),
                )
            for replacement in task.get("superseded_by_task_ids", []):
                if replacement in ids:
                    connection.execute(
                        "INSERT INTO task_relationship VALUES (?,?,?)",
                        (task_id, replacement, "superseded_by"),
                    )
        graph = json.loads((root / "harness/task-graph.json").read_text())
        for edge in graph["edges"]:
            if (
                edge["kind"] in {"order", "ordered_before"}
                and edge["source"] in ids
                and edge["target"] in ids
            ):
                connection.execute(
                    "INSERT OR IGNORE INTO task_relationship VALUES (?,?,?)",
                    (edge["source"], edge["target"], "ordered_before"),
                )

    @staticmethod
    def _migrate_evidence(
        connection: sqlite3.Connection, root: Path, unresolved: list[str]
    ) -> None:
        for module in _module_inventory(root):
            path = root / module["path"]
            if not path.is_file():
                unresolved.append(f"unresolved test module: {module['path']}")
                continue
            source = path.read_bytes()
            tree = ast.parse(source, filename=module["path"])
            module_id = "test-module." + _slug(
                path.relative_to(root / "python/tests").with_suffix("").as_posix()
            ).replace("-", ".")
            subject = (
                module.get("sut")
                or module.get("artifact")
                or path.stem.removeprefix("test__")
            )
            connection.execute(
                "INSERT INTO test_module VALUES (?,?,?,?,?,?)",
                (
                    module_id,
                    module["path"],
                    _sha256(source),
                    module["mode"],
                    subject,
                    _EVIDENCE_CLASSES[module["evidence_class"]],
                ),
            )
            for node in ast.walk(tree):
                if not isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) or not node.name.startswith("test_"):
                    continue
                doc = ast.get_docstring(node, clean=False) or ""
                match = _EVIDENCE_ID.search(doc)
                owner_node = f"{module['path']}::{node.name}"
                old_id = match.group(1) if match is not None else None
                canonical = (
                    old_id
                    if old_id is not None
                    and _IDENTIFIER.fullmatch(old_id)
                    and old_id.split(".", 1)[0] in _EVIDENCE_CLASSES.values()
                    else _canonical_evidence_id(module, node.name)
                )
                naming = "semantic"
                claim_summary = (
                    node.name.removeprefix("test_")
                    .replace("__", ": ")
                    .replace("_", " ")
                )
                try:
                    connection.execute(
                        "INSERT INTO evidence_claim VALUES (?,?,?,?)",
                        (
                            canonical,
                            _EVIDENCE_CLASSES[module["evidence_class"]],
                            claim_summary,
                            naming,
                        ),
                    )
                    connection.execute(
                        "INSERT INTO evidence_owner VALUES (?,?,?,?)",
                        (
                            canonical,
                            module_id,
                            owner_node,
                            "test_function"
                            if module["mode"] == "class_owned"
                            else "artifact_test",
                        ),
                    )
                except sqlite3.IntegrityError as exc:
                    unresolved.append(
                        f"duplicate evidence identity or owner: {canonical} ({exc})"
                    )
                    continue
                if old_id is not None and old_id != canonical:
                    try:
                        connection.execute(
                            "INSERT INTO evidence_alias VALUES (?,?,?)",
                            (old_id, canonical, "historical"),
                        )
                    except sqlite3.IntegrityError:
                        unresolved.append(f"duplicate historical alias: {old_id}")

    @staticmethod
    def _migrate_collected_nodes(
        connection: sqlite3.Connection, root: Path, unresolved: list[str]
    ) -> None:
        completed = subprocess.run(
            [str(root / "python/.venv/bin/pytest"), "--collect-only", "-q"],
            cwd=root / "python",
            check=True,
            text=True,
            capture_output=True,
        )
        modules = {
            path: module_id
            for module_id, path in connection.execute(
                "SELECT module_id,source_path FROM test_module"
            )
        }
        owners = {
            (module_id, node_id.rsplit("::", 1)[-1]): evidence_id
            for evidence_id, module_id, node_id in connection.execute(
                "SELECT evidence_id,module_id,owner_node_id FROM evidence_owner"
            )
        }
        invalid_parameters: set[str] = set()
        for line in completed.stdout.splitlines():
            if not line.startswith("tests/") or "::" not in line:
                continue
            node_id = "python/" + line
            module_path, *parts = node_id.split("::")
            module_id = modules.get(module_path)
            if module_id is None:
                unresolved.append(f"unresolved collected test module: {module_path}")
                continue
            final = parts[-1]
            function_name = final.split("[", 1)[0]
            evidence_id = owners.get((module_id, function_name))
            if evidence_id is None:
                unresolved.append(
                    f"missing evidence owner for collected node: {node_id}"
                )
                continue
            parameter_id = None
            if "[" in final and final.endswith("]"):
                candidate = final.split("[", 1)[1][:-1]
                if re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", candidate):
                    parameter_id = candidate
                else:
                    invalid_parameters.add(candidate)
            connection.execute(
                "INSERT INTO test_node VALUES (?,?,?,?)",
                (node_id, module_id, evidence_id, parameter_id),
            )
        if invalid_parameters:
            unresolved.append(
                f"{len(invalid_parameters)} collected composite parameter IDs use "
                "non-snake-case pytest composition and require normalization"
            )

    @staticmethod
    def _migrate_agents_and_skills(connection: sqlite3.Connection, root: Path) -> None:
        skill_paths = sorted(
            (
                *root.glob(".pi/skills/*/SKILL.md"),
                *root.glob(".agents/skills/*/SKILL.md"),
            ),
            key=lambda item: item.as_posix(),
        )
        skill_ids: set[str] = set()
        for path in skill_paths:
            relative = path.relative_to(root).as_posix()
            meta = _frontmatter(path.read_text())
            skill_id = _slug(meta.get("name", path.parent.name)).replace("-", ".")
            if skill_id in skill_ids:
                skill_id = "project." + skill_id
            skill_ids.add(skill_id)
            canonical = root / "harness/pi/skills" / path.parent.name / "SKILL.md"
            descriptor = (
                root / "harness/pi/skills" / path.parent.name / "descriptor.json"
            )
            connection.execute(
                "INSERT INTO skill_definition VALUES (?,?,?,?,?,?)",
                (
                    skill_id,
                    canonical.relative_to(root).as_posix()
                    if canonical.exists()
                    else relative,
                    relative,
                    descriptor.relative_to(root).as_posix()
                    if descriptor.exists()
                    else None,
                    _sha256(path.read_bytes()),
                    1,
                ),
            )
        by_name = {
            row[0].replace(".", "-"): row[0]
            for row in connection.execute("SELECT skill_id FROM skill_definition")
        }
        for path in sorted(root.glob(".pi/agents/*.md"), key=lambda item: item.name):
            meta = _frontmatter(path.read_text())
            agent_id = _slug(meta.get("name", path.stem)).replace("-", ".")
            access = "writer" if meta.get("acceptanceRole") == "writer" else "read_only"
            connection.execute(
                "INSERT INTO agent_definition VALUES (?,?,?,?,?,?)",
                (
                    agent_id,
                    path.relative_to(root).as_posix(),
                    _sha256(path.read_bytes()),
                    "durable",
                    access,
                    1,
                ),
            )
            for name in (
                item.strip()
                for item in meta.get("skills", "").split(",")
                if item.strip()
            ):
                routed_skill_id = by_name.get(name)
                if routed_skill_id is not None:
                    connection.execute(
                        "INSERT OR IGNORE INTO agent_skill_route VALUES (?,?)",
                        (agent_id, routed_skill_id),
                    )

    @staticmethod
    def _migrate_resources(connection: sqlite3.Connection, root: Path) -> None:
        manifests = (
            (
                root / "harness/pi/resource-manifest.json",
                "generic",
                root / "harness/pi",
            ),
            (
                root / "harness/local/resource-manifest.json",
                "project_local",
                root / "harness/local",
            ),
        )
        resources: list[tuple[dict[str, Any], str, Path]] = []
        for manifest_path, layer, resource_root in manifests:
            document = json.loads(manifest_path.read_text())
            for resource in document["resources"]:
                resources.append((resource, layer, resource_root))
        ids = {resource["resource_id"] for resource, _, _ in resources}
        for resource, layer, resource_root in resources:
            path = resource_root / resource["path"]
            digest = (
                _sha256(path.read_bytes())
                if path.is_file()
                else resource["content_identity"]["digest"]
            )
            connection.execute(
                "INSERT INTO resource_definition VALUES (?,?,?,?,?,?,?)",
                (
                    resource["resource_id"],
                    layer,
                    resource["resource_kind"],
                    path.relative_to(root).as_posix(),
                    digest,
                    resource["format_version"],
                    1,
                ),
            )
        for resource, _layer, _resource_root in resources:
            for dependency in resource["dependency_ids"]:
                if dependency in ids:
                    connection.execute(
                        "INSERT INTO resource_dependency VALUES (?,?)",
                        (resource["resource_id"], dependency),
                    )
            if resource["resource_kind"] == "profile":
                for index, dependency in enumerate(resource["dependency_ids"]):
                    if dependency in ids:
                        connection.execute(
                            "INSERT OR IGNORE INTO resource_profile_membership "
                            "VALUES (?,?,?)",
                            (resource["resource_id"], dependency, index),
                        )

    @staticmethod
    def _migrate_decisions(connection: sqlite3.Connection, root: Path) -> None:
        for path in sorted(
            (root / ".pi/checkpoints").glob("*.json"), key=lambda item: item.name
        ):
            if path.name.endswith("schema.json"):
                continue
            document = json.loads(path.read_text())
            decision_id = document.get("checkpoint_id") or path.stem
            status = str(document.get("status", "unresolved"))
            resolved = (
                status in {"resolved", "accepted", "cancelled", "superseded"}
                or document.get("resolved_at") is not None
            )
            disposition = document.get("normalized_decision")
            if disposition is not None and type(disposition) is not str:
                disposition = json.dumps(
                    disposition,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            task_id = document.get("task_id")
            if (
                task_id is not None
                and connection.execute(
                    "SELECT 1 FROM task_definition WHERE task_id=?", (task_id,)
                ).fetchone()
                is None
            ):
                task_id = None
            connection.execute(
                "INSERT INTO decision_reference VALUES (?,?,?,?,?,?)",
                (
                    decision_id,
                    path.relative_to(root).as_posix(),
                    _sha256(path.read_bytes()),
                    task_id,
                    disposition,
                    "resolved" if resolved else "unresolved",
                ),
            )


class HarnessControlVerifier:
    """Verify integrity, foreign keys, semantic identity, and SQL reconstruction."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> HarnessControlVerificationResult:
        """Reconstruct the database and compare logical and raw identities."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        database = repository_root / CONTROL_DATABASE_PATH
        sql_path = repository_root / CONTROL_SQL_PATH
        reconstructed = database.with_name("harness-control.reconstructed.sqlite3")
        _execute_script(reconstructed, sql_path.read_bytes())
        try:
            with (
                sqlite3.connect(database) as source,
                sqlite3.connect(reconstructed) as target,
            ):
                integrity = str(source.execute("PRAGMA integrity_check").fetchone()[0])
                foreign = len(source.execute("PRAGMA foreign_key_check").fetchall())
                source_digest = _semantic_digest_normalized(source)
                target_digest = _semantic_digest_normalized(target)
                source_projections = _projections(source)
                target_projections = _projections(target)
            return HarnessControlVerificationResult(
                integrity,
                foreign,
                source_digest,
                target_digest,
                _sha256(database.read_bytes()),
                _sha256(reconstructed.read_bytes()),
                source_projections == target_projections,
            )
        finally:
            reconstructed.unlink(missing_ok=True)
            Path(str(reconstructed) + "-wal").unlink(missing_ok=True)
            Path(str(reconstructed) + "-shm").unlink(missing_ok=True)


def _semantic_digest_normalized(connection: sqlite3.Connection) -> str:
    current = connection.execute(
        "SELECT value FROM harness_metadata WHERE key='semantic_digest'"
    ).fetchone()
    connection.execute(
        "UPDATE harness_metadata SET value='' WHERE key='semantic_digest'"
    )
    digest = semantic_digest(connection)
    connection.execute(
        "UPDATE harness_metadata SET value=? WHERE key='semantic_digest'",
        (current[0] if current else "",),
    )
    return digest
