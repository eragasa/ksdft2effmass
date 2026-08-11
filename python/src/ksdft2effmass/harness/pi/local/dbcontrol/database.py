"""SQLite connection, semantic identity, and deterministic SQL mechanics."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .encoding import _ControlEncoding
from .schema import _SCHEMA, _TABLE_ORDER

_CATALOG_COUNT_TABLES = (
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


class _ControlDatabase:
    """Own deterministic operations over one SQLite control connection."""

    __slots__ = ("connection",)

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def ordered_rows(self, table: str) -> list[tuple[Any, ...]]:
        columns = [
            row[1] for row in self.connection.execute(f"PRAGMA table_info({table})")
        ]
        order = ",".join(f'"{name}"' for name in columns)
        return list(
            self.connection.execute(f'SELECT {order} FROM "{table}" ORDER BY {order}')
        )

    def semantic_digest(self) -> str:
        """Hash ordered logical table contents rather than SQLite file bytes."""
        tables = [
            row[0]
            for row in self.connection.execute(
                "SELECT name FROM sqlite_schema WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        payload = [(table, self.ordered_rows(table)) for table in tables]
        return _ControlEncoding.sha256(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        )

    @staticmethod
    def _sql_literal(value: object) -> str:
        if value is None:
            return "NULL"
        if type(value) is int:
            return str(value)
        if type(value) is not str:
            raise TypeError(f"unsupported SQL literal {type(value).__name__}")
        return "'" + value.replace("'", "''") + "'"

    def deterministic_sql_export(self) -> bytes:
        """Return stable schema and ordered inserts for exact reconstruction."""
        schema_lines = _SCHEMA.strip().splitlines()
        pragma_lines = [line for line in schema_lines if line.startswith("PRAGMA ")]
        definition_lines = [
            line for line in schema_lines if not line.startswith("PRAGMA ")
        ]
        lines = [
            "-- Generated from authoritative harness control state; do not edit.",
            *pragma_lines,
            "BEGIN IMMEDIATE;",
            *definition_lines,
        ]
        for table in _TABLE_ORDER:
            columns = [
                row[1] for row in self.connection.execute(f"PRAGMA table_info({table})")
            ]
            names = ",".join(f'"{name}"' for name in columns)
            for row in self.ordered_rows(table):
                values = ",".join(self._sql_literal(value) for value in row)
                lines.append(f'INSERT INTO "{table}" ({names}) VALUES ({values});')
        lines.extend(["COMMIT;", "PRAGMA wal_checkpoint(TRUNCATE);", ""])
        return "\n".join(lines).encode()

    def normalized_semantic_digest(self) -> str:
        """Hash logical table content with the self-referential digest normalized.

        Normalization is performed in memory so verification can use an immutable
        read-only SQLite connection without creating WAL or shared-memory sidecars.
        """
        tables = [
            row[0]
            for row in self.connection.execute(
                "SELECT name FROM sqlite_schema WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        payload: list[tuple[str, list[tuple[Any, ...]]]] = []
        for table in tables:
            rows = self.ordered_rows(table)
            if table == "harness_metadata":
                rows = [
                    (key, "" if key == "semantic_digest" else value)
                    for key, value in rows
                ]
            payload.append((table, rows))
        return _ControlEncoding.sha256(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        )

    def catalog_counts(self) -> tuple[tuple[str, int], ...]:
        """Return deterministic migration-result catalog counts."""
        return tuple(
            (
                table,
                int(
                    self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[
                        0
                    ]
                ),
            )
            for table in _CATALOG_COUNT_TABLES
        )

    @classmethod
    def reconstruct(cls, path: Path, sql: bytes) -> None:
        """Materialize one database from deterministic SQL bytes."""
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
