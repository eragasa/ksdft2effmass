#!/usr/bin/env python3
"""Atomically rebuild the local research-results SQLite projection.

This command reads retained files under ``calculations/research-monograph``. It does
not execute calculations, verifiers, plotting scripts, or external calculators.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import mimetypes
import os
import sqlite3
import tempfile
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = 1
TEXT_PREVIEW_LIMIT_BYTES = 32 * 1024
MAX_SCALARS_PER_DOCUMENT = 5_000
TEXT_SUFFIXES = frozenset(
    {
        ".csv",
        ".err",
        ".ini",
        ".json",
        ".jsonl",
        ".log",
        ".md",
        ".out",
        ".py",
        ".tex",
        ".toml",
        ".tsv",
        ".txt",
        ".yaml",
        ".yml",
    }
)
IMAGE_SUFFIXES = frozenset({".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"})
DOCUMENT_SUFFIXES = frozenset({".pdf"})
EXCLUDED_DIRECTORY_NAMES = frozenset({"__pycache__", "build"})
STATUS_KEY_FRAGMENTS = (
    "accepted",
    "authorized",
    "complete",
    "converged",
    "decision",
    "disposition",
    "outcome",
    "passed",
    "state",
    "status",
    "success",
    "verified",
)
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

SCHEMA_SQL = """
PRAGMA application_id = 1263748178;
PRAGMA user_version = 1;

CREATE TABLE projection_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT, WITHOUT ROWID;

CREATE TABLE calculations (
    calculation_id TEXT PRIMARY KEY,
    root_path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    status_text TEXT,
    status_source_path TEXT,
    artifact_count INTEGER NOT NULL CHECK (artifact_count >= 0)
) STRICT, WITHOUT ROWID;

CREATE TABLE artifacts (
    artifact_id INTEGER PRIMARY KEY,
    calculation_id TEXT NOT NULL REFERENCES calculations(calculation_id),
    path TEXT NOT NULL UNIQUE,
    path_within_calculation TEXT NOT NULL,
    name TEXT NOT NULL,
    extension TEXT NOT NULL,
    media_type TEXT NOT NULL,
    artifact_kind TEXT NOT NULL CHECK (
        artifact_kind IN (
            'binary', 'document', 'image', 'json', 'log', 'manifest',
            'markdown', 'source', 'table', 'text'
        )
    ),
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    text_preview TEXT,
    text_truncated INTEGER NOT NULL CHECK (text_truncated IN (0, 1)),
    json_valid INTEGER CHECK (json_valid IS NULL OR json_valid IN (0, 1)),
    UNIQUE (calculation_id, path_within_calculation)
) STRICT;

CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    calculation_id TEXT NOT NULL REFERENCES calculations(calculation_id),
    result_artifact_id INTEGER NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
    label TEXT NOT NULL,
    source_kind TEXT NOT NULL CHECK (source_kind = 'retained_result_json'),
    status_text TEXT
) STRICT, WITHOUT ROWID;

CREATE TABLE scalar_observations (
    scalar_id INTEGER PRIMARY KEY,
    calculation_id TEXT NOT NULL REFERENCES calculations(calculation_id),
    run_id TEXT REFERENCES runs(run_id),
    artifact_id INTEGER NOT NULL REFERENCES artifacts(artifact_id),
    json_path TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('descriptor', 'metric', 'status')),
    value_type TEXT NOT NULL CHECK (
        value_type IN ('boolean', 'null', 'number', 'string')
    ),
    numeric_value REAL,
    text_value TEXT,
    unit TEXT,
    UNIQUE (artifact_id, json_path)
) STRICT;

CREATE TABLE manifest_observations (
    observation_id INTEGER PRIMARY KEY,
    calculation_id TEXT NOT NULL REFERENCES calculations(calculation_id),
    manifest_artifact_id INTEGER NOT NULL REFERENCES artifacts(artifact_id),
    retained_artifact_id INTEGER REFERENCES artifacts(artifact_id),
    retained_path TEXT,
    expected_sha256 TEXT NOT NULL CHECK (length(expected_sha256) = 64),
    actual_sha256 TEXT,
    state TEXT NOT NULL CHECK (
        state IN ('match', 'mismatch', 'missing', 'outside_repository')
    )
) STRICT;

CREATE INDEX artifacts_calculation_kind
    ON artifacts(calculation_id, artifact_kind, path);
CREATE INDEX runs_calculation
    ON runs(calculation_id, label);
CREATE INDEX scalar_observations_calculation_role
    ON scalar_observations(calculation_id, role, name);
CREATE INDEX scalar_observations_run
    ON scalar_observations(run_id, role, name);
CREATE INDEX manifest_observations_calculation_state
    ON manifest_observations(calculation_id, state);

CREATE VIEW presentation_artifacts AS
SELECT
    artifact_id,
    calculation_id,
    path,
    path_within_calculation,
    name,
    media_type,
    artifact_kind,
    size_bytes,
    sha256,
    text_preview,
    text_truncated,
    json_valid
FROM artifacts
WHERE artifact_kind IN (
    'document', 'image', 'json', 'log', 'manifest', 'markdown', 'table', 'text'
);

CREATE VIEW run_results AS
SELECT
    r.run_id,
    r.calculation_id,
    r.label,
    r.source_kind,
    r.status_text,
    a.path AS result_path,
    a.media_type,
    a.size_bytes,
    a.sha256,
    a.text_preview,
    a.text_truncated,
    a.json_valid
FROM runs AS r
JOIN artifacts AS a ON a.artifact_id = r.result_artifact_id;
"""


@dataclass(frozen=True, slots=True)
class SourceArtifact:
    """Describe one safe repository-relative source artifact."""

    source_path: Path
    repository_path: str
    calculation_path: str
    name: str
    extension: str
    media_type: str
    artifact_kind: str
    size_bytes: int
    sha256: str
    text_preview: str | None
    text_truncated: bool
    json_value: JsonValue | None
    json_valid: bool | None


@dataclass(frozen=True, slots=True)
class ScalarObservation:
    """Describe one scalar leaf projected from a retained JSON mapping."""

    json_path: str
    name: str
    role: str
    value_type: str
    numeric_value: float | None
    text_value: str | None
    unit: str | None


@dataclass(frozen=True, slots=True)
class ResearchResultsProjectionRequest:
    """Identify the source repository and derived SQLite destination."""

    repository_root: Path
    output_path: Path


@dataclass(frozen=True, slots=True)
class ResearchResultsProjectionResult:
    """Report the identity and row counts of one completed projection generation."""

    output_path: Path
    sha256: str
    calculation_count: int
    run_count: int
    artifact_count: int
    scalar_observation_count: int
    manifest_observation_count: int


class ResearchResultsProjectionRebuilder:
    """Atomically rebuild the read-only research-results projection."""

    def execute(
        self, request: ResearchResultsProjectionRequest
    ) -> ResearchResultsProjectionResult:
        """Build, validate, replace, and identify one complete database generation."""
        repository_root = request.repository_root.resolve(strict=True)
        output_path = request.output_path.resolve()
        _rebuild_projection(repository_root, output_path)
        with sqlite3.connect(
            f"file:{output_path.as_posix()}?mode=ro&immutable=1", uri=True
        ) as connection:
            counts = {
                table: int(
                    connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                )
                for table in (
                    "calculations",
                    "runs",
                    "artifacts",
                    "scalar_observations",
                    "manifest_observations",
                )
            }
        return ResearchResultsProjectionResult(
            output_path=output_path,
            sha256=_sha256(output_path),
            calculation_count=counts["calculations"],
            run_count=counts["runs"],
            artifact_count=counts["artifacts"],
            scalar_observation_count=counts["scalar_observations"],
            manifest_observation_count=counts["manifest_observations"],
        )


def _repository_relative(path: Path, repository_root: Path) -> str:
    resolved = path.resolve(strict=True)
    try:
        relative = resolved.relative_to(repository_root.resolve(strict=True))
    except ValueError as error:
        raise ValueError(f"path is outside repository root: {path}") from error
    if path.is_symlink():
        raise ValueError(f"symbolic links are not accepted as artifacts: {path}")
    return relative.as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _source_files(root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in root.rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and not any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts)
        )
    )


def _artifact_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    lower_name = path.name.lower()
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in DOCUMENT_SUFFIXES:
        return "document"
    if suffix == ".json":
        return "json"
    if suffix == ".md":
        return "markdown"
    if suffix in {".csv", ".tsv"}:
        return "table"
    if suffix in {".log", ".out", ".err"}:
        return "log"
    if suffix == ".py":
        return "source"
    if (
        lower_name == "sha256sums"
        or lower_name.endswith("-sha256sums")
        or lower_name.endswith(".sha256")
    ):
        return "manifest"
    if suffix in TEXT_SUFFIXES or not suffix:
        return "text"
    return "binary"


def _media_type(path: Path, kind: str) -> str:
    explicit = {
        "json": "application/json",
        "manifest": "text/plain",
        "markdown": "text/markdown",
        "source": "text/x-python",
        "table": "text/csv"
        if path.suffix.lower() == ".csv"
        else "text/tab-separated-values",
    }
    if kind in explicit:
        return explicit[kind]
    guessed, _encoding = mimetypes.guess_type(path.name)
    return guessed or (
        "text/plain" if kind in {"log", "text"} else "application/octet-stream"
    )


def _text_preview(path: Path, artifact_kind: str) -> tuple[str | None, bool]:
    if artifact_kind not in {
        "json",
        "log",
        "manifest",
        "markdown",
        "source",
        "table",
        "text",
    }:
        return None, False
    with path.open("rb") as stream:
        payload = stream.read(TEXT_PREVIEW_LIMIT_BYTES + 1)
    truncated = len(payload) > TEXT_PREVIEW_LIMIT_BYTES
    return payload[:TEXT_PREVIEW_LIMIT_BYTES].decode(
        "utf-8", errors="replace"
    ), truncated


def _reject_nonstandard_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def _json_value(path: Path) -> tuple[JsonValue | None, bool | None]:
    if path.suffix.lower() != ".json":
        return None, None
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_nonstandard_json_constant,
        )
    except OSError, UnicodeError, ValueError, json.JSONDecodeError:
        return None, False
    if not isinstance(value, (dict, list, str, int, float, bool)) and value is not None:
        return None, False
    return value, True


def _source_artifact(
    path: Path, calculation_root: Path, repository_root: Path
) -> SourceArtifact:
    kind = _artifact_kind(path)
    preview, truncated = _text_preview(path, kind)
    json_value, json_valid = _json_value(path)
    return SourceArtifact(
        source_path=path,
        repository_path=_repository_relative(path, repository_root),
        calculation_path=path.relative_to(calculation_root).as_posix(),
        name=path.name,
        extension=path.suffix.lower(),
        media_type=_media_type(path, kind),
        artifact_kind=kind,
        size_bytes=path.stat().st_size,
        sha256=_sha256(path),
        text_preview=preview,
        text_truncated=truncated,
        json_value=json_value,
        json_valid=json_valid,
    )


def _first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    return fallback


def _status_excerpt(text: str) -> str | None:
    lines = text.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        normalized = line.strip().lower()
        if normalized in {"## status", "## status and scope", "## scope"}:
            start = index + 1
            break
    if start is None:
        return None
    selected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        selected.append(line)
        if sum(len(item) + 1 for item in selected) >= 4_000:
            break
    excerpt = "\n".join(selected).strip()
    return excerpt or None


def _result_document(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() == ".json" and (
        name in {"result.json", "results.json"}
        or name.endswith("-result.json")
        or name.endswith("_result.json")
        or name.endswith("-results.json")
        or name.endswith("_results.json")
    )


def _json_path(parent: str, key: str) -> str:
    if key.isidentifier():
        return f"{parent}.{key}"
    return f"{parent}[{json.dumps(key, ensure_ascii=False)}]"


def _scalar_role(name: str, value: JsonScalar) -> str:
    normalized = name.lower()
    if any(fragment in normalized for fragment in STATUS_KEY_FRAGMENTS):
        return "status"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "metric"
    return "descriptor"


def _specific_unit(mapping: Mapping[str, JsonValue], name: str) -> str | None:
    candidate = mapping.get(f"{name}_unit")
    if isinstance(candidate, str) and candidate.strip():
        return candidate.strip()
    candidate = mapping.get(f"{name}_units")
    if isinstance(candidate, str) and candidate.strip():
        return candidate.strip()
    return None


def _scalar_record(
    *, json_path: str, name: str, value: JsonScalar, unit: str | None
) -> ScalarObservation:
    if value is None:
        value_type = "null"
        numeric_value = None
        text_value = None
    elif isinstance(value, bool):
        value_type = "boolean"
        numeric_value = None
        text_value = "true" if value else "false"
    elif isinstance(value, (int, float)):
        value_type = "number"
        converted = float(value)
        numeric_value = converted if math.isfinite(converted) else None
        text_value = str(value)
    else:
        value_type = "string"
        numeric_value = None
        text_value = value[:4_000]
    return ScalarObservation(
        json_path=json_path,
        name=name,
        role=_scalar_role(name, value),
        value_type=value_type,
        numeric_value=numeric_value,
        text_value=text_value,
        unit=unit,
    )


def _walk_scalars(
    value: JsonValue,
    *,
    parent_path: str = "$",
    limit: int = MAX_SCALARS_PER_DOCUMENT,
) -> tuple[ScalarObservation, ...]:
    observations: list[ScalarObservation] = []

    def walk(current: JsonValue, current_path: str) -> None:
        if len(observations) >= limit:
            return
        if isinstance(current, dict):
            mapping: Mapping[str, JsonValue] = current
            for name in sorted(mapping):
                child = mapping[name]
                child_path = _json_path(current_path, name)
                if isinstance(child, dict):
                    walk(child, child_path)
                elif isinstance(child, list):
                    if len(child) <= 100 and all(
                        isinstance(item, dict) for item in child
                    ):
                        for index, item in enumerate(child):
                            walk(item, f"{child_path}[{index}]")
                else:
                    observations.append(
                        _scalar_record(
                            json_path=child_path,
                            name=name,
                            value=child,
                            unit=_specific_unit(mapping, name),
                        )
                    )
                if len(observations) >= limit:
                    return
        elif isinstance(current, list) and len(current) <= 100:
            for index, item in enumerate(current):
                if isinstance(item, (dict, list)):
                    walk(item, f"{current_path}[{index}]")
                if len(observations) >= limit:
                    return

    walk(value, parent_path)
    return tuple(observations)


def _explicit_document_status(value: JsonValue | None) -> str | None:
    if not isinstance(value, dict):
        return None
    preferred_keys = ("status", "outcome", "decision", "disposition", "state")
    remaining_status_keys = tuple(
        key
        for key in sorted(value)
        if key not in preferred_keys
        and any(fragment in key.lower() for fragment in STATUS_KEY_FRAGMENTS)
    )
    for key in preferred_keys + remaining_status_keys:
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()[:1_000]
        if isinstance(candidate, bool):
            return "true" if candidate else "false"
    return None


def _manifest_file(path: Path) -> bool:
    lower_name = path.name.lower()
    return (
        lower_name == "sha256sums"
        or lower_name.endswith("-sha256sums")
        or lower_name.endswith(".sha256")
    )


def _manifest_lines(path: Path) -> Iterator[tuple[str, str]]:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split(maxsplit=1)
        if len(parts) != 2:
            continue
        expected = parts[0].lower()
        if len(expected) != 64 or any(
            character not in "0123456789abcdef" for character in expected
        ):
            continue
        yield expected, parts[1].lstrip("*")


def _insert_artifact(
    connection: sqlite3.Connection,
    calculation_id: str,
    artifact: SourceArtifact,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO artifacts (
            calculation_id, path, path_within_calculation, name, extension,
            media_type, artifact_kind, size_bytes, sha256, text_preview,
            text_truncated, json_valid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            calculation_id,
            artifact.repository_path,
            artifact.calculation_path,
            artifact.name,
            artifact.extension,
            artifact.media_type,
            artifact.artifact_kind,
            artifact.size_bytes,
            artifact.sha256,
            artifact.text_preview,
            int(artifact.text_truncated),
            None if artifact.json_valid is None else int(artifact.json_valid),
        ),
    )
    if cursor.lastrowid is None:
        raise RuntimeError(
            f"SQLite did not return an artifact identity for {artifact.name}"
        )
    return cursor.lastrowid


def _populate_calculation(
    connection: sqlite3.Connection,
    calculation_root: Path,
    repository_root: Path,
) -> None:
    calculation_id = calculation_root.name
    root_path = _repository_relative(calculation_root, repository_root)
    source_artifacts = tuple(
        _source_artifact(path, calculation_root, repository_root)
        for path in _source_files(calculation_root)
    )
    readme = next(
        (
            artifact
            for artifact in source_artifacts
            if artifact.calculation_path == "README.md"
        ),
        None,
    )
    readme_text = readme.text_preview if readme and readme.text_preview else ""
    title = _first_heading(readme_text, calculation_id.replace("-", " ").title())
    status_text = _status_excerpt(readme_text)
    status_source_path = readme.repository_path if status_text and readme else None
    connection.execute(
        """
        INSERT INTO calculations (
            calculation_id, root_path, title, status_text, status_source_path,
            artifact_count
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            calculation_id,
            root_path,
            title,
            status_text,
            status_source_path,
            len(source_artifacts),
        ),
    )

    artifact_ids: dict[str, int] = {}
    repository_artifacts: dict[str, SourceArtifact] = {}
    for artifact in source_artifacts:
        artifact_id = _insert_artifact(connection, calculation_id, artifact)
        artifact_ids[artifact.repository_path] = artifact_id
        repository_artifacts[artifact.repository_path] = artifact

    run_ids: dict[int, str] = {}
    for artifact in source_artifacts:
        artifact_id = artifact_ids[artifact.repository_path]
        if (
            not _result_document(artifact.source_path)
            or artifact.json_valid is not True
        ):
            continue
        run_id = f"result:{artifact.repository_path}"
        connection.execute(
            """
            INSERT INTO runs (
                run_id, calculation_id, result_artifact_id, label, source_kind,
                status_text
            ) VALUES (?, ?, ?, ?, 'retained_result_json', ?)
            """,
            (
                run_id,
                calculation_id,
                artifact_id,
                artifact.name,
                _explicit_document_status(artifact.json_value),
            ),
        )
        run_ids[artifact_id] = run_id

    for artifact in source_artifacts:
        if artifact.json_valid is not True or artifact.json_value is None:
            continue
        artifact_id = artifact_ids[artifact.repository_path]
        associated_run_id = run_ids.get(artifact_id)
        for observation in _walk_scalars(artifact.json_value):
            connection.execute(
                """
                INSERT INTO scalar_observations (
                    calculation_id, run_id, artifact_id, json_path, name, role,
                    value_type, numeric_value, text_value, unit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    calculation_id,
                    associated_run_id,
                    artifact_id,
                    observation.json_path,
                    observation.name,
                    observation.role,
                    observation.value_type,
                    observation.numeric_value,
                    observation.text_value,
                    observation.unit,
                ),
            )

    for manifest in source_artifacts:
        if not _manifest_file(manifest.source_path):
            continue
        manifest_artifact_id = artifact_ids[manifest.repository_path]
        for expected_sha256, listed_name in _manifest_lines(manifest.source_path):
            listed_path = manifest.source_path.parent / listed_name
            retained_repository_path: str | None
            retained_artifact_id: int | None
            actual_sha256: str | None
            try:
                retained_repository_path = _repository_relative(
                    listed_path, repository_root
                )
            except FileNotFoundError, ValueError:
                try:
                    candidate = listed_path.resolve(strict=False)
                    candidate.relative_to(repository_root.resolve(strict=True))
                except ValueError:
                    state = "outside_repository"
                    retained_repository_path = None
                else:
                    state = "missing"
                    retained_repository_path = candidate.relative_to(
                        repository_root.resolve(strict=True)
                    ).as_posix()
                retained_artifact_id = None
                actual_sha256 = None
            else:
                retained_artifact_id = artifact_ids.get(retained_repository_path)
                retained_artifact = repository_artifacts.get(retained_repository_path)
                actual_sha256 = (
                    retained_artifact.sha256
                    if retained_artifact is not None
                    else _sha256(listed_path)
                )
                state = "match" if actual_sha256 == expected_sha256 else "mismatch"
            connection.execute(
                """
                INSERT INTO manifest_observations (
                    calculation_id, manifest_artifact_id, retained_artifact_id,
                    retained_path, expected_sha256, actual_sha256, state
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    calculation_id,
                    manifest_artifact_id,
                    retained_artifact_id,
                    retained_repository_path,
                    expected_sha256,
                    actual_sha256,
                    state,
                ),
            )


def _metadata_rows() -> tuple[tuple[str, str], ...]:
    return (
        ("schema_version", str(SCHEMA_VERSION)),
        ("source_root", "calculations/research-monograph"),
        ("path_semantics", "repository-relative-posix"),
        (
            "builder",
            "ksdft2effmass.campaigns.research_monograph.results_projection",
        ),
        ("text_preview_limit_bytes", str(TEXT_PREVIEW_LIMIT_BYTES)),
        (
            "run_semantics",
            "one run row per valid retained JSON result document; "
            "not an execution claim",
        ),
    )


def _calculation_roots(repository_root: Path) -> tuple[Path, ...]:
    source_root = repository_root / "calculations" / "research-monograph"
    if not source_root.is_dir():
        raise ValueError(f"calculation root does not exist: {source_root}")
    return tuple(
        directory
        for directory in sorted(source_root.iterdir())
        if directory.is_dir()
        and not directory.is_symlink()
        and directory.name != "campaigns"
    )


def _validate_database(connection: sqlite3.Connection) -> None:
    integrity = connection.execute("PRAGMA integrity_check").fetchone()
    if integrity is None or integrity[0] != "ok":
        raise RuntimeError(f"SQLite integrity check failed: {integrity}")
    foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
    if foreign_keys:
        raise RuntimeError(f"SQLite foreign-key check failed: {foreign_keys[:5]}")
    unsafe_paths = connection.execute(
        """
        SELECT path FROM artifacts
        WHERE path LIKE '/%'
           OR path = '..'
           OR path LIKE '../%'
           OR path LIKE '%/../%'
        LIMIT 1
        """
    ).fetchone()
    if unsafe_paths is not None:
        raise RuntimeError(
            f"unsafe artifact path entered projection: {unsafe_paths[0]}"
        )


def _rebuild_projection(repository_root: Path, output_path: Path) -> None:
    repository_root = repository_root.resolve(strict=True)
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent
    )
    os.close(descriptor)
    temporary_path = Path(temporary_name)
    try:
        connection = sqlite3.connect(temporary_path)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = DELETE")
            connection.execute("PRAGMA synchronous = FULL")
            connection.executescript(SCHEMA_SQL)
            connection.executemany(
                "INSERT INTO projection_metadata (key, value) VALUES (?, ?)",
                _metadata_rows(),
            )
            for calculation_root in _calculation_roots(repository_root):
                _populate_calculation(connection, calculation_root, repository_root)
            connection.commit()
            _validate_database(connection)
        finally:
            connection.close()
        os.chmod(temporary_path, 0o600)
        with temporary_path.open("rb") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary_path, output_path)
        directory_descriptor = os.open(output_path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary_path.unlink(missing_ok=True)


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Atomically rebuild the local research-results SQLite projection."
    )
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = _parse_arguments()
    repository_root = arguments.repository.resolve()
    output_path = (
        arguments.output.resolve()
        if arguments.output is not None
        else repository_root / "ui" / "analysis" / "build" / "results.sqlite"
    )
    result = ResearchResultsProjectionRebuilder().execute(
        ResearchResultsProjectionRequest(
            repository_root=repository_root,
            output_path=output_path,
        )
    )
    print(result.output_path)
    print(
        f"calculations={result.calculation_count} "
        f"runs={result.run_count} "
        f"artifacts={result.artifact_count} "
        f"scalar_observations={result.scalar_observation_count} "
        f"manifest_observations={result.manifest_observation_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
