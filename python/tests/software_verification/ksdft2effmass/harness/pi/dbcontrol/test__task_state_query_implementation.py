r"""Software verification of private explicit-input Task-state query.

Evidence profile: routine

Bounded artifact scope: private Task-state query representation.

Facet and represented meaning

The module verifies that ``_TaskStateQuery`` retains every explicit input.

Intrinsic and cross-object scope

Only constructor state is exercised; filesystem collaborators are excluded.

VVUQ and scientific exclusions

This is software verification only; authority, scientific validation, and UQ are
excluded.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.dbcontrol.inspection import _TaskStateQuery

pytestmark = pytest.mark.software_verification


def test_constructor__explicit_inputs__preserves_operation_scope() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state-query.constructor.explicit-inputs

    Requirement: The query retains Task, selection, identity, root, and ownership input.

    Method: Construct from distinct literal values.

    Oracle: Constructor inputs fix every retained slot.

    Acceptance: All five represented inputs match exactly.

    Interpretation: Failure indicates ambient or lost query state.

    Limitations: Filesystem inspection is excluded.
    """  # noqa: E501
    value = _TaskStateQuery(
        Path("/repo"),
        "task.json",
        "selection.json",
        "task.test",
        "ownership.json",
    )
    assert value.repository_root == Path("/repo")
    assert value.task_path == "task.json"
    assert value.selection_path == "selection.json"
    assert value.task_id == "task.test"
    assert value.ownership_manifest_path == "ownership.json"
