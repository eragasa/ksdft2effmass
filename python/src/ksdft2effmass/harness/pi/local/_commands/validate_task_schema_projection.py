"""Validate the project-local one-Task JSON cutover and documentation projection."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType
from typing import Any

from . import validate_documentation_projection


def _generic(path: Path) -> ModuleType:
    if path.is_symlink() or not path.is_file():
        raise ValueError("generic validator must name a regular nonsymlink file")
    if path.name != "validate_documentation_projection.py":
        raise ValueError("generic validator has the wrong maintained identity")
    return validate_documentation_projection


def _schema_codes(diagnostics: tuple[str, ...]) -> tuple[str, ...]:
    codes = []
    for diagnostic in diagnostics:
        keyword = diagnostic.rsplit(":", 1)[-1]
        codes.append(
            {
                "required": "TASK_SCHEMA_REQUIRED",
                "additionalProperties": "TASK_SCHEMA_ADDITIONAL_PROPERTIES",
            }.get(keyword, f"TASK_SCHEMA_{keyword.upper()}")
        )
    return tuple(sorted(set(codes)))


def relation_codes(
    task: dict[str, Any], chain: dict[str, Any], record_path: str
) -> tuple[str, ...]:
    """Return fail-closed project Task/chain relational diagnostics."""
    for field in (
        "task_prerequisite_ids",
        "external_prerequisite_ids",
        "authority_reference_paths",
    ):
        values = task[field]
        if values != sorted(values):
            return ("TASK_ARRAY_NOT_SORTED",)
    task_id = task["task_id"]
    task_deps = set(task["task_prerequisite_ids"])
    external = set(task["external_prerequisite_ids"])
    if task_id in task_deps or task_id in external:
        return ("TASK_PREREQUISITE_SELF",)
    if task_deps & external:
        return ("TASK_PREREQUISITE_OVERLAP",)
    entries = chain.get("task_sequence")
    if type(entries) is not list:
        return ("CHAIN_TASK_SEQUENCE_INVALID",)
    referenced = [
        item
        for item in entries
        if type(item) is dict and item.get("record") == record_path
    ]
    if len(referenced) != 1 or referenced[0].get("id") != task_id:
        return ("TASK_CHAIN_ID_MISMATCH",)
    entry = referenced[0]
    duplicated = {
        "status",
        "prerequisites",
        "parent_task_id",
        "task_prerequisite_ids",
        "external_prerequisite_ids",
        "explicit_activation_required",
        "objective",
        "authority_reference_paths",
        "authorized_scope",
        "completion_criteria",
        "exclusions",
        "intake_path",
    } & set(entry)
    if duplicated:
        return ("TASK_CHAIN_AUTHORITY_DUPLICATION",)
    member_ids = [item.get("id") for item in entries if type(item) is dict]
    if any(member_ids.count(dep) != 1 for dep in task_deps):
        return ("TASK_PREREQUISITE_NOT_CHAIN_MEMBER",)
    if chain.get("automatic_successor_activation") is not False:
        return ("TASK_AUTOMATIC_SUCCESSOR_FORBIDDEN",)
    activated = chain.get("explicitly_activated_task_ids")
    if (
        type(activated) is not list
        or activated != sorted(activated)
        or len(activated) != len(set(activated))
        or any(task_id_value not in member_ids for task_id_value in activated)
    ):
        return ("TASK_ACTIVATION_CONFLICT",)
    is_active = task["status"] == "active"
    if is_active != (chain.get("active_task") == task_id):
        return ("TASK_ACTIVATION_CONFLICT",)
    activation_count = activated.count(task_id)
    if is_active and task["explicit_activation_required"] and activation_count != 1:
        return ("TASK_ACTIVATION_CONFLICT",)
    if not task["explicit_activation_required"] and activation_count:
        return ("TASK_ACTIVATION_CONFLICT",)
    return ()


def run(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "generic-validator",
        "task-schema",
        "profile-schema",
        "profile",
        "task",
        "chain",
        "expected",
        "generated",
        "oracle-index",
        "fixtures-root",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--task-record-path", required=True)
    args = parser.parse_args(argv)
    diagnostics: list[str] = []
    try:
        generic = _generic(args.generic_validator)
        task_schema = generic.load_json(args.task_schema)
        profile = generic.load_json(args.profile)
        diagnostics.extend(
            _schema_codes(
                generic.schema_diagnostics(
                    profile, generic.load_json(args.profile_schema)
                )
            )
        )
        task = generic.load_json(args.task)
        diagnostics.extend(_schema_codes(generic.schema_diagnostics(task, task_schema)))
        chain = generic.load_json(args.chain)
        record_path = args.task_record_path
        diagnostics.extend(relation_codes(task, chain, record_path))
        context_task = dict(task)
        context_task["intake_path"] = Path(task["intake_path"]).name
        rendered = generic.render({"task": context_task, "chain": chain}, profile)
        if rendered != args.expected.read_bytes():
            diagnostics.append("TASK_RENDER_EXPECTED_DRIFT")
        if rendered != args.generated.read_bytes():
            diagnostics.append("TASK_RENDER_LIVE_DRIFT")
        oracle = generic.load_json(args.oracle_index)["task_record"]
        for relative, expected_codes in oracle.items():
            fixture = generic.load_json(args.fixtures_root / relative)
            actual = list(
                _schema_codes(generic.schema_diagnostics(fixture, task_schema))
            )
            if not actual:
                fixture_chain = json.loads(json.dumps(chain))
                fixture_chain["active_task"] = (
                    fixture["task_id"] if fixture.get("status") == "active" else None
                )
                fixture_path = record_path
                if relative.endswith("record-chain-id-mismatch.json"):
                    fixture_path = record_path
                if relative.endswith("active-without-chain-activation.json"):
                    fixture_chain["explicitly_activated_task_ids"] = []
                if relative.endswith("automatic-successor-activation.json"):
                    fixture_chain["automatic_successor_activation"] = True
                if relative.endswith("chain-authority-duplication.json"):
                    selected_entry = next(
                        item
                        for item in fixture_chain["task_sequence"]
                        if item.get("record") == record_path
                    )
                    selected_entry["status"] = fixture["status"]
                actual.extend(relation_codes(fixture, fixture_chain, fixture_path))
            if sorted(actual) != sorted(expected_codes):
                diagnostics.append(
                    f"TASK_FIXTURE_ORACLE_MISMATCH:{relative}:{','.join(actual)}"
                )
        for relative, expected_codes in generic.load_json(args.oracle_index)[
            "task_projection"
        ].items():
            candidate = (
                args.fixtures_root.parent / "task-control-reference" / relative
            ).read_bytes()
            actual = []
            if relative.endswith("expected-drift.md") and rendered != candidate:
                actual.append("TASK_RENDER_EXPECTED_DRIFT")
            if relative.endswith("live-drift.md") and rendered != candidate:
                actual.append("TASK_RENDER_LIVE_DRIFT")
            if sorted(actual) != sorted(expected_codes):
                diagnostics.append(
                    f"TASK_FIXTURE_ORACLE_MISMATCH:{relative}:{','.join(actual)}"
                )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        diagnostics.append(f"TASK_INPUT_INVALID:{type(exc).__name__}:{exc}")
    result = {
        "diagnostics": sorted(set(diagnostics)),
        "schema_version": 1,
        "status": "PASS" if not diagnostics else "FAIL",
    }
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0 if not diagnostics else 1
