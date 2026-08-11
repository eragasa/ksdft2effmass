"""Thin command wrapper for bounded durable task-state inspection."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi import (
    TaskStateInspectionRequest,
    TaskStateInspectionResult,
    TaskStateInspector,
    ValidationIssue,
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


def result_object(result: TaskStateInspectionResult) -> dict[str, object]:
    """Return the deterministic command projection of one public result."""
    return {
        "active_task": result.active_task_id,
        "artifact_paths": list(result.artifact_paths),
        "chain_path": result.chain_path,
        "completion_command": list(result.completion_command),
        "completion_validator_path": result.completion_validator_path,
        "durable_handoff_record_status": result.durable_handoff_record_status,
        "durable_run_record_status": result.durable_run_record_status,
        "findings": [_issue_object(issue) for issue in result.validation.issues],
        "handoff_record_paths": list(result.handoff_record_paths),
        "inspected_paths": list(result.inspected_paths),
        "limitations": list(result.limitations),
        "ownership_manifest_path": result.ownership_manifest_path,
        "read_paths": list(result.read_paths),
        "repository_root": result.repository_root.as_posix(),
        "reviewers": [list(value) for value in result.reviewers],
        "run_record_paths": list(result.run_record_paths),
        "schema_version": result.schema_version,
        "status": result.validation.status,
        "task_id": result.task_id,
        "task_record_path": result.task_record_path,
        "task_status": result.task_status,
        "writers": [list(value) for value in result.writers],
    }


def run(argv: Sequence[str] | None = None) -> int:
    """Parse explicit inputs, invoke the ActionObject, and render canonical JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--chain", required=True)
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args(argv)
    try:
        request = TaskStateInspectionRequest(
            1,
            args.root.absolute(),
            args.chain,
            args.task_id,
        )
        result = TaskStateInspector().execute(request)
        payload = result_object(result)
        exit_status = 0 if result.validation.status != "FAIL" else 1
    except (TypeError, ValueError, OSError) as exc:
        payload = {
            "error": str(exc),
            "schema_version": 1,
            "status": "ERROR",
        }
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
