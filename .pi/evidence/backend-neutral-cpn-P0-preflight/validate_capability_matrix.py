"""Validate the structured P0 capability matrix and malformed probes."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

EXPECTED_CAPABILITIES = {
    "SNAKES package resolution",
    "SNAKES installation",
    "SNAKES import",
    "Python compatibility",
    "basic net construction",
    "colored structured tokens",
    "multiset markings",
    "guards",
    "bindings",
    "arc expressions",
    "transition firing",
    "failure/retry feasibility",
    "provenance join feasibility",
    "neutral marking extraction",
    "state-space/reachability",
    "SNAKES Graphviz plugin",
    "system Graphviz",
    "MyST installation",
    "MyST import",
    "Sphinx/MyST build",
    "Obsidian-style mathematics",
    "mixed RST/Markdown navigation",
    "license metadata",
    "dependency placement",
}
STATUSES = {
    "PASS",
    "CONDITIONAL_PASS",
    "FAIL",
    "NOT_AVAILABLE",
    "NOT_APPLICABLE",
}
CLASSIFICATIONS = {"blocking", "optional", "human_decision"}
REQUIRED_FIELDS = {
    "capability",
    "status",
    "evidence_artifact",
    "exact_environment",
    "limitations",
    "required_correction",
    "blocking_or_optional_classification",
}


def validate(document: Any, evidence_directory: Path) -> list[str]:
    """Return every structural or referential matrix error."""

    errors: list[str] = []
    if not isinstance(document, dict):
        return ["root must be an object"]
    if document.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if document.get("task_id") != "backend-neutral-cpn-P0-preflight":
        errors.append("task_id mismatch")
    if document.get("overall_recommendation") not in STATUSES:
        errors.append("overall_recommendation is invalid")
    exact_environment = document.get("exact_environment")
    if not isinstance(exact_environment, dict):
        errors.append("exact_environment must be an object")
        environment_id = None
    else:
        environment_id = exact_environment.get("environment_id")
        if not isinstance(environment_id, str) or not environment_id:
            errors.append("exact_environment.environment_id must be nonempty")
    capabilities = document.get("capabilities")
    if not isinstance(capabilities, list):
        return errors + ["capabilities must be an array"]

    names: list[Any] = []
    for index, record in enumerate(capabilities):
        prefix = f"capabilities[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(record)
        extra = set(record) - REQUIRED_FIELDS
        if missing:
            errors.append(f"{prefix} missing fields: {sorted(missing)}")
        if extra:
            errors.append(f"{prefix} extra fields: {sorted(extra)}")
        name = record.get("capability")
        names.append(name)
        if record.get("status") not in STATUSES:
            errors.append(f"{prefix}.status is invalid")
        artifact = record.get("evidence_artifact")
        if not isinstance(artifact, str) or not artifact:
            errors.append(f"{prefix}.evidence_artifact must be nonempty")
        elif not (evidence_directory / artifact).is_file():
            errors.append(f"{prefix}.evidence_artifact does not exist: {artifact}")
        if record.get("exact_environment") != environment_id:
            errors.append(f"{prefix}.exact_environment does not match environment_id")
        limitations = record.get("limitations")
        if not isinstance(limitations, list) or not all(
            isinstance(item, str) and item for item in limitations
        ):
            errors.append(f"{prefix}.limitations must be nonempty strings")
        correction = record.get("required_correction")
        if not isinstance(correction, str) or not correction:
            errors.append(f"{prefix}.required_correction must be nonempty")
        if record.get("blocking_or_optional_classification") not in CLASSIFICATIONS:
            errors.append(f"{prefix}.blocking_or_optional_classification is invalid")
    if len(names) != len(set(names)):
        errors.append("capability names must be unique")
    actual = set(names)
    if actual != EXPECTED_CAPABILITIES:
        errors.append(
            "capability inventory mismatch: "
            f"missing={sorted(EXPECTED_CAPABILITIES - actual)}, "
            f"extra={sorted(actual - EXPECTED_CAPABILITIES)}"
        )
    return errors


def _self_test(document: dict[str, Any], evidence_directory: Path) -> list[str]:
    """Require malformed omissions, enums, references, and duplicates to fail."""

    probes: list[tuple[str, dict[str, Any]]] = []

    missing = copy.deepcopy(document)
    del missing["capabilities"][0]["status"]
    probes.append(("missing_status", missing))

    invalid_status = copy.deepcopy(document)
    invalid_status["capabilities"][0]["status"] = "MAYBE"
    probes.append(("invalid_status", invalid_status))

    missing_artifact = copy.deepcopy(document)
    missing_artifact["capabilities"][0]["evidence_artifact"] = "absent.json"
    probes.append(("missing_artifact", missing_artifact))

    duplicate = copy.deepcopy(document)
    duplicate["capabilities"][1]["capability"] = duplicate["capabilities"][0][
        "capability"
    ]
    probes.append(("duplicate_capability", duplicate))

    wrong_environment = copy.deepcopy(document)
    wrong_environment["capabilities"][0]["exact_environment"] = "other"
    probes.append(("wrong_environment", wrong_environment))

    failures = [
        name
        for name, malformed in probes
        if not validate(malformed, evidence_directory)
    ]
    if failures:
        raise AssertionError(f"malformed probes unexpectedly passed: {failures}")
    return [name for name, _ in probes]


def main() -> int:
    """Validate one matrix and optionally execute malformed-result probes."""

    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    matrix = arguments.matrix.resolve()
    document = json.loads(matrix.read_text(encoding="utf-8"))
    errors = validate(document, matrix.parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {len(document['capabilities'])} capability records validated")
    if arguments.self_test:
        probes = _self_test(document, matrix.parent)
        print(f"PASS: malformed probes rejected: {', '.join(probes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
