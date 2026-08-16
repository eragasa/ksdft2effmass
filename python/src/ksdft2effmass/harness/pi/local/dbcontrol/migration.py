"""Private synchronization boundary for maintained Harness projections."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

from ..control.generation import (
    _HarnessProjectionGeneration,
    _HarnessProjectionGenerationBuilder,
)
from .records import _HarnessProjectionRequest, _HarnessProjectionSyncResult


class _HarnessProjectionSynchronizer:
    """Synchronize explicit repository inputs into maintained Harness projections.

    Complete candidate orchestration belongs to the private project-local control
    layer. This private Action validates the candidate and remains the sole owner of
    failure-safe maintained publication.
    """

    __slots__ = ()

    @staticmethod
    def _publish_generation(
        generation: _HarnessProjectionGeneration, repository_root: Path
    ) -> None:
        """Prepare, stage, verify, and publish one validated candidate generation.

        Publication reads candidate bytes and maps them to their maintained
        repository destinations exclusively inside this sole publishing boundary.
        It uses same-directory atomic replacements for individual files.
        It does not claim filesystem-level multi-file atomicity: if one replacement
        fails, retained backups restore every previously published output before the
        error is returned.
        """
        if type(generation) is not _HarnessProjectionGeneration:
            raise TypeError("generation must be _HarnessProjectionGeneration")
        outputs = {
            repository_root / relative: candidate.read_bytes()
            for relative, candidate in generation.artifacts
        }
        database_path = next(
            repository_root / relative
            for relative, candidate in generation.artifacts
            if candidate == generation.database_path
        )
        semantic_digest = generation.semantic_digest
        destinations = tuple(sorted(outputs, key=lambda path: path.as_posix()))
        staged = {
            destination: destination.with_name(
                f".{destination.name}.harness-control-staged"
            )
            for destination in destinations
        }
        backups = {
            destination: destination.with_name(
                f".{destination.name}.harness-control-backup"
            )
            for destination in destinations
        }
        existed = {destination: destination.exists() for destination in destinations}
        staged_database = staged[database_path]
        database_sidecars = tuple(
            Path(str(staged_database) + suffix)
            for suffix in ("-wal", "-shm", "-journal")
        )
        temporary_paths = (*staged.values(), *backups.values(), *database_sidecars)
        try:
            for destination in destinations:
                destination.parent.mkdir(parents=True, exist_ok=True)
                staged[destination].unlink(missing_ok=True)
                backups[destination].unlink(missing_ok=True)
                staged[destination].write_bytes(outputs[destination])
            for destination in destinations:
                if staged[destination].read_bytes() != outputs[destination]:
                    raise RuntimeError(
                        f"staged output verification failed: {destination}"
                    )
            with sqlite3.connect(staged_database) as connection:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                foreign_keys = list(connection.execute("PRAGMA foreign_key_check"))
                stored_digest = connection.execute(
                    "SELECT value FROM harness_metadata WHERE key='semantic_digest'"
                ).fetchone()
            if integrity != "ok" or foreign_keys or stored_digest != (semantic_digest,):
                raise RuntimeError("staged authoritative database verification failed")
            for path in database_sidecars:
                path.unlink(missing_ok=True)
        except Exception:
            for path in temporary_paths:
                path.unlink(missing_ok=True)
            raise
        try:
            for destination in destinations:
                if existed[destination]:
                    destination.replace(backups[destination])
            for destination in destinations:
                staged[destination].replace(destination)
        except Exception as publish_error:
            try:
                for destination in reversed(destinations):
                    if backups[destination].exists():
                        destination.unlink(missing_ok=True)
                        backups[destination].replace(destination)
                    elif not existed[destination]:
                        destination.unlink(missing_ok=True)
            except Exception as rollback_error:
                raise RuntimeError(
                    "control generation publication and rollback both failed"
                ) from rollback_error
            raise RuntimeError(
                "control generation publication failed; previous generation restored"
            ) from publish_error
        finally:
            for path in temporary_paths:
                path.unlink(missing_ok=True)

    def execute(
        self, request: _HarnessProjectionRequest
    ) -> _HarnessProjectionSyncResult:
        """Build, validate, and publish one complete control generation."""
        if type(request) is not _HarnessProjectionRequest:
            raise TypeError("request must be _HarnessProjectionRequest")
        builder = _HarnessProjectionGenerationBuilder()
        with TemporaryDirectory(prefix="harness-projection-sync-") as raw_workspace:
            generation = builder.execute(request, Path(raw_workspace).resolve())
            builder.validate(generation)
            self._publish_generation(generation, request.repository_root)
            return _HarnessProjectionSyncResult(
                generation.schema_version,
                generation.semantic_digest,
                generation.counts,
                generation.unresolved_naming_issues,
                generation.projection_paths,
            )
