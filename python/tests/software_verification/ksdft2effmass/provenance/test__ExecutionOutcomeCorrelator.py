"""Evidence class and represented meaning
Software verification of stateless request/outcome identity correlation.
Owned contract, oracle, and scope
ExecutionOutcomeCorrelator is the SUT; literal request, correlation, and attempt
comparisons are the oracle.
VVUQ and scientific exclusions
Evidence performs no execution and excludes numerical verification, scientific
validation, UQ, provenance truth, and cross-language conformance.
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


def _request() -> ExternalExecutionRequest:
    """Evidence ID
    Supports SV-PROV-054 and SV-PROV-055 and owns no separate identifier.
    Requirement
    Provide one explicit valid request correlation source.
    Method
    Construct a root request with fixed request, correlation, and attempt identities.
    Oracle
    Literal identities are independently visible to assertions.
    Acceptance
    Valid construction succeeds without I/O.
    Interpretation
    Helper failure is setup failure only.
    Limitations
    No authorization or execution occurs.
    """
    return ExternalExecutionRequest(
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "tool",
        "cap",
        "install",
        "auth",
        (),
        (),
        "prov",
    )


def test_method__execute_correlation__covers_result_failure_and_attempt_identity() -> (
    None
):
    """Evidence ID
    SV-PROV-054
    Requirement
    The action correlates both result and failure by exact request, correlation, and
    attempt identities in canonical issue order.
    Method
    Exercise a fully matching result and a failure mismatching all three literal
    identities.
    Oracle
    Direct comparison of visible strings predicts empty or three-item issue tuples.
    Acceptance
    Match derives CORRELATED/result_id; mismatch derives MISMATCH/failure_id with
    request, correlation, attempt issues.
    Interpretation
    Failure indicates correlation logic, order, or outcome identity drift.
    Limitations
    External activity and provenance truth are excluded.
    """
    result = ExternalExecutionResult(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        (),
        "manifest",
        "prov",
    )
    failure = ExternalExecutionFailure(
        "failure-1",
        "other-request",
        "other-corr",
        "other-attempt",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.REJECTED,
        (),
        "prov",
    )
    matched = SUT().execute(_request(), result)
    mismatched = SUT().execute(_request(), failure)
    assert (matched.status, matched.outcome_id, matched.issues) == (
        CorrelationStatus.CORRELATED,
        "result-1",
        (),
    )
    assert (mismatched.status, mismatched.outcome_id, mismatched.issues) == (
        CorrelationStatus.MISMATCH,
        "failure-1",
        (
            CorrelationIssue.REQUEST_ID_MISMATCH,
            CorrelationIssue.CORRELATION_ID_MISMATCH,
            CorrelationIssue.ATTEMPT_ID_MISMATCH,
        ),
    )


def test_method__execute_semantic_types__rejects_unrecognized_records() -> None:
    """Evidence ID
    SV-PROV-055
    Requirement
    The action accepts exactly request and result-or-failure public families.
    Method
    Pass mapping lookalikes at each argument boundary.
    Oracle
    The public signature requires TypeError without coercion.
    Acceptance
    Each wrong semantic input raises TypeError.
    Interpretation
    Failure indicates an unintentionally broadened boundary.
    Limitations
    Subclass behavior is not separately partitioned.
    """
    result = ExternalExecutionResult(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        (),
        "manifest",
        "prov",
    )
    with pytest.raises(TypeError):
        SUT().execute({}, result)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT().execute(_request(), {})  # type: ignore[arg-type]
