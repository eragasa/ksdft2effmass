"""Thin orchestration for repository-specific control migration."""

from __future__ import annotations

import sqlite3

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
            _RepositoryControlIngestor(connection, root, unresolved).execute()
            connection.commit()
            projector = _ControlProjector(connection)
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
        finally:
            connection.close()
        sql_path = root / CONTROL_SQL_PATH
        sql_path.write_bytes(sql_bytes)
        _ControlDatabase.reconstruct(database_path, sql_bytes)
        working.unlink(missing_ok=True)
        for path, (_kind, payload) in sorted(projections.items()):
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        manifest_bytes = _ControlProjector.projection_manifest_bytes(
            control_schema_version=CONTROL_SCHEMA_VERSION,
            semantic_database_digest=final_digest,
            sql_path=CONTROL_SQL_PATH,
            sql_bytes=sql_bytes,
            projections=projections,
            unresolved_naming_issues=tuple(sorted(unresolved)),
        )
        (root / PROJECTION_MANIFEST_PATH).write_bytes(manifest_bytes)
        with sqlite3.connect(database_path) as final:
            counts = _ControlDatabase(final).catalog_counts()
        return HarnessControlMigrationResult(
            CONTROL_SCHEMA_VERSION,
            final_digest,
            counts,
            tuple(sorted(unresolved)),
            tuple(sorted(projections)),
        )
