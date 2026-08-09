"""Record one explicit HarnessTask migration disposition from exact inputs."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from .. import HumanReviewDecisionRecorder
from ._harness_task_migration_cli import (
    CommandInputError,
    canonical_json_bytes,
    prepare_review,
    read_input,
    resolved_root,
    sha256,
    write_atomic,
)
from .task_model import (
    HarnessTaskMigrationDisposition,
    HarnessTaskMigrationFileDispositionRecorder,
)

_GENERIC = ("accepted", "bounded_correction", "deferred", "rejected")
_MIGRATION = tuple(item.value for item in HarnessTaskMigrationDisposition)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--source-markdown", required=True, type=Path)
    parser.add_argument("--source-revision", required=True)
    git_group = parser.add_mutually_exclusive_group(required=True)
    git_group.add_argument("--git-object")
    git_group.add_argument("--git-object-absent", action="store_true")
    parser.add_argument("--candidate-task-json", required=True, type=Path)
    parser.add_argument("--source-mapping-record", required=True, type=Path)
    parser.add_argument("--projection-profile", required=True, type=Path)
    parser.add_argument("--review-document", required=True, type=Path)
    parser.add_argument("--expected-review-sha256", required=True)
    parser.add_argument("--expected-review-byte-count", required=True, type=int)
    parser.add_argument("--expected-packet-binding-sha256", required=True)
    response_group = parser.add_mutually_exclusive_group(required=True)
    response_group.add_argument("--human-response-file", type=Path)
    response_group.add_argument("--human-response")
    parser.add_argument("--generic-disposition", required=True, choices=_GENERIC)
    parser.add_argument("--authorized-correction-scope", action="append", default=[])
    parser.add_argument("--migration-disposition", required=True, choices=_MIGRATION)
    parser.add_argument("--output-disposition-record", required=True, type=Path)
    return parser


def _emit(value: object, *, stream: TextIO | None = None) -> None:
    print(
        canonical_json_bytes(value).decode("ascii"),
        end="",
        file=sys.stdout if stream is None else stream,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Revalidate exact material, invoke both recorders, and write canonical JSON.

    Exit status ``0`` is success, ``1`` is deterministic incompatibility or stale
    binding, ``2`` is invalid command input, and ``3`` is unexpected failure.
    """
    try:
        args = _parser().parse_args(argv)
        root = resolved_root(args.repository_root)
        source = read_input(root, args.source_markdown, "source Markdown")
        candidate = read_input(root, args.candidate_task_json, "candidate Task JSON")
        mappings = read_input(root, args.source_mapping_record, "source mapping record")
        profile = read_input(root, args.projection_profile, "projection profile")
        review_document = read_input(root, args.review_document, "review document")
        if args.human_response_file is not None:
            response_bytes = read_input(
                root, args.human_response_file, "human response"
            )
            try:
                human_response = response_bytes.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise CommandInputError("human response must be UTF-8") from exc
        else:
            human_response = args.human_response
        git_object = None if args.git_object_absent else args.git_object
    except (CommandInputError, OSError, TypeError, ValueError) as exc:
        _emit({"error": str(exc), "schema_version": 1, "status": "INVALID_INPUT"})
        return 2
    try:
        prepared = prepare_review(
            source_path=args.source_markdown.as_posix(),
            source_revision=args.source_revision,
            git_object=git_object,
            source_content=source,
            candidate_payload=candidate,
            mapping_payload=mappings,
            profile_payload=profile,
            review_output_path=args.review_document.as_posix(),
        )
        if prepared.packet_binding_sha256 != args.expected_packet_binding_sha256:
            raise ValueError("packet binding substitution or staleness")
        if review_document != prepared.document.content:
            raise ValueError("review document substitution or staleness")
        if len(review_document) != args.expected_review_byte_count:
            raise ValueError("review document byte count is stale")
        if sha256(review_document) != args.expected_review_sha256:
            raise ValueError("review document SHA-256 is stale")
        decision = HumanReviewDecisionRecorder().execute(
            prepared.packet.request.human_review_packet,
            human_response,
            args.generic_disposition,
            tuple(args.authorized_correction_scope),
        )
        disposition = HarnessTaskMigrationFileDispositionRecorder().execute(
            prepared.packet,
            decision,
            HarnessTaskMigrationDisposition(args.migration_disposition),
        )
        record = {
            "authorized_correction_scope": list(decision.authorized_scope),
            "candidate_json_sha256": prepared.candidate_json_sha256,
            "generic_disposition": decision.disposition,
            "human_response": decision.human_response,
            "migration_disposition": disposition.migration_disposition.value,
            "packet_binding_sha256": prepared.packet_binding_sha256,
            "record_kind": "ksdft2effmass.harness-task-migration-file-disposition",
            "review_document": {
                "byte_count": len(review_document),
                "path": args.review_document.as_posix(),
                "sha256": sha256(review_document),
            },
            "schema_version": 1,
            "source": {
                "byte_count": len(source),
                "git_object": git_object,
                "path": args.source_markdown.as_posix(),
                "revision": args.source_revision,
                "sha256": sha256(source),
            },
        }
        payload = canonical_json_bytes(record)
        output = write_atomic(
            root,
            args.output_disposition_record,
            payload,
            "output disposition record",
        )
    except CommandInputError as exc:
        _emit({"error": str(exc), "schema_version": 1, "status": "INVALID_INPUT"})
        return 2
    except (TypeError, ValueError) as exc:
        _emit({"error": str(exc), "schema_version": 1, "status": "INVALID_DISPOSITION"})
        return 1
    _emit(
        {
            "disposition_record": {
                "byte_count": len(payload),
                "path": output.relative_to(root).as_posix(),
                "sha256": sha256(payload),
            },
            "packet_binding_sha256": prepared.packet_binding_sha256,
            "schema_version": 1,
            "status": "PASS",
        }
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - last-resort boundary
        _emit(
            {
                "error": f"{type(exc).__name__}: {exc}",
                "schema_version": 1,
                "status": "INTERNAL_ERROR",
            },
            stream=sys.stderr,
        )
        raise SystemExit(3) from exc
