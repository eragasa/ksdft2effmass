"""Private source-aware comparison of maintained and candidate control state."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

from ..dbcontrol.constants import CONTROL_SCHEMA_VERSION
from ..dbcontrol.database import _ControlDatabase
from ..dbcontrol.encoding import _ControlEncoding
from ..dbcontrol.records import (
    _HarnessProjectionVerificationFinding,
    _HarnessProjectionVerificationResult,
)
from .generation import _HarnessProjectionGenerationBuilder
from .inputs import _HarnessProjectionInputResolver


class _HarnessProjectionSourceVerifier:
    """Generate one canonical candidate and compare publisher-owned maintained state."""

    __slots__ = ()

    @staticmethod
    def _finding(
        code: str, path: Path | None, message: str
    ) -> _HarnessProjectionVerificationFinding:
        return _HarnessProjectionVerificationFinding(
            code, None if path is None else path.as_posix(), message
        )

    @staticmethod
    def _readonly_connection(path: Path) -> sqlite3.Connection:
        """Open immutable read-only SQLite without repository sidecars."""
        return sqlite3.connect(
            path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True
        )

    @staticmethod
    def _confined_source(repository_root: Path, relative: Path) -> Path:
        """Return one source only when every existing component is nonsymlinked."""
        if relative.is_absolute() or not relative.parts or ".." in relative.parts:
            raise ValueError("projection source must be root-relative")
        root = repository_root.resolve(strict=True)
        if root != repository_root or root.is_symlink():
            raise ValueError("repository_root must be canonical and nonsymlinked")
        source = root
        for part in relative.parts:
            source /= part
            if source.is_symlink():
                raise ValueError(
                    f"projection source contains a symlink: {relative.as_posix()}"
                )
            if source.exists() and source != root / relative and not source.is_dir():
                raise ValueError(
                    "projection source parent is not a directory: "
                    f"{relative.as_posix()}"
                )
        resolved = source.resolve(strict=False)
        if root != resolved and root not in resolved.parents:
            raise ValueError("projection source escapes repository_root")
        return source

    @staticmethod
    def _unexpected_owned_paths(
        root: Path, candidate_paths: frozenset[Path], task_root: Path
    ) -> tuple[Path, ...]:
        """Return unexpected files only inside the frozen publisher-owned domain."""
        observed: set[Path] = set()
        task_records = root / task_root
        if task_records.is_dir():
            observed.update(
                path.relative_to(root)
                for path in task_records.glob("*.json")
                if path.is_file()
            )
        return tuple(
            sorted(observed - candidate_paths, key=lambda path: path.as_posix())
        )

    def execute(self, repository_root: Path) -> _HarnessProjectionVerificationResult:
        """Return deterministic source-aware conformance without maintained writes."""
        inputs = _HarnessProjectionInputResolver().execute(repository_root)
        request = inputs.request
        root = request.repository_root
        configuration = request.harness_configuration
        assert configuration is not None
        database_relative = Path(configuration.persistence.state_database_path)
        sql_relative = Path(configuration.persistence.sql_export_path)
        manifest_relative = Path(configuration.persistence.projection_manifest_path)
        builder = _HarnessProjectionGenerationBuilder()
        with TemporaryDirectory(prefix="harness-control-verification-") as workspace:
            try:
                generation = builder.execute(request, Path(workspace).resolve())
                builder.validate(generation)
            except (SyntaxError, ValueError) as exc:
                database_path = self._confined_source(root, database_relative)
                raw_source = (
                    _ControlEncoding.sha256(database_path.read_bytes())
                    if database_path.is_file()
                    else ""
                )
                finding = self._finding(
                    "source_input_failure",
                    None,
                    f"canonical source input is nonconforming: {exc}",
                )
                return _HarnessProjectionVerificationResult(
                    "not_checked",
                    0,
                    "",
                    "",
                    raw_source,
                    "",
                    False,
                    False,
                    False,
                    False,
                    (finding,),
                )
            candidate = dict(generation.artifacts)
            candidate_paths = frozenset(candidate)
            findings: list[_HarnessProjectionVerificationFinding] = []
            database_path = self._confined_source(root, database_relative)
            integrity = "missing"
            foreign_count = 0
            source_digest = ""
            source_schema: tuple[str] | None = None
            source_schema_identity: tuple[tuple[object, ...], ...] = ()
            raw_source = ""
            if not database_path.is_file():
                findings.append(
                    self._finding(
                        "missing_artifact",
                        database_relative,
                        "maintained control database is missing",
                    )
                )
            else:
                raw_source = _ControlEncoding.sha256(database_path.read_bytes())
                try:
                    with self._readonly_connection(database_path) as source:
                        integrity = str(
                            source.execute("PRAGMA integrity_check").fetchone()[0]
                        )
                        foreign_rows = tuple(source.execute("PRAGMA foreign_key_check"))
                        foreign_count = len(foreign_rows)
                        source_schema = source.execute(
                            "SELECT value FROM harness_metadata "
                            "WHERE key='control_schema_version'"
                        ).fetchone()
                        source_schema_identity = tuple(
                            source.execute(
                                "SELECT type,name,tbl_name,sql FROM sqlite_schema "
                                "WHERE name NOT LIKE 'sqlite_%' "
                                "ORDER BY type,name,tbl_name,sql"
                            )
                        )
                        source_digest = _ControlDatabase(
                            source
                        ).normalized_semantic_digest()
                except sqlite3.DatabaseError:
                    integrity = "invalid"
                    findings.append(
                        self._finding(
                            "integrity_failure",
                            database_relative,
                            "maintained control database cannot be read as SQLite",
                        )
                    )
            if integrity != "ok" and not any(
                item.code == "integrity_failure" for item in findings
            ):
                findings.append(
                    self._finding(
                        "integrity_failure",
                        database_relative,
                        f"SQLite integrity_check reported {integrity}",
                    )
                )
            if foreign_count:
                findings.append(
                    self._finding(
                        "foreign_key_failure",
                        database_relative,
                        f"SQLite foreign_key_check reported {foreign_count} row(s)",
                    )
                )
            with self._readonly_connection(generation.database_path) as candidate_db:
                candidate_schema_identity = tuple(
                    candidate_db.execute(
                        "SELECT type,name,tbl_name,sql FROM sqlite_schema "
                        "WHERE name NOT LIKE 'sqlite_%' "
                        "ORDER BY type,name,tbl_name,sql"
                    )
                )
            schema_agrees = (
                source_schema == (str(CONTROL_SCHEMA_VERSION),)
                and source_schema_identity == candidate_schema_identity
            )
            if not schema_agrees:
                findings.append(
                    self._finding(
                        "schema_disagreement",
                        database_relative,
                        "maintained control schema version disagrees with "
                        "the candidate",
                    )
                )
            if source_digest != generation.semantic_digest:
                findings.append(
                    self._finding(
                        "semantic_disagreement",
                        database_relative,
                        "maintained logical table content disagrees with "
                        "source-derived state",
                    )
                )
            sql_identical = self._compare_exact(
                root,
                sql_relative,
                candidate[sql_relative],
                findings,
            )
            manifest_identical = self._compare_exact(
                root,
                manifest_relative,
                candidate[manifest_relative],
                findings,
            )
            projections_identical = True
            for relative in (Path(path) for path in generation.projection_paths):
                if not self._compare_exact(
                    root, relative, candidate[relative], findings
                ):
                    projections_identical = False
            unexpected = self._unexpected_owned_paths(
                root, candidate_paths, Path(configuration.catalogs.task_root)
            )
            for relative in unexpected:
                projections_identical = False
                findings.append(
                    self._finding(
                        "unexpected_artifact",
                        relative,
                        "unexpected file exists inside a publisher-owned "
                        "generated root",
                    )
                )
            ordered = tuple(
                sorted(
                    set(findings),
                    key=lambda item: (item.code, item.path or "", item.message),
                )
            )
            return _HarnessProjectionVerificationResult(
                integrity,
                foreign_count,
                source_digest,
                generation.semantic_digest,
                raw_source,
                _ControlEncoding.sha256(generation.database_path.read_bytes()),
                projections_identical,
                schema_agrees,
                sql_identical,
                manifest_identical,
                ordered,
            )

    def _compare_exact(
        self,
        root: Path,
        relative: Path,
        candidate: Path,
        findings: list[_HarnessProjectionVerificationFinding],
    ) -> bool:
        """Compare one exact artifact and append one stable expected finding."""
        maintained = self._confined_source(root, relative)
        if not maintained.is_file():
            findings.append(
                self._finding(
                    "missing_artifact",
                    relative,
                    "maintained generated artifact is missing",
                )
            )
            return False
        if maintained.read_bytes() != candidate.read_bytes():
            findings.append(
                self._finding(
                    "changed_artifact",
                    relative,
                    "maintained generated artifact differs from "
                    "source-derived candidate",
                )
            )
            return False
        return True
