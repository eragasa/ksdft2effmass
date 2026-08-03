r"""Value-semantics evidence for ``OperatorRecordCompatibilityResult``.

System under test
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
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification


def make_issue(
    code: OperatorRecordCompatibilityMismatchCode = (
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
    ),
) -> OperatorRecordCompatibilityIssue:
    """Construct deterministic synthetic compatibility-audit evidence.

    Parameters
    ----------
    code
        Public enum member passed unchanged into the Issue's sole authoritative
        ``code`` field. Omission selects ``OPERATOR_KIND_MISMATCH``.

    Returns
    -------
    OperatorRecordCompatibilityIssue
        A directly constructed synthetic Issue without helper-side coercion or
        canonicalization.

    Notes
    -----
    This helper performs no analyzer execution and establishes neither mismatch
    reachability nor scientific validity.
    """

    return OperatorRecordCompatibilityIssue(code)


def make_result(
    *,
    reference_identifier: str = "reference",
    candidate_identifier: str = "candidate",
    issues: tuple[OperatorRecordCompatibilityIssue, ...] | None = None,
) -> OperatorRecordCompatibilityResult:
    """Construct one independently valid synthetic audit ResultObject.

    Parameters
    ----------
    reference_identifier
        Deterministic synthetic reference identifier.
    candidate_identifier
        Deterministic synthetic candidate identifier.
    issues
        Canonically ordered Issue tuple. ``None`` selects one deterministic
        ``OPERATOR_KIND_MISMATCH`` Issue; an explicit empty tuple remains empty.

    Returns
    -------
    OperatorRecordCompatibilityResult
        Directly constructed synthetic structural audit state.

    Notes
    -----
    Identifiers and any explicit Issue tuple are passed unchanged to the public
    constructor without coercion, copying policy, or sorting. Only ``issues=None``
    triggers the documented deterministic one-Issue fixture transformation. The
    helper does not invoke an analyzer and supplies no physical or scientific
    evidence.
    """

    canonical_issues = (make_issue(),) if issues is None else issues
    return OperatorRecordCompatibilityResult(
        reference_identifier,
        candidate_identifier,
        canonical_issues,
    )


def test_enforce_immutable_slotted_state() -> None:
    """SV-ORCAR-011: reject mutation of stored, derived, and dynamic state.

    Requirement
        Stored fields and derived properties cannot be reassigned, undeclared
        attributes cannot be added, and no per-instance ``__dict__`` exists.
    Method
        Attempt each listed public or dynamic assignment on one valid result.
    Oracle
        The approved frozen slotted ResultObject architecture requires exact
        ``FrozenInstanceError`` behavior for ordinary assignment.
    Acceptance
        All six assignments raise ``FrozenInstanceError`` and ``__dict__`` is
        absent.
    Interpretation
        Passing protects audit evidence after direct or analyzer construction.
    Limitations
        No private attributes or invariant-bypass techniques are inspected.
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
        "reference-identifier",
        "candidate-identifier",
        "issue-collection-emptiness",
        "one-issue-code",
        "issue-count",
    ],
)
def test_provide_exact_structural_equality(difference_case: str) -> None:
    """SV-ORCAR-012: compare exact stored audit state component by component.

    Requirement
        Independent results are equal exactly when all three stored fields are
        equal; each independently varied field makes them unequal.
    Method
        Build two equal baseline results and one valid variant selected by the
        meaningful parameter ID.
    Oracle
        The approved ResultObject equality contract is exact structural dataclass
        equality over identifiers and canonically ordered Issue values.
    Acceptance
        Baselines are equal; the selected variant and an unrelated object are not.
    Interpretation
        Passing establishes exact structural audit equality by authoritative
        stored state.
    Limitations
        Equality is not free-form text comparison, approximate numerical or
        physical equivalence, analyzer correctness, or compatibility proof. Hash
        behavior is audited outside assertions because no hash contract exists.
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
