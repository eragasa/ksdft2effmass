r"""Software verification of ``OperatorRecordCompatibilityResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the construction facet. System under test
-----------------
The system under test is the immutable compatibility-audit ResultObject.

Evidence class
--------------
This module provides software-verification evidence ``SV-ORCAR-001`` through
``SV-ORCAR-005`` and ``SV-ORCAR-013`` only.

Stored fields
-------------
The ResultObject stores exactly ``reference_identifier``,
``candidate_identifier``, and the exact built-in tuple ``issues``.

Derived properties
------------------
``rules_applied`` is the complete canonical mismatch-code tuple and
``is_compatible`` is true exactly when ``issues == ()``. Neither is constructor
state.

Canonical ordering
------------------
``CANONICAL_RULES`` is a test-side reference to the public enum iteration order
already verified independently by ``SV-OCMC-001``. This module does not
independently verify enum membership, names, values, or order; it verifies that
the ResultObject admits and derives that public sequence.

Test strategy, oracle, and acceptance criteria
----------------------------------------------
Direct public construction covers empty, partial, and complete canonical issue
collections, derived properties, rejection of derived-state overrides, and
serialization exclusions. The oracle is the approved ResultObject source and
Sphinx contract. Passing requires exact stored and derived state without analyzer
execution. Failure may indicate a ResultObject regression, contract/documentation
mismatch, or evidence defect requiring investigation.

Ownership boundaries
--------------------
The ResultObject protects audit-state structure. It does not execute rules or
establish mismatch reachability; those responsibilities belong to
``OperatorRecordCompatibilityAnalyzer``. Exact enum ordering belongs to
``SV-OCMC-001``.

Python/Rust representation boundary
-----------------------------------
The stored fields and derived-state rules are conceptually portable to a Rust
struct, but no Rust implementation or conformance is established.

Scientific-validation status
----------------------------
Scientific validation has not been performed. Passing does not establish
physical compatibility or approximate operator equivalence.

UQ status
---------
Uncertainty quantification has not been performed. This structural audit result
contains no uncertainty model or propagation procedure.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordCompatibilityResult``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from dataclasses import fields
from typing import get_type_hints

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordCompatibilityResult

# This test-side tuple references the public enum order whose exact membership
# and ordering are independently owned by SV-OCMC-001.
CANONICAL_RULES = tuple(OperatorRecordCompatibilityMismatchCode)


def make_issue(
    code: OperatorRecordCompatibilityMismatchCode = (
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
    ),
) -> OperatorRecordCompatibilityIssue:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Compatibility-result cases require a public issue with the requested
    mismatch code
    and canonical record identifiers.

    Method: Construct or inspect only the named synthetic fixture operation (make
    issue); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    return OperatorRecordCompatibilityIssue(code)


def test_constructor__construct_compatible_empty_issue_result__is_enforced() -> None:
    r"""Evidence ID: SV-ORCAR-001

    Requirement: The ResultObject stores exactly three declared fields and accepts an
    empty exact
    tuple as compatible audit state.

    Method: Construct directly, inspect public values, public dataclass fields, and
    resolved
    annotations.

    Oracle: The approved ResultObject contract declares the two string identifiers and
    exact
    Issue tuple as its only stored fields.

    Acceptance: Fields and annotations match exactly; identifiers and empty tuple are
    retained; the
    tuple is built-in and compatibility is true.

    Interpretation: Passing establishes the compatible direct-construction boundary.

    Limitations: No compatibility rule executes and no record pair is analyzed.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", ())

    assert tuple(field.name for field in fields(OperatorRecordCompatibilityResult)) == (
        "reference_identifier",
        "candidate_identifier",
        "issues",
    )
    resolved_annotations = get_type_hints(OperatorRecordCompatibilityResult)
    assert resolved_annotations["reference_identifier"] is str
    assert resolved_annotations["candidate_identifier"] is str
    assert (
        resolved_annotations["issues"] == tuple[OperatorRecordCompatibilityIssue, ...]
    )
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.issues == ()
    assert type(result.issues) is tuple
    assert result.is_compatible is True


@pytest.mark.parametrize(
    "codes",
    [
        pytest.param(
            (OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,),
            id="single_issue",
        ),
        pytest.param(
            (
                OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,
                OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
            ),
            id="canonical_multi_issue",
        ),
        pytest.param(CANONICAL_RULES, id="complete_canonical_issues"),
    ],
)
def test_constructor__construct_canonical_single_and_multi_issue__is_enforced(
    codes: tuple[OperatorRecordCompatibilityMismatchCode, ...],
) -> None:
    r"""Evidence ID: SV-ORCAR-002

    Requirement: One, multiple distinct, and all public mismatch codes are admitted when
    represented
    by Issues in canonical order.

    Method: Construct synthetic Issues directly from each parameterized code tuple.

    Oracle: ``CANONICAL_RULES`` references the public enum order already verified by
    ``the
    owning evidence``; Result admission is the evidence under test here.

    Acceptance: Stored Issue code identity and order exactly match the supplied
    canonical sequence,
    including the complete public tuple.

    Interpretation: Passing establishes structural admission of canonical Issue
    sequences.

    Limitations: It does not establish that an analyzer can produce these sequences from
    independently valid records.
    """

    issues = tuple(make_issue(code) for code in codes)

    result = OperatorRecordCompatibilityResult("reference", "candidate", issues)

    assert type(result.issues) is tuple
    assert tuple(issue.code for issue in result.issues) == codes
    if codes == CANONICAL_RULES:
        assert tuple(issue.code for issue in result.issues) == tuple(
            OperatorRecordCompatibilityMismatchCode
        )


@pytest.mark.parametrize(
    "issues",
    [
        pytest.param((), id="empty_issues"),
        pytest.param(
            (make_issue(OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH),),
            id="nonempty_issues",
        ),
    ],
)
def test_field__represented_state__derive_complete_canonical_rules_applied(
    issues: tuple[OperatorRecordCompatibilityIssue, ...],
) -> None:
    r"""Evidence ID: SV-ORCAR-003

    Requirement: ``rules_applied`` always equals the complete public enum tuple and is
    an exact
    built-in tuple, independently of reported issues.

    Method: Inspect the derived property on empty and nonempty valid results.

    Oracle: The approved property contract derives ``CANONICAL_RULES``; enum content
    itself
    remains independently owned by ``the owning evidence``.

    Acceptance: Both results expose the same exact built-in canonical tuple.

    Interpretation: Passing establishes ResultObject derivation of complete rule
    coverage.

    Limitations: It does not verify enum membership independently or execute those
    rules.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", issues)

    assert result.rules_applied == CANONICAL_RULES
    assert type(result.rules_applied) is tuple


@pytest.mark.parametrize(
    "issues",
    [
        pytest.param((), id="empty_compatible"),
        pytest.param((make_issue(),), id="single_issue_incompatible"),
        pytest.param(
            (
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
                ),
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
                ),
            ),
            id="multiple_issues_incompatible",
        ),
    ],
)
def test_field__represented__derive_compatibility_only_from_issue_emptiness(
    issues: tuple[OperatorRecordCompatibilityIssue, ...],
) -> None:
    r"""Evidence ID: SV-ORCAR-004

    Requirement: Empty issues imply true compatibility and every nonempty tuple implies
    false
    compatibility.

    Method: Construct empty, single-Issue, and multi-Issue valid results.

    Oracle: The approved property equation is ``is_compatible == (issues == ())``.

    Acceptance: The property is the exact Boolean result of that expression.

    Interpretation: Passing prevents independently stored contradictory compatibility
    state.

    Limitations: Derived software state is not evidence of physical compatibility.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", issues)

    assert result.is_compatible is (issues == ())


@pytest.mark.parametrize(
    "derived_kwargs",
    [
        pytest.param({"is_compatible": False}, id="is_compatible_keyword"),
        pytest.param({"rules_applied": CANONICAL_RULES}, id="rules_applied_keyword"),
    ],
)
def test_constructor__derived_property_keywords__are_rejected(
    derived_kwargs: dict[str, object],
) -> None:
    r"""Evidence ID: SV-ORCAR-005

    Requirement: Neither ``is_compatible`` nor ``rules_applied`` is constructor state.

    Method: Attempt a fourth positional argument and each derived-property keyword.

    Oracle: The approved constructor contains exactly the three stored fields.

    Acceptance: Every unsupported call raises ``TypeError`` without relying on complete
    interpreter-generated message text.

    Interpretation: Passing prevents contradictory or caller-selected derived audit
    state.

    Limitations: Interpreter diagnostic wording is not made part of the public contract.
    """
    with pytest.raises(TypeError):
        OperatorRecordCompatibilityResult(
            "reference", "candidate", (), **derived_kwargs
        )


def test_constructor__fourth_positional_derived_state__is_rejected() -> None:
    r"""Evidence ID: SV-ORCAR-014

    Requirement: Derived compatibility state cannot be supplied as a fourth positional
    field.

    Method: Call the public constructor with valid stored fields and one extra Boolean.

    Oracle: The accepted constructor contains exactly three stored fields.

    Acceptance: Exactly ``TypeError`` is raised.

    Interpretation: A pass confirms positional arity; failure indicates
    represented-state drift.

    Limitations: Keyword rejection, physical compatibility, validation, UQ, and Rust are
    excluded.
    """
    with pytest.raises(TypeError):
        OperatorRecordCompatibilityResult("reference", "candidate", (), False)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    "api_name",
    [
        pytest.param("to_json", id="to_json"),
        pytest.param("from_json", id="from_json"),
        pytest.param("to_dict", id="to_dict"),
        pytest.param("from_dict", id="from_dict"),
        pytest.param("serialize", id="serialize"),
        pytest.param("deserialize", id="deserialize"),
    ],
)
def test_method__serialize__exclude_unsupported_serialization_apis(
    api_name: str,
) -> None:
    r"""Evidence ID: SV-ORCAR-013

    Requirement: No listed object-owned serialization method is approved.

    Method: Inspect the public class and one valid instance for each API name.

    Oracle: The approved architecture requires a separate serializer and versioned
    schema for
    any future compatibility-result wire format.

    Acceptance: Every listed API is absent from class and instance.

    Interpretation: Passing preserves explicit serializer ownership.

    Limitations: This does not specify or test a future compatibility-result schema.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", ())

    assert not hasattr(OperatorRecordCompatibilityResult, api_name)
    assert not hasattr(result, api_name)
