"""Command adapter for one explicit task-ownership manifest preflight."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.local.task_ownership_validation import (
    OwnershipValidationError,
    _TaskOwnershipManifestValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Run the command-line ownership preflight."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--task-record", required=True, type=Path)
    parser.add_argument("--ownership-manifest", required=True, type=Path)
    arguments = parser.parse_args(argv)
    try:
        root = arguments.repository_root.resolve(strict=True)
        task_record_path = (
            arguments.task_record
            if arguments.task_record.is_absolute()
            else root / arguments.task_record
        )
        ownership_manifest_path = (
            arguments.ownership_manifest
            if arguments.ownership_manifest.is_absolute()
            else root / arguments.ownership_manifest
        )
        manifest_path = (
            _TaskOwnershipManifestValidator()
            .execute(
                task_record_path,
                ownership_manifest_path,
                arguments.task,
                repository_root=root,
            )
            .manifest_path
        )
    except (OSError, OwnershipValidationError) as error:
        print(f"task ownership preflight failed: {error}", file=sys.stderr)
        return 1
    print(f"task ownership preflight passed: {manifest_path.relative_to(root)}")
    return 0
