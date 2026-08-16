"""Private source-aware comparison of maintained and candidate control state."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

from ..dbcontrol.constants import (
    CONTROL_DATABASE_PATH,
    CONTROL_SCHEMA_VERSION,
    CONTROL_SQL_PATH,
    PROJECTION_MANIFEST_PATH,
)
from ..dbcontrol.database import _ControlDatabase
from ..dbcontrol.encoding import _ControlEncoding
from ..dbcontrol.records import (
    HarnessControlVerificationFinding,
    HarnessControlVerificationResult,
)
from .generation import _HarnessControlGenerationBuilder
from .inputs import _HarnessControlInputResolver


class _HarnessControlSourceVerifier:
    """Generate one canonical candidate and compare publisher-owned maintained state."""

    __slots__ = ()

    @staticmethod
    def _finding(
        code: str, path: Path | None, message: str
    ) -> HarnessControlVerificationFinding:
        return HarnessControlVerificationFinding(
            code, None if path is None else path.as_posix(), message
        )

    @staticmethod
    def _readonly_connection(path: Path) -> sqlite3.Connection:
        """Open immutable read-only SQLite without repository sidecars."""
        return sqlite3.connect(
            path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True
        )

    @staticmethod
    def _unexpected_owned_paths(
        root: Path, candidate_paths: frozenset[Path]
    ) -> tuple[Path, ...]:
        """Return unexpected files only inside the frozen publisher-owned domain."""
        observed: set[Path] = set()
        task_records = root / "harness/tasks"
        if task_records.is_dir():
            observed.update(
                path.relative_to(root)
                for path in task_records.glob("*.json")
                if path.is_file()
            )
        return tuple(
            sorted(observed - candidate_paths, key=lambda path: path.as_posix())
        )

    def execute(self, repository_root: Path) -> HarnessControlVerificationResult:
        """Return deterministic source-aware conformance without maintained writes."""
        inputs = _HarnessControlInputResolver().execute(repository_root)
        root = inputs.request.repository_root
        builder = _HarnessControlGenerationBuilder()
        with TemporaryDirectory(prefix="harness-control-verification-") as workspace:
            try:
                generation = builder.execute(inputs.request, Path(workspace).resolve())
                builder.validate(generation)
            except (SyntaxError, ValueError) as exc:
                database_path = root / CONTROL_DATABASE_PATH
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
                return HarnessControlVerificationResult(
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
            findings: list[HarnessControlVerificationFinding] = []
            database_path = root / CONTROL_DATABASE_PATH
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
                        CONTROL_DATABASE_PATH,
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
                            CONTROL_DATABASE_PATH,
                            "maintained control database cannot be read as SQLite",
                        )
                    )
            if integrity != "ok" and not any(
                item.code == "integrity_failure" for item in findings
            ):
                findings.append(
                    self._finding(
                        "integrity_failure",
                        CONTROL_DATABASE_PATH,
                        f"SQLite integrity_check reported {integrity}",
                    )
                )
            if foreign_count:
                findings.append(
                    self._finding(
                        "foreign_key_failure",
                        CONTROL_DATABASE_PATH,
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
                        CONTROL_DATABASE_PATH,
                        "maintained control schema version disagrees with "
                        "the candidate",
                    )
                )
            if source_digest != generation.semantic_digest:
                findings.append(
                    self._finding(
                        "semantic_disagreement",
                        CONTROL_DATABASE_PATH,
                        "maintained logical table content disagrees with "
                        "source-derived state",
                    )
                )
            sql_identical = self._compare_exact(
                root,
                CONTROL_SQL_PATH,
                candidate[CONTROL_SQL_PATH],
                findings,
            )
            manifest_identical = self._compare_exact(
                root,
                PROJECTION_MANIFEST_PATH,
                candidate[PROJECTION_MANIFEST_PATH],
                findings,
            )
            projections_identical = True
            for relative in (Path(path) for path in generation.projection_paths):
                if not self._compare_exact(
                    root, relative, candidate[relative], findings
                ):
                    projections_identical = False
            unexpected = self._unexpected_owned_paths(root, candidate_paths)
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
            return HarnessControlVerificationResult(
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
        findings: list[HarnessControlVerificationFinding],
    ) -> bool:
        """Compare one exact artifact and append one stable expected finding."""
        maintained = root / relative
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
