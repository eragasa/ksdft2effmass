"""SQLite connection, semantic identity, and deterministic SQL mechanics."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .encoding import _sha256
from .schema import _SCHEMA, _TABLE_ORDER


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
