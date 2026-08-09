"""Prepare one deterministic HarnessTask migration review from explicit files."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from ._harness_task_migration_cli import (
    CommandInputError,
    canonical_json_bytes,
    ensure_identical_output,
    prepare_review,
    read_input,
    resolved_root,
)


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
    parser.add_argument("--output-review-document", required=True, type=Path)
    return parser


def _emit(value: object, *, stream: TextIO | None = None) -> None:
    payload = canonical_json_bytes(value).decode("ascii")
    print(payload, end="", file=sys.stdout if stream is None else stream)


def main(argv: Sequence[str] | None = None) -> int:
    """Invoke accepted ActionObjects and make one review document available.

    Exit status ``0`` is success, ``1`` is deterministic packet invalidity, ``2``
    is invalid command input, and ``3`` is an unexpected command failure.
    """
    try:
        args = _parser().parse_args(argv)
        root = resolved_root(args.repository_root)
        source = read_input(root, args.source_markdown, "source Markdown")
        candidate = read_input(root, args.candidate_task_json, "candidate Task JSON")
        mappings = read_input(root, args.source_mapping_record, "source mapping record")
        profile = read_input(root, args.projection_profile, "projection profile")
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
            review_output_path=args.output_review_document.as_posix(),
        )
        output = ensure_identical_output(
            root,
            args.output_review_document,
            prepared.document.content,
            "output review document",
        )
    except CommandInputError as exc:
        _emit({"error": str(exc), "schema_version": 1, "status": "INVALID_INPUT"})
        return 2
    except (TypeError, ValueError) as exc:
        _emit({"error": str(exc), "schema_version": 1, "status": "INVALID_PACKET"})
        return 1
    _emit(
        {
            "candidate_json_sha256": prepared.candidate_json_sha256,
            "packet_binding_sha256": prepared.packet_binding_sha256,
            "review_document": {
                "byte_count": len(prepared.document.content),
                "path": output.relative_to(root).as_posix(),
                "sha256": prepared.document.artifact_identity.digest,
            },
            "result": "available",
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
