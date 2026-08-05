#!/usr/bin/env python3
"""Run the explicitly configured repository-local harness validation route."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROUTES = {"legacy", "local", "shadow"}


def emit(payload: dict[str, Any]) -> None:
    """Emit the stable machine-readable result."""
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def fail(code: str) -> int:
    emit({"schema_version": 1, "status": "FAIL", "error": code})
    return 2


def load_configuration(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or set(value) != {
        "rollback_route",
        "route",
        "schema_version",
    }:
        return None
    if value.get("schema_version") != 1:
        return None
    if value.get("route") not in ROUTES or value.get("rollback_route") != "legacy":
        return None
    return value


REPLAY_RELATIVE_PATH = Path(
    ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
)
PAIR_CLASSIFICATIONS = {
    "accepted-checksum-catalogs": "intentional",
    "checkpoint-validator": "intentional",
    "evidence-id-audit-h4-selection": "equivalent",
    "h3-resource-validator": "equivalent",
    "ownership-validator-h4": "equivalent",
    "ownership-validator-legacy-p1-boundary-owned": "intentional",
    "skill-capability-and-explicit-descriptor-selection": "intentional",
    "task-chain-explicit-selection": "equivalent",
}
COMPARISON_KEYS = (
    "status",
    "exit_status",
    "issue_facts",
    "paths",
    "related_identities",
    "state",
    "inventory",
    "report_identity",
)


def replay_command(root: Path, side: str) -> tuple[str, ...]:
    return (
        sys.executable,
        str(root / REPLAY_RELATIVE_PATH),
        "--side",
        side,
        "--no-write",
    )


def run_replay(root: Path, side: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    command_id = f"selected-validator-replay-{side}"
    try:
        completed = subprocess.run(
            replay_command(root, side),
            cwd=root,
            env={"PYTHONHASHSEED": "0", "PYTHONIOENCODING": "utf-8"},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
        )
        exit_status = completed.returncode
        payload = json.loads(completed.stdout) if exit_status == 0 else None
        if not isinstance(payload, dict) or payload.get("side") != side:
            payload = None
            if exit_status == 0:
                exit_status = 1
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        exit_status = 127
        payload = None
    return {"command_id": command_id, "exit_status": exit_status}, payload


def run_route(root: Path, name: str) -> dict[str, Any]:
    command, _payload = run_replay(root, name)
    return {
        "route": name,
        "status": "PASS" if command["exit_status"] == 0 else "FAIL",
        "commands": [command],
    }


def indexed_observations(payload: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if payload is None or payload.get("schema_version") != 1:
        return {}
    observations = payload.get("observations")
    if not isinstance(observations, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for item in observations:
        if not isinstance(item, dict) or not isinstance(item.get("pair_id"), str):
            return {}
        result[item["pair_id"]] = item
    return result if len(result) == len(observations) else {}


def run_shadow(root: Path) -> dict[str, Any]:
    legacy_command, legacy_payload = run_replay(root, "legacy")
    local_command, local_payload = run_replay(root, "local")
    legacy = indexed_observations(legacy_payload)
    local = indexed_observations(local_payload)
    classifications: dict[str, str] = {}
    expected_ids = set(PAIR_CLASSIFICATIONS)
    if set(legacy) == expected_ids and set(local) == expected_ids:
        for pair_id in sorted(expected_ids):
            left = legacy[pair_id]
            right = local[pair_id]
            same_inputs = left.get("input_identities") == right.get(
                "input_identities"
            ) and left.get("input_set_hash") == right.get("input_set_hash")
            left_observation = left.get("observation")
            right_observation = right.get("observation")
            differences = []
            if isinstance(left_observation, dict) and isinstance(
                right_observation, dict
            ):
                differences = [
                    key
                    for key in COMPARISON_KEYS
                    if left_observation.get(key) != right_observation.get(key)
                ]
            expected = PAIR_CLASSIFICATIONS[pair_id]
            if (
                not same_inputs
                or not isinstance(left_observation, dict)
                or not isinstance(right_observation, dict)
            ):
                classifications[pair_id] = "defect"
            elif expected == "equivalent" and not differences:
                classifications[pair_id] = "equivalent"
            elif expected == "intentional" and differences:
                classifications[pair_id] = "intentional"
            else:
                classifications[pair_id] = "defect"
    for pair_id in sorted(expected_ids - (set(legacy) & set(local))):
        classifications[pair_id] = "deferred"
    commands = [legacy_command, local_command]
    passed = (
        all(command["exit_status"] == 0 for command in commands)
        and set(classifications) == expected_ids
        and all(
            value in {"equivalent", "intentional"} for value in classifications.values()
        )
    )
    return {
        "route": "shadow",
        "status": "PASS" if passed else "FAIL",
        "commands": commands,
        "classifications": classifications,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--route-config", required=True)
    args = parser.parse_args()
    root = Path(args.repository_root)
    config_path = Path(args.route_config)
    if not root.is_absolute():
        return fail("repository-root-not-absolute")
    if not config_path.is_absolute():
        return fail("route-config-not-absolute")
    if not root.is_dir():
        return fail("repository-root-not-directory")
    config = load_configuration(config_path)
    if config is None:
        return fail("route-config-invalid")

    selected = config["route"]
    outcome = run_shadow(root) if selected == "shadow" else run_route(root, selected)
    passed = outcome["status"] == "PASS"
    emit(
        {
            "schema_version": 1,
            "selected_route": selected,
            "rollback_route": config["rollback_route"],
            "status": "PASS" if passed else "FAIL",
            "routes": [outcome],
        }
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
