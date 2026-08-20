"""Focused regression tests for versioned task-ownership preflight contracts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi.local.task_ownership_validation import (
    OwnershipValidationError,
    _TaskOwnershipManifestValidator,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CONTROL_ROOT = REPOSITORY_ROOT / ".pi/task-ownership"
FIXTURES = Path(__file__).parent / "fixtures"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _agent_record(
    name: str,
    acceptance_role: str,
    prose: str = "",
) -> str:
    return f"---\nname: {name}\nacceptanceRole: {acceptance_role}\n---\n\n{prose}\n"


def _make_repository(
    tmp_path: Path,
    *,
    profile: bool = True,
    manifest_mutator: Callable[[dict[str, Any]], None] | None = None,
    matrix_mutator: Callable[[dict[str, Any]], None] | None = None,
) -> tuple[Path, Path]:
    root = tmp_path / "repository"
    control = root / ".pi/task-ownership"
    control.mkdir(parents=True)
    for schema_name in (
        "ownership.schema.json",
        "ownership-v2.schema.json",
        "evidence-branch-matrix.schema.json",
    ):
        shutil.copy2(CONTROL_ROOT / schema_name, control / schema_name)

    task_path = root / "harness/tasks/TASK.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "schema_version": 3,
                "task_id": "TASK",
                "title": "Synthetic Task",
                "status": "active",
                "status_detail": None,
                "parent_task_id": None,
                "task_prerequisite_ids": [],
                "external_prerequisite_ids": [],
                "superseded_by_task_ids": [],
                "explicit_activation_required": True,
                "objective": "Exercise operation-scoped ownership.",
                "authority_reference_paths": ["records/authority.md"],
                "authorized_scope": ["Validate the synthetic manifest."],
                "completion_criteria": ["Validation is deterministic."],
                "exclusions": ["No operation is executed."],
                "intake_path": None,
                "archived_source": None,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    authorization_path = root / ".pi/evidence/TASK-AUTH-001.md"
    authorization_path.parent.mkdir(parents=True)
    authorization_path.write_text(
        "<!-- evidence-branch-authorization "
        '{"profile":"evidence-branches-v1",'
        '"decision_id":"TASK-AUTH-001","authorized":true} -->\n',
        encoding="utf-8",
    )
    (root / ".pi/agents").mkdir(parents=True)
    records = {
        "implementation.md": ("implementation-agent", "writer"),
        "tests.md": ("test-agent", "writer"),
        "documentation.md": ("documentation-agent", "writer"),
        "reviewer.md": ("review-agent", "read-only"),
    }
    for filename, (name, acceptance_role) in records.items():
        (root / ".pi/agents" / filename).write_text(
            _agent_record(name, acceptance_role), encoding="utf-8"
        )
    (control / "complete.py").write_text("raise SystemExit(0)\n", encoding="utf-8")

    fixture_name = (
        "ownership-v2-profile.json" if profile else "ownership-v2-no-profile.json"
    )
    manifest = _read_json(FIXTURES / "valid" / fixture_name)
    manifest["task_record"] = "harness/tasks/TASK.json"
    if manifest_mutator is not None:
        manifest_mutator(manifest)
    manifest_path = control / "manifest.json"
    _write_json(manifest_path, manifest)

    if profile:
        matrix = _read_json(FIXTURES / "valid/evidence-branch-matrix.json")
        matrix["task_record"] = "harness/tasks/TASK.json"
        matrix["authorization"]["record"] = ".pi/evidence/TASK-AUTH-001.md"
        if matrix_mutator is not None:
            matrix_mutator(matrix)
        matrix_path = root / manifest["orchestration_profile"]["branch_matrix"]
        _write_json(matrix_path, matrix)

    return root, task_path


def _validation_path(
    task_path: Path, manifest_path: Path, task_id: str, root: Path
) -> Path:
    return (
        _TaskOwnershipManifestValidator()
        .execute(
            task_path,
            manifest_path,
            task_id,
            repository_root=root,
        )
        .manifest_path
    )


def _validate(root: Path, task_path: Path) -> Path:
    return _validation_path(
        task_path,
        root / ".pi/task-ownership/manifest.json",
        "TASK",
        root,
    )


def _install_invalid_matrix(root: Path, fixture_name: str) -> None:
    matrix = _read_json(FIXTURES / "invalid" / fixture_name)
    if "task_record" in matrix:
        matrix["task_record"] = "harness/tasks/TASK.json"
    authorization = matrix.get("authorization")
    if isinstance(authorization, dict) and "record" in authorization:
        authorization["record"] = (
            ".pi/evidence/missing-authorization.md"
            if fixture_name == "evidence-branch-matrix-wrong-authorization.json"
            else ".pi/evidence/TASK-AUTH-001.md"
        )
    _write_json(
        root / ".pi/task-ownership/tests/fixtures/valid/evidence-branch-matrix.json",
        matrix,
    )


def _expect_failure(
    root: Path, chain_path: Path, match: str
) -> pytest.ExceptionInfo[Exception]:
    with pytest.raises(OwnershipValidationError, match=match) as error:
        _validate(root, chain_path)
    return error


def test_current_version_1_p1_manifest_remains_valid() -> None:
    """The durable P1 version-1 manifest retains its compatibility behavior."""
    path = _validation_path(
        REPOSITORY_ROOT / "harness/tasks/P1.json",
        REPOSITORY_ROOT
        / ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json",
        "P1",
        REPOSITORY_ROOT,
    )
    assert path == (
        REPOSITORY_ROOT
        / ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json"
    )


def test_explicit_task_identity_mismatch_fails(tmp_path: Path) -> None:
    """The operation-scoped Task input must match the requested identity."""
    root, task_path = _make_repository(tmp_path, profile=False)
    task = _read_json(task_path)
    task["task_id"] = "OTHER"
    _write_json(task_path, task)

    _expect_failure(root, task_path, "identity does not match")


def test_declared_manifest_remains_fail_closed(tmp_path: Path) -> None:
    """Declaring a manifest retains all existing fail-closed validation."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["schema_version"] = 99

    root, chain_path = _make_repository(
        tmp_path, profile=False, manifest_mutator=mutate
    )

    _expect_failure(root, chain_path, "must select supported version 1 or 2")


def test_version_2_without_optional_profile_is_valid(tmp_path: Path) -> None:
    """Ordinary version-2 tasks do not have to enable evidence branches."""
    root, chain_path = _make_repository(tmp_path, profile=False)
    assert _validate(root, chain_path) == root / ".pi/task-ownership/manifest.json"


def test_valid_evidence_branch_profile_is_valid(tmp_path: Path) -> None:
    """A complete generic evidence-branches-v1 matrix passes preflight."""
    root, chain_path = _make_repository(tmp_path)
    assert _validate(root, chain_path) == root / ".pi/task-ownership/manifest.json"


def test_direct_completion_validator_argv_is_valid(tmp_path: Path) -> None:
    """Version 2 permits the exact declared path as the complete argv."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["completion_validator"]["command"] = [".pi/task-ownership/complete.py"]

    root, chain_path = _make_repository(
        tmp_path, profile=False, manifest_mutator=mutate
    )
    assert _validate(root, chain_path) == root / ".pi/task-ownership/manifest.json"


def test_v2_structured_scope_ignores_negated_agent_prose(tmp_path: Path) -> None:
    """Agent prose cannot revoke or grant structured version-2 path ownership."""
    root, chain_path = _make_repository(tmp_path)
    (root / ".pi/agents/implementation.md").write_text(
        _agent_record(
            "implementation-agent",
            "writer",
            "This agent does not own `work/implementation` or "
            "`.pi/task-ownership`; it claims `outside/structured/scope`.",
        ),
        encoding="utf-8",
    )
    assert _validate(root, chain_path) == root / ".pi/task-ownership/manifest.json"


def test_version_2_manifest_receives_full_schema_validation(tmp_path: Path) -> None:
    """Schema-invalid fields fail before semantic orchestration checks."""
    root, chain_path = _make_repository(tmp_path, profile=False)
    invalid = _read_json(FIXTURES / "invalid/ownership-v2-schema-extra-property.json")
    _write_json(root / ".pi/task-ownership/manifest.json", invalid)
    error = _expect_failure(root, chain_path, r"JSON Schema violations")
    assert "manifest.unexpected" in str(error.value)
    assert "manifest.owners.writers" in str(error.value)


@pytest.mark.parametrize(
    ("fixture_name", "match"),
    [
        ("evidence-branch-matrix-one-branch.json", "is too short"),
        (
            "evidence-branch-matrix-one-role-deterministic.json",
            "activation requires at least two writer roles",
        ),
        (
            "evidence-branch-matrix-missing-authorization.json",
            "authorization.*required property",
        ),
    ],
)
def test_profile_activation_and_authorization_shape_rejections(
    tmp_path: Path, fixture_name: str, match: str
) -> None:
    """Activation and structured authorization fail closed."""
    root, chain_path = _make_repository(tmp_path)
    _install_invalid_matrix(root, fixture_name)
    _expect_failure(root, chain_path, match)


def test_authorization_record_must_exist(tmp_path: Path) -> None:
    """A matrix cannot cite a missing durable authorization record."""
    root, chain_path = _make_repository(tmp_path)
    _install_invalid_matrix(root, "evidence-branch-matrix-wrong-authorization.json")
    _expect_failure(root, chain_path, "matrix.authorization.record does not exist")


@pytest.mark.parametrize(
    ("task_text", "match"),
    [
        (
            "Decision TASK-AUTH-001 does NOT authorize evidence-branches-v1.\n",
            "must contain exactly one affirmative",
        ),
        (
            '<!-- evidence-branch-authorization {"profile":"other-profile",'
            + '"decision_id":"TASK-AUTH-001","authorized":true} -->\n',
            "does not affirm the declared profile and decision",
        ),
        (
            '<!-- evidence-branch-authorization {"profile":"evidence-branches-v1",'
            + '"decision_id":"OTHER","authorized":true} -->\n',
            "does not affirm the declared profile and decision",
        ),
        (
            '<!-- evidence-branch-authorization {"profile":"evidence-branches-v1",'
            + '"decision_id":"TASK-AUTH-001","authorized":false} -->\n',
            "does not affirm the declared profile and decision",
        ),
    ],
)
def test_authorization_record_requires_exact_affirmative_marker(
    tmp_path: Path, task_text: str, match: str
) -> None:
    """Negation or mismatched structured fields cannot authorize the profile."""
    root, chain_path = _make_repository(tmp_path)
    (root / ".pi/evidence/TASK-AUTH-001.md").write_text(
        task_text,
        encoding="utf-8",
    )
    _expect_failure(root, chain_path, match)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("path", "../outside.py", "must not contain traversal"),
        ("path", "/tmp/outside.py", "must be repository-relative"),
    ],
)
def test_completion_validator_rejects_non_repository_paths(
    tmp_path: Path, field: str, value: str, match: str
) -> None:
    """Traversal and absolute validator paths fail with field-specific errors."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["completion_validator"][field] = value

    root, chain_path = _make_repository(
        tmp_path, profile=False, manifest_mutator=mutate
    )
    _expect_failure(root, chain_path, match)


def test_owned_path_rejects_symlink_escape(tmp_path: Path) -> None:
    """A non-existing leaf under an escaping symlink is outside the repository."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["owners"]["writers"][0]["owned_paths"] = ["escape/owned"]

    root, chain_path = _make_repository(
        tmp_path, profile=False, manifest_mutator=mutate
    )
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "escape").symlink_to(outside, target_is_directory=True)
    implementation_record = root / ".pi/agents/implementation.md"
    implementation_record.write_text(
        _agent_record("implementation-agent", "writer"), encoding="utf-8"
    )
    _expect_failure(root, chain_path, "escapes the repository through a symlink")


def test_branch_path_must_be_subset_of_owner_scope(tmp_path: Path) -> None:
    """A branch cannot widen the manifest writer's declared scope."""

    def mutate(matrix: dict[str, Any]) -> None:
        matrix["branches"][0]["owned_paths"] = ["work/unowned"]
        matrix["branches"][0]["evidence_paths"] = ["work/unowned/evidence.json"]

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    _expect_failure(root, chain_path, "outside owner role")


def test_writer_scopes_reject_normalized_overlap(tmp_path: Path) -> None:
    """Nested writer scopes are rejected before branch dispatch."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["owners"]["writers"][1]["owned_paths"] = ["work/implementation/tests"]

    root, chain_path = _make_repository(tmp_path, manifest_mutator=mutate)
    (root / ".pi/agents/tests.md").write_text(
        _agent_record("test-agent", "writer"), encoding="utf-8"
    )
    _expect_failure(root, chain_path, "writer owned_paths overlap")


def test_branch_evidence_must_be_owned_by_its_branch(tmp_path: Path) -> None:
    """Evidence cannot be assigned outside its branch even within owner scope."""

    def mutate(matrix: dict[str, Any]) -> None:
        matrix["branches"][0]["owned_paths"] = ["work/implementation/source"]
        matrix["branches"][0]["evidence_paths"] = ["work/implementation/review.json"]

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    _expect_failure(root, chain_path, "lacks branch/owner ownership")


def test_duplicate_branch_ids_are_rejected(tmp_path: Path) -> None:
    """Stable branch identities must be unique."""

    def mutate(matrix: dict[str, Any]) -> None:
        duplicate = deepcopy(matrix["branches"][0])
        duplicate["owned_paths"] = ["work/implementation/duplicate"]
        duplicate["evidence_paths"] = ["work/implementation/duplicate/evidence.json"]
        matrix["branches"].append(duplicate)

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    _expect_failure(root, chain_path, "matrix.branches IDs must be unique")


def test_branch_cycles_are_rejected_from_invalid_fixture(tmp_path: Path) -> None:
    """Prerequisite cycles fail deterministically with the cycle path."""
    root, chain_path = _make_repository(tmp_path)
    _install_invalid_matrix(root, "evidence-branch-matrix-cycle.json")
    _expect_failure(root, chain_path, "prerequisites contain a cycle")


@pytest.mark.parametrize(
    ("fixture_name", "match"),
    [
        ("evidence-branch-matrix-orphan-stage.json", "not referenced"),
        ("evidence-branch-matrix-wrong-stage-owner.json", "is not a writer"),
        (
            "evidence-branch-matrix-wrong-stage-evidence.json",
            "is outside owner role",
        ),
        (
            "evidence-branch-matrix-completion-mismatch.json",
            "does not equal the manifest completion command",
        ),
    ],
)
def test_validation_stage_ownership_and_completion_binding(
    tmp_path: Path, fixture_name: str, match: str
) -> None:
    """Stages are referenced, writer-owned, and bound to the completion gate."""
    root, chain_path = _make_repository(tmp_path)
    _install_invalid_matrix(root, fixture_name)
    _expect_failure(root, chain_path, match)


@pytest.mark.parametrize(
    ("checkpoint", "match"),
    [
        (None, "requires one existing checkpoint"),
        (
            {"checkpoint_id": "HC-1", "task_id": "OTHER", "status": "blocked"},
            "belongs to another task",
        ),
        (
            {"checkpoint_id": "HC-1", "task_id": "TASK", "status": "resolved"},
            "is not unresolved",
        ),
    ],
)
def test_protected_branch_requires_existing_unresolved_same_task_checkpoint(
    tmp_path: Path, checkpoint: dict[str, str] | None, match: str
) -> None:
    """Protected work binds only to one unresolved checkpoint for this task."""

    def mutate(matrix: dict[str, Any]) -> None:
        branch = matrix["branches"][0]
        branch["classification"] = "protected_checkpoint"
        branch["checkpoint_ids"] = ["HC-1"]

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    if checkpoint is not None:
        _write_json(root / ".pi/checkpoints/HC-1.json", checkpoint)
    _expect_failure(root, chain_path, match)


def test_deterministic_branch_cannot_name_checkpoint(tmp_path: Path) -> None:
    """Schema conditionals reject checkpoint IDs on deterministic branches."""

    def mutate(matrix: dict[str, Any]) -> None:
        matrix["branches"][0]["checkpoint_ids"] = ["HC-1"]

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    _expect_failure(root, chain_path, "JSON Schema violations")


def test_reviewer_role_cannot_own_branch(tmp_path: Path) -> None:
    """The consolidated reviewer remains independent and read-only."""

    def mutate(matrix: dict[str, Any]) -> None:
        matrix["branches"][0]["owner_role"] = "consolidated-review"

    root, chain_path = _make_repository(tmp_path, matrix_mutator=mutate)
    _expect_failure(root, chain_path, "reviewer-only and cannot own a branch")


@pytest.mark.parametrize(
    "command",
    [
        ["python", ".pi/task-ownership/other.py"],
        ["python", ".pi/task-ownership/complete.py", "--unbound-argument"],
    ],
)
def test_completion_command_has_exact_validator_argv(
    tmp_path: Path, command: list[str]
) -> None:
    """The validator path cannot be substituted or followed by unbound arguments."""

    def mutate(manifest: dict[str, Any]) -> None:
        manifest["completion_validator"]["command"] = command

    root, chain_path = _make_repository(
        tmp_path, profile=False, manifest_mutator=mutate
    )
    (root / ".pi/task-ownership/other.py").write_text(
        "raise SystemExit(0)\n", encoding="utf-8"
    )
    _expect_failure(root, chain_path, "must be exactly")


def test_correction_cycle_limit_greater_than_one_is_rejected(
    tmp_path: Path,
) -> None:
    """The approved profile cannot silently become an iterative repair loop."""
    root, chain_path = _make_repository(tmp_path)
    invalid = _read_json(FIXTURES / "invalid/ownership-v2-correction-limit-2.json")
    _write_json(root / ".pi/task-ownership/manifest.json", invalid)
    _expect_failure(
        root,
        chain_path,
        r"orchestration_profile.correction_cycle_limit.*1 was expected",
    )


def test_cli_explicit_inputs_success_and_identity_mismatch() -> None:
    """The public CLI reports stable output streams and nonzero failures."""
    task_record = "harness/tasks/P1.json"
    manifest = ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json"
    command = [
        sys.executable,
        "-m",
        "ksdft2effmass.harness.cli",
        "validate-task-ownership",
        "--repository-root",
        str(REPOSITORY_ROOT),
        "--task-record",
        task_record,
        "--ownership-manifest",
        manifest,
    ]

    passed = subprocess.run(
        [*command, "--task", "P1"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert passed.returncode == 0
    assert passed.stderr == ""
    assert passed.stdout == (
        "task ownership preflight passed: "
        ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json\n"
    )

    mismatch = subprocess.run(
        [*command, "--task", "MISSING"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert mismatch.returncode == 1
    assert mismatch.stdout == ""
    assert "identity does not match" in mismatch.stderr

    missing_command = command.copy()
    missing_command[missing_command.index("--task-record") + 1] = (
        "harness/tasks/does-not-exist.json"
    )
    missing = subprocess.run(
        [*missing_command, "--task", "P1"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert missing.returncode == 1
    assert missing.stdout == ""
    assert "No such file or directory" in missing.stderr
    assert "Traceback" not in missing.stderr
