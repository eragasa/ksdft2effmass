r"""Software verification of ``ExecutionCorrelationResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This module verifies immutable request/outcome identifiers, canonical issue tuples, and
derived correlation status.

Intrinsic and cross-object scope

--------------------------------
``ExecutionCorrelationResult`` is the sole SUT. Portable identifier grammar, the closed
issue order, declared dataclass fields, and exact Python equality supply the oracles.

VVUQ and scientific exclusions

------------------------------
Passing establishes ResultObject mapping and invariants only. It excludes external
execution, provenance truth, numerical verification, scientific validation, UQ,
portability, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.provenance import (
    CorrelationIssue,
    CorrelationStatus,
    ExecutionCorrelationResult,
)

SUT = ExecutionCorrelationResult
pytestmark = pytest.mark.software_verification


def test_constructor__correlation_fields__maps_exact_values() -> None:
    """Evidence ID: SV-PROV-175

    Requirement: Construction maps request identity, outcome identity, and issue tuple
    exactly.

    Method: Construct a result with distinct identifiers and one canonical issue.

    Oracle: Literal inputs and constructor field order fix represented state.

    Acceptance: All three public fields equal their inputs exactly.

    Interpretation: Failure indicates constructor mapping or represented-state drift.

    Limitations: The constructor does not inspect request or outcome records.
    """
    issues = (CorrelationIssue.REQUEST_ID_MISMATCH,)
    value = SUT("request-1", "outcome-1", issues)
    assert (value.request_id, value.outcome_id, value.issues) == (
        "request-1",
        "outcome-1",
        issues,
    )


@pytest.mark.parametrize(
    ("issues", "status"),
    [
        pytest.param((), CorrelationStatus.CORRELATED, id="no_issues"),
        pytest.param(
            (CorrelationIssue.REQUEST_ID_MISMATCH,),
            CorrelationStatus.MISMATCH,
            id="one_issue",
        ),
    ],
)
def test_property__status__derives_from_issue_emptiness(
    issues: tuple[CorrelationIssue, ...], status: CorrelationStatus
) -> None:
    """Evidence ID: SV-PROV-051

    Requirement: Empty issues derive CORRELATED and every nonempty canonical tuple
    derives MISMATCH.

    Method: Construct empty and singleton issue partitions.

    Oracle: Tuple emptiness independently predicts the exact status member.

    Acceptance: Each case returns the listed enum member.

    Interpretation: Failure indicates incorrect status derivation.

    Limitations: Issue reachability from real records is covered by the correlator.
    """
    assert SUT("request-1", "outcome-1", issues).status is status


def test_field__status_storage__excludes_derived_property() -> None:
    """Evidence ID: SV-PROV-164

    Requirement: Derived status is absent from represented result fields.

    Method: Inspect the public dataclass field inventory.

    Oracle: The public ResultObject contract declares exactly request_id, outcome_id,
    and
    issues.

    Acceptance: Field names equal the literal three-name tuple and exclude status.

    Interpretation: Failure indicates duplicated derived state.

    Limitations: Reflection does not assess hostile runtime mutation.
    """
    assert tuple(field.name for field in fields(SUT)) == (
        "request_id",
        "outcome_id",
        "issues",
    )


@pytest.mark.parametrize(
    "issues",
    [
        pytest.param((CorrelationIssue.REQUEST_ID_MISMATCH,), id="request_singleton"),
        pytest.param(
            (CorrelationIssue.CORRELATION_ID_MISMATCH,), id="correlation_singleton"
        ),
        pytest.param((CorrelationIssue.ATTEMPT_ID_MISMATCH,), id="attempt_singleton"),
        pytest.param(
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
            ),
            id="request_correlation_pair",
        ),
        pytest.param(
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="request_attempt_pair",
        ),
        pytest.param(
            (
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="correlation_attempt_pair",
        ),
        pytest.param(
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            ),
            id="all_issues",
        ),
    ],
)
def test_field__issue_tuple_cases__accepts_canonical_subsets(
    issues: tuple[CorrelationIssue, ...],
) -> None:
    """Evidence ID: SV-PROV-165

    Requirement: Every singleton, ordered two-issue subset, and complete issue tuple is
    representable.

    Method: Construct all seven nonempty canonical subsets with explicit semantic case
    IDs.

    Oracle: The declared request-correlation-attempt enum order fixes each valid tuple.

    Acceptance: The stored issues tuple equals the supplied tuple exactly and status is
    MISMATCH.

    Interpretation: Failure indicates overrestriction, reordering, or storage drift.

    Limitations: The cases are synthetic and do not perform external execution.
    """
    value = SUT("request-1", "outcome-1", issues)
    assert value.issues == issues
    assert value.status is CorrelationStatus.MISMATCH


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("request_id", id="request_identifier"),
        pytest.param("outcome_id", id="outcome_identifier"),
    ],
)
def test_field__identifier_semantic_type__rejects_non_string(field_name: str) -> None:
    """Evidence ID: SV-PROV-166

    Requirement: Both identifiers accept only built-in strings.

    Method: Replace one identifier at a time with bytes.

    Oracle: The public semantic type contract requires TypeError without coercion.

    Acceptance: Each partition raises TypeError.

    Interpretation: Failure indicates weakened identifier typing.

    Limitations: Malformed built-in strings are independently partitioned.
    """
    values: dict[str, object] = {
        "request_id": "request-1",
        "outcome_id": "outcome-1",
        "issues": (),
    }
    values[field_name] = b"identifier"
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field_name", "identifier"),
    [
        pytest.param("request_id", "", id="request_empty_identifier"),
        pytest.param("request_id", "bad id", id="request_embedded_space"),
        pytest.param("request_id", "e\u0301", id="request_non_nfc_identifier"),
        pytest.param("request_id", "\ud800", id="request_unicode_surrogate"),
        pytest.param("request_id", "a" * 129, id="request_overlength_identifier"),
        pytest.param("outcome_id", "", id="outcome_empty_identifier"),
        pytest.param("outcome_id", "bad id", id="outcome_embedded_space"),
        pytest.param("outcome_id", "e\u0301", id="outcome_non_nfc_identifier"),
        pytest.param("outcome_id", "\ud800", id="outcome_unicode_surrogate"),
        pytest.param("outcome_id", "a" * 129, id="outcome_overlength_identifier"),
    ],
)
def test_field__identifier_value__rejects_nonportable_text(
    field_name: str, identifier: str
) -> None:
    """Evidence ID: SV-PROV-167

    Requirement: Both identifiers obey the nonempty portable identifier grammar.

    Method: Partition empty, embedded-space, non-NFC, surrogate, and overlength values
    for
    each field.

    Oracle: The public identifier grammar rejects every literal.

    Acceptance: Each case raises ValueError.

    Interpretation: Failure indicates malformed identifier acceptance.

    Limitations: The declared grammar partitions are sampled, not every possible string.
    """
    values = {"request_id": "request-1", "outcome_id": "outcome-1", "issues": ()}
    values[field_name] = identifier
    with pytest.raises(ValueError):
        SUT(**values)  # type: ignore[arg-type]


def test_field__issues_tuple_type__rejects_list() -> None:
    """Evidence ID: SV-PROV-052

    Requirement: issues must be a built-in tuple rather than a list lookalike.

    Method: Construct with an empty list and valid identifiers.

    Oracle: The public immutable tuple contract requires TypeError.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates coercion or mutable issue storage.

    Limitations: Tuple member typing is independently covered.
    """
    with pytest.raises(TypeError):
        SUT("request-1", "outcome-1", [])  # type: ignore[arg-type]


def test_field__issue_member_type__rejects_string_lookalike() -> None:
    """Evidence ID: SV-PROV-168

    Requirement: Every issue member must be a CorrelationIssue enum value.

    Method: Construct with a tuple containing the matching raw string.

    Oracle: The public enum semantic type boundary requires TypeError without coercion.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates raw-string issue coercion.

    Limitations: Future enum expansion is outside P2.
    """
    with pytest.raises(TypeError):
        SUT("request-1", "outcome-1", ("request_id_mismatch",))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "issues",
    [
        pytest.param(
            (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.REQUEST_ID_MISMATCH,
            ),
            id="duplicate_request_issue",
        ),
        pytest.param(
            (
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
                CorrelationIssue.REQUEST_ID_MISMATCH,
            ),
            id="reverse_order",
        ),
    ],
)
def test_field__issue_canonicalization__rejects_duplicates_and_wrong_order(
    issues: tuple[CorrelationIssue, ...],
) -> None:
    """Evidence ID: SV-PROV-169

    Requirement: Issues are unique and ordered request, correlation, then attempt.

    Method: Partition a duplicate tuple and a reverse-order tuple.

    Oracle: The closed enum declaration order and set semantics reject both states.

    Acceptance: Each case raises ValueError.

    Interpretation: Failure indicates noncanonical retained correlation evidence.

    Limitations: Only the version-1 issue vocabulary is covered.
    """
    with pytest.raises(ValueError):
        SUT("request-1", "outcome-1", issues)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-170

    Requirement: Correlation results are operationally immutable through ordinary
    assignment.

    Method: Assign another valid outcome identifier after construction.

    Oracle: The public frozen ResultObject contract requires FrozenInstanceError.

    Acceptance: Reassignment raises FrozenInstanceError.

    Interpretation: Failure indicates mutable durable result state.

    Limitations: Hostile reflection is excluded.
    """
    value = SUT("request-1", "outcome-1", ())
    with pytest.raises(FrozenInstanceError):
        value.outcome_id = "outcome-2"  # type: ignore[misc]


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID: SV-PROV-171

    Requirement: Equality compares request ID, outcome ID, and issues exactly.

    Method: Compare equal constructions and three variants, each changing exactly one
    field.

    Oracle: Each independent literal field difference and dataclass value semantics
    predict
    inequality.

    Acceptance: Equal state compares equal and every single-field variant compares
    unequal.

    Interpretation: Failure indicates incomplete or nonexact value semantics.

    Limitations: Equality does not prove provenance truth or actual execution
    correlation.
    """
    baseline = SUT("request-1", "outcome-1", ())
    assert baseline == SUT("request-1", "outcome-1", ())
    assert baseline != SUT("request-2", "outcome-1", ())
    assert baseline != SUT("request-1", "outcome-2", ())
    assert baseline != SUT(
        "request-1", "outcome-1", (CorrelationIssue.REQUEST_ID_MISMATCH,)
    )
