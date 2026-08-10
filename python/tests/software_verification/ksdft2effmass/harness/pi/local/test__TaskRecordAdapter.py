r"""Software verification of ``TaskRecordAdapter``.

Facet and represented meaning

The module verifies explicit adaptation of selected project Task records.

Intrinsic and cross-object scope

``TaskRecordAdapter`` is the sole owner; chain and activation bytes are explicit inputs.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

import json
from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import TaskRecordAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = TaskRecordAdapter


def selected_inputs() -> tuple[tuple[tuple[str, bytes], ...], bytes, bytes]:
    """Evidence ID: Owns no identifier; supports SV-HL-038.

    Requirement: The enclosing test requires explicit current H4 input bytes.

    Method: Read only the paths named by the fixed chain and activation records.

    Oracle: The selected repository files define the controlled setup bytes.

    Acceptance: Return Task documents, chain bytes, and activation bytes without
    adaptation.

    Interpretation: Failure indicates controlled setup drift.

    Limitations: This helper owns no independent evidence claim.
    """
    root = repository_root()
    chain_bytes = (root / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    activation_bytes = (
        root / ".pi/evidence/pi-harness-incubation/H4/activation.json"
    ).read_bytes()
    chain = json.loads(chain_bytes)
    documents = tuple(
        (item["record"], (root / item["record"]).read_bytes())
        for item in reversed(chain["task_sequence"])
    )
    return documents, chain_bytes, activation_bytes


def test_method__execute__sorts_selected_tasks_and_fails_closed_when_missing() -> None:
    """Evidence ID: SV-HL-038

    Requirement: Explicitly selected Task records are complete and ordered
    deterministically.

    Method: Adapt the current reversed H4 selection, then omit H3 and adapt again.

    Oracle: The supplied chain selects H0 through H4 plus ``harness.extraction`` and
    requires every selected record.

    Acceptance: The complete result passes in lexical Task order; the incomplete result
    fails with
    no value and reports missing selected Task bytes.

    Interpretation: Failure indicates ordering drift or permissive fallback discovery.

    Limitations: The test does not establish chain semantics, scientific validity, or
    UQ.
    """
    documents, chain_bytes, activation_bytes = selected_inputs()
    result = TaskRecordAdapter().execute(documents, chain_bytes, activation_bytes)
    assert result.validation.status == "PASS"
    assert [item.task_id for item in cast(Any, result.value)] == [
        "H0",
        "H1",
        "H2",
        "H3",
        "H4",
        "harness.extraction",
    ]
    selected_chain = json.loads(chain_bytes)
    h3_path = next(
        item["record"] for item in selected_chain["task_sequence"] if item["id"] == "H3"
    )
    incomplete = TaskRecordAdapter().execute(
        tuple(item for item in documents if item[0] != h3_path),
        chain_bytes,
        activation_bytes,
    )
    assert incomplete.validation.status == "FAIL"
    assert incomplete.value is None
    assert "missing selected task bytes" in incomplete.validation.issues[0].detail


def test_method__execute__validates_complete_json_task_and_chain_agreement() -> None:
    """Evidence ID: SV-HL-045

    Requirement: A chain-referenced JSON Task must satisfy the complete local shape,
    preserve canonical prerequisites, and agree with chain-owned activation facts.

    Method: Adapt one complete JSON Task, then independently introduce duplicated chain
    authority, identity disagreement, and noncanonical prerequisite ordering.

    Oracle: The accepted file-per-Task contract and chain allocation define the exact
    valid fields, canonical order, identity join, and activation relation.

    Acceptance: The valid Task produces the expected TaskReference; every isolated
    contract defect fails without a value and reports its represented conflict.

    Interpretation: Failure indicates incomplete Task validation, silent normalization,
    or ambiguous Task/chain authority.

    Limitations: This verifies one project-local JSON pilot and retained Markdown
    composition; it does not establish persistence, SQLite behavior, or activation.
    """
    json_path = "records/example.task.json"
    json_task = {
        "schema_version": 1,
        "task_id": "example.task",
        "title": "Example Task",
        "status": "active",
        "parent_task_id": "parent.task",
        "task_prerequisite_ids": ["prior.task"],
        "external_prerequisite_ids": ["external.decision"],
        "explicit_activation_required": True,
        "objective": "Verify one complete JSON Task.",
        "authority_reference_paths": ["records/decision.json"],
        "authorized_scope": ["Adapt this synthetic Task."],
        "completion_criteria": ["The public adaptation passes."],
        "exclusions": ["No work is activated."],
        "intake_path": "records/intake.md",
        "archived_source": None,
    }
    mixed_chain = {
        "active_task": "example.task",
        "automatic_successor_activation": False,
        "explicitly_activated_task_ids": ["example.task"],
        "task_sequence": [
            {
                "id": "prior.task",
                "record": "records/prior.md",
                "prerequisites": [],
                "status": "completed",
            },
            {"id": "example.task", "record": json_path},
        ],
    }
    prior = ("records/prior.md", b"# Prior\n\nStatus: completed\n")

    def adapt_json_task(task: dict[str, object], chain: dict[str, object]) -> Any:
        documents = (prior, (json_path, json.dumps(task).encode()))
        return TaskRecordAdapter().execute(documents, json.dumps(chain).encode(), b"{}")

    adapted_json = adapt_json_task(json_task, mixed_chain)
    assert adapted_json.validation.status == "PASS"
    selected = next(
        item for item in cast(Any, adapted_json.value) if item.task_id == "example.task"
    )
    assert selected.task_prerequisite_ids == ("prior.task",)
    assert selected.external_prerequisite_ids == ("external.decision",)
    assert selected.status == "active"
    assert selected.explicit_activation_required is True

    duplicated_chain = json.loads(json.dumps(mixed_chain))
    duplicated_chain["task_sequence"][1]["status"] = "active"
    duplicated = adapt_json_task(json_task, duplicated_chain)
    assert duplicated.validation.status == "FAIL"
    assert "duplicated" in duplicated.validation.issues[0].detail

    mismatched_task = {**json_task, "task_id": "different.task"}
    mismatch = adapt_json_task(mismatched_task, mixed_chain)
    assert mismatch.validation.status == "FAIL"
    assert "identity differs" in mismatch.validation.issues[0].detail

    unsorted_task = {
        **json_task,
        "task_prerequisite_ids": ["prior.task", "another.task"],
    }
    unsorted = adapt_json_task(unsorted_task, mixed_chain)
    assert unsorted.validation.status == "FAIL"
    assert "unique and sorted" in unsorted.validation.issues[0].detail

    incomplete_task = dict(json_task)
    del incomplete_task["title"]
    incomplete = adapt_json_task(incomplete_task, mixed_chain)
    assert incomplete.validation.status == "FAIL"
    assert "missing title" in incomplete.validation.issues[0].detail
