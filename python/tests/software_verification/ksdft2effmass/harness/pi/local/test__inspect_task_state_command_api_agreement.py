r"""Software verification of inspect Task-state command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies exact JSON and exit agreement between the thin command and public
explicit-input Task-state inspection API.

Intrinsic and cross-object scope

The command/API relation is primary; literal Task and selection documents provide the
invocation oracle.

VVUQ and scientific exclusions

Passing establishes command integration only, not authority, execution, numerical
verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import TaskStateInspectionRequest, TaskStateInspector
from ksdft2effmass.harness.pi.local._commands.inspect_task_state import result_object

pytestmark = pytest.mark.software_verification

TASK_PATH = "harness/tasks/example.json"
SELECTION_PATH = "harness/task-selection.json"
TASK_ID = "example.task"


def write_command_repository(root: Path) -> None:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-079 and SV-HARNESS-080.

    Requirement: Command evidence requires exact canonical inputs.

    Method: Write literal Task and selection JSON.

    Oracle: Literal bytes fix both command inputs.

    Acceptance: Create exactly the declared files.

    Interpretation: Failure supports fixture diagnosis only.

    Limitations: The helper does not invoke either compared surface.
    """
    task = root / TASK_PATH
    task.parent.mkdir(parents=True)
    task.write_text(
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
                "objective": "Provide controlled command input.",
                "authority_reference_paths": ["records/authority.md"],
                "authorized_scope": ["Inspect controlled inputs."],
                "completion_criteria": ["Projection agrees."],
                "exclusions": ["No authority is inferred."],
                "intake_path": None,
                "archived_source": None,
            }
        )
    )
    selection = root / SELECTION_PATH
    selection.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_task_id": None,
                "explicit_activation_receipt_ids": [],
                "automatic_successor_activation": False,
            }
        )
    )


def run_command(root: Path, task_id: str) -> subprocess.CompletedProcess[str]:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-079 and SV-HARNESS-080.

    Requirement: Agreement evidence requires the documented command invocation.

    Method: Invoke the CLI with exact explicit arguments and capture output.

    Oracle: The public command contract fixes argv and one JSON line.

    Acceptance: Return the unmodified completed process.

    Interpretation: Failure supports command-boundary diagnosis only.

    Limitations: Process startup is environmental.
    """
    return subprocess.run(
        (
            sys.executable,
            str(
                Path(__file__).resolve().parents[7]
                / "python/src/cli/inspect_task_state.py"
            ),
            "--root",
            str(root),
            "--task",
            TASK_PATH,
            "--selection",
            SELECTION_PATH,
            "--task-id",
            task_id,
        ),
        check=False,
        capture_output=True,
        text=True,
    )


def test_artifact__valid_command_api_projection__agrees_exactly(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-079

    Requirement: The command exactly renders a successful public ActionObject result.

    Method: Invoke API and command against the same controlled root.

    Oracle: ``result_object`` is the declared mechanical projection.

    Acceptance: Exit zero and decoded JSON equals the API projection.

    Interpretation: Failure identifies argument, rendering, or routing drift.

    Limitations: This checks one valid controlled repository.
    """
    write_command_repository(tmp_path)
    root = tmp_path.resolve()
    api_result = TaskStateInspector().execute(
        TaskStateInspectionRequest(2, root, TASK_PATH, SELECTION_PATH, TASK_ID)
    )
    command = run_command(root, TASK_ID)
    assert command.returncode == 0
    assert json.loads(command.stdout) == result_object(api_result)
    assert command.stderr == ""


def test_artifact__invalid_command_api_projection__agrees_exactly(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-080

    Requirement: The command preserves public findings for identity disagreement.

    Method: Request an identity different from the exact Task input through both APIs.

    Oracle: Exact identity agreement is required and maps to exit one.

    Acceptance: Exit one and decoded JSON equals the API projection.

    Interpretation: Failure identifies diagnostic or exit-status disagreement.

    Limitations: Malformed argv uses argparse's standard mapping.
    """
    write_command_repository(tmp_path)
    root = tmp_path.resolve()
    missing = "missing.task"
    api_result = TaskStateInspector().execute(
        TaskStateInspectionRequest(2, root, TASK_PATH, SELECTION_PATH, missing)
    )
    command = run_command(root, missing)
    assert command.returncode == 1
    assert json.loads(command.stdout) == result_object(api_result)
    assert command.stderr == ""
