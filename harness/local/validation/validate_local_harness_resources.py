#!/usr/bin/env -S python/.venv/bin/python
"""Validate explicitly supplied current harness resource composition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ksdft2effmass.harness.pi import ResourceResolver, ValidationIssue
from ksdft2effmass.harness.pi.local import (
    LocalHarnessContext,
    LocalHarnessContextLoader,
    LocalIssue,
    RepositoryRoots,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--generic-resource-root", type=Path, required=True)
    parser.add_argument("--local-resource-root", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--generic-manifest", type=Path, required=True)
    parser.add_argument("--local-manifest", type=Path, required=True)
    return parser


def _emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def _issue_payload(issue: LocalIssue | ValidationIssue) -> dict[str, object]:
    detail = issue.detail if isinstance(issue, LocalIssue) else issue.message
    return {
        "code": issue.code,
        "detail": detail,
        "path": str(issue.path) if issue.path is not None else None,
    }


def _read_file(path: Path, root: Path, label: str) -> bytes:
    if not path.is_absolute():
        raise ValueError(f"{label} path must be absolute")
    if ".." in path.parts:
        raise ValueError(f"{label} path must not contain parent traversal")
    try:
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise ValueError(
            f"{label} path must resolve below its explicit resource root"
        ) from exc
    if resolved_path != path or not path.is_file() or path.is_symlink():
        raise ValueError(f"{label} path must select a nonsymlink regular file")
    return path.read_bytes()


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        for value, label in (
            (args.repository_root, "repository root"),
            (args.generic_resource_root, "generic resource root"),
            (args.local_resource_root, "local resource root"),
        ):
            if not value.is_absolute():
                raise ValueError(f"{label} must be an absolute path")
            if ".." in value.parts or value.resolve(strict=True) != value:
                raise ValueError(f"{label} must be a resolved nonsymlink path")
        roots = RepositoryRoots(
            args.repository_root,
            args.generic_resource_root,
            args.local_resource_root,
        )
        profile_bytes = _read_file(args.profile, roots.local_resource_root, "profile")
        generic_bytes = _read_file(
            args.generic_manifest, roots.generic_resource_root, "generic manifest"
        )
        local_bytes = _read_file(
            args.local_manifest, roots.local_resource_root, "local manifest"
        )
    except (OSError, TypeError, ValueError) as exc:
        _emit(
            {
                "error": str(exc),
                "resources": [],
                "schema_version": 1,
                "stage": "input",
                "status": "INVALID_INPUT",
            }
        )
        return 2

    try:
        adapted = LocalHarnessContextLoader().execute(
            roots, profile_bytes, generic_bytes, local_bytes
        )
        if type(adapted.value) is not LocalHarnessContext:
            _emit(
                {
                    "issues": [
                        _issue_payload(issue) for issue in adapted.validation.issues
                    ],
                    "resources": [],
                    "schema_version": 1,
                    "stage": "context",
                    "status": "FAIL",
                }
            )
            return 1
        context = adapted.value
        resource_ids = tuple(
            sorted(
                resource.resource_id
                for manifest in (context.generic_manifest, context.local_manifest)
                for resource in manifest.resources
            )
        )
        resources: list[dict[str, object]] = []
        failed = False
        for resource_id in resource_ids:
            result = ResourceResolver().execute(
                resource_id,
                roots.generic_resource_root,
                context.generic_manifest,
                context.generic_manifest_identity,
                roots.local_resource_root,
                context.local_manifest,
                context.local_manifest_identity,
                context.profile,
            )
            failed = failed or result.validation.status == "FAIL"
            resources.append(
                {
                    "issues": [
                        _issue_payload(issue) for issue in result.validation.issues
                    ],
                    "resource_id": resource_id,
                    "status": result.validation.status,
                }
            )
        _emit(
            {
                "issues": [],
                "resources": resources,
                "schema_version": 1,
                "stage": "resources",
                "status": "FAIL" if failed else "PASS",
            }
        )
        return 1 if failed else 0
    except Exception as exc:  # noqa: BLE001 - last-resort command boundary
        _emit(
            {
                "error": f"{type(exc).__name__}: {exc}",
                "resources": [],
                "schema_version": 1,
                "stage": "internal",
                "status": "INTERNAL_ERROR",
            }
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
