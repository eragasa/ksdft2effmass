"""Render reusable project-local checkpoint repository validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ..checkpoint_validation import _CheckpointRepositoryValidator


def run(argv: Sequence[str] | None = None) -> int:
    """Validate one explicit checkpoint repository and render stable diagnostics."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--include-fixtures", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    result = _CheckpointRepositoryValidator().execute(
        args.repository_root.resolve(strict=True),
        include_fixtures=args.include_fixtures,
        dry_run=args.dry_run,
    )
    for stage, passed in result.dry_run_stages:
        print(f"dry_run_{stage}={'passed' if passed else 'failed'}")
    print(f"checkpoint_records_validated={result.record_count}")
    print(f"unresolved_checkpoints={len(result.unresolved_paths)}")
    print(f"duplicate_resolved_decisions={len(result.duplicate_decisions)}")
    for error in result.errors:
        print(f"ERROR: {error}")
    return 1 if result.errors else 0
