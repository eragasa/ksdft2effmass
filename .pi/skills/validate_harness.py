#!/usr/bin/env -S python/.venv/bin/python
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
CURRENT_LOCAL_REPLAY_PATH = Path(
    "harness/local/validation/replay_current_validators.py"
)
CURRENT_LOCAL_CHECK_IDS = {
    "current-architecture-decision-cases",
    "current-skill-capabilities",
    "current-h3-resources",
}
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
    except OSError:
        return {"command_id": command_id, "exit_status": 127}, None
    try:
        parsed = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    payload = parsed if isinstance(parsed, dict) else None
    return {
        "command_id": command_id,
        "exit_status": completed.returncode,
    }, payload


def indexed_observations(
    payload: dict[str, Any] | None, side: str
) -> dict[str, dict[str, Any]]:
    expected_ids = set(PAIR_CLASSIFICATIONS)
    if (
        payload is None
        or set(payload) != {"observations", "pair_ids", "schema_version", "side"}
        or payload.get("schema_version") != 1
        or payload.get("side") != side
    ):
        return {}
    pair_ids = payload.get("pair_ids")
    observations = payload.get("observations")
    if (
        not isinstance(pair_ids, list)
        or any(not isinstance(pair_id, str) for pair_id in pair_ids)
        or len(pair_ids) != len(set(pair_ids))
        or set(pair_ids) != expected_ids
        or not isinstance(observations, list)
    ):
        return {}
    result: dict[str, dict[str, Any]] = {}
    required_observation_keys = {"command", *COMPARISON_KEYS}
    for item in observations:
        if (
            not isinstance(item, dict)
            or set(item)
            != {"input_identities", "input_set_hash", "observation", "pair_id"}
            or not isinstance(item.get("pair_id"), str)
            or not isinstance(item.get("input_identities"), list)
            or not isinstance(item.get("input_set_hash"), str)
            or not isinstance(item.get("observation"), dict)
            or set(item["observation"]) != required_observation_keys
        ):
            return {}
        result[item["pair_id"]] = item
    if (
        len(result) != len(observations)
        or set(result) != expected_ids
        or set(result) != set(pair_ids)
    ):
        return {}
    return result


def observations_pass(observations: dict[str, dict[str, Any]]) -> bool:
    expected_ids = set(PAIR_CLASSIFICATIONS)
    return set(observations) == expected_ids and all(
        item["observation"].get("status") == "PASS"
        and type(item["observation"].get("exit_status")) is int
        and item["observation"]["exit_status"] == 0
        for item in observations.values()
    )


def run_current_local(root: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Run the maintained current validator replay, never the H4 checksum catalog."""
    command_id = "selected-validator-replay-local"
    target = root / CURRENT_LOCAL_REPLAY_PATH
    try:
        completed = subprocess.run(
            (sys.executable, str(target), "--repository-root", str(root)),
            cwd=root,
            env={"PYTHONHASHSEED": "0", "PYTHONIOENCODING": "utf-8"},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return {"command_id": command_id, "exit_status": 127}, None
    try:
        parsed = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    return {
        "command_id": command_id,
        "exit_status": completed.returncode,
    }, parsed if isinstance(parsed, dict) else None


def current_local_passes(payload: dict[str, Any] | None) -> bool:
    """Validate the closed current-replay result shape and exact required checks."""
    if payload is None or set(payload) != {
        "checks",
        "schema_version",
        "side",
        "status",
    }:
        return False
    if (
        payload.get("schema_version") != 1
        or payload.get("side") != "local"
        or payload.get("status") != "PASS"
    ):
        return False
    checks = payload.get("checks")
    if not isinstance(checks, list):
        return False
    indexed: dict[str, dict[str, Any]] = {}
    for item in checks:
        if not isinstance(item, dict) or set(item) != {
            "check_id",
            "exit_status",
            "status",
        }:
            return False
        check_id = item.get("check_id")
        if not isinstance(check_id, str) or check_id in indexed:
            return False
        indexed[check_id] = item
    return set(indexed) == CURRENT_LOCAL_CHECK_IDS and all(
        item.get("status") == "PASS"
        and type(item.get("exit_status")) is int
        and item["exit_status"] == 0
        for item in indexed.values()
    )


def run_route(root: Path, name: str) -> dict[str, Any]:
    if name == "local":
        command, payload = run_current_local(root)
        passed = command["exit_status"] == 0 and current_local_passes(payload)
    else:
        command, payload = run_replay(root, name)
        observations = indexed_observations(payload, name)
        passed = command["exit_status"] == 0 and observations_pass(observations)
    return {
        "route": name,
        "status": "PASS" if passed else "FAIL",
        "commands": [command],
    }


def run_shadow(root: Path) -> dict[str, Any]:
    legacy_command, legacy_payload = run_replay(root, "legacy")
    local_command, local_payload = run_replay(root, "local")
    legacy = indexed_observations(legacy_payload, "legacy")
    local = indexed_observations(local_payload, "local")
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
        and observations_pass(legacy)
        and observations_pass(local)
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
