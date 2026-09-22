r"""Software verification of ``TaskStateInspector``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies bounded inspection of exact canonical Task, selection, and
optional operation-scoped ownership inputs.

Intrinsic and cross-object scope

The sole SUT is ``TaskStateInspector``; controlled literal documents provide
independent identity, path, ordering, and failure oracles.

VVUQ and scientific exclusions

Passing establishes bounded software inspection only, not authority, execution,
numerical verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    TaskStateInspectionRequest,
    TaskStateInspectionResult,
    TaskStateInspector,
)

pytestmark = pytest.mark.software_verification
SUT = TaskStateInspector
TASK_ID = "example.task"
TASK_PATH = "harness/tasks/example.json"
SELECTION_PATH = "harness/task-selection.json"
OWNERSHIP_PATH = ".pi/task-ownership/example.json"
COMPLETION_PATH = "tools/check.py"


def write_repository(root: Path, *, selected: str | None = None) -> None:
    """Evidence ID: Owns no identifier; supports the TaskStateInspector cases.

    Requirement: Action evidence requires one controlled explicit-input tree.

    Method: Write literal Task, selection, ownership, and completion files.

    Oracle: The literal documents independently fix every supplied path.

    Acceptance: Create exactly the declared controlled files.

    Interpretation: Failure supports fixture diagnosis only.

    Limitations: The helper does not invoke the SUT.
    """
    task_path = root / TASK_PATH
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "schema_version": 3,
                "task_id": TASK_ID,
                "title": "Example Task",
                "status": "completed",
                "status_detail": None,
                "parent_task_id": None,
                "task_prerequisite_ids": [],
                "external_prerequisite_ids": [],
                "superseded_by_task_ids": [],
                "explicit_activation_required": True,
                "objective": "Provide controlled inspection input.",
                "authority_reference_paths": ["records/authority.md"],
                "authorized_scope": ["Inspect controlled inputs."],
                "completion_criteria": ["Inspection is deterministic."],
                "exclusions": ["No authority is inferred."],
                "intake_path": None,
                "archived_source": None,
            }
        )
    )
    selection_path = root / SELECTION_PATH
    selection_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_task_id": selected,
                "explicit_activation_receipt_ids": [],
                "automatic_successor_activation": False,
            }
        )
    )
    ownership_path = root / OWNERSHIP_PATH
    ownership_path.parent.mkdir(parents=True)
    ownership_path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "task_id": TASK_ID,
                "task_record": TASK_PATH,
                "owners": {
                    "writers": [
                        {
                            "role": "tests",
                            "agent": "z-writer",
                            "owned_paths": ["tests"],
                        },
                        {
                            "role": "implementation",
                            "agent": "a-writer",
                            "owned_paths": ["src"],
                        },
                    ],
                    "reviewers": [
                        {"role": "review-z", "agent": "z-reviewer"},
                        {"role": "review-a", "agent": "a-reviewer"},
                    ],
                },
                "completion_validator": {
                    "path": COMPLETION_PATH,
                    "command": ["python", COMPLETION_PATH],
                    "required_before_review": True,
                },
            }
        )
    )
    completion = root / COMPLETION_PATH
    completion.parent.mkdir(parents=True)
    completion.write_text("# controlled completion artifact\n")


def request(root: Path, *, ownership: bool = True) -> TaskStateInspectionRequest:
    """Evidence ID: Owns no identifier; supports the TaskStateInspector cases.

    Requirement: Action cases require one exact public request shape.

    Method: Construct a request from controlled constants.

    Oracle: Constants independently fix all explicit inputs.

    Acceptance: Return one valid immutable request.

    Interpretation: Failure supports fixture diagnosis only.

    Limitations: The helper performs no filesystem reads.
    """
    return TaskStateInspectionRequest(
        2,
        root.resolve(),
        TASK_PATH,
        SELECTION_PATH,
        TASK_ID,
        OWNERSHIP_PATH if ownership else None,
    )


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-HARNESS-071

    Requirement: TaskStateInspector is a stateless ActionObject.

    Method: Inspect instance storage and declared slots.

    Oracle: The public contract prohibits retained roots and mutable caches.

    Acceptance: The instance has no dictionary and empty slots.

    Interpretation: Failure identifies unauthorized retained state.

    Limitations: Execute behavior is covered separately.
    """
    value = SUT()
    assert not hasattr(value, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_declared_state__reports_exact_inputs(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-072

    Requirement: Execute reads only the exact Task, selection, ownership, and completion
    inputs.

    Method: Inspect a controlled valid tree.

    Oracle: Literal files fix status, selection, command, and sorted assignments.

    Acceptance: The result reports those facts exactly and passes validation.

    Interpretation: Failure identifies reference, parsing, or ordering drift.

    Limitations: Authority and runtime history remain excluded.
    """
    write_repository(tmp_path, selected=TASK_ID)
    result = SUT().execute(request(tmp_path))
    assert type(result) is TaskStateInspectionResult
    assert result.task_status == "completed"
    assert result.selected_task_id == TASK_ID
    assert result.task_path == TASK_PATH
    assert result.selection_path == SELECTION_PATH
    assert result.ownership_manifest_path == OWNERSHIP_PATH
    assert result.completion_command == ("python", COMPLETION_PATH)
    assert result.writers == (
        ("implementation", "a-writer"),
        ("tests", "z-writer"),
    )
    assert result.reviewers == (
        ("review-a", "a-reviewer"),
        ("review-z", "z-reviewer"),
    )
    assert result.inspected_paths == result.read_paths
    assert result.validation.status == "PASS"


def test_method__execute_task_identity__fails_closed(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-171

    Requirement: The explicit Task record must agree with the requested identity.

    Method: Replace the controlled identity with a different literal identity.

    Oracle: The request and Task bytes independently establish disagreement.

    Acceptance: Validation fails with REFERENCE_INVALID.

    Interpretation: Failure identifies fallback discovery or identity-check loss.

    Limitations: Complete Task schema validation belongs to the Task deserializer.
    """
    write_repository(tmp_path)
    task = json.loads((tmp_path / TASK_PATH).read_text())
    task["task_id"] = "different.task"
    (tmp_path / TASK_PATH).write_text(json.dumps(task))
    result = SUT().execute(request(tmp_path))
    assert result.task_status is None
    assert any(
        issue.code == "PIH.TASK_STATE.REFERENCE_INVALID"
        for issue in result.validation.issues
    )


def test_method__execute_optional_ownership__does_not_discover_manifest(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-073

    Requirement: Ownership is an optional operation-scoped input, never ambient state.

    Method: Retain a manifest file but omit its path from the request.

    Oracle: The request fixes the complete allowed input set.

    Acceptance: The manifest is not inspected and assignments remain empty.

    Interpretation: Failure identifies forbidden ownership discovery.

    Limitations: Whether an operation requires ownership is authority-policy owned.
    """
    write_repository(tmp_path)
    result = SUT().execute(request(tmp_path, ownership=False))
    assert result.validation.status == "PASS"
    assert OWNERSHIP_PATH not in result.inspected_paths
    assert result.writers == ()
    assert result.reviewers == ()


@pytest.mark.parametrize(
    "missing_path",
    (
        pytest.param(TASK_PATH, id="missing_task"),
        pytest.param(SELECTION_PATH, id="missing_selection"),
        pytest.param(OWNERSHIP_PATH, id="missing_ownership"),
    ),
)
def test_method__execute_missing_reference__reports_exact_path(
    tmp_path: Path, missing_path: str
) -> None:
    """Evidence ID: SV-HARNESS-074

    Requirement: Each supplied but missing reference fails at its exact path.

    Method: Remove one supplied file before inspection.

    Oracle: The request independently fixes the required path.

    Acceptance: Validation reports PIH.PATH.MISSING at that path.

    Interpretation: Failure identifies silent omission or fallback discovery.

    Limitations: Filesystem races after inspection are excluded.
    """
    write_repository(tmp_path)
    (tmp_path / missing_path).unlink()
    result = SUT().execute(request(tmp_path))
    assert any(
        issue.code == "PIH.PATH.MISSING" and issue.path == missing_path
        for issue in result.validation.issues
    )


def test_method__execute_ownership_identity__fails_closed(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-075

    Requirement: An explicit ownership manifest must match the requested Task.

    Method: Change only the manifest Task identity.

    Oracle: Request and manifest identities independently establish disagreement.

    Acceptance: Validation reports OWNERSHIP_INVALID.

    Interpretation: Failure identifies cross-Task assignment acceptance.

    Limitations: Authorization remains outside inspection.
    """
    write_repository(tmp_path)
    ownership = json.loads((tmp_path / OWNERSHIP_PATH).read_text())
    ownership["task_id"] = "different.task"
    (tmp_path / OWNERSHIP_PATH).write_text(json.dumps(ownership))
    result = SUT().execute(request(tmp_path))
    assert any(
        issue.code == "PIH.TASK_STATE.OWNERSHIP_INVALID"
        for issue in result.validation.issues
    )


def test_method__execute_malformed_selection__fails_closed(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-076

    Requirement: Selection input is closed and automatic succession remains disabled.

    Method: Set automatic successor activation true.

    Oracle: The accepted selection-v1 contract requires literal false.

    Acceptance: Validation reports REFERENCE_INVALID at the selection path.

    Interpretation: Failure identifies weakened selection policy.

    Limitations: Task eligibility and authority are excluded.
    """
    write_repository(tmp_path)
    selection = json.loads((tmp_path / SELECTION_PATH).read_text())
    selection["automatic_successor_activation"] = True
    (tmp_path / SELECTION_PATH).write_text(json.dumps(selection))
    result = SUT().execute(request(tmp_path))
    assert any(
        issue.code == "PIH.TASK_STATE.REFERENCE_INVALID"
        and issue.path == SELECTION_PATH
        for issue in result.validation.issues
    )


def test_method__execute_symlink_reference__rejects_indirection(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-077

    Requirement: Exact durable references reject symlinked components.

    Method: Replace the Task with a symlink to a controlled file.

    Oracle: Root confinement prohibits symlink traversal.

    Acceptance: Validation reports PIH.PATH.SYMLINK at the Task path.

    Interpretation: Failure identifies hidden indirection.

    Limitations: Platforms without symlink support may skip.
    """
    write_repository(tmp_path)
    target = tmp_path / "target.json"
    target.write_bytes((tmp_path / TASK_PATH).read_bytes())
    task = tmp_path / TASK_PATH
    task.unlink()
    try:
        task.symlink_to(target)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    result = SUT().execute(request(tmp_path))
    assert any(
        issue.code == "PIH.PATH.SYMLINK" and issue.path == TASK_PATH
        for issue in result.validation.issues
    )


def test_method__execute_repeated_request__ignores_ambient_decoys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID: SV-HARNESS-078

    Requirement: Inspection is deterministic and performs no directory discovery.

    Method: Add chain, SQLite, and unrelated decoys; prohibit discovery methods; run
    twice.

    Oracle: The request names the complete inspectable input set.

    Acceptance: Results are equal and no decoy is inspected.

    Interpretation: Failure identifies ambient authority or nondeterminism.

    Limitations: Exact supplied reads remain required.
    """
    write_repository(tmp_path)
    decoys = (
        ".pi/chains/legacy.json",
        "harness/state/harness-control.sqlite3",
        "unrelated/run.json",
    )
    chain_decoy = tmp_path / decoys[0]
    chain_decoy.parent.mkdir(parents=True, exist_ok=True)
    chain_decoy.write_text("{}")
    database_decoy = tmp_path / decoys[1]
    database_decoy.parent.mkdir(parents=True, exist_ok=True)
    database_decoy.write_text("{}")
    run_decoy = tmp_path / decoys[2]
    run_decoy.parent.mkdir(parents=True, exist_ok=True)
    run_decoy.write_text("{}")

    def reject_discovery(*_arguments: object, **_keywords: object) -> object:
        raise AssertionError("directory discovery is prohibited")

    monkeypatch.setattr(Path, "glob", reject_discovery)
    monkeypatch.setattr(Path, "rglob", reject_discovery)
    monkeypatch.setattr(Path, "iterdir", reject_discovery)
    first = SUT().execute(request(tmp_path))
    second = SUT().execute(request(tmp_path))
    assert first == second
    assert decoys[0] not in first.inspected_paths
    assert decoys[1] not in first.inspected_paths
    assert decoys[2] not in first.inspected_paths
