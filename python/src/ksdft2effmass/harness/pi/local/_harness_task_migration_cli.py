"""Shared explicit-input translation for HarnessTask migration commands.

This private module performs bounded filesystem observation and translates closed
project-local JSON inputs into the accepted immutable DataObjects.  Existing
ActionObjects remain the only owners of serialization, rendering, comparison,
packet preparation, and disposition compatibility.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .. import (
    ArtifactIdentity,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewPreparer,
    HumanReviewTarget,
)
from .task_model import (
    HarnessTaskDeserializer,
    HarnessTaskDocumentationComparator,
    HarnessTaskDocumentationContent,
    HarnessTaskDocumentationRenderer,
    HarnessTaskDocumentSource,
    HarnessTaskMigrationReviewDocument,
    HarnessTaskMigrationReviewPacket,
    HarnessTaskMigrationReviewPacketPreparer,
    HarnessTaskMigrationReviewPacketRenderer,
    HarnessTaskMigrationReviewPacketRequest,
    HarnessTaskProjectionProfile,
    HarnessTaskSerializer,
    HarnessTaskSourceDisposition,
    HarnessTaskSourceMapping,
)

_CONTRACT_REFERENCES = (
    ".pi/evidence/docs-json/task-model-contract/harness-task-contract.md",
    ".pi/tasks/harness.simplification.docs-json.task-document-migration.json",
    ".pi/evidence/task-control/task-document-human-mediation-decision.md",
)


class CommandInputError(ValueError):
    """Identify invalid paths, files, or closed command representations."""


@dataclass(frozen=True, slots=True)
class PreparedMigrationReview:
    """Hold one reconstructed packet, document, and canonical packet binding."""

    packet: HarnessTaskMigrationReviewPacket
    document: HarnessTaskMigrationReviewDocument
    packet_binding_sha256: str
    candidate_json_sha256: str


def canonical_json_bytes(value: object) -> bytes:
    """Return compact canonical JSON bytes with one final LF."""
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def sha256(content: bytes) -> str:
    """Return the lowercase SHA-256 digest of exact bytes."""
    return hashlib.sha256(content).hexdigest()


def artifact_identity(content: bytes) -> ArtifactIdentity:
    """Return the accepted exact-byte identity DataObject."""
    return ArtifactIdentity(1, "sha256", sha256(content))


def resolved_root(path: Path) -> Path:
    """Validate one explicit absolute resolved nonsymlink repository root."""
    if not path.is_absolute() or ".." in path.parts:
        raise CommandInputError("repository root must be absolute without traversal")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise CommandInputError("repository root must exist") from exc
    if resolved != path or path.is_symlink() or not path.is_dir():
        raise CommandInputError(
            "repository root must be a resolved nonsymlink directory"
        )
    return path


def confined_path(root: Path, supplied: Path, label: str, *, output: bool) -> Path:
    """Resolve one explicit root-relative path without traversal or symlinks."""
    if supplied.is_absolute() or ".." in supplied.parts or not supplied.parts:
        raise CommandInputError(
            f"{label} must be a root-relative path without traversal"
        )
    candidate = root.joinpath(supplied)
    try:
        parent = candidate.parent.resolve(strict=True)
        parent.relative_to(root)
    except (OSError, ValueError) as exc:
        raise CommandInputError(
            f"{label} parent must exist below repository root"
        ) from exc
    if parent != candidate.parent or candidate.parent.is_symlink():
        raise CommandInputError(f"{label} must not traverse a symlink")
    if output:
        if candidate.exists() or candidate.is_symlink():
            try:
                resolved = candidate.resolve(strict=True)
            except OSError as exc:
                raise CommandInputError(f"{label} is not a valid output file") from exc
            if (
                resolved != candidate
                or candidate.is_symlink()
                or not candidate.is_file()
            ):
                raise CommandInputError(
                    f"{label} must be absent or a nonsymlink regular file"
                )
        return candidate
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise CommandInputError(f"{label} must exist below repository root") from exc
    if resolved != candidate or candidate.is_symlink() or not candidate.is_file():
        raise CommandInputError(f"{label} must name a nonsymlink regular file")
    return candidate


def read_input(root: Path, supplied: Path, label: str) -> bytes:
    """Read one confined explicit input file."""
    path = confined_path(root, supplied, label, output=False)
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CommandInputError(f"could not read {label}") from exc


def write_atomic(root: Path, supplied: Path, content: bytes, label: str) -> Path:
    """Atomically create one explicit confined output without replacement."""
    path = confined_path(root, supplied, label, output=True)
    if path.exists() or path.is_symlink():
        raise CommandInputError(f"{label} already exists and is immutable")
    temporary: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    except OSError as exc:
        raise CommandInputError(f"could not atomically write {label}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return path


def parse_json_object(payload: bytes, label: str) -> dict[str, Any]:
    """Decode one duplicate-free UTF-8 JSON object."""

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise CommandInputError(f"{label} contains duplicate key {key}")
            result[key] = value
        return result

    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CommandInputError(f"{label} must be UTF-8 JSON") from exc
    if type(value) is not dict:
        raise CommandInputError(f"{label} must contain one JSON object")
    return value


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    """Require exact closed JSON object keys."""
    if set(value) != expected:
        missing = sorted(expected - set(value))
        unknown = sorted(set(value) - expected)
        detail = f"missing {missing[0]}" if missing else f"unknown {unknown[0]}"
        raise CommandInputError(f"{label} has {detail}")


def _identity_object(value: ArtifactIdentity) -> dict[str, object]:
    return {
        "algorithm": value.algorithm,
        "digest": value.digest,
        "schema_version": value.schema_version,
    }


def _detail(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def _mapping_inputs(
    payload: bytes,
    source_path: str,
    source_revision: str,
    git_object: str | None,
    source_content: bytes,
) -> tuple[str, tuple[HarnessTaskSourceMapping, ...]]:
    record = parse_json_object(payload, "source mapping record")
    exact_keys(
        record,
        {
            "byte_count",
            "documentation_path",
            "git_object",
            "mappings",
            "schema_version",
            "source_path",
            "source_revision",
            "source_sha256",
        },
        "source mapping record",
    )
    if record["schema_version"] != 1:
        raise CommandInputError("source mapping record schema_version must equal 1")
    expected = {
        "source_path": source_path,
        "source_revision": source_revision,
        "git_object": git_object,
        "byte_count": len(source_content),
        "source_sha256": sha256(source_content),
    }
    for name, expected_value in expected.items():
        if record[name] != expected_value:
            raise ValueError(f"stale source {name}")
    documentation_path = record["documentation_path"]
    if type(documentation_path) is not str:
        raise CommandInputError("documentation_path must be a string")
    raw_mappings = record["mappings"]
    if type(raw_mappings) is not list:
        raise CommandInputError("mappings must be a JSON array")
    source_identity = artifact_identity(source_content)
    mappings: list[HarnessTaskSourceMapping] = []
    keys = {
        "disposition",
        "end_byte",
        "mapping_id",
        "rationale",
        "span_sha256",
        "start_byte",
        "target_references",
        "transformation",
    }
    for index, raw in enumerate(raw_mappings):
        if type(raw) is not dict:
            raise CommandInputError(f"mapping {index} must be an object")
        exact_keys(raw, keys, f"mapping {index}")
        targets = raw["target_references"]
        if type(targets) is not list:
            raise CommandInputError(
                f"mapping {index} target_references must be an array"
            )
        start = raw["start_byte"]
        end = raw["end_byte"]
        if type(start) is not int or type(end) is not int:
            raise CommandInputError(f"mapping {index} bounds must be integers")
        span = source_content[start:end] if 0 <= start <= end else b""
        if raw["span_sha256"] != sha256(span):
            raise ValueError(f"mapping {index} span identity is stale")
        mappings.append(
            HarnessTaskSourceMapping(
                raw["mapping_id"],
                source_identity,
                start,
                end,
                artifact_identity(span),
                HarnessTaskSourceDisposition(raw["disposition"]),
                tuple(targets),
                raw["transformation"],
                raw["rationale"],
            )
        )
    return documentation_path, tuple(mappings)


def _projection(payload: bytes) -> HarnessTaskProjectionProfile:
    record = parse_json_object(payload, "projection profile")
    exact_keys(
        record,
        {
            "final_lf",
            "profile_id",
            "schema_version",
            "template_bytes_base64",
            "template_encoding",
            "template_identity",
        },
        "projection profile",
    )
    if record["template_encoding"] != "base64":
        raise CommandInputError("projection profile template_encoding must be base64")
    try:
        template = base64.b64decode(record["template_bytes_base64"], validate=True)
    except (TypeError, ValueError) as exc:
        raise CommandInputError(
            "projection profile template must be canonical base64"
        ) from exc
    identity_record = record["template_identity"]
    if type(identity_record) is not dict:
        raise CommandInputError(
            "projection profile template_identity must be an object"
        )
    exact_keys(
        identity_record,
        {"algorithm", "digest", "schema_version"},
        "projection profile template_identity",
    )
    if identity_record != _identity_object(artifact_identity(template)):
        raise ValueError("projection profile template identity is stale")
    return HarnessTaskProjectionProfile(
        record["schema_version"],
        record["profile_id"],
        template,
        artifact_identity(template),
        record["final_lf"],
    )


def _review_packet(
    request: HarnessTaskMigrationReviewPacketRequest,
) -> HumanReviewPacket:
    source = request.source
    rendered = request.rendered_documentation
    comparison = request.comparison
    canonical_identity = artifact_identity(request.canonical_task_json)
    mapping_account = [
        {
            "disposition": mapping.disposition.value,
            "end_byte": mapping.end_byte,
            "mapping_id": mapping.mapping_id,
            "rationale": mapping.rationale,
            "source_identity": _identity_object(mapping.source_identity),
            "span_identity": _identity_object(mapping.span_identity),
            "start_byte": mapping.start_byte,
            "target_references": list(mapping.target_references),
            "transformation": mapping.transformation,
        }
        for mapping in request.mappings
    ]
    opaque_blocks = [
        {
            "mapping_id": mapping.mapping_id,
            "preserved": True,
            "span_identity": _identity_object(mapping.span_identity),
        }
        for mapping in request.mappings
        if mapping.disposition
        is HarnessTaskSourceDisposition.DOCUMENTATION_OWNED_CONTENT
    ]
    observations = (
        HumanReviewObservation(
            "harness-task-migration.candidate-json",
            "candidate canonical HarnessTask JSON identity",
            "passed",
            "The candidate canonical JSON is bound to the reviewed packet.",
            request.candidate_task.documentation_path,
            _detail(
                {
                    "byte_count": len(request.canonical_task_json),
                    "candidate_task_id": request.candidate_task.task_id,
                    "identity": _identity_object(canonical_identity),
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.comparison",
            "exact source and rendered byte comparison",
            "failed" if comparison.unmapped_spans else "passed",
            "The exact comparison result is bound to the reviewed packet.",
            rendered.path,
            _detail(
                {
                    "differences": list(comparison.differences),
                    "rendered_identity": _identity_object(comparison.rendered_identity),
                    "source_identity": _identity_object(comparison.source_identity),
                    "status": comparison.status,
                    "unmapped_spans": [
                        list(span) for span in comparison.unmapped_spans
                    ],
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.limitations",
            "applicable comparison limitations",
            "passed",
            "Every applicable comparison limitation is bound to the packet.",
            rendered.path,
            _detail({"limitations": list(comparison.limitations)}),
        ),
        HumanReviewObservation(
            "harness-task-migration.mappings",
            "source mappings and unmapped-span account",
            "failed" if comparison.unmapped_spans else "passed",
            "All source mappings and unmapped spans are bound to the packet.",
            source.path,
            _detail(
                {
                    "mappings": mapping_account,
                    "unmapped_spans": [
                        list(span) for span in comparison.unmapped_spans
                    ],
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.opaque-blocks",
            "opaque documentation-block preservation",
            "passed",
            "Every documentation-owned source block is preserved exactly.",
            rendered.path,
            _detail({"documentation_blocks": opaque_blocks}),
        ),
        HumanReviewObservation(
            "harness-task-migration.rendered",
            "rendered-document identity",
            "passed",
            "The rendered document bytes are bound to the reviewed packet.",
            rendered.path,
            _detail(
                {
                    "byte_count": len(rendered.content),
                    "identity": _identity_object(rendered.artifact_identity),
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.source",
            "source identity and byte count",
            "passed",
            "The exact source bytes are bound to the reviewed packet.",
            source.path,
            _detail(
                {
                    "artifact_identity": _identity_object(source.artifact_identity),
                    "byte_count": source.byte_count,
                    "git_object": source.git_object,
                    "path": source.path,
                    "revision": source.revision,
                }
            ),
        ),
    )
    target = HumanReviewTarget(
        f"harness-task-migration.{request.candidate_task.task_id}",
        source.revision,
        f"HarnessTask migration candidate {request.candidate_task.task_id} "
        f"from {source.path} to {rendered.path}",
        (source.path, rendered.path),
        "software_verification",
        _CONTRACT_REFERENCES,
    )
    return HumanReviewPreparer().execute(
        target, observations, comparison.findings, comparison.limitations
    )


def prepare_review(
    *,
    source_path: str,
    source_revision: str,
    git_object: str | None,
    source_content: bytes,
    candidate_payload: bytes,
    mapping_payload: bytes,
    profile_payload: bytes,
    review_output_path: str,
) -> PreparedMigrationReview:
    """Reconstruct and validate one packet from exact explicit input bytes."""
    source = HarnessTaskDocumentSource(
        source_path,
        source_revision,
        git_object,
        source_content,
        len(source_content),
        artifact_identity(source_content),
    )
    task = HarnessTaskDeserializer().execute(candidate_payload)
    canonical = HarnessTaskSerializer().execute(task)
    if candidate_payload != canonical:
        raise ValueError("candidate HarnessTask JSON must be canonical")
    documentation_path, mappings = _mapping_inputs(
        mapping_payload, source_path, source_revision, git_object, source_content
    )
    if documentation_path != task.documentation_path:
        raise ValueError("mapping documentation_path differs from candidate Task")
    documentation_mappings = tuple(
        mapping
        for mapping in mappings
        if mapping.disposition
        is HarnessTaskSourceDisposition.DOCUMENTATION_OWNED_CONTENT
    )
    content = HarnessTaskDocumentationContent(
        source.artifact_identity,
        documentation_path,
        tuple(mapping.mapping_id for mapping in documentation_mappings),
        tuple(
            source_content[mapping.start_byte : mapping.end_byte]
            for mapping in documentation_mappings
        ),
    )
    profile = _projection(profile_payload)
    rendered = HarnessTaskDocumentationRenderer().execute(task, content, profile)
    comparison = HarnessTaskDocumentationComparator().execute(
        source, rendered, mappings
    )
    placeholder_target = HumanReviewTarget(
        f"harness-task-migration.{task.task_id}",
        source.revision,
        f"HarnessTask migration candidate {task.task_id} "
        f"from {source.path} to {rendered.path}",
        (source.path, rendered.path),
        "software_verification",
        _CONTRACT_REFERENCES,
    )
    placeholder = HumanReviewPreparer().execute(
        placeholder_target, (), comparison.findings, comparison.limitations
    )
    draft = HarnessTaskMigrationReviewPacketRequest(
        source,
        mappings,
        task,
        canonical,
        content,
        profile,
        rendered,
        comparison,
        placeholder,
    )
    review = _review_packet(draft)
    request = HarnessTaskMigrationReviewPacketRequest(
        source,
        mappings,
        task,
        canonical,
        content,
        profile,
        rendered,
        comparison,
        review,
    )
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(request)
    document = HarnessTaskMigrationReviewPacketRenderer().execute(packet)
    binding = canonical_json_bytes(
        {
            "candidate_json_sha256": sha256(candidate_payload),
            "mapping_record_sha256": sha256(mapping_payload),
            "profile_sha256": sha256(profile_payload),
            "rendered_document_sha256": rendered.artifact_identity.digest,
            "review_document": {
                "path": review_output_path,
                "sha256": document.artifact_identity.digest,
            },
            "source": {
                "byte_count": source.byte_count,
                "git_object": source.git_object,
                "path": source.path,
                "revision": source.revision,
                "sha256": source.artifact_identity.digest,
            },
        }
    )
    return PreparedMigrationReview(
        packet, document, sha256(binding), sha256(candidate_payload)
    )
