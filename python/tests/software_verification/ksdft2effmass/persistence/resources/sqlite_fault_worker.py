"""Synthetic local Python process fixture for actual transaction crash boundaries.

Python's __main__ entry point only adapts explicit argv into the fixture owner.
The private seam changes acknowledgement timing, never the stored candidate.
"""

import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch

from ksdft2effmass.persistence import Commit, Revision, SQLiteAtomicRevisionStore


class SQLiteFaultWorker:
    """Pause at one requested boundary until the parent terminates this process."""

    @staticmethod
    def execute(path: Path, phase: str) -> None:
        if phase not in ("before", "after"):
            raise ValueError("unknown fixture phase")
        store = SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=1000, max_payload_bytes=1024
        )
        candidate = Commit(
            "r1", Revision("s", "r2", "r1", "schema", "content", b"next"), "k2"
        )
        with patch.object(
            SQLiteAtomicRevisionStore,
            "_commit_transaction",
            staticmethod(
                SQLiteFaultWorker.after
                if phase == "after"
                else SQLiteFaultWorker.before
            ),
        ):
            store.commit(candidate)

    @staticmethod
    def before(connection: sqlite3.Connection) -> None:
        print("before", flush=True)
        sys.stdin.readline()
        raise RuntimeError("parent must terminate fixture process")

    @staticmethod
    def after(connection: sqlite3.Connection) -> None:
        connection.execute("COMMIT")
        print("after", flush=True)
        sys.stdin.readline()
        raise RuntimeError("parent must terminate fixture process")


if __name__ == "__main__":
    SQLiteFaultWorker.execute(Path(sys.argv[1]), sys.argv[2])
