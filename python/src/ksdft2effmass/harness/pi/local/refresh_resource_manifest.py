"""Thin read-only command for explicit resource-manifest identity refresh."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from .. import (
    DeserializeJsonRecord,
    RefreshResourceManifest,
    ResourceManifest,
    ResourceManifestRefreshRequest,
    ResourceManifestRefreshResult,
    SerializeJsonRecord,
    ValidationIssue,
    ValidationResult,
    WireRecordKind,
)


def _issue_object(issue: ValidationIssue) -> dict[str, object]:
    return {
        "code": issue.code,
        "message": issue.message,
        "path": issue.path,
        "related_ids": list(issue.related_ids),
        "severity": issue.severity,
        "subject_id": issue.subject_id,
    }


def _command_object(
    result: ResourceManifestRefreshResult,
) -> dict[str, object]:
    proposed_manifest: str | None = None
    if result.manifest is not None:
        serialized = SerializeJsonRecord().execute(result.manifest)
        if serialized.payload is None:
            raise AssertionError("successful serialization must contain payload")
        proposed_manifest = serialized.payload.decode("utf-8")
    return {
        "changed_resource_ids": list(result.changed_resource_ids),
        "findings": [_issue_object(issue) for issue in result.validation.issues],
        "proposed_manifest": proposed_manifest,
        "schema_version": 1,
        "status": result.validation.status,
    }


def _failure_object(validation: ValidationResult) -> dict[str, object]:
    return {
        "changed_resource_ids": [],
        "findings": [_issue_object(issue) for issue in validation.issues],
        "proposed_manifest": None,
        "schema_version": 1,
        "status": validation.status,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Parse explicit inputs, invoke the ActionObject, and emit canonical JSON.

    Exit status ``0`` reports a proposal, ``1`` reports structured validation
    failure, ``2`` reports invalid command inputs, and ``3`` is reserved for the
    last-resort command boundary. The command never writes the manifest.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--resource-id", required=True, action="append")
    args = parser.parse_args(argv)
    try:
        if not args.manifest.is_absolute():
            raise ValueError("manifest path must be absolute")
        if args.manifest.is_symlink() or not args.manifest.is_file():
            raise ValueError("manifest path must name a regular nonsymlink file")
        decoded = DeserializeJsonRecord().execute(
            WireRecordKind.ResourceManifest, args.manifest.read_bytes()
        )
        if decoded.validation.status == "FAIL":
            payload = _failure_object(decoded.validation)
            exit_status = 1
        else:
            if type(decoded.record) is not ResourceManifest:
                raise AssertionError("resource manifest decoder returned wrong kind")
            request = ResourceManifestRefreshRequest(
                args.root,
                decoded.record,
                tuple(args.resource_id),
            )
            result = RefreshResourceManifest().execute(request)
            payload = _command_object(result)
            exit_status = 0 if result.validation.status != "FAIL" else 1
    except (TypeError, ValueError, OSError) as exc:
        payload = {"error": str(exc), "schema_version": 1, "status": "ERROR"}
        exit_status = 2
    print(
        json.dumps(
            payload,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return exit_status


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - last-resort command boundary
        print(
            json.dumps(
                {"error": str(exc), "schema_version": 1, "status": "ERROR"},
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(3) from exc
