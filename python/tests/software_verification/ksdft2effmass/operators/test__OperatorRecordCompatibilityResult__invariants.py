r"""Invariant evidence for ``OperatorRecordCompatibilityResult``.

System under test
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
"""

from typing import Any

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification

# This test-side tuple references enum order already verified by SV-OCMC-001.
CANONICAL_RULES = tuple(OperatorRecordCompatibilityMismatchCode)


class IssueTuple(tuple):
    """Synthetic tuple subclass for the exact built-in-type boundary.

    The fixture contains otherwise ordinary synthetic values but must be rejected
    before element validation because the public ``issues`` boundary requires
    ``type(issues) is tuple``.
    """


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
    Construction performs no analyzer execution and establishes neither mismatch
    reachability nor scientific validity.
    """

    return OperatorRecordCompatibilityIssue(code)


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "expected_exception"),
    [
        pytest.param("reference_identifier", "", ValueError, id="reference-empty"),
        pytest.param("reference_identifier", 1, TypeError, id="reference-integer"),
        pytest.param("reference_identifier", None, TypeError, id="reference-none"),
        pytest.param("reference_identifier", True, TypeError, id="reference-boolean"),
        pytest.param("candidate_identifier", "", ValueError, id="candidate-empty"),
        pytest.param("candidate_identifier", 1, TypeError, id="candidate-integer"),
        pytest.param("candidate_identifier", None, TypeError, id="candidate-none"),
        pytest.param("candidate_identifier", True, TypeError, id="candidate-boolean"),
    ],
)
def test_enforce_identifier_invariants(
    field_name: str,
    invalid_value: Any,
    expected_exception: type[Exception],
) -> None:
    """SV-ORCAR-006: enforce each identifier's type and value invariants.

    Requirement
        Each identifier is an independently validated nonempty string; wrong
        semantic types raise ``TypeError`` and empty strings raise ``ValueError``.
    Method
        Change exactly one named identifier per parameterized construction.
    Oracle
        The approved source contract documents field-specific identifier
        diagnostics and the repository type/value exception taxonomy.
    Acceptance
        The exact exception category is raised and its diagnostic names the
        independently invalid reference or candidate identifier.
    Interpretation
        Passing establishes identifier validation without cross-field masking.
    Limitations
        Identifier content has provenance meaning only and is not scientifically
        validated here.
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
        pytest.param(IssueTuple((make_issue(),)), id="tuple-subclass"),
        pytest.param({"not-an-issue"}, id="set-sentinel"),
        pytest.param(frozenset({"not-an-issue"}), id="frozenset-sentinel"),
        pytest.param("not-an-issue-tuple", id="string"),
        pytest.param(b"not-an-issue-tuple", id="bytes"),
        pytest.param(object(), id="arbitrary-object"),
    ],
)
def test_require_exact_builtin_tuple_for_issues(invalid_issues: Any) -> None:
    """SV-ORCAR-007: reject every representative non-exact tuple container.

    Requirement
        ``issues`` requires ``type(issues) is tuple`` before element validation.
    Method
        Supply mutable, iterable, set-like, scalar, subclass, and arbitrary
        containers; set fixtures contain only an unrelated hashable sentinel.
    Oracle
        The approved public boundary rejects rather than canonicalizes every
        non-exact built-in tuple.
    Acceptance
        Each case raises ``TypeError`` with the exact-tuple diagnostic.
    Interpretation
        Passing establishes container-type precedence over element checks.
    Limitations
        No Issue or Result is used as a set member or dictionary key, so this
        evidence creates no implicit hashability contract.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", invalid_issues)

    assert "exact tuple" in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_issue",
    [
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
            id="raw-enum-member",
        ),
        pytest.param("energy_unit_mismatch", id="raw-machine-string"),
        pytest.param(None, id="none"),
        pytest.param(True, id="python-boolean"),
        pytest.param(object(), id="arbitrary-object"),
    ],
)
def test_require_public_compatibility_issue_elements(invalid_issue: Any) -> None:
    """SV-ORCAR-008: reject non-Issue elements inside an exact tuple.

    Requirement
        Every exact-tuple element is an ``OperatorRecordCompatibilityIssue``;
        codes and raw values are not coerced.
    Method
        Place one representative invalid element in an exact built-in tuple.
    Oracle
        The approved element validation raises ``TypeError`` naming the public
        Issue type.
    Acceptance
        Every case raises ``TypeError`` with an Issue-specific diagnostic.
    Interpretation
        Passing establishes the public element boundary after tuple admission.
    Limitations
        This does not exercise analyzer construction of valid Issues.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", (invalid_issue,))

    diagnostic = str(exc_info.value)
    assert "compatibility issues" in diagnostic
    assert "OperatorRecordCompatibilityIssue" in diagnostic


def test_reject_duplicated_mismatch_codes_from_distinct_issues() -> None:
    """SV-ORCAR-009: reject duplicated codes independent of Issue identity.

    Requirement
        No two stored Issues may carry the same mismatch code.
    Method
        Construct two distinct Issue objects containing the same enum member.
    Oracle
        The approved ResultObject invariant defines duplication by code, not
        repeated object identity.
    Acceptance
        Distinct objects share code identity and their tuple raises the documented
        duplicate-code ``ValueError``.
    Interpretation
        Passing establishes authoritative code-level uniqueness.
    Limitations
        The case does not imply that the mismatch is analyzer-reachable.
    """

    code = OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    first = make_issue(code)
    second = make_issue(code)

    assert first is not second
    assert first.code is second.code
    with pytest.raises(ValueError) as exc_info:
        OperatorRecordCompatibilityResult("reference", "candidate", (first, second))

    assert "must not be duplicated" in str(exc_info.value)


def test_reject_noncanonical_issue_ordering() -> None:
    """SV-ORCAR-010: reject distinct valid Issues in reversed rule order.

    Requirement
        Issue codes must preserve their relative canonical enum order.
    Method
        Place ``OPERATOR_KIND_MISMATCH`` before the earlier
        ``STATE_SPACE_KIND_MISMATCH`` and construct through the public boundary.
    Oracle
        ``CANONICAL_RULES`` supplies the already-verified public order; the
        ResultObject's rejection policy is under test.
    Acceptance
        Construction raises the documented canonical-order ``ValueError``.
    Interpretation
        Passing complements positive canonical admission under ``SV-ORCAR-002``.
    Limitations
        No private ordering helper is called and no analyzer rule executes.
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
