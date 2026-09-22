"""Project-neutral read-only SQLite access for Task lifecycle state."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class _TaskStateDatabaseReader:
    """Read Task lifecycle rows through the generic SQLite contract."""

    __slots__ = ("database_path",)

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def read(self, task_id: str) -> tuple[str, bool] | None:
        """Read one Task lifecycle row without mutating control state."""
        if not self.database_path.is_file():
            return None
        with sqlite3.connect(
            f"file:{self.database_path}?mode=ro", uri=True
        ) as connection:
            row = connection.execute(
                "SELECT lifecycle_status,is_active FROM task_state WHERE task_id=?",
                (task_id,),
            ).fetchone()
        return None if row is None else (str(row[0]), bool(row[1]))
