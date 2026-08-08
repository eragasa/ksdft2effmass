r"""Software verification of ``CheckpointDecisionResolutionRequest``.

Facet and represented meaning
Software verification of explicit immutable checkpoint-resolution inputs.

Intrinsic and cross-object scope
The sole primary SUT is ``CheckpointDecisionResolutionRequest``. Exact field types,
identifier and timestamp validity, distinct statuses, verbatim response storage,
equality, and immutability are in scope. Human-intent interpretation is excluded.

VVUQ and scientific exclusions
Passing establishes only the stated software contract, not scientific validity,
uncertainty quantification, human acceptance, or operational authorization.
"""

from __future__ import annotations

from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    CheckpointDecisionResolutionRequest,
    CheckpointRecord,
)

pytestmark = pytest.mark.software_verification
SUT = CheckpointDecisionResolutionRequest


def make_pending_checkpoint_for_request() -> CheckpointRecord:
    """Evidence ID
    Owns no identifier; supports request-constructor evidence.
    Requirement
    Tests require one independently valid unresolved generic checkpoint.
    Method
    Construct a public CheckpointRecord from fixed exact fields.
    Oracle
    The public CheckpointRecord contract defines valid support input.
    Acceptance
    Return one immutable pending checkpoint with two declared options.
    Interpretation
    Failure indicates invalid setup rather than request behavior.
    Limitations
    This helper owns no independent evidence claim.
    """
    return CheckpointRecord(
        1,
        "T1-HC01",
        "T1",
        "episode-T1",
        "pending",
        "contract",
        "2026-08-04T00:00:00Z",
        "Choose an option.",
        (("A", "Accept.", None), ("B", "Defer.", "Remain blocked.")),
        None,
        None,
        None,
        None,
        ("tasks/T1.json",),
        "blocked",
    )


def make_valid_request_values() -> dict[str, Any]:
    """Evidence ID
    Owns no identifier; supports request-constructor evidence.
    Requirement
    Constructor partitions require one complete valid field mapping.
    Method
    Return fixed explicit values without normalization or clock access.
    Oracle
    The accepted request contract fixes every support value.
    Acceptance
    Return values that construct one valid request.
    Interpretation
    Failure indicates invalid setup rather than request behavior.
    Limitations
    This helper owns no independent evidence claim.
    """
    return {
        "checkpoint": make_pending_checkpoint_for_request(),
        "expected_unresolved_status": "pending",
        "resolved_status": "resolved",
        "human_response": "  Approve option A.\n",
        "normalized_decision": "A",
        "resolved_at": "2026-08-04T00:01:02Z",
        "authorized_scope": "bounded implementation",
    }


def test_constructor__valid_fields__maps_exact_values_and_verbatim_response() -> None:
    """Evidence ID
    SV-HARNESS-098
    Requirement
    A valid request preserves every explicit field, including human text verbatim.
    Method
    Construct two requests from the same complete valid field mapping.
    Oracle
    Exact supplied values and dataclass equality provide the independent oracle.
    Acceptance
    Every field maps exactly, whitespace is preserved, and equal requests compare
    equal.
    Interpretation
    Failure indicates mapping, normalization, or value-semantic drift.
    Limitations
    Construction does not select an option or authorize checkpoint persistence.
    """
    values = make_valid_request_values()
    request = SUT(**values)
    assert request.checkpoint is values["checkpoint"]
    assert request.expected_unresolved_status == "pending"
    assert request.resolved_status == "resolved"
    assert request.human_response == "  Approve option A.\n"
    assert request.normalized_decision == "A"
    assert request.resolved_at == "2026-08-04T00:01:02Z"
    assert request.authorized_scope == "bounded implementation"
    assert request == SUT(**values)


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    [
        ("checkpoint", object(), TypeError),
        ("expected_unresolved_status", 1, TypeError),
        ("resolved_status", 1, TypeError),
        ("resolved_status", "pending", ValueError),
        ("expected_unresolved_status", "", ValueError),
        ("resolved_status", "bad status", ValueError),
        ("human_response", 1, TypeError),
        ("human_response", "", ValueError),
        ("normalized_decision", 1, TypeError),
        ("normalized_decision", "bad decision", ValueError),
        ("resolved_at", 1, TypeError),
        ("resolved_at", "2026-08-04T00:01:02+00:00", ValueError),
        ("resolved_at", "2026-02-30T00:01:02Z", ValueError),
        ("authorized_scope", 1, TypeError),
        ("authorized_scope", "", ValueError),
    ],
    ids=[
        "wrong_checkpoint_type",
        "wrong_expected_status_type",
        "wrong_resolved_status_type",
        "equal_statuses",
        "empty_status",
        "malformed_status",
        "wrong_human_response_type",
        "empty_human_response",
        "wrong_decision_type",
        "malformed_decision",
        "wrong_timestamp_type",
        "malformed_timestamp",
        "impossible_timestamp",
        "wrong_scope_type",
        "empty_scope",
    ],
)
def test_constructor__invalid_field__raises_semantic_exception(
    field: str, value: Any, exception: type[Exception]
) -> None:
    """Evidence ID
    SV-HARNESS-099
    Requirement
    Wrong semantic types raise TypeError and typed invariant violations ValueError.
    Method
    Replace one valid request field with each required invalid partition.
    Oracle
    The public request invariant table fixes each exception family.
    Acceptance
    Every partition raises the declared exception family.
    Interpretation
    Failure indicates type, identifier, timestamp, or nonempty-contract drift.
    Limitations
    Option membership and checkpoint lifecycle are ActionObject concerns.
    """
    values = make_valid_request_values()
    values[field] = value
    with pytest.raises(exception):
        SUT(**values)


def test_field__frozen_assignment__raises_attribute_error() -> None:
    """Evidence ID
    SV-HARNESS-100
    Requirement
    Request state is immutable after construction.
    Method
    Assign to one public field through a runtime-selected field name.
    Oracle
    Frozen dataclass assignment semantics are the exact oracle.
    Acceptance
    Assignment raises AttributeError and the response remains unchanged.
    Interpretation
    Failure indicates an unauthorized mutable request boundary.
    Limitations
    The nested checkpoint has its own independent immutability contract.
    """
    request = SUT(**make_valid_request_values())
    field = "human_response"
    with pytest.raises(AttributeError):
        setattr(request, field, "rewritten")
    assert request.human_response == "  Approve option A.\n"
