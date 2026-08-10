"""Thin orchestration for repository-specific control migration."""

from __future__ import annotations

import sqlite3

from .constants import (
    _GENERATOR_ID,
    CONTROL_SCHEMA_VERSION,
    CONTROL_SQL_PATH,
    PROJECTION_MANIFEST_PATH,
)
from .database import (
    _execute_script,
    _semantic_digest_normalized,
    deterministic_sql_export,
    semantic_digest,
)
from .encoding import _json_bytes, _sha256
from .ingestion import _RepositoryControlIngestor
from .projections import _projections
from .records import HarnessControlMigrationRequest, HarnessControlMigrationResult
from .schema import _SCHEMA


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
        ingestor = _RepositoryControlIngestor()
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
            ingestor._migrate_tasks(connection, root)
            ingestor._migrate_evidence(connection, root, unresolved)
            ingestor._migrate_collected_nodes(connection, root, unresolved)
            ingestor._migrate_agents_and_skills(connection, root)
            ingestor._migrate_resources(connection, root)
            ingestor._migrate_decisions(connection, root)
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
        for obsolete in (
            root / "harness/tasks/H5.json",
            root / "docs/harness/tasks/H5.md",
        ):
            obsolete.unlink(missing_ok=True)
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
                    "task_alias",
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
