r"""Software verification for the residual-analysis numerical-error enum.

System under test
-----------------
``OperatorRecordComparisonNumericalErrorCode`` is the closed public numerical-
error enum for residual analysis. Its machine-readable string values and
declaration order are stable parts of the audited contract. Despite the retained
historical ``Comparison`` name, ``OperatorRecordResidualAnalyzer`` owns production
emission of these codes. ``OperatorRecordComparator`` may propagate lower-layer
exceptions as a Workflow but neither calculates residual metrics nor owns this
taxonomy. The enum itself performs no metric calculation or error detection.

Semantic categories
-------------------
``NONFINITE_METRIC`` means a finite represented-difference matrix led to a
residual metric that cannot be represented as a finite binary64 scalar, including
a mathematically finite norm exceeding finite ``float64`` range.
``LINEAR_ALGEBRA_FAILURE`` means spectral-norm computation failed because the SVD
backend raised a linear-algebra failure or returned nonfinite singular values
while computing ``epsilon_2 = sigma_max(Delta H)``.
``METRIC_ORDER_VIOLATION`` means independently computed raw metrics violated
``0 <= epsilon_max <= epsilon_2 <= epsilon_F`` by more than the analyzer-owned
floating-point allowance. Within-allowance differences are canonicalized by the
analyzer and do not produce this error.

Taxonomy and ownership boundaries
---------------------------------
Represented subtraction failure uses
``OperatorRecordDifferenceNumericalErrorCode``; residual-analysis failure uses
``OperatorRecordComparisonNumericalErrorCode``. An enum category does not decide
whether a residual is physically or scientifically acceptable.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-ORCNEC-001``
through ``SV-ORCNEC-006``. An independently written literal tuple is the oracle
for exact names, values, and order. Public ``Enum.__members__``, Python 3.14
``StrEnum`` behavior, documented name/value lookups, and standard Enum exception
classes verify the remaining closed-vocabulary contract. Production error
generation belongs to residual-analyzer software tests. Metric accuracy and
floating-point behavior belong to residual-analyzer numerical-verification
modules.

Interpretation and VVUQ boundaries
----------------------------------
Passing establishes enum vocabulary and lookup behavior only. Failure may
indicate an enum regression, contract/documentation mismatch, or evidence defect
requiring investigation. These tests do not establish production emission,
residual-norm accuracy, roundoff-allowance correctness, backend-independent SVD
reliability, scientific acceptability, scientific validation, uncertainty
quantification, Rust implementation, or Rust conformance. ``StrEnum`` behavior
does not approve a serialized exception format.
"""

import re
from enum import StrEnum

import pytest

from ksdft2effmass.operators import OperatorRecordComparisonNumericalErrorCode

pytestmark = pytest.mark.software_verification


# This immutable literal is independent of production enum iteration so an
# implementation change cannot regenerate its own expected contract.
EXPECTED_MEMBERS = (
    (
        "NONFINITE_METRIC",
        "nonfinite_metric",
    ),
    (
        "LINEAR_ALGEBRA_FAILURE",
        "linear_algebra_failure",
    ),
    (
        "METRIC_ORDER_VIOLATION",
        "metric_order_violation",
    ),
)


def test_exact_closed_member_sequence_and_stable_values() -> None:
    """SV-ORCNEC-001: verify exact names, values, count, and order.

    Evidence ID
        ``SV-ORCNEC-001``.
    Requirement
        Public iteration contains exactly the three approved residual-error
        members with their stable values in declaration order.
    Method
        Compare public enum iteration with the independently written literal
        ``EXPECTED_MEMBERS`` tuple.
    Oracle
        The approved closed enum contract is the literal ordered name/value
        sequence, not a sequence generated from production members.
    Interpretation
        Passing establishes exact count, names, values, order, and absence of
        unapproved additional iterable members.
    Limitations
        This does not inspect source location or establish production emission,
        numerical algorithms, scientific validation, uncertainty quantification,
        or Rust conformance.
    """

    assert (
        tuple(
            (code.name, code.value)
            for code in OperatorRecordComparisonNumericalErrorCode
        )
        == EXPECTED_MEMBERS
    )


def test_public_member_registry_contains_no_aliases() -> None:
    """SV-ORCNEC-002: verify exact declared names and alias absence.

    Evidence ID
        ``SV-ORCNEC-002``.
    Requirement
        The public Enum registry has exactly the three approved declaration-order
        keys, each mapped to its corresponding public member, with no aliases.
    Method
        Inspect documented ``Enum.__members__`` keys, values, and count and
        compare its count with public iteration.
    Oracle
        The approved no-alias contract permits only the three literal public
        names in ``EXPECTED_MEMBERS`` order.
    Interpretation
        Passing distinguishes three declared names, three iterable members, and
        zero hidden aliases.
    Limitations
        No private Enum attributes, production analyzer behavior, numerical
        verification, scientific validation, uncertainty quantification, or Rust
        conformance are tested.
    """

    expected_names = (
        "NONFINITE_METRIC",
        "LINEAR_ALGEBRA_FAILURE",
        "METRIC_ORDER_VIOLATION",
    )
    expected_registry_values = (
        OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC,
        OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE,
        OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION,
    )
    registry = OperatorRecordComparisonNumericalErrorCode.__members__

    assert tuple(registry) == expected_names
    assert tuple(registry.values()) == expected_registry_values
    assert len(registry) == 3
    assert len(tuple(OperatorRecordComparisonNumericalErrorCode)) == 3


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            code,
            id=f"SV-ORCNEC-003-{code.value.replace('_', '-')}",
        )
        for code in tuple(OperatorRecordComparisonNumericalErrorCode)
    ],
)
def test_python_314_strenum_and_machine_readable_value_behavior(
    code: OperatorRecordComparisonNumericalErrorCode,
) -> None:
    """SV-ORCNEC-003: verify ``StrEnum`` and machine-string behavior.

    Evidence ID
        ``SV-ORCNEC-003``; parameter IDs derive from stable code values without
        assigning additional evidence identifiers.
    Requirement
        The enum subclasses Python 3.14 ``StrEnum`` and each member behaves as
        its ASCII lowercase snake-case machine-readable value.
    Method
        Inspect public inheritance, string identity/equality, ``str()``, explicit
        lexical full match, and ASCII encoding for every public member.
    Oracle
        Python 3.14 ``StrEnum`` semantics and the approved machine-value lexical
        convention.
    Interpretation
        Passing establishes deterministic Python string behavior and lexical
        form for all current members.
    Limitations
        No JSON, ``repr()``, hash, pickle, wire format, metric computation,
        scientific validation, uncertainty quantification, or Rust conformance
        is tested.
    """

    assert issubclass(OperatorRecordComparisonNumericalErrorCode, StrEnum)
    assert isinstance(code, str)
    assert code == code.value
    assert str(code) == code.value
    assert re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", code.value) is not None
    code.value.encode("ascii")


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            code,
            id=f"SV-ORCNEC-004-{code.value.replace('_', '-')}",
        )
        for code in tuple(OperatorRecordComparisonNumericalErrorCode)
    ],
)
def test_value_based_lookup_round_trips(
    code: OperatorRecordComparisonNumericalErrorCode,
) -> None:
    """SV-ORCNEC-004: verify lookup by every stable public value.

    Evidence ID
        ``SV-ORCNEC-004``; parameter IDs identify each stable value.
    Requirement
        ``EnumClass(value)`` returns the canonical enum singleton for every
        approved machine-readable value.
    Method
        Construct the enum from each member's public value and compare by
        identity with that member.
    Oracle
        Standard Enum value lookup and the approved stable values.
    Interpretation
        Passing establishes deterministic value-based construction round trips.
    Limitations
        Uppercase, padded, byte, integer, and unrelated-enum coercions are not
        approved as successful behavior. No analyzer execution, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    assert OperatorRecordComparisonNumericalErrorCode(code.value) is code


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            code,
            id=f"SV-ORCNEC-005-{code.value.replace('_', '-')}",
        )
        for code in tuple(OperatorRecordComparisonNumericalErrorCode)
    ],
)
def test_name_based_lookup_round_trips(
    code: OperatorRecordComparisonNumericalErrorCode,
) -> None:
    """SV-ORCNEC-005: verify lookup by every public member name.

    Evidence ID
        ``SV-ORCNEC-005``; parameter IDs identify the corresponding stable code.
    Requirement
        ``EnumClass[name]`` returns the canonical enum singleton for every
        approved public member name.
    Method
        Subscribe by each member's public ``name`` and compare by identity.
    Oracle
        Standard Enum name lookup and the approved public names.
    Interpretation
        Passing establishes deterministic name-based lookup distinct from value-
        based construction.
    Limitations
        Member names are not machine-readable values. No metric calculation,
        production emission, scientific validation, uncertainty quantification,
        or Rust conformance is tested.
    """

    assert OperatorRecordComparisonNumericalErrorCode[code.name] is code


@pytest.mark.parametrize(
    "lookup_kind",
    [
        pytest.param("invalid-value", id="SV-ORCNEC-006-invalid-value"),
        pytest.param("invalid-name", id="SV-ORCNEC-006-invalid-name"),
    ],
)
def test_invalid_lookup_exception_taxonomy(lookup_kind: str) -> None:
    """SV-ORCNEC-006: verify exact standard Enum lookup exceptions.

    Evidence ID
        ``SV-ORCNEC-006``; parameter IDs distinguish value and name lookup.
    Requirement
        An unknown value raises ``ValueError`` and an unknown name raises
        ``KeyError`` through their respective public lookup forms.
    Method
        Exercise one representative invalid ``EnumClass(value)`` construction
        and one invalid ``EnumClass[name]`` subscription.
    Oracle
        Standard Enum taxonomy specifies ``ValueError`` for invalid values and
        ``KeyError`` for invalid names.
    Interpretation
        Passing establishes predictable exact lookup-failure categories.
    Limitations
        Standard-library exception messages are not frozen. No broad exception
        tuple, residual algorithm, differencer, Workflow, scientific validation,
        uncertainty quantification, or Rust conformance is tested.
    """

    if lookup_kind == "invalid-value":
        with pytest.raises(ValueError):
            OperatorRecordComparisonNumericalErrorCode("unknown_residual_error")
    else:
        with pytest.raises(KeyError):
            OperatorRecordComparisonNumericalErrorCode["UNKNOWN_RESIDUAL_ERROR"]
