r"""Software verification of ``OperatorRecordCompatibilityResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the value semantics facet. System under test
-----------------
The system under test is immutable value behavior of compatibility audit results.

Evidence class
--------------
This module provides software-verification evidence ``SV-ORCAR-011`` and
``SV-ORCAR-012`` only.

Stored fields
-------------
Exact value state consists of ``reference_identifier``, ``candidate_identifier``,
and the canonical exact tuple ``issues``.

Derived properties
------------------
``rules_applied`` and ``is_compatible`` are read-only derived properties and are
not independent equality state.

Canonical ordering
------------------
All unequal Issue tuples used here remain independently valid and canonically
ordered according to the public enum sequence owned by ``SV-OCMC-001``.

Test strategy, oracle, and acceptance criteria
----------------------------------------------
Tests exercise frozen slotted assignment behavior and independently vary every
stored equality component while preserving valid state. The oracle is the
approved immutable DataObject/ResultObject architecture and exact structural
equality contract. Passing requires mutation rejection and exact value equality.
Failure may indicate a ResultObject regression, contract mismatch, or evidence
defect requiring investigation.

Ownership boundaries
--------------------
Equality compares audit state; it does not execute compatibility rules, establish
mismatch reachability, or determine physical or approximate operator equivalence.

Python/Rust representation boundary
-----------------------------------
Immutable fields and exact structural equality are conceptually portable to a
Rust value struct, but no Rust implementation or conformance is established.

Scientific-validation status
----------------------------
Scientific validation has not been performed. Equality of audit records is not
physical-model validation.

UQ status
---------
Uncertainty quantification has not been performed. Exact equality introduces no
uncertainty model or propagation.

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

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordCompatibilityResult

EQUALITY_FIELDS = ("reference_identifier", "candidate_identifier", "issues")


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


def make_result(
    *,
    reference_identifier: str = "reference",
    candidate_identifier: str = "candidate",
    issues: tuple[OperatorRecordCompatibilityIssue, ...] | None = None,
) -> OperatorRecordCompatibilityResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Value-semantics cases require a valid difference result while
    independently
    selecting its matrix, unit, and compatibility audit.

    Method: Construct or inspect only the named synthetic fixture operation (make
    result); the
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

    canonical_issues = (make_issue(),) if issues is None else issues
    return OperatorRecordCompatibilityResult(
        reference_identifier,
        candidate_identifier,
        canonical_issues,
    )


def test_constructor__enforce_immutable_slotted_state__is_enforced() -> None:
    r"""Evidence ID: SV-ORCAR-011

    Requirement: Stored fields and derived properties cannot be reassigned, undeclared
    attributes
    cannot be added, and no per-instance ``__dict__`` exists.

    Method: Attempt each listed public or dynamic assignment on one valid result.

    Oracle: The approved frozen slotted ResultObject architecture requires exact
    ``FrozenInstanceError`` behavior for ordinary assignment.

    Acceptance: All six assignments raise ``FrozenInstanceError`` and ``__dict__`` is
    absent.

    Interpretation: Passing protects audit evidence after direct or analyzer
    construction.

    Limitations: No private attributes or invariant-bypass techniques are inspected.
    """

    result = make_result()

    with pytest.raises(FrozenInstanceError):
        result.reference_identifier = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.candidate_identifier = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.issues = ()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.rules_applied = ()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.is_compatible = True  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.unexpected = "dynamic state"  # type: ignore[attr-defined]

    assert not hasattr(result, "__dict__")


@pytest.mark.parametrize(
    "difference_case",
    [
        pytest.param("reference-identifier", id="reference_identifier"),
        pytest.param("candidate-identifier", id="candidate_identifier"),
        pytest.param("issue-collection-emptiness", id="issue_collection_emptiness"),
        pytest.param("one-issue-code", id="one_issue_code"),
        pytest.param("issue-count", id="issue_count"),
    ],
)
def test_method__eq__provide_exact_structural_equality(difference_case: str) -> None:
    r"""Evidence ID: SV-ORCAR-012

    Requirement: Independent results are equal exactly when all three stored fields are
    equal; each
    independently varied field makes them unequal.

    Method: Build two equal baseline results and one valid variant selected by the
    meaningful
    parameter ID.

    Oracle: The approved ResultObject equality contract is exact structural dataclass
    equality
    over identifiers and canonically ordered Issue values.

    Acceptance: Baselines are equal; the selected variant and an unrelated object are
    not.

    Interpretation: Passing establishes exact structural audit equality by authoritative
    stored state.

    Limitations: Equality is not free-form text comparison, approximate numerical or
    physical
    equivalence, analyzer correctness, or compatibility proof. Hash behavior is audited
    outside assertions because no hash contract exists.
    """

    same_code_left = make_result()
    same_code_right = make_result()

    if difference_case == "reference-identifier":
        different = make_result(reference_identifier="other-reference")
    elif difference_case == "candidate-identifier":
        different = make_result(candidate_identifier="other-candidate")
    elif difference_case == "issue-collection-emptiness":
        different = make_result(issues=())
    elif difference_case == "one-issue-code":
        different = make_result(
            issues=(
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
                ),
            )
        )
    else:
        different = make_result(
            issues=(
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
                ),
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
                ),
            )
        )

    assert same_code_left == same_code_right
    assert same_code_left != different
    assert same_code_left != object()
