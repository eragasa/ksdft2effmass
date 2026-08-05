"""Evidence class and represented meaning
Software verification of immutable request/outcome correlation results.
Owned contract, oracle, and scope
ExecutionCorrelationResult is the SUT; canonical issue ordering and derived status are
the oracle.
VVUQ and scientific exclusions
Evidence excludes execution, numerical verification, scientific validation, UQ, physical
correctness, and cross-language conformance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.provenance import (
    CorrelationIssue,
    CorrelationStatus,
    ExecutionCorrelationResult,
)

SUT = ExecutionCorrelationResult
pytestmark = pytest.mark.software_verification


def test_constructor__correlation_fields__derive_status_from_issues() -> None:
    """Evidence ID
    SV-PROV-051
    Requirement
    Empty issues derive CORRELATED and canonical nonempty issues derive MISMATCH without
    stored status.
    Method
    Construct empty and complete three-issue public results and inspect
    fields/properties.
    Oracle
    Issue emptiness independently determines the derived status.
    Acceptance
    Statuses are exact, outcome identity maps unchanged, and status is absent from
    dataclass fields.
    Interpretation
    Failure indicates mapping or derived-status drift.
    Limitations
    This constructor does not inspect actual request/outcome records.
    """
    correlated = SUT("request-1", "result-1", ())
    mismatch = SUT(
        "request-1",
        "failure-1",
        (
            CorrelationIssue.REQUEST_ID_MISMATCH,
            CorrelationIssue.CORRELATION_ID_MISMATCH,
            CorrelationIssue.ATTEMPT_ID_MISMATCH,
        ),
    )
    assert correlated.status is CorrelationStatus.CORRELATED
    assert mismatch.status is CorrelationStatus.MISMATCH
    assert mismatch.outcome_id == "failure-1"
    assert "status" not in {field.name for field in fields(SUT)}


def test_constructor__issue_order_and_uniqueness__rejects_noncanonical_states() -> None:
    """Evidence ID
    SV-PROV-052
    Requirement
    Issues are exact enums in request, correlation, attempt order without duplicates.
    Method
    Pass a list, string issue, reverse order, and duplicate issue.
    Oracle
    The public three-member issue order fixes the canonical partition.
    Acceptance
    Wrong semantic types raise TypeError and ordering/duplication raise ValueError.
    Interpretation
    Failure indicates noncanonical correlation evidence.
    Limitations
    Only version-1 issue kinds are covered.
    """
    with pytest.raises(TypeError):
        SUT("r", "o", [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("r", "o", ("request_id_mismatch",))  # type: ignore[arg-type]
    for issues in (
        (CorrelationIssue.ATTEMPT_ID_MISMATCH, CorrelationIssue.REQUEST_ID_MISMATCH),
        (CorrelationIssue.REQUEST_ID_MISMATCH, CorrelationIssue.REQUEST_ID_MISMATCH),
    ):
        with pytest.raises(ValueError):
            SUT("r", "o", issues)


def test_field__correlation_enum_values__match_closed_taxonomy() -> None:
    """Evidence ID
    SV-PROV-053
    Requirement
    Status and issue vocabularies include exact request, correlation, and attempt
    semantics.
    Method
    Enumerate both public enum types.
    Oracle
    The corrected version-1 taxonomy fixes exact ordered values.
    Acceptance
    Both value tuples match exactly.
    Interpretation
    Failure indicates Python or wire vocabulary drift.
    Limitations
    Enumeration does not prove a real outcome correlation.
    """
    assert tuple(item.value for item in CorrelationStatus) == ("correlated", "mismatch")
    assert tuple(item.value for item in CorrelationIssue) == (
        "request_id_mismatch",
        "correlation_id_mismatch",
        "attempt_id_mismatch",
    )
