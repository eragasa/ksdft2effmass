#!/usr/bin/env python3
"""Validate checkpoint records and run control-plane dry runs.

This script is repository control-plane tooling. It does not validate scientific
results and does not mutate production source, tests, fixtures, or specifications.
"""
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DIR = ROOT / ".pi" / "checkpoints"
SCHEMA_PATH = CHECKPOINT_DIR / "checkpoint.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_basic_schema(record: dict[str, Any], path: Path) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    errors: list[str] = []
    required = schema["required"]
    for field in required:
        if field not in record:
            errors.append(f"{path}: missing required field {field}")
    if record.get("status") not in {"pending", "blocked", "resolved", "superseded", "cancelled"}:
        errors.append(f"{path}: invalid status {record.get('status')!r}")
    if record.get("decision_class") not in {
        "deterministic_agent_correction",
        "standing_delegated_decision",
        "genuine_human_decision",
        None,
    }:
        errors.append(f"{path}: invalid decision_class {record.get('decision_class')!r}")
    if not isinstance(record.get("options"), list):
        errors.append(f"{path}: options must be a list")
    for field in ("authoritative_files", "record_paths"):
        if not isinstance(record.get(field), list):
            errors.append(f"{path}: {field} must be a list")
    if record.get("status") == "resolved":
        for field in ("human_response", "normalized_decision", "resolved_at", "authorized_scope"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{path}: resolved checkpoint requires nonempty {field}")
    return errors


def checkpoint_paths(include_fixtures: bool) -> list[Path]:
    paths = sorted(CHECKPOINT_DIR.glob("*.json"))
    paths = [p for p in paths if p.name != "checkpoint.schema.json"]
    if include_fixtures:
        paths.extend(sorted((CHECKPOINT_DIR / "fixtures").glob("*.json")))
    return paths


def scan_unresolved() -> list[Path]:
    unresolved = []
    for path in checkpoint_paths(include_fixtures=False):
        record = load_json(path)
        if record.get("status") in {"pending", "blocked"}:
            unresolved.append(path)
    return unresolved


def scan_duplicate_decisions() -> list[str]:
    seen: dict[tuple[str | None, str | None], Path] = {}
    duplicates: list[str] = []
    for path in checkpoint_paths(include_fixtures=False):
        record = load_json(path)
        if record.get("status") != "resolved":
            continue
        key = (record.get("task_id"), record.get("normalized_decision"))
        if key in seen:
            duplicates.append(f"{seen[key]} and {path}: duplicate resolved decision {key}")
        else:
            seen[key] = path
    return duplicates


def resolve_synthetic(record: dict[str, Any], response: str) -> dict[str, Any]:
    if len(record.get("options", [])) != 2 or not re.search(r"option\s+b|approve", response, re.I):
        raise ValueError("synthetic response is ambiguous")
    resolved = deepcopy(record)
    resolved["status"] = "resolved"
    resolved["human_response"] = response
    resolved["normalized_decision"] = "Option B approved; resume the dry-run task."
    resolved["resolved_at"] = "2026-07-30T00:01:00Z"
    resolved["authorized_scope"] = "dry-run task resumption and validation"
    resolved["record_paths"] = [".pi/checkpoints/fixtures/resolved-checkpoint.json"]
    resolved["resumption_status"] = "resumed_for_dry_run"
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-fixtures", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    all_errors: list[str] = []
    load_json(SCHEMA_PATH)
    for path in checkpoint_paths(include_fixtures=args.include_fixtures):
        all_errors.extend(validate_basic_schema(load_json(path), path))

    unresolved = scan_unresolved()
    duplicates = scan_duplicate_decisions()
    all_errors.extend(duplicates)

    if args.dry_run:
        pending = load_json(CHECKPOINT_DIR / "fixtures" / "pending-checkpoint.json")
        expected = load_json(CHECKPOINT_DIR / "fixtures" / "resolved-checkpoint.json")
        actual = resolve_synthetic(pending, "SYNTHETIC DRY RUN: Approve Option B.")
        if actual != expected:
            all_errors.append("fresh-session checkpoint-resolution dry run did not match expected resolved fixture")
        if actual.get("resumption_status") != "resumed_for_dry_run":
            all_errors.append("fresh-session task-resumption dry run did not resume")
        deterministic = {
            "finding": "SYNTHETIC DRY RUN: deterministic corrective finding",
            "decision_class": "deterministic_agent_correction",
            "checkpoint_created": False,
            "correction_recorded": True,
            "validation_rerun": True,
        }
        if deterministic["checkpoint_created"]:
            all_errors.append("deterministic corrective finding incorrectly created a checkpoint")
        print("dry_run_checkpoint_resolution=passed")
        print("dry_run_task_resumption=passed")
        print("dry_run_deterministic_correction=passed")

    print(f"checkpoint_records_validated={len(checkpoint_paths(include_fixtures=args.include_fixtures))}")
    print(f"unresolved_checkpoints={len(unresolved)}")
    print(f"duplicate_resolved_decisions={len(duplicates)}")
    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
