"""Thin verification of control integrity and deterministic reconstruction."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .constants import CONTROL_DATABASE_PATH, CONTROL_SQL_PATH
from .database import _ControlDatabase
from .encoding import _ControlEncoding
from .projections import _ControlProjector
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
        _ControlDatabase.reconstruct(reconstructed, sql_path.read_bytes())
        try:
            with (
                sqlite3.connect(database) as source,
                sqlite3.connect(reconstructed) as target,
            ):
                integrity = str(source.execute("PRAGMA integrity_check").fetchone()[0])
                foreign = len(source.execute("PRAGMA foreign_key_check").fetchall())
                source_digest = _ControlDatabase(source).normalized_semantic_digest()
                target_digest = _ControlDatabase(target).normalized_semantic_digest()
                source_projections = _ControlProjector(source).render_all()
                target_projections = _ControlProjector(target).render_all()
                source_rows = tuple(
                    source.execute(
                        "SELECT source_path,sha256 FROM test_module "
                        "ORDER BY source_path"
                    )
                )
            repository_sources_match = all(
                (repository_root / path).is_file()
                and _ControlEncoding.sha256((repository_root / path).read_bytes())
                == digest
                for path, digest in source_rows
            )
            maintained_projections_match = all(
                not (repository_root / path).exists()
                or (repository_root / path).read_bytes() == payload
                for path, (_kind, payload) in source_projections.items()
            )
            return HarnessControlVerificationResult(
                integrity,
                foreign,
                source_digest,
                target_digest,
                _ControlEncoding.sha256(database.read_bytes()),
                _ControlEncoding.sha256(reconstructed.read_bytes()),
                source_projections == target_projections
                and repository_sources_match
                and maintained_projections_match,
            )
        finally:
            reconstructed.unlink(missing_ok=True)
            Path(str(reconstructed) + "-wal").unlink(missing_ok=True)
            Path(str(reconstructed) + "-shm").unlink(missing_ok=True)
