#!/usr/bin/env -S python/.venv/bin/python
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

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DIR = ROOT / ".pi" / "checkpoints"
SCHEMA_PATH = CHECKPOINT_DIR / "checkpoint.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(
    record: Any, path: Path, validator: Draft202012Validator
) -> list[str]:
    """Return complete Draft 2020-12 checkpoint-schema violations.

    Errors are sorted by instance path so repeated validation is deterministic.
    The authoritative JSON Schema owns field types, required properties,
    additional-property rejection, option structure, enums, and resolved-record
    conditional constraints.
    """

    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(record), key=lambda item: list(item.absolute_path)
    ):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{path}:{location}: {error.message}")
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
    """Return duplicate resolutions of the same checkpoint identity and option.

    Different checkpoints for one task may legitimately use the same local option
    label, such as ``A``. Duplicate detection therefore keys the durable checkpoint
    identity rather than the task identity.
    """

    seen: dict[tuple[str | None, str | None], Path] = {}
    duplicates: list[str] = []
    for path in checkpoint_paths(include_fixtures=False):
        record = load_json(path)
        if record.get("status") != "resolved":
            continue
        key = (record.get("checkpoint_id"), record.get("normalized_decision"))
        if key in seen:
            duplicates.append(
                f"{seen[key]} and {path}: duplicate resolved decision {key}"
            )
        else:
            seen[key] = path
    return duplicates


def response_approves_option_b(response: str) -> bool:
    """Return whether a synthetic response unambiguously approves only Option B."""

    normalized = " ".join(response.casefold().split())
    rejects = re.search(
        r"\b(?:reject(?:ed|ing|s)?|do not approve|don't approve)\b", normalized
    )
    approves = re.search(r"\bapprove(?:d|s|ing)?\b", normalized)
    selects_b = re.search(r"\boption\s+b\b", normalized)
    selects_a = re.search(r"\boption\s+a\b", normalized)
    return bool(approves and selects_b and not selects_a and not rejects)


def resolve_synthetic(record: dict[str, Any], response: str) -> dict[str, Any]:
    """Resolve the fixed dry-run fixture after an unambiguous Option-B response."""

    option_ids = [option.get("id") for option in record.get("options", [])]
    if option_ids != ["A", "B"] or not response_approves_option_b(response):
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
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for path in checkpoint_paths(include_fixtures=args.include_fixtures):
        all_errors.extend(validate_schema(load_json(path), path, validator))

    unresolved = scan_unresolved()
    duplicates = scan_duplicate_decisions()
    all_errors.extend(duplicates)

    if args.dry_run:
        stage_errors: dict[str, int] = {}
        pending = load_json(CHECKPOINT_DIR / "fixtures" / "pending-checkpoint.json")
        expected = load_json(CHECKPOINT_DIR / "fixtures" / "resolved-checkpoint.json")

        start = len(all_errors)
        actual = resolve_synthetic(pending, "SYNTHETIC DRY RUN: Approve Option B.")
        if actual != expected:
            all_errors.append(
                "fresh-session checkpoint-resolution dry run did not match expected resolved fixture"
            )
        for contradictory in (
            "I do not approve Option B.",
            "Approve Option A.",
            "Option B is rejected.",
        ):
            try:
                resolve_synthetic(pending, contradictory)
            except ValueError:
                continue
            all_errors.append(
                f"synthetic resolver accepted ambiguous response: {contradictory!r}"
            )
        stage_errors["checkpoint_resolution"] = len(all_errors) - start

        start = len(all_errors)
        if actual.get("resumption_status") != "resumed_for_dry_run":
            all_errors.append("fresh-session task-resumption dry run did not resume")
        stage_errors["task_resumption"] = len(all_errors) - start

        start = len(all_errors)
        deterministic = {
            "finding": "SYNTHETIC DRY RUN: deterministic corrective finding",
            "decision_class": "deterministic_agent_correction",
            "checkpoint_created": False,
            "correction_recorded": True,
            "validation_rerun": True,
        }
        if deterministic["checkpoint_created"]:
            all_errors.append(
                "deterministic corrective finding incorrectly created a checkpoint"
            )
        stage_errors["deterministic_correction"] = len(all_errors) - start

        start = len(all_errors)
        invalid_extra = deepcopy(pending)
        invalid_extra["forbidden_extra_property"] = True
        if not validate_schema(
            invalid_extra, Path("<dry-run-extra-property>"), validator
        ):
            all_errors.append(
                "Draft 2020-12 dry run failed to reject an additional property"
            )
        invalid_option = deepcopy(pending)
        invalid_option["options"][0]["unexpected"] = "forbidden"
        if not validate_schema(
            invalid_option, Path("<dry-run-option-shape>"), validator
        ):
            all_errors.append(
                "Draft 2020-12 dry run failed to reject an invalid option shape"
            )
        stage_errors["checkpoint_schema"] = len(all_errors) - start

        for stage in (
            "checkpoint_schema",
            "checkpoint_resolution",
            "task_resumption",
            "deterministic_correction",
        ):
            status = "passed" if stage_errors[stage] == 0 else "failed"
            print(f"dry_run_{stage}={status}")

    print(
        f"checkpoint_records_validated={len(checkpoint_paths(include_fixtures=args.include_fixtures))}"
    )
    print(f"unresolved_checkpoints={len(unresolved)}")
    print(f"duplicate_resolved_decisions={len(duplicates)}")
    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
