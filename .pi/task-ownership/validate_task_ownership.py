#!/usr/bin/env -S python/.venv/bin/python
"""Fail closed when a chain task lacks explicit implementation/test ownership."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHAIN = ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json"
AGENT_NAME = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)
ACCEPTANCE_ROLE = re.compile(r"^acceptanceRole:\s*(\S+)\s*$", re.MULTILINE)
PYTHON_COMMAND = re.compile(r"^(?:python|python3|python3\.\d+)$")
AUTHORIZATION_MARKER = re.compile(
    r"^<!-- evidence-branch-authorization (?P<payload>\{.*\}) -->$",
    re.MULTILINE,
)


class OwnershipValidationError(ValueError):
    """Report a malformed or incomplete task-ownership launch contract."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise OwnershipValidationError(f"cannot load {path}: {error}") from error
    if not isinstance(value, dict):
        raise OwnershipValidationError(f"{path} must contain a JSON object")
    return value


def _schema_errors(
    instance: dict[str, Any], schema_path: Path, field: str
) -> list[str]:
    schema = _load_json(schema_path)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise OwnershipValidationError(
            f"{field} schema is invalid: {schema_path}: {error}"
        ) from error
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(instance),
        key=lambda item: (list(item.absolute_path), item.message),
    ):
        location = ".".join(str(part) for part in error.absolute_path)
        if error.validator == "additionalProperties" and isinstance(
            error.instance, dict
        ):
            declared = error.schema.get("properties", {})
            extras = sorted(set(error.instance) - set(declared))
            errors.extend(
                f"{field}.{'.'.join(filter(None, (location, extra)))}: "
                "additional property is not allowed"
                for extra in extras
            )
            continue
        location = location or "<root>"
        errors.append(f"{field}.{location}: {error.message}")
    return errors


def _validate_schema(instance: dict[str, Any], schema_path: Path, field: str) -> None:
    errors = _schema_errors(instance, schema_path, field)
    if errors:
        raise OwnershipValidationError("JSON Schema violations: " + "; ".join(errors))


def _normalized_repo_path(value: object, field: str, root: Path) -> str:
    if not isinstance(value, str) or not value:
        raise OwnershipValidationError(
            f"{field} must be a nonempty repository-relative path"
        )
    if "\\" in value or value.startswith("/") or Path(value).is_absolute():
        raise OwnershipValidationError(f"{field} must be repository-relative: {value}")
    parts = value.split("/")
    if ".." in parts:
        raise OwnershipValidationError(f"{field} must not contain traversal: {value}")
    normalized = posixpath.normpath(value)
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        raise OwnershipValidationError(f"{field} must be repository-relative: {value}")
    root_resolved = root.resolve()
    resolved = (root / normalized).resolve(strict=False)
    try:
        resolved.relative_to(root_resolved)
    except ValueError as error:
        raise OwnershipValidationError(
            f"{field} escapes the repository through a symlink: {value}"
        ) from error
    return normalized.rstrip("/")


def _repo_path(
    value: object, field: str, root: Path, *, must_exist: bool = True
) -> Path:
    normalized = _normalized_repo_path(value, field, root)
    path = root / normalized
    if must_exist and not path.exists():
        raise OwnershipValidationError(f"{field} does not exist: {value}")
    return path


def _validate_agent_v1(role: str, value: object, root: Path) -> tuple[str, set[str]]:
    if not isinstance(value, dict):
        raise OwnershipValidationError(f"owners.{role} must be an object")
    agent = value.get("agent")
    if not isinstance(agent, str) or not agent:
        raise OwnershipValidationError(f"owners.{role}.agent must be a nonempty string")
    record = _repo_path(value.get("agent_record"), f"owners.{role}.agent_record", root)
    record_text = record.read_text(encoding="utf-8")
    match = AGENT_NAME.search(record_text)
    if match is None or match.group(1) != agent:
        raise OwnershipValidationError(
            f"owners.{role}.agent {agent!r} does not match the agent record"
        )
    paths_value = value.get("owned_paths", [])
    if not isinstance(paths_value, list) or any(
        not isinstance(path, str) or not path for path in paths_value
    ):
        raise OwnershipValidationError(f"owners.{role}.owned_paths must be strings")
    normalized_paths = {
        _normalized_repo_path(path, f"owners.{role}.owned_paths[{index}]", root)
        for index, path in enumerate(paths_value)
    }
    undeclared_paths = [path for path in paths_value if path not in record_text]
    if undeclared_paths:
        raise OwnershipValidationError(
            f"owners.{role} paths are absent from the agent record: {undeclared_paths}"
        )
    return agent, normalized_paths


def _paths_overlap(left: set[str], right: set[str]) -> bool:
    """Return whether either declared path contains a path from the other set."""
    return any(
        first == second
        or first.startswith(f"{second}/")
        or second.startswith(f"{first}/")
        for first in left
        for second in right
    )


def _validate_v1(
    manifest: dict[str, Any], task: dict[str, Any], task_id: str, root: Path
) -> None:
    if manifest.get("schema_version") != 1 or manifest.get("task_id") != task_id:
        raise OwnershipValidationError(
            "ownership manifest version/task identity mismatch"
        )
    task_record = _repo_path(manifest.get("task_record"), "manifest.task_record", root)
    if task_record != _repo_path(task.get("record"), "task.record", root):
        raise OwnershipValidationError("manifest task_record does not match the chain")

    owners = manifest.get("owners")
    if not isinstance(owners, dict):
        raise OwnershipValidationError("manifest.owners must be an object")
    implementation, implementation_paths = _validate_agent_v1(
        "implementation", owners.get("implementation"), root
    )
    tests, test_paths = _validate_agent_v1("tests", owners.get("tests"), root)
    documentation, documentation_paths = _validate_agent_v1(
        "documentation", owners.get("documentation"), root
    )
    if len({implementation, tests, documentation}) != 3:
        raise OwnershipValidationError(
            "implementation, test, and documentation writers must differ"
        )
    if (
        _paths_overlap(implementation_paths, test_paths)
        or _paths_overlap(implementation_paths, documentation_paths)
        or _paths_overlap(test_paths, documentation_paths)
    ):
        raise OwnershipValidationError("writer owned_paths must not overlap")
    if not any(path.startswith("python/src/") for path in implementation_paths):
        raise OwnershipValidationError(
            "implementation owner must own a python/src path"
        )
    if any(
        path.startswith(("python/tests/", "docs/")) for path in implementation_paths
    ):
        raise OwnershipValidationError(
            "implementation owner must not own tests or docs"
        )
    if not test_paths or any(
        not path.startswith("python/tests/") for path in test_paths
    ):
        raise OwnershipValidationError(
            "test owner paths must remain under python/tests"
        )
    if not documentation_paths or any(
        path != "docs" and not path.startswith("docs/") for path in documentation_paths
    ):
        raise OwnershipValidationError(
            "documentation owner paths must remain under docs"
        )

    reviewers = owners.get("reviewers")
    if not isinstance(reviewers, list) or not reviewers:
        raise OwnershipValidationError("at least one reviewer is required")
    reviewer_names = {
        _validate_agent_v1(f"reviewers[{index}]", item, root)[0]
        for index, item in enumerate(reviewers)
    }
    if len(reviewer_names) != len(reviewers):
        raise OwnershipValidationError("reviewer agents must be unique")
    if reviewer_names & {implementation, tests, documentation}:
        raise OwnershipValidationError("reviewers must be independent of writer owners")

    policy = manifest.get("test_ownership")
    if not isinstance(policy, dict):
        raise OwnershipValidationError("manifest.test_ownership must be an object")
    if policy.get("module_rule") != "test__ClassName.py":
        raise OwnershipValidationError("test module rule must be test__ClassName.py")
    if policy.get("artifact_module_rule") != "declared_exact_filename":
        raise OwnershipValidationError(
            "artifact module rule must be declared_exact_filename"
        )
    artifact_modules = policy.get("artifact_modules")
    if (
        not isinstance(artifact_modules, list)
        or not artifact_modules
        or len(set(artifact_modules)) != len(artifact_modules)
        or any(
            not isinstance(name, str)
            or re.fullmatch(r"test__[A-Za-z][A-Za-z0-9]*\.py", name) is None
            for name in artifact_modules
        )
    ):
        raise OwnershipValidationError(
            "artifact_modules must contain unique exact pytest filenames"
        )
    if (
        not isinstance(policy.get("inventory_source"), str)
        or not policy["inventory_source"]
    ):
        raise OwnershipValidationError("test inventory_source is required")
    _repo_path(
        policy.get("inventory_artifact"),
        "test_ownership.inventory_artifact",
        root,
    )
    kinds = policy.get("dedicated_module_kinds")
    required_kinds = {
        "DataObject",
        "ResultObject",
        "ActionObject",
        "independent_constructor_invariant_owner",
    }
    if not isinstance(kinds, list) or not required_kinds.issubset(set(kinds)):
        raise OwnershipValidationError("dedicated module kinds are incomplete")
    exceptions = policy.get("exceptions")
    if not isinstance(exceptions, dict) or set(exceptions) != {
        "enums",
        "marker_exceptions",
        "package_schema_gates",
    }:
        raise OwnershipValidationError(
            "test exceptions must classify enums, marker exceptions, "
            "and package/schema gates"
        )
    if any(
        not isinstance(values, list)
        or any(not isinstance(value, str) or not value for value in values)
        for values in exceptions.values()
    ):
        raise OwnershipValidationError(
            "test exception classifications must be string arrays"
        )
    gate_owner = policy.get("non_class_gate_owner")
    if not isinstance(gate_owner, str) or not gate_owner:
        raise OwnershipValidationError("non_class_gate_owner is required")
    completion = policy.get("completion_validator")
    if (
        not isinstance(completion, dict)
        or completion.get("required_before_review") is not True
    ):
        raise OwnershipValidationError(
            "completion validator must be required before review"
        )
    _repo_path(completion.get("path"), "test_ownership.completion_validator.path", root)
    if not isinstance(completion.get("command"), str) or not completion["command"]:
        raise OwnershipValidationError("completion validator command is required")


def _validate_path_collection(values: list[str], field: str, root: Path) -> list[str]:
    normalized = [
        _normalized_repo_path(value, f"{field}[{index}]", root)
        for index, value in enumerate(values)
    ]
    for index, path in enumerate(normalized):
        for previous in normalized[:index]:
            if _paths_overlap({path}, {previous}):
                raise OwnershipValidationError(
                    f"{field} contains duplicate or overlapping normalized paths: "
                    f"{previous!r} and {path!r}"
                )
    return normalized


def _path_is_within(path: str, scopes: list[str]) -> bool:
    return any(path == scope or path.startswith(f"{scope}/") for scope in scopes)


def _validate_v2_agent(
    value: dict[str, Any], field: str, root: Path, *, writer: bool
) -> tuple[str, str, list[str]]:
    role = value["role"]
    agent = value["agent"]
    record = _repo_path(value["agent_record"], f"{field}.agent_record", root)
    record_text = record.read_text(encoding="utf-8")
    name_match = AGENT_NAME.search(record_text)
    if name_match is None or name_match.group(1) != agent:
        raise OwnershipValidationError(
            f"{field}.agent {agent!r} does not match the agent record"
        )
    expected_acceptance_role = "writer" if writer else "read-only"
    role_match = ACCEPTANCE_ROLE.search(record_text)
    if role_match is None or role_match.group(1) != expected_acceptance_role:
        raise OwnershipValidationError(
            f"{field}.agent_record acceptanceRole must be {expected_acceptance_role!r}"
        )
    paths: list[str] = []
    if writer:
        paths = _validate_path_collection(
            value["owned_paths"], f"{field}.owned_paths", root
        )
    return role, agent, paths


def _validate_completion_validator(
    completion: dict[str, Any], root: Path
) -> tuple[str, list[str]]:
    declared = _normalized_repo_path(
        completion["path"], "manifest.completion_validator.path", root
    )
    _repo_path(completion["path"], "manifest.completion_validator.path", root)
    command = completion["command"]
    valid_direct = (
        len(command) == 1
        and _normalized_repo_path(
            command[0], "manifest.completion_validator.command[0]", root
        )
        == declared
    )
    valid_python = False
    if len(command) == 2 and PYTHON_COMMAND.fullmatch(Path(command[0]).name):
        valid_python = (
            _normalized_repo_path(
                command[1], "manifest.completion_validator.command[1]", root
            )
            == declared
        )
    if not valid_direct and not valid_python:
        raise OwnershipValidationError(
            "manifest.completion_validator.command must be exactly [path] or "
            "[python-like, path] for the declared validator"
        )
    return declared, command


def _validate_authorization_marker(
    record_text: str, decision_id: str, profile: str
) -> None:
    """Require one exact affirmative machine-readable authorization marker."""
    matches = list(AUTHORIZATION_MARKER.finditer(record_text))
    if len(matches) != 1:
        raise OwnershipValidationError(
            "matrix.authorization.record must contain exactly one affirmative "
            "evidence-branch authorization marker"
        )
    try:
        payload = json.loads(matches[0].group("payload"))
    except json.JSONDecodeError as error:
        raise OwnershipValidationError(
            "matrix.authorization.record contains an invalid authorization marker"
        ) from error
    expected = {
        "profile": profile,
        "decision_id": decision_id,
        "authorized": True,
    }
    if payload != expected:
        raise OwnershipValidationError(
            "matrix.authorization.record authorization marker does not affirm "
            "the declared profile and decision"
        )


def _checkpoint_records(root: Path) -> dict[str, list[dict[str, Any]]]:
    records: dict[str, list[dict[str, Any]]] = {}
    checkpoint_dir = root / ".pi/checkpoints"
    if not checkpoint_dir.exists():
        return records
    for path in sorted(checkpoint_dir.glob("*.json")):
        if path.name == "checkpoint.schema.json":
            continue
        record = _load_json(path)
        checkpoint_id = record.get("checkpoint_id")
        if isinstance(checkpoint_id, str):
            records.setdefault(checkpoint_id, []).append(record)
    return records


def _validate_acyclic(branches: list[dict[str, Any]]) -> None:
    by_id = {branch["id"]: branch for branch in branches}
    state: dict[str, int] = {}

    def visit(branch_id: str, stack: list[str]) -> None:
        if state.get(branch_id) == 1:
            cycle = " -> ".join([*stack, branch_id])
            raise OwnershipValidationError(
                f"matrix.branches prerequisites contain a cycle: {cycle}"
            )
        if state.get(branch_id) == 2:
            return
        state[branch_id] = 1
        for prerequisite in by_id[branch_id]["prerequisites"]:
            visit(prerequisite, [*stack, branch_id])
        state[branch_id] = 2

    for branch_id in by_id:
        visit(branch_id, [])


def _validate_matrix(
    matrix: dict[str, Any],
    manifest: dict[str, Any],
    task: dict[str, Any],
    writers: dict[str, tuple[str, list[str]]],
    reviewer_roles: set[str],
    completion_path: str,
    completion_command: list[str],
    root: Path,
) -> None:
    schema_path = root / ".pi/task-ownership/evidence-branch-matrix.schema.json"
    _validate_schema(matrix, schema_path, "matrix")
    if matrix["task_id"] != manifest["task_id"]:
        raise OwnershipValidationError("matrix.task_id does not match the manifest")
    matrix_task_record = _repo_path(matrix["task_record"], "matrix.task_record", root)
    if matrix_task_record != _repo_path(task["record"], "task.record", root):
        raise OwnershipValidationError("matrix.task_record does not match the chain")
    if matrix["profile"] != manifest["orchestration_profile"]["profile"]:
        raise OwnershipValidationError("matrix.profile does not match the manifest")

    authorization = matrix["authorization"]
    authorization_record = _repo_path(
        authorization["record"], "matrix.authorization.record", root
    )
    if authorization_record != matrix_task_record or (
        authorization_record
        != _repo_path(manifest["task_record"], "manifest.task_record", root)
    ):
        raise OwnershipValidationError(
            "matrix.authorization.record must equal the manifest/task record"
        )
    authorization_text = authorization_record.read_text(encoding="utf-8")
    _validate_authorization_marker(
        authorization_text,
        authorization["decision_id"],
        matrix["profile"],
    )

    stages = matrix["validation_stages"]
    stage_ids = [stage["id"] for stage in stages]
    if len(stage_ids) != len(set(stage_ids)):
        raise OwnershipValidationError("matrix.validation_stages IDs must be unique")
    completion_stages = [stage for stage in stages if stage["kind"] == "completion"]
    if len(completion_stages) != 1:
        raise OwnershipValidationError(
            "matrix.validation_stages must contain exactly one completion stage"
        )
    for index, stage in enumerate(stages):
        field = f"matrix.validation_stages[{index}]"
        role = stage["owner_role"]
        if role not in writers:
            raise OwnershipValidationError(
                f"{field}.owner_role is not a writer: {role}"
            )
        evidence_paths = _validate_path_collection(
            stage["evidence_paths"], f"{field}.evidence_paths", root
        )
        for path in evidence_paths:
            if not _path_is_within(path, writers[role][1]):
                raise OwnershipValidationError(
                    f"{field}.evidence_paths is outside owner role {role!r} "
                    f"scope: {path}"
                )
        if stage["kind"] == "completion":
            if stage["command"] != completion_command:
                raise OwnershipValidationError(
                    f"{field}.command does not equal the manifest completion command"
                )
            if completion_path not in evidence_paths:
                raise OwnershipValidationError(
                    f"{field}.evidence_paths must include the declared validator path"
                )

    branches = matrix["branches"]
    branch_ids = [branch["id"] for branch in branches]
    if len(branch_ids) != len(set(branch_ids)):
        raise OwnershipValidationError("matrix.branches IDs must be unique")
    branch_roles = {branch["owner_role"] for branch in branches}
    branch_classifications = {branch["classification"] for branch in branches}
    if len(branch_roles) < 2 and branch_classifications != {
        "deterministic_now",
        "protected_checkpoint",
    }:
        raise OwnershipValidationError(
            "matrix activation requires at least two writer roles or both "
            "deterministic_now and protected_checkpoint branches"
        )
    known_branches = set(branch_ids)
    known_stages = set(stage_ids)
    referenced_stages: set[str] = set()
    checkpoint_records = _checkpoint_records(root)
    all_branch_paths: list[tuple[str, str]] = []

    for index, branch in enumerate(branches):
        field = f"matrix.branches[{index}]"
        role = branch["owner_role"]
        if role in reviewer_roles:
            raise OwnershipValidationError(
                f"{field}.owner_role is reviewer-only and cannot own a branch: {role}"
            )
        if role not in writers:
            raise OwnershipValidationError(f"{field}.owner_role is unknown: {role}")
        writer_paths = writers[role][1]
        branch_paths = _validate_path_collection(
            branch["owned_paths"], f"{field}.owned_paths", root
        )
        evidence_paths = _validate_path_collection(
            branch["evidence_paths"], f"{field}.evidence_paths", root
        )
        for path in branch_paths:
            if not _path_is_within(path, writer_paths):
                raise OwnershipValidationError(
                    f"{field}.owned_paths is outside owner role {role!r} scope: {path}"
                )
            for other_id, other_path in all_branch_paths:
                if _paths_overlap({path}, {other_path}):
                    raise OwnershipValidationError(
                        f"{field}.owned_paths overlaps branch {other_id!r}: "
                        f"{other_path!r} and {path!r}"
                    )
            all_branch_paths.append((branch["id"], path))
        for path in evidence_paths:
            if not _path_is_within(path, writer_paths) or not _path_is_within(
                path, branch_paths
            ):
                raise OwnershipValidationError(
                    f"{field}.evidence_paths lacks branch/owner ownership: {path}"
                )
        if len(branch["prerequisites"]) != len(set(branch["prerequisites"])):
            raise OwnershipValidationError(f"{field}.prerequisites must be unique")
        unknown_prerequisites = set(branch["prerequisites"]) - known_branches
        if unknown_prerequisites:
            raise OwnershipValidationError(
                f"{field}.prerequisites reference unknown branches: "
                f"{sorted(unknown_prerequisites)}"
            )
        if branch["id"] in branch["prerequisites"]:
            raise OwnershipValidationError(
                f"{field}.prerequisites must not reference its own branch"
            )
        if len(branch["validation_stage_ids"]) != len(
            set(branch["validation_stage_ids"])
        ):
            raise OwnershipValidationError(
                f"{field}.validation_stage_ids must be unique"
            )
        referenced_stages.update(branch["validation_stage_ids"])
        missing_stages = set(branch["validation_stage_ids"]) - known_stages
        if missing_stages:
            raise OwnershipValidationError(
                f"{field}.validation_stage_ids reference missing stages: "
                f"{sorted(missing_stages)}"
            )
        if branch["classification"] == "protected_checkpoint":
            for checkpoint_id in branch["checkpoint_ids"]:
                records = checkpoint_records.get(checkpoint_id, [])
                if len(records) != 1:
                    raise OwnershipValidationError(
                        f"{field}.checkpoint_ids requires one existing checkpoint: "
                        f"{checkpoint_id}"
                    )
                checkpoint = records[0]
                if checkpoint.get("task_id") != manifest["task_id"]:
                    raise OwnershipValidationError(
                        f"{field}.checkpoint_ids checkpoint belongs to another task: "
                        f"{checkpoint_id}"
                    )
                if checkpoint.get("status") not in {"pending", "blocked"}:
                    raise OwnershipValidationError(
                        f"{field}.checkpoint_ids checkpoint is not unresolved: "
                        f"{checkpoint_id}"
                    )
    orphan_stages = known_stages - referenced_stages
    if orphan_stages:
        raise OwnershipValidationError(
            "matrix.validation_stages are not referenced by any branch: "
            f"{sorted(orphan_stages)}"
        )
    _validate_acyclic(branches)


def _validate_v2(
    manifest: dict[str, Any], task: dict[str, Any], task_id: str, root: Path
) -> None:
    if manifest["task_id"] != task_id:
        raise OwnershipValidationError("manifest.task_id does not match the chain task")
    manifest_task_record = _repo_path(
        manifest["task_record"], "manifest.task_record", root
    )
    if manifest_task_record != _repo_path(task.get("record"), "task.record", root):
        raise OwnershipValidationError("manifest.task_record does not match the chain")

    writers: dict[str, tuple[str, list[str]]] = {}
    writer_agents: set[str] = set()
    all_writer_paths: list[tuple[str, str]] = []
    for index, owner in enumerate(manifest["owners"]["writers"]):
        role, agent, paths = _validate_v2_agent(
            owner, f"manifest.owners.writers[{index}]", root, writer=True
        )
        if role in writers:
            raise OwnershipValidationError("manifest writer roles must be unique")
        if agent in writer_agents:
            raise OwnershipValidationError("manifest writer agents must be unique")
        for path in paths:
            for other_role, other_path in all_writer_paths:
                if _paths_overlap({path}, {other_path}):
                    raise OwnershipValidationError(
                        "manifest writer owned_paths overlap: "
                        f"{other_role}:{other_path} and {role}:{path}"
                    )
            all_writer_paths.append((role, path))
        writers[role] = (agent, paths)
        writer_agents.add(agent)

    reviewer_roles: set[str] = set()
    reviewer_agents: set[str] = set()
    for index, reviewer in enumerate(manifest["owners"]["reviewers"]):
        role, agent, _ = _validate_v2_agent(
            reviewer,
            f"manifest.owners.reviewers[{index}]",
            root,
            writer=False,
        )
        if role in reviewer_roles or role in writers:
            raise OwnershipValidationError("manifest owner roles must be unique")
        if agent in reviewer_agents:
            raise OwnershipValidationError("manifest reviewer agents must be unique")
        reviewer_roles.add(role)
        reviewer_agents.add(agent)
    if writer_agents & reviewer_agents:
        raise OwnershipValidationError("reviewers must be independent of writer owners")

    completion_path, completion_command = _validate_completion_validator(
        manifest["completion_validator"], root
    )
    profile = manifest.get("orchestration_profile")
    if profile is None:
        return
    if profile["correction_cycle_limit"] != 1:
        raise OwnershipValidationError(
            "manifest.orchestration_profile.correction_cycle_limit must equal 1"
        )
    matrix_path = _repo_path(
        profile["branch_matrix"],
        "manifest.orchestration_profile.branch_matrix",
        root,
    )
    matrix = _load_json(matrix_path)
    _validate_matrix(
        matrix,
        manifest,
        task,
        writers,
        reviewer_roles,
        completion_path,
        completion_command,
        root,
    )


def validate(chain_path: Path, task_id: str, *, root: Path = ROOT) -> Path:
    """Validate one task and return its ownership-manifest path."""
    root = root.resolve()
    chain = _load_json(chain_path)
    tasks = chain.get("task_sequence")
    if not isinstance(tasks, list):
        raise OwnershipValidationError("chain.task_sequence must be an array")
    matches = [
        task for task in tasks if isinstance(task, dict) and task.get("id") == task_id
    ]
    if len(matches) != 1:
        raise OwnershipValidationError(f"expected exactly one chain task {task_id!r}")
    task = matches[0]
    manifest_path = _repo_path(
        task.get("ownership_manifest"), "task.ownership_manifest", root
    )
    manifest = _load_json(manifest_path)
    schema_version = manifest.get("schema_version")
    if schema_version == 1:
        schema_path = root / ".pi/task-ownership/ownership.schema.json"
        _validate_schema(manifest, schema_path, "manifest")
        _validate_v1(manifest, task, task_id, root)
    elif schema_version == 2:
        schema_path = root / ".pi/task-ownership/ownership-v2.schema.json"
        _validate_schema(manifest, schema_path, "manifest")
        _validate_v2(manifest, task, task_id, root)
    else:
        raise OwnershipValidationError(
            "manifest.schema_version must select supported version 1 or 2"
        )
    return manifest_path


def main() -> int:
    """Run the command-line ownership preflight."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--chain", type=Path, default=DEFAULT_CHAIN)
    arguments = parser.parse_args()
    chain_path = (
        arguments.chain if arguments.chain.is_absolute() else ROOT / arguments.chain
    )
    try:
        manifest_path = validate(chain_path, arguments.task)
    except OwnershipValidationError as error:
        print(f"task ownership preflight failed: {error}", file=sys.stderr)
        return 1
    print(f"task ownership preflight passed: {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
