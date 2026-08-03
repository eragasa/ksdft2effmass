r"""Construction evidence for ``OperatorRecordCompatibilityResult``.

System under test
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

# This test-side tuple references the public enum order whose exact membership
# and ordering are independently owned by SV-OCMC-001.
CANONICAL_RULES = tuple(OperatorRecordCompatibilityMismatchCode)


def make_issue(
    code: OperatorRecordCompatibilityMismatchCode = (
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
    ),
) -> OperatorRecordCompatibilityIssue:
    """Construct deterministic synthetic compatibility-audit evidence.

    Parameters
    ----------
    code
        Public mismatch code to store. The deterministic default is
        ``OPERATOR_KIND_MISMATCH``.

    Returns
    -------
    OperatorRecordCompatibilityIssue
        A directly constructed synthetic Issue.

    Notes
    -----
    ``code`` is passed unchanged, without coercion or canonicalization, into the
    Issue's sole authoritative stored field. Only omission selects the documented
    deterministic default. This helper performs no analyzer execution and
    establishes neither mismatch reachability nor scientific validity.
    """

    return OperatorRecordCompatibilityIssue(code)


def test_construct_compatible_empty_issue_result() -> None:
    """SV-ORCAR-001: construct exact stored state with no issues.

    Requirement
        The ResultObject stores exactly three declared fields and accepts an
        empty exact tuple as compatible audit state.
    Method
        Construct directly, inspect public values, public dataclass fields, and
        resolved annotations.
    Oracle
        The approved ResultObject contract declares the two string identifiers
        and exact Issue tuple as its only stored fields.
    Acceptance
        Fields and annotations match exactly; identifiers and empty tuple are
        retained; the tuple is built-in and compatibility is true.
    Interpretation
        Passing establishes the compatible direct-construction boundary.
    Limitations
        No compatibility rule executes and no record pair is analyzed.
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
            id="single-issue",
        ),
        pytest.param(
            (
                OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,
                OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
            ),
            id="canonical-multi-issue",
        ),
        pytest.param(CANONICAL_RULES, id="complete-canonical-issues"),
    ],
)
def test_construct_canonical_single_and_multi_issue_results(
    codes: tuple[OperatorRecordCompatibilityMismatchCode, ...],
) -> None:
    """SV-ORCAR-002: admit canonical partial and complete issue sequences.

    Requirement
        One, multiple distinct, and all public mismatch codes are admitted when
        represented by Issues in canonical order.
    Method
        Construct synthetic Issues directly from each parameterized code tuple.
    Oracle
        ``CANONICAL_RULES`` references the public enum order already verified by
        ``SV-OCMC-001``; Result admission is the evidence under test here.
    Acceptance
        Stored Issue code identity and order exactly match the supplied canonical
        sequence, including the complete public tuple.
    Interpretation
        Passing establishes structural admission of canonical Issue sequences.
    Limitations
        It does not establish that an analyzer can produce these sequences from
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
        pytest.param((), id="empty-issues"),
        pytest.param(
            (make_issue(OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH),),
            id="nonempty-issues",
        ),
    ],
)
def test_derive_complete_canonical_rules_applied(
    issues: tuple[OperatorRecordCompatibilityIssue, ...],
) -> None:
    """SV-ORCAR-003: derive the complete rule sequence for every result state.

    Requirement
        ``rules_applied`` always equals the complete public enum tuple and is an
        exact built-in tuple, independently of reported issues.
    Method
        Inspect the derived property on empty and nonempty valid results.
    Oracle
        The approved property contract derives ``CANONICAL_RULES``; enum content
        itself remains independently owned by ``SV-OCMC-001``.
    Acceptance
        Both results expose the same exact built-in canonical tuple.
    Interpretation
        Passing establishes ResultObject derivation of complete rule coverage.
    Limitations
        It does not verify enum membership independently or execute those rules.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", issues)

    assert result.rules_applied == CANONICAL_RULES
    assert type(result.rules_applied) is tuple


@pytest.mark.parametrize(
    "issues",
    [
        pytest.param((), id="empty-compatible"),
        pytest.param((make_issue(),), id="single-issue-incompatible"),
        pytest.param(
            (
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
                ),
                make_issue(
                    OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
                ),
            ),
            id="multiple-issues-incompatible",
        ),
    ],
)
def test_derive_compatibility_only_from_issue_emptiness(
    issues: tuple[OperatorRecordCompatibilityIssue, ...],
) -> None:
    """SV-ORCAR-004: derive compatibility solely from Issue-tuple emptiness.

    Requirement
        Empty issues imply true compatibility and every nonempty tuple implies
        false compatibility.
    Method
        Construct empty, single-Issue, and multi-Issue valid results.
    Oracle
        The approved property equation is ``is_compatible == (issues == ())``.
    Acceptance
        The property is the exact Boolean result of that expression.
    Interpretation
        Passing prevents independently stored contradictory compatibility state.
    Limitations
        Derived software state is not evidence of physical compatibility.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", issues)

    assert result.is_compatible is (issues == ())


def test_prevent_constructor_override_of_derived_properties() -> None:
    """SV-ORCAR-005: reject positional and keyword derived-state overrides.

    Requirement
        Neither ``is_compatible`` nor ``rules_applied`` is constructor state.
    Method
        Attempt a fourth positional argument and each derived-property keyword.
    Oracle
        The approved constructor contains exactly the three stored fields.
    Acceptance
        Every unsupported call raises ``TypeError`` without relying on complete
        interpreter-generated message text.
    Interpretation
        Passing prevents contradictory or caller-selected derived audit state.
    Limitations
        Interpreter diagnostic wording is not made part of the public contract.
    """

    with pytest.raises(TypeError):
        OperatorRecordCompatibilityResult(  # type: ignore[call-arg]
            "reference", "candidate", (), False
        )

    for derived_kwargs in (
        {"is_compatible": False},
        {"rules_applied": CANONICAL_RULES},
    ):
        with pytest.raises(TypeError):
            OperatorRecordCompatibilityResult(
                "reference", "candidate", (), **derived_kwargs
            )


@pytest.mark.parametrize(
    "api_name",
    ["to_json", "from_json", "to_dict", "from_dict", "serialize", "deserialize"],
)
def test_exclude_unsupported_serialization_apis(api_name: str) -> None:
    """SV-ORCAR-013: exclude an independent ResultObject wire-format API.

    Requirement
        No listed object-owned serialization method is approved.
    Method
        Inspect the public class and one valid instance for each API name.
    Oracle
        The approved architecture requires a separate serializer and versioned
        schema for any future compatibility-result wire format.
    Acceptance
        Every listed API is absent from class and instance.
    Interpretation
        Passing preserves explicit serializer ownership.
    Limitations
        This does not specify or test a future compatibility-result schema.
    """

    result = OperatorRecordCompatibilityResult("reference", "candidate", ())

    assert not hasattr(OperatorRecordCompatibilityResult, api_name)
    assert not hasattr(result, api_name)
