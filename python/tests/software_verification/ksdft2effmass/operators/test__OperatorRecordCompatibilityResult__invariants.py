r"""Software verification of ``OperatorRecordCompatibilityResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the invariants facet. System under test
-----------------
The system under test is direct construction of compatibility-audit ResultObject
state at its public validation boundary.

Evidence class
--------------
This module provides software-verification evidence ``SV-ORCAR-006`` through
``SV-ORCAR-010`` only.

Stored fields
-------------
The validated stored fields are two nonempty string identifiers and ``issues`` as
an exact built-in tuple of public ``OperatorRecordCompatibilityIssue`` values.

Derived properties
------------------
``rules_applied`` and ``is_compatible`` are derived and are not validated as
independently supplied fields in this module.

Canonical ordering
------------------
``CANONICAL_RULES`` is a test-side reference to public enum iteration whose exact
content is owned by ``SV-OCMC-001``. Issue tuples must contain unique codes in the
relative order defined by that sequence.

Test strategy, oracle, and acceptance criteria
----------------------------------------------
Independent invalid families exercise identifier taxonomy, exact container type,
public element type, duplicate-code rejection, and ordering rejection. The oracle
is the approved public source/Sphinx invariant contract. Passing requires exact
exception categories and diagnostics without private-helper calls. Failure may
indicate a validation regression, contract mismatch, or evidence defect.

Ownership boundaries
--------------------
These checks protect direct ResultObject structure. Analyzer rule execution and
mismatch reachability are excluded. Positive canonical admission is owned by
``SV-ORCAR-002``.

Python/Rust representation boundary
-----------------------------------
The explicit tuple, element, uniqueness, and ordering invariants are conceptually
portable to validated Rust construction, but Rust conformance is not tested.

Scientific-validation status
----------------------------
Scientific validation has not been performed. These constructor failures do not
establish physical incompatibility.

UQ status
---------
Uncertainty quantification has not been performed; no uncertainty is represented
or propagated by these structural invariants.

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

from typing import Any

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordCompatibilityResult

# This test-side tuple references enum order already verified by SV-OCMC-001.
CANONICAL_RULES = tuple(OperatorRecordCompatibilityMismatchCode)


class IssueTuple(tuple):
    r"""Synthetic tuple subclass for the exact built-in-type boundary.

    The fixture contains otherwise ordinary synthetic values but must be rejected
    before element validation because the public ``issues`` boundary requires
    ``type(issues) is tuple``.
    """


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


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "expected_exception"),
    [
        pytest.param("reference_identifier", "", ValueError, id="reference_empty"),
        pytest.param("reference_identifier", 1, TypeError, id="reference_integer"),
        pytest.param("reference_identifier", None, TypeError, id="reference_none"),
        pytest.param("reference_identifier", True, TypeError, id="reference_boolean"),
        pytest.param("candidate_identifier", "", ValueError, id="candidate_empty"),
        pytest.param("candidate_identifier", 1, TypeError, id="candidate_integer"),
        pytest.param("candidate_identifier", None, TypeError, id="candidate_none"),
        pytest.param("candidate_identifier", True, TypeError, id="candidate_boolean"),
    ],
)
def test_constructor__enforce_identifier_invariants__is_enforced(
    field_name: str,
    invalid_value: Any,
    expected_exception: type[Exception],
) -> None:
    r"""Evidence ID: SV-ORCAR-006

    Requirement: Each identifier is an independently validated nonempty string; wrong
    semantic types
    raise ``TypeError`` and empty strings raise ``ValueError``.

    Method: Change exactly one named identifier per parameterized construction.

    Oracle: The approved source contract documents field-specific identifier diagnostics
    and the
    repository type/value exception taxonomy.

    Acceptance: The exact exception category is raised and its diagnostic names the
    independently
    invalid reference or candidate identifier.

    Interpretation: Passing establishes identifier validation without cross-field
    masking.

    Limitations: Identifier content has provenance meaning only and is not
    scientifically validated
    here.
    """

    kwargs: dict[str, Any] = {
        "reference_identifier": "reference",
        "candidate_identifier": "candidate",
        "issues": (),
    }
    kwargs[field_name] = invalid_value

    with pytest.raises(expected_exception) as exc_info:
        OperatorRecordCompatibilityResult(**kwargs)

    expected_field = (
        "reference identifier"
        if field_name.startswith("reference")
        else "candidate identifier"
    )
    assert expected_field in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_issues",
    [
        pytest.param([make_issue()], id="list"),
        pytest.param((issue for issue in (make_issue(),)), id="generator"),
        pytest.param(IssueTuple((make_issue(),)), id="tuple_subclass"),
        pytest.param({"not-an-issue"}, id="set_sentinel"),
        pytest.param(frozenset({"not-an-issue"}), id="frozenset_sentinel"),
        pytest.param("not-an-issue-tuple", id="string"),
        pytest.param(b"not-an-issue-tuple", id="bytes"),
        pytest.param(object(), id="arbitrary_object"),
    ],
)
def test_method__require__require_exact_builtin_tuple_for_issues(
    invalid_issues: Any,
) -> None:
    r"""Evidence ID: SV-ORCAR-007

    Requirement: ``issues`` requires ``type(issues) is tuple`` before element
    validation.

    Method: Supply mutable, iterable, set-like, scalar, subclass, and arbitrary
    containers; set
    fixtures contain only an unrelated hashable sentinel.

    Oracle: The approved public boundary rejects rather than canonicalizes every
    non-exact
    built-in tuple.

    Acceptance: Each case raises ``TypeError`` with the exact-tuple diagnostic.

    Interpretation: Passing establishes container-type precedence over element checks.

    Limitations: No Issue or Result is used as a set member or dictionary key, so this
    evidence
    creates no implicit hashability contract.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", invalid_issues)

    assert "exact tuple" in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_issue",
    [
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
            id="raw_enum_member",
        ),
        pytest.param("energy_unit_mismatch", id="raw_machine_string"),
        pytest.param(None, id="none"),
        pytest.param(True, id="python_boolean"),
        pytest.param(object(), id="arbitrary_object"),
    ],
)
def test_method__require__require_public_compatibility_issue_elements(
    invalid_issue: Any,
) -> None:
    r"""Evidence ID: SV-ORCAR-008

    Requirement: Every exact-tuple element is an ``OperatorRecordCompatibilityIssue``;
    codes and raw
    values are not coerced.

    Method: Place one representative invalid element in an exact built-in tuple.

    Oracle: The approved element validation raises ``TypeError`` naming the public Issue
    type.

    Acceptance: Every case raises ``TypeError`` with an Issue-specific diagnostic.

    Interpretation: Passing establishes the public element boundary after tuple
    admission.

    Limitations: This does not exercise analyzer construction of valid Issues.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", (invalid_issue,))

    diagnostic = str(exc_info.value)
    assert "compatibility issues" in diagnostic
    assert "OperatorRecordCompatibilityIssue" in diagnostic


def test_field__reject_duplicated_mismatch_codes_from_distinct__is_exact() -> None:
    r"""Evidence ID: SV-ORCAR-009

    Requirement: No two stored Issues may carry the same mismatch code.

    Method: Construct two distinct Issue objects containing the same enum member.

    Oracle: The approved ResultObject invariant defines duplication by code, not
    repeated object
    identity.

    Acceptance: Distinct objects share code identity and their tuple raises the
    documented
    duplicate-code ``ValueError``.

    Interpretation: Passing establishes authoritative code-level uniqueness.

    Limitations: The case does not imply that the mismatch is analyzer-reachable.
    """

    code = OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    first = make_issue(code)
    second = make_issue(code)

    assert first is not second
    assert first.code is second.code
    with pytest.raises(ValueError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", (first, second))

    assert "must not be duplicated" in str(exc_info.value)


def test_field__reject_noncanonical_issue_ordering__is_exact() -> None:
    r"""Evidence ID: SV-ORCAR-010

    Requirement: Issue codes must preserve their relative canonical enum order.

    Method: Place ``OPERATOR_KIND_MISMATCH`` before the earlier
    ``STATE_SPACE_KIND_MISMATCH``
    and construct through the public boundary.

    Oracle: ``CANONICAL_RULES`` supplies the already-verified public order; the
    ResultObject's
    rejection policy is under test.

    Acceptance: Construction raises the documented canonical-order ``ValueError``.

    Interpretation: Passing complements positive canonical admission under ``the owning
    evidence``.

    Limitations: No private ordering helper is called and no analyzer rule executes.
    """

    assert CANONICAL_RULES.index(
        OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
    ) < CANONICAL_RULES.index(
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
    )
    reversed_issues = (
        make_issue(OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH),
        make_issue(OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH),
    )

    with pytest.raises(ValueError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", reversed_issues)

    assert "canonical mismatch-code order" in str(exc_info.value)
