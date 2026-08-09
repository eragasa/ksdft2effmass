r"""Software verification of ``ExecutionOutcomeCorrelator``.

Facet and represented meaning

-----------------------------
This module verifies stateless exact comparison of request, correlation, and attempt
identities for both successful-result and structured-failure outcome families.

Intrinsic and cross-object scope

--------------------------------
``ExecutionOutcomeCorrelator`` is the sole SUT. Public request and outcome records are
collaborators; direct comparison of independently selected literal IDs supplies the
oracle and canonical issue order.

VVUQ and scientific exclusions

------------------------------
Passing establishes correlation logic and result mapping only. It excludes external
execution, authorization validity, provenance truth, numerical verification, scientific
validation, UQ, portability, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import (
    CorrelationIssue,
    CorrelationStatus,
    ExecutionOutcomeCorrelator,
    ExternalExecutionFailure,
    ExternalExecutionRequest,
    ExternalExecutionResult,
    ExternalExecutionStatus,
    ExternalFailureCode,
    ExternalFailureStage,
)

SUT = ExecutionOutcomeCorrelator
pytestmark = pytest.mark.software_verification


def make_execution_request() -> ExternalExecutionRequest:
    """Evidence ID: Owns no identifier; supports SV-PROV-054, SV-PROV-055, SV-PROV-172,
    and SV-PROV-173.

    Requirement: Provide one explicit immutable request with independently visible
    correlation IDs.

    Method: Construct the public request record with request-1, correlation-1, and
    attempt-1.

    Oracle: Literal constructor inputs fix the three source identities and other valid
    fields.

    Acceptance: A valid request is returned without authorization lookup or execution.

    Interpretation: Failure is collaborator setup failure rather than correlator
    evidence.

    Limitations: The request is synthetic and does not authorize external activity.
    """
    return ExternalExecutionRequest(
        "request-1",
        "correlation-1",
        "attempt-1",
        None,
        "tool-1",
        "capability-1",
        "installation-1",
        "authorization-1",
        (),
        (),
        "provenance-1",
    )


@pytest.mark.parametrize(
    ("request_matches", "correlation_matches", "attempt_matches", "expected_issues"),
    [
        pytest.param(True, True, True, (), id="all_match"),
        pytest.param(
            False,
            True,
            True,
            (CorrelationIssue.REQUEST_ID_MISMATCH,),
            id="request_only_mismatch",
        ),
        pytest.param(
            True,
            False,
            True,
            (CorrelationIssue.CORRELATION_ID_MISMATCH,),
            id="correlation_only_mismatch",
        ),
        pytest.param(
            True,
            True,
            False,
            (CorrelationIssue.ATTEMPT_ID_MISMATCH,),
            id="attempt_only_mismatch",
        ),
        pytest.param(
            False,
            False,
            True,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
            ),
            id="request_correlation_mismatch",
        ),
        pytest.param(
            False,
            True,
            False,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="request_attempt_mismatch",
        ),
        pytest.param(
            True,
            False,
            False,
            (
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="correlation_attempt_mismatch",
        ),
        pytest.param(
            False,
            False,
            False,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="all_mismatch",
        ),
    ],
)
def test_method__execute_result_identity_combinations__returns_exact_correlation(
    request_matches: bool,
    correlation_matches: bool,
    attempt_matches: bool,
    expected_issues: tuple[CorrelationIssue, ...],
) -> None:
    """Evidence ID: SV-PROV-054

    Requirement: Result outcomes report exactly the mismatching subset of three
    identities in
    canonical order.

    Method: Exercise all eight match/mismatch combinations with the required semantic
    case IDs.

    Oracle: Independent literal equality predicts issue membership; tuple emptiness
    predicts
    status.

    Acceptance: Issues, status, copied request ID, and result outcome ID each equal
    their exact
    expected values.

    Interpretation: Failure indicates comparison, all-issues-on-any-mismatch, ordering,
    status, or
    mapping defects.

    Limitations: Result content and external execution are not validated.
    """
    outcome = ExternalExecutionResult(
        "result-1",
        "request-1" if request_matches else "other-request",
        "correlation-1" if correlation_matches else "other-correlation",
        "attempt-1" if attempt_matches else "other-attempt",
        ExternalExecutionStatus.COMPLETED,
        (),
        "manifest-1",
        "provenance-1",
    )
    result = SUT().execute(make_execution_request(), outcome)
    expected_status = (
        CorrelationStatus.CORRELATED
        if not expected_issues
        else CorrelationStatus.MISMATCH
    )
    assert result.issues == expected_issues
    assert result.status is expected_status
    assert result.request_id == "request-1"
    assert result.outcome_id == "result-1"


@pytest.mark.parametrize(
    ("request_matches", "correlation_matches", "attempt_matches", "expected_issues"),
    [
        pytest.param(True, True, True, (), id="all_match"),
        pytest.param(
            False,
            True,
            True,
            (CorrelationIssue.REQUEST_ID_MISMATCH,),
            id="request_only_mismatch",
        ),
        pytest.param(
            True,
            False,
            True,
            (CorrelationIssue.CORRELATION_ID_MISMATCH,),
            id="correlation_only_mismatch",
        ),
        pytest.param(
            True,
            True,
            False,
            (CorrelationIssue.ATTEMPT_ID_MISMATCH,),
            id="attempt_only_mismatch",
        ),
        pytest.param(
            False,
            False,
            True,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
            ),
            id="request_correlation_mismatch",
        ),
        pytest.param(
            False,
            True,
            False,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="request_attempt_mismatch",
        ),
        pytest.param(
            True,
            False,
            False,
            (
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="correlation_attempt_mismatch",
        ),
        pytest.param(
            False,
            False,
            False,
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="all_mismatch",
        ),
    ],
)
def test_method__execute_failure_identity_combinations__returns_exact_correlation(
    request_matches: bool,
    correlation_matches: bool,
    attempt_matches: bool,
    expected_issues: tuple[CorrelationIssue, ...],
) -> None:
    """Evidence ID: SV-PROV-172

    Requirement: Failure outcomes report exactly the mismatching subset of three
    identities in
    canonical order.

    Method: Exercise all eight match/mismatch combinations with the required semantic
    case IDs.

    Oracle: Independent literal equality predicts issue membership; tuple emptiness
    predicts
    status.

    Acceptance: Issues, status, copied request ID, and failure outcome ID each equal
    their exact
    expected values.

    Interpretation: Failure indicates comparison, all-issues-on-any-mismatch, ordering,
    status, or
    mapping defects.

    Limitations: Failure cause, diagnostics, and external execution are not validated.
    """
    outcome = ExternalExecutionFailure(
        "failure-1",
        "request-1" if request_matches else "other-request",
        "correlation-1" if correlation_matches else "other-correlation",
        "attempt-1" if attempt_matches else "other-attempt",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.REJECTED,
        (),
        "provenance-1",
    )
    result = SUT().execute(make_execution_request(), outcome)
    expected_status = (
        CorrelationStatus.CORRELATED
        if not expected_issues
        else CorrelationStatus.MISMATCH
    )
    assert result.issues == expected_issues
    assert result.status is expected_status
    assert result.request_id == "request-1"
    assert result.outcome_id == "failure-1"


def test_method__execute_request_type__rejects_mapping_lookalike() -> None:
    """Evidence ID: SV-PROV-055

    Requirement: request must be an ExternalExecutionRequest rather than a mapping
    lookalike.

    Method: Pass an empty mapping with a valid successful result.

    Oracle: The public signature requires TypeError without coercion.

    Acceptance: execute raises TypeError.

    Interpretation: Failure indicates an unintentionally broadened request boundary.

    Limitations: Subclass behavior is not separately partitioned.
    """
    outcome = ExternalExecutionResult(
        "result-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        (),
        "manifest-1",
        "provenance-1",
    )
    with pytest.raises(TypeError):
        SUT().execute({}, outcome)  # type: ignore[arg-type]


def test_method__execute_outcome_type__rejects_mapping_lookalike() -> None:
    """Evidence ID: SV-PROV-173

    Requirement: outcome must be an ExternalExecutionResult or ExternalExecutionFailure.

    Method: Pass an empty mapping with a valid request.

    Oracle: The public outcome union requires TypeError without coercion.

    Acceptance: execute raises TypeError.

    Interpretation: Failure indicates an unintentionally broadened outcome boundary.

    Limitations: Accepted-family subclasses are not separately partitioned.
    """
    with pytest.raises(TypeError):
        SUT().execute(make_execution_request(), {})  # type: ignore[arg-type]
