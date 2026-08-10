"""Read-only SQLite access for authoritative Task lifecycle state."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def _load_task_state(database_path: Path, task_id: str) -> tuple[str, bool] | None:
    """Read one Task lifecycle row without mutating control state."""
    if not database_path.is_file():
        return None
    with sqlite3.connect(f"file:{database_path}?mode=ro", uri=True) as connection:
        row = connection.execute(
            "SELECT lifecycle_status,is_active FROM task_state WHERE task_id=?",
            (task_id,),
        ).fetchone()
    return None if row is None else (str(row[0]), bool(row[1]))
