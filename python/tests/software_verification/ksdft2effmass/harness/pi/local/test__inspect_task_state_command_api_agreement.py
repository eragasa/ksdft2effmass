r"""Software verification of inspect task state command api agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies exact JSON and exit agreement between the thin project-local
command and the public generic task-state inspection API.

Intrinsic and cross-object scope

The command/API relation is primary; literal controlled repository documents and the
public result projection provide exact independent invocation oracles.

VVUQ and scientific exclusions

Passing establishes command integration only, not runtime history, review independence,
numerical verification, scientific validation, UQ, or human acceptance.
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

CHAIN_PATH = ".pi/chains/example.json"
TASK_ID = "example.task"


def write_command_repository(root: Path) -> None:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-079 and SV-HARNESS-080.

    Requirement: Command/API agreement cases require one controlled explicit
    durable-state tree.

    Method: Write one chain, task, ownership, and completion file below the supplied
    root.

    Oracle: Literal bytes independently fix the only references available to both
    invocations.

    Acceptance: The helper creates exactly the declared controlled files.

    Interpretation: Failure supports fixture diagnosis and makes no independent evidence
    claim.

    Limitations: The helper does not invoke either compared surface.
    """
    chain = {
        "name": "example",
        "active_task": None,
        "task_sequence": [
            {
                "id": TASK_ID,
                "record": ".pi/tasks/example.md",
                "ownership_manifest": ".pi/task-ownership/example.json",
                "prerequisites": [],
                "status": "completed",
            }
        ],
    }
    ownership = {
        "schema_version": 2,
        "task_id": TASK_ID,
        "task_record": ".pi/tasks/example.md",
        "owners": {
            "writers": [
                {
                    "role": "implementation",
                    "agent": "writer",
                    "owned_paths": ["src"],
                }
            ],
            "reviewers": [{"role": "review", "agent": "reviewer"}],
        },
        "completion_validator": {
            "path": "tools/check.py",
            "command": ["python", "tools/check.py"],
            "required_before_review": True,
        },
    }
    chain_file = root / CHAIN_PATH
    chain_file.parent.mkdir(parents=True, exist_ok=True)
    chain_file.write_text(json.dumps(chain))
    ownership_file = root / ".pi/task-ownership/example.json"
    ownership_file.parent.mkdir(parents=True, exist_ok=True)
    ownership_file.write_text(json.dumps(ownership))
    task = root / ".pi/tasks/example.md"
    task.parent.mkdir(parents=True, exist_ok=True)
    task.write_text("# Example\n\nStatus: completed\n")
    completion = root / "tools/check.py"
    completion.parent.mkdir(parents=True, exist_ok=True)
    completion.write_text("# completion artifact\n")


def run_command(root: Path, task_id: str) -> subprocess.CompletedProcess[str]:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-079 and SV-HARNESS-080.

    Requirement: Agreement evidence requires the documented module invocation with
    explicit inputs.

    Method: Invoke the module through the canonical current test interpreter and capture
    output.

    Oracle: The documented command form fixes argv and expects one canonical JSON line.

    Acceptance: The helper returns the completed process without modifying its result.

    Interpretation: Failure supports command-boundary diagnosis and owns no evidence
    result.

    Limitations: Interpreter installation and operating-system process startup are
    environmental.
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
            "--chain",
            CHAIN_PATH,
            "--task-id",
            task_id,
        ),
        check=False,
        capture_output=True,
        text=True,
    )


def test_artifact__valid_command_api_projection__agrees_exactly(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-079

    Requirement: The thin command exactly renders a successful public ActionObject
    result.

    Method: Invoke the API and documented module command against the same controlled
    root.

    Oracle: ``result_object`` is the command's declared mechanical projection of the
    public
    result.

    Acceptance: Exit status is zero and decoded command JSON equals the API projection
    exactly.

    Interpretation: Failure identifies wrapper argument, rendering, action routing, or
    exit-map drift.

    Limitations: This checks one valid controlled repository and not interactive runtime
    state.
    """
    write_command_repository(tmp_path)
    root = tmp_path.resolve()
    api_result = TaskStateInspector().execute(
        TaskStateInspectionRequest(1, root, CHAIN_PATH, TASK_ID)
    )
    command = run_command(root, TASK_ID)
    assert command.returncode == 0
    assert json.loads(command.stdout) == result_object(api_result)
    assert command.stderr == ""


def test_artifact__invalid_command_api_projection__agrees_exactly(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-080

    Requirement: The thin command preserves public findings and maps invalid durable
    state nonzero.

    Method: Request the same absent task identity through the API and documented
    command.

    Oracle: Exact task selection yields the public TASK_MISSING result and exit status
    one.

    Acceptance: Exit status is one and decoded command JSON equals the API projection
    exactly.

    Interpretation: Failure identifies diagnostic loss or exit-status disagreement in
    the wrapper.

    Limitations: Malformed argv uses argparse's separate standard error mapping.
    """
    write_command_repository(tmp_path)
    root = tmp_path.resolve()
    missing = "missing.task"
    api_result = TaskStateInspector().execute(
        TaskStateInspectionRequest(1, root, CHAIN_PATH, missing)
    )
    command = run_command(root, missing)
    assert command.returncode == 1
    assert json.loads(command.stdout) == result_object(api_result)
    assert command.stderr == ""
