r"""Software verification of ``CheckpointDecisionResolutionResult``.

Facet and represented meaning

Software verification of immutable checkpoint-resolution outcomes.

Intrinsic and cross-object scope

The sole primary SUT is ``CheckpointDecisionResolutionResult``. Exact field types,
success/failure value consistency, changed semantics, equality, and immutability are
in scope. Transformation behavior and persistence are excluded.

VVUQ and scientific exclusions

Passing establishes only the result-record software contract, not scientific
validity, uncertainty quantification, human acceptance, or operational completion.
"""

from __future__ import annotations

from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    CheckpointDecisionResolutionResult,
    CheckpointRecord,
    ValidationIssue,
    ValidationResult,
)

pytestmark = pytest.mark.software_verification
SUT = CheckpointDecisionResolutionResult


def make_resolved_checkpoint_for_result() -> CheckpointRecord:
    """Evidence ID: Owns no identifier; supports resolution-result evidence.

    Requirement: Result tests require one independently valid resolved checkpoint.

    Method: Construct a public CheckpointRecord from fixed exact fields.

    Oracle: The public CheckpointRecord contract defines valid support input.

    Acceptance: Return one immutable resolved checkpoint.

    Interpretation: Failure indicates invalid setup rather than result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    return CheckpointRecord(
        1,
        "T1-HC01",
        "T1",
        "episode-T1",
        "resolved",
        "contract",
        "2026-08-04T00:00:00Z",
        "Choose an option.",
        (("A", "Accept.", None),),
        "Approve A.",
        "A",
        "2026-08-04T00:01:02Z",
        "bounded implementation",
        ("tasks/T1.json",),
        "blocked",
    )


def make_pass_checkpoint_validation() -> ValidationResult:
    """Evidence ID: Owns no identifier; supports successful result-state evidence.

    Requirement: Result tests require exact issue-free validation.

    Method: Construct PASS with no findings.

    Oracle: ValidationResult's public contract fixes this state.

    Acceptance: Return one exact successful ValidationResult.

    Interpretation: Failure indicates invalid setup rather than result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    return ValidationResult(1, "PASS", ())


def make_fail_checkpoint_validation() -> ValidationResult:
    """Evidence ID: Owns no identifier; supports failed result-state evidence.

    Requirement: Result tests require one registered checkpoint failure.

    Method: Construct STATUS_CONFLICT and its matching FAIL aggregate.

    Oracle: ValidationResult's public contract fixes issue/status consistency.

    Acceptance: Return one exact failed ValidationResult.

    Interpretation: Failure indicates invalid setup rather than result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    issue = ValidationIssue(
        1,
        "PIH.CHECKPOINT.STATUS_CONFLICT",
        "ERROR",
        "T1-HC01",
        None,
        ("cancelled", "pending", "resolved"),
        "Checkpoint status matches neither explicit request status.",
    )
    return ValidationResult(1, "FAIL", (issue,))


def test_constructor__successful_changed_and_unchanged__map_exact_values() -> None:
    """Evidence ID: SV-HARNESS-101

    Requirement: Successful results represent both a changed transformation and
    idempotent no-op.

    Method: Construct changed and unchanged results with the same exact successful
    inputs.

    Oracle: The accepted result contract and dataclass equality fix represented values.

    Acceptance: Both retain the checkpoint, exact bool values, PASS validation, and
    equal copies.

    Interpretation: Failure indicates successful-state, bool, or equality drift.

    Limitations: Construction does not prove the ActionObject selected the correct
    state.
    """
    checkpoint = make_resolved_checkpoint_for_result()
    validation = make_pass_checkpoint_validation()
    changed = SUT(checkpoint, True, validation)
    unchanged = SUT(checkpoint, False, validation)
    assert changed.checkpoint is checkpoint and changed.changed is True
    assert unchanged.checkpoint is checkpoint and unchanged.changed is False
    assert changed.validation is validation and unchanged.validation is validation
    assert changed == SUT(checkpoint, True, validation)
    assert unchanged == SUT(checkpoint, False, validation)


def test_constructor__failed_result__contains_no_partial_checkpoint() -> None:
    """Evidence ID: SV-HARNESS-102

    Requirement: Failed results contain no checkpoint and report changed=False.

    Method: Construct the exact failure partition from a registered validation issue.

    Oracle: The accepted no-partial-result contract fixes all three fields.

    Acceptance: Construction succeeds only with None, exact False, and FAIL validation.

    Interpretation: Failure indicates partial-result or failure-state drift.

    Limitations: This does not establish which Action input produced the failure.
    """
    validation = make_fail_checkpoint_validation()
    result = SUT(None, False, validation)
    assert result.checkpoint is None
    assert result.changed is False
    assert result.validation is validation


@pytest.mark.parametrize(
    ("checkpoint", "changed", "validation", "exception"),
    [
        (object(), False, make_pass_checkpoint_validation(), TypeError),
        (
            make_resolved_checkpoint_for_result(),
            1,
            make_pass_checkpoint_validation(),
            TypeError,
        ),
        (make_resolved_checkpoint_for_result(), False, object(), TypeError),
        (None, False, make_pass_checkpoint_validation(), ValueError),
        (
            make_resolved_checkpoint_for_result(),
            False,
            make_fail_checkpoint_validation(),
            ValueError,
        ),
        (None, True, make_fail_checkpoint_validation(), ValueError),
    ],
    ids=[
        "wrong_checkpoint_type",
        "nonbool_changed",
        "wrong_validation_type",
        "success_without_checkpoint",
        "failure_with_checkpoint",
        "changed_failure",
    ],
)
def test_constructor__invalid_result_state__raises_semantic_exception(
    checkpoint: Any,
    changed: Any,
    validation: Any,
    exception: type[Exception],
) -> None:
    """Evidence ID: SV-HARNESS-103

    Requirement: Result types and success/failure/changed consistency fail closed.

    Method: Construct each required wrong-type and contradictory-state partition.

    Oracle: The public result invariant table fixes TypeError versus ValueError.

    Acceptance: Every partition raises its declared exception family.

    Interpretation: Failure indicates exact-bool, partial-result, or consistency drift.

    Limitations: Warning-status behavior is outside these exact PASS/FAIL partitions.
    """
    with pytest.raises(exception):
        SUT(checkpoint, changed, validation)


def test_field__frozen_assignment__raises_attribute_error() -> None:
    """Evidence ID: SV-HARNESS-104

    Requirement: Result state is immutable after construction.

    Method: Assign through a runtime-selected public field name.

    Oracle: Frozen dataclass assignment semantics are the exact oracle.

    Acceptance: Assignment raises AttributeError and changed remains True.

    Interpretation: Failure indicates an unauthorized mutable ResultObject boundary.

    Limitations: The nested checkpoint owns its own immutability contract.
    """
    result = SUT(
        make_resolved_checkpoint_for_result(),
        True,
        make_pass_checkpoint_validation(),
    )
    field = "changed"
    with pytest.raises(AttributeError):
        setattr(result, field, False)
    assert result.changed is True
