r"""Software verification of ``TaskStateInspectionRequest``.

Facet and represented meaning
This module verifies the immutable explicit filesystem and task-selection request.
Intrinsic and cross-object scope
The sole SUT is ``TaskStateInspectionRequest``; literal paths and identifiers provide
exact constructor oracles.
VVUQ and scientific exclusions
Passing establishes request software semantics only, not repository truth, runtime
history, numerical verification, scientific validation, UQ, or human acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import TaskStateInspectionRequest

pytestmark = pytest.mark.software_verification
SUT = TaskStateInspectionRequest


def test_constructor__explicit_boundary__preserves_exact_state(tmp_path: Path) -> None:
    """Evidence ID
    SV-HARNESS-066
    Requirement
    The request represents one explicit absolute root, chain path, and task identity.
    Method
    Construct the request from controlled literal values and a pytest absolute path.
    Oracle
    The constructor inputs independently fix every represented field.
    Acceptance
    All four public fields equal the supplied values exactly.
    Interpretation
    Failure identifies request construction or represented-state drift.
    Limitations
    Filesystem existence and referenced-state validity are action-owned.
    """
    root = tmp_path.resolve()
    request = SUT(1, root, ".pi/chains/example.json", "example.task")
    assert request.schema_version == 1
    assert request.repository_root == root
    assert request.chain_path == ".pi/chains/example.json"
    assert request.task_id == "example.task"


def test_field__immutable_state__rejects_reassignment(tmp_path: Path) -> None:
    """Evidence ID
    SV-HARNESS-067
    Requirement
    A task-state inspection request is operationally immutable.
    Method
    Construct a valid request and attempt public task-identity reassignment.
    Oracle
    Frozen dataclass semantics require reassignment to raise FrozenInstanceError.
    Acceptance
    Reassignment raises exactly FrozenInstanceError.
    Interpretation
    Failure identifies loss of the immutable request boundary.
    Limitations
    Path-object internals and action execution are excluded.
    """
    request = SUT(1, tmp_path.resolve(), "chain.json", "example.task")
    with pytest.raises(FrozenInstanceError):
        request.task_id = "other.task"  # type: ignore[misc]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(
            (True, Path("/tmp"), "chain.json", "task"), id="boolean_version_wrong_type"
        ),
        pytest.param((1, "/tmp", "chain.json", "task"), id="string_root_wrong_type"),
        pytest.param((1, Path("relative"), "chain.json", "task"), id="relative_root"),
        pytest.param(
            (1, Path("/tmp"), "/chain.json", "task"), id="absolute_chain_path"
        ),
        pytest.param(
            (1, Path("/tmp"), "../chain.json", "task"), id="traversal_chain_path"
        ),
        pytest.param(
            (1, Path("/tmp"), "chain.json", "bad task"), id="invalid_task_identity"
        ),
    ),
)
def test_constructor__input_invariants__reject_invalid_values(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID
    SV-HARNESS-068
    Requirement
    Request fields reject wrong semantic types, implicit roots, and unsafe paths.
    Method
    Supply one controlled invalid constructor partition per parameter case.
    Oracle
    The explicit-boundary contract fixes the accepted version, Path, path, and ID forms.
    Acceptance
    Every declared invalid partition raises TypeError or ValueError.
    Interpretation
    Failure identifies intrinsic request-policy drift or an unsafe implicit boundary.
    Limitations
    Existing-file, symlink, and root-confinement checks are action-owned.
    """
    with pytest.raises((TypeError, ValueError)):
        SUT(*arguments)  # type: ignore[arg-type]
