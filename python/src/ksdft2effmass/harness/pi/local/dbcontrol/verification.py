"""Thin verification of control integrity and deterministic reconstruction."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .constants import CONTROL_DATABASE_PATH, CONTROL_SQL_PATH
from .database import _execute_script, _semantic_digest_normalized
from .encoding import _sha256
from .projections import _projections
from .records import HarnessControlVerificationResult


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
