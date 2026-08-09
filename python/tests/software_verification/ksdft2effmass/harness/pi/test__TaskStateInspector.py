r"""Software verification of ``TaskStateInspector``.

Facet and represented meaning

This module verifies bounded resolution of one task's declared durable repository state.

Intrinsic and cross-object scope

The sole SUT is ``TaskStateInspector``; controlled repository trees and literal chain
and
ownership documents supply independent path, ordering, and missing-state oracles.

VVUQ and scientific exclusions

Passing establishes bounded software inspection only, not interactive run history,
review independence, numerical verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    TaskStateInspectionRequest,
    TaskStateInspectionResult,
    TaskStateInspector,
)

pytestmark = pytest.mark.software_verification
SUT = TaskStateInspector
TASK_ID = "example.task"
CHAIN_PATH = ".pi/chains/example.json"
TASK_PATH = ".pi/tasks/example.md"
OWNERSHIP_PATH = ".pi/task-ownership/example.json"
COMPLETION_PATH = "tools/check.py"
ARTIFACT_PATH = "records/artifact.json"
JSON_TASK_PATH = ".pi/tasks/example.json"


def write_controlled_repository(
    root: Path,
    *,
    task_id: str = TASK_ID,
    task_record: str = TASK_PATH,
    ownership_path: str = OWNERSHIP_PATH,
    extra_task_fields: dict[str, Any] | None = None,
) -> None:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-071 through SV-HARNESS-078
    and SV-HARNESS-171.

    Requirement: Action evidence requires one explicit controlled durable-state tree.

    Method: Write literal chain, task, ownership, completion, and artifact files below
    one root.

    Oracle: The literal documents independently declare every path the action may
    inspect.

    Acceptance: The helper creates only the named controlled files and applies explicit
    task fields.

    Interpretation: Failure supports diagnosis of fixture setup rather than action
    correctness.

    Limitations: The helper owns no evidence and does not invoke the SUT.
    """
    chain = {
        "name": "example",
        "active_task": None,
        "task_sequence": [
            {
                "id": task_id,
                "record": task_record,
                "ownership_manifest": ownership_path,
                "prerequisites": [],
                "status": "completed",
                "artifact_paths": [ARTIFACT_PATH],
                **(extra_task_fields or {}),
            }
        ],
    }
    ownership = {
        "schema_version": 2,
        "task_id": TASK_ID,
        "task_record": TASK_PATH,
        "owners": {
            "writers": [
                {"role": "tests", "agent": "z-writer", "owned_paths": ["tests"]},
                {"role": "implementation", "agent": "a-writer", "owned_paths": ["src"]},
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
    chain_path = root / CHAIN_PATH
    chain_path.parent.mkdir(parents=True, exist_ok=True)
    chain_path.write_text(json.dumps(chain))
    task_path = root / TASK_PATH
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text("# Example task\n\nStatus: completed\n")
    ownership_file = root / OWNERSHIP_PATH
    ownership_file.parent.mkdir(parents=True, exist_ok=True)
    ownership_file.write_text(json.dumps(ownership))
    completion_path = root / COMPLETION_PATH
    completion_path.parent.mkdir(parents=True, exist_ok=True)
    completion_path.write_text("# controlled completion artifact\n")
    artifact_path = root / ARTIFACT_PATH
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text("{}\n")


def request(root: Path, task_id: str = TASK_ID) -> TaskStateInspectionRequest:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-071 through SV-HARNESS-078
    and SV-HARNESS-171.

    Requirement: Action cases require one exact public request shape.

    Method: Construct the request with the controlled absolute root and chain path.

    Oracle: The fixture constants independently fix the selected task and chain.

    Acceptance: The helper returns one valid public request without filesystem
    discovery.

    Interpretation: Failure supports diagnosis of fixture or request-contract drift.

    Limitations: The helper owns no evidence and does not execute the action.
    """
    return TaskStateInspectionRequest(1, root.resolve(), CHAIN_PATH, task_id)


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-HARNESS-071

    Requirement: TaskStateInspector is a concrete stateless ActionObject.

    Method: Construct the action and inspect its instance storage boundary.

    Oracle: The maintained-tool contract prohibits retained roots, caches, and mutable
    state.

    Acceptance: The instance has no dictionary and the class declares empty slots.

    Interpretation: Failure identifies unauthorized retained state.

    Limitations: Execute behavior is covered separately.
    """
    value = SUT()
    assert not hasattr(value, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_declared_state__reports_exact_bounded_records(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-072

    Requirement: Execute resolves the exact selected task and only its declared durable
    references.

    Method: Inspect a controlled valid chain with task, ownership, completion, and
    artifact
    files.

    Oracle: The literal tree fixes status, paths, completion command, and sorted role
    identities.

    Acceptance: The result exactly reports the declared facts, read paths, and no
    validation issues.

    Interpretation: Failure identifies task resolution, ordering, reference, or
    result-construction
    drift.

    Limitations: Undeclared runtime history and interactive reviewer counts remain
    excluded.
    """
    write_controlled_repository(tmp_path)
    result = SUT().execute(request(tmp_path))
    assert type(result) is TaskStateInspectionResult
    assert result.task_status == "completed"
    assert result.active_task_id is None
    assert result.task_record_path == TASK_PATH
    assert result.ownership_manifest_path == OWNERSHIP_PATH
    assert result.completion_validator_path == COMPLETION_PATH
    assert result.completion_command == ("python", COMPLETION_PATH)
    assert result.writers == (
        ("implementation", "a-writer"),
        ("tests", "z-writer"),
    )
    assert result.reviewers == (
        ("review-a", "a-reviewer"),
        ("review-z", "z-reviewer"),
    )
    assert result.artifact_paths == (ARTIFACT_PATH,)
    assert result.durable_run_record_status == "not_declared"
    assert result.durable_handoff_record_status == "not_declared"
    assert result.inspected_paths == result.read_paths
    assert result.validation.status == "PASS"


def test_method__execute_json_task__uses_exact_reference_identity_and_status(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-171

    Requirement: TaskStateInspector reads a JSON Task only through the selected exact
    chain reference and obtains identity and status from that record.

    Method: Replace one controlled Markdown reference with a JSON reference, inspect it,
    retain an irrelevant chain status field, and then change the JSON identity.

    Oracle: The generic inspection contract owns exact path selection, duplicate-key
    rejection, identity agreement, and status extraction but not local Task schema
    policy.

    Acceptance: Exact-reference inspection reports JSON status and only the JSON path;
    identity disagreement fails with REFERENCE_INVALID.

    Interpretation: Failure indicates fallback discovery, chain-status precedence, local
    policy leakage, or missing identity validation.

    Limitations: Complete project-local schema and Task/chain authority validation
    belongs to local adapters and validators; no activation or persistence is
    established.
    """
    write_controlled_repository(tmp_path)
    chain_file = tmp_path / CHAIN_PATH
    chain = json.loads(chain_file.read_text())
    entry = chain["task_sequence"][0]
    entry["record"] = JSON_TASK_PATH
    del entry["prerequisites"]
    chain_file.write_text(json.dumps(chain))
    json_task = tmp_path / JSON_TASK_PATH
    json_task.write_text(json.dumps({"task_id": TASK_ID, "status": "active"}))
    ownership_file = tmp_path / OWNERSHIP_PATH
    ownership = json.loads(ownership_file.read_text())
    ownership["task_record"] = JSON_TASK_PATH
    ownership_file.write_text(json.dumps(ownership))

    json_result = SUT().execute(request(tmp_path))
    assert json_result.task_status == "active"
    assert json_result.task_record_path == JSON_TASK_PATH
    assert JSON_TASK_PATH in json_result.read_paths
    assert TASK_PATH not in json_result.read_paths
    assert json_result.validation.status == "PASS"

    json_task.write_text(json.dumps({"task_id": "different.task", "status": "active"}))
    mismatched = SUT().execute(request(tmp_path))
    assert mismatched.validation.status == "FAIL"
    assert any(
        issue.code == "PIH.TASK_STATE.REFERENCE_INVALID"
        for issue in mismatched.validation.issues
    )


def test_method__execute_unknown_task__reports_required_resolution_failure(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-073

    Requirement: An exact task identity absent from the selected chain is an explicit
    failure.

    Method: Request an unknown identity from an otherwise valid controlled chain.

    Oracle: Exact task selection requires one and only one matching chain entry.

    Acceptance: The result has no task status and contains PIH.TASK_STATE.TASK_MISSING.

    Interpretation: Failure identifies guessing, fallback selection, or missing
    diagnostics.

    Limitations: Similar task names and cross-chain discovery are intentionally
    excluded.
    """
    write_controlled_repository(tmp_path)
    result = SUT().execute(request(tmp_path, "missing.task"))
    assert result.task_status is None
    assert tuple(issue.code for issue in result.validation.issues) == (
        "PIH.TASK_STATE.TASK_MISSING",
    )


@pytest.mark.parametrize(
    ("missing_path", "expected_result_field"),
    (
        pytest.param(TASK_PATH, "task_record_path", id="missing_task_record"),
        pytest.param(
            OWNERSHIP_PATH, "ownership_manifest_path", id="missing_ownership_record"
        ),
    ),
)
def test_method__execute_missing_required_reference__reports_exact_path(
    tmp_path: Path,
    missing_path: str,
    expected_result_field: str,
) -> None:
    """Evidence ID: SV-HARNESS-074

    Requirement: A declared task or ownership record that is absent is reported as
    invalid state.

    Method: Remove one selected required file from the controlled repository before
    inspection.

    Oracle: The chain's exact reference fixes the missing path without any fallback
    search.

    Acceptance: Validation fails with PIH.PATH.MISSING at the selected path while
    retaining its
    field.

    Interpretation: Failure identifies silent omission, recursive fallback, or
    path-reporting drift.

    Limitations: Filesystem races after inspection are excluded.
    """
    write_controlled_repository(tmp_path)
    (tmp_path / missing_path).unlink()
    result = SUT().execute(request(tmp_path))
    assert getattr(result, expected_result_field) == missing_path
    assert any(
        issue.code == "PIH.PATH.MISSING" and issue.path == missing_path
        for issue in result.validation.issues
    )


def test_method__execute_declared_missing_run__distinguishes_absence(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-075

    Requirement: A declared-but-missing run record differs from no declared run record.

    Method: Add one exact absent run-record path to the controlled task entry.

    Oracle: The declaration fixes both the expected status and missing path.

    Acceptance: Run status is declared_missing and validation reports PIH.PATH.MISSING
    there.

    Interpretation: Failure identifies conflation of undeclared and invalid durable
    runtime state.

    Limitations: Interactive runtime observations are outside repository state.
    """
    run_path = "records/run.json"
    write_controlled_repository(
        tmp_path,
        extra_task_fields={"run_record_paths": [run_path]},
    )
    result = SUT().execute(request(tmp_path))
    assert result.run_record_paths == (run_path,)
    assert result.durable_run_record_status == "declared_missing"
    assert any(issue.path == run_path for issue in result.validation.issues)


def test_method__execute_traversal_declaration__fails_without_root_escape(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-076

    Requirement: Declared artifact paths cannot traverse above the explicit repository
    root.

    Method: Supply one task entry whose artifact declaration contains a parent segment.

    Oracle: The established ResourcePath policy prohibits traversal segments.

    Acceptance: Validation fails and no inspected or read path contains the traversal
    value.

    Interpretation: Failure identifies unsafe path acceptance or an attempted root
    escape.

    Limitations: Operating-system permission policy is excluded.
    """
    write_controlled_repository(
        tmp_path,
        extra_task_fields={"artifact_paths": ["../outside.json"]},
    )
    result = SUT().execute(request(tmp_path))
    assert result.validation.status == "FAIL"
    assert "../outside.json" not in result.inspected_paths
    assert "../outside.json" not in result.read_paths


def test_method__execute_symlink_reference__rejects_indirection(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-077

    Requirement: Exact durable references reject symlinked files and path components.

    Method: Replace the declared task record with a symlink to a controlled regular
    file.

    Oracle: The action contract prohibits symlink traversal under the explicit root.

    Acceptance: Validation contains PIH.PATH.SYMLINK for the declared task-record path.

    Interpretation: Failure identifies filesystem-boundary weakening or hidden
    indirection.

    Limitations: Platforms without symlink support may skip this controlled case.
    """
    write_controlled_repository(tmp_path)
    target = tmp_path / "target.md"
    target.write_text("# target\n")
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


def test_method__execute_repeated_request__ignores_undeclared_decoys(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-HARNESS-078

    Requirement: Repeated inspection is equal and performs no recursive or directory
    discovery.

    Method: Add unrelated decoy run and handoff files, prohibit Path glob/iterdir
    methods, and
    execute the same request twice.

    Oracle: Only literal chain references may be inspected; decoys are undeclared and
    irrelevant.

    Acceptance: Results are equal, discovery hooks are unused, and no decoy path is
    reported.

    Interpretation: Failure identifies retained state, nondeterminism, or forbidden
    recursive discovery.

    Limitations: Direct reads of declared files remain required operational behavior.
    """
    write_controlled_repository(tmp_path)
    decoys = ("unrelated/run.json", "unrelated/handoff.json")
    run_decoy = tmp_path / decoys[0]
    run_decoy.parent.mkdir(parents=True, exist_ok=True)
    run_decoy.write_text("{}")
    handoff_decoy = tmp_path / decoys[1]
    handoff_decoy.write_text("{}")

    def reject_discovery(*_arguments: object, **_keywords: object) -> object:
        raise AssertionError("directory discovery is prohibited")

    monkeypatch.setattr(Path, "glob", reject_discovery)
    monkeypatch.setattr(Path, "rglob", reject_discovery)
    monkeypatch.setattr(Path, "iterdir", reject_discovery)
    action = SUT()
    first = action.execute(request(tmp_path))
    second = action.execute(request(tmp_path))
    assert first == second
    assert all(relative not in first.inspected_paths for relative in decoys)
