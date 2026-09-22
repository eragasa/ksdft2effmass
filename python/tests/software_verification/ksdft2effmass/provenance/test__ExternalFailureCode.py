r"""Software verification of ``ExternalFailureCode``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies the closed version-1 operational-failure
vocabulary, ``StrEnum`` inheritance, exact ordered names and values, alias
absence, value construction, name lookup, and rejection behavior.

Intrinsic and cross-object scope

--------------------------------
The sole SUT is ``ExternalFailureCode``. Its six members classify
already-observed failures at an external-operation boundary. Literal version-1
vocabulary and Python enum semantics provide exact oracles; lookup performs no
external operation.

VVUQ and scientific exclusions

------------------------------
These operational codes do not independently classify or establish solver
convergence, numerical error, model inadequacy, scientific invalidity,
uncertainty, external-execution correctness, or provenance truth.
"""

from enum import StrEnum
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import ExternalFailureCode

SUT = ExternalFailureCode
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID: SV-PROV-074

    Requirement: The enum is an alias-free StrEnum with the exact six ordered failure
    codes.

    Method: Inspect inheritance, iteration, the public member mapping, and member
    counts.

    Oracle: The accepted version-1 vocabulary fixes all six literal name/value pairs.

    Acceptance: Inheritance, order, names, values, member keys, alias absence, and count
    are exact.

    Interpretation: Passing establishes the closed ordered external-failure-code
    vocabulary.

    Limitations: This test does not exercise lookup or observe an external failure.
    """
    expected = (
        ("UNAVAILABLE", "unavailable"),
        ("NOT_AUTHORIZED", "not_authorized"),
        ("REJECTED", "rejected"),
        ("INTERRUPTED", "interrupted"),
        ("MALFORMED_RESULT", "malformed_result"),
        ("INTERNAL_ERROR", "internal_error"),
    )
    assert issubclass(SUT, StrEnum)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == tuple(name for name, _ in expected)
    assert len(SUT.__members__) == 6
    assert len(tuple(SUT)) == 6


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(
            "unavailable", ExternalFailureCode.UNAVAILABLE, id="unavailable_code"
        ),
        pytest.param(
            "not_authorized",
            ExternalFailureCode.NOT_AUTHORIZED,
            id="not_authorized_code",
        ),
        pytest.param("rejected", ExternalFailureCode.REJECTED, id="rejected_code"),
        pytest.param(
            "interrupted", ExternalFailureCode.INTERRUPTED, id="interrupted_code"
        ),
        pytest.param(
            "malformed_result",
            ExternalFailureCode.MALFORMED_RESULT,
            id="malformed_result_code",
        ),
        pytest.param(
            "internal_error",
            ExternalFailureCode.INTERNAL_ERROR,
            id="internal_error_code",
        ),
    ],
)
def test_method__call__constructs_each_code_from_wire_value(
    value: str, expected: ExternalFailureCode
) -> None:
    """Evidence ID: SV-PROV-188

    Requirement: Each accepted wire value constructs its corresponding canonical failure
    code.

    Method: Call value construction for each explicit wire-value/member pair.

    Oracle: The expected values are literal public ``ExternalFailureCode`` members.

    Acceptance: Every construction result is the supplied expected member by identity.

    Interpretation: Passing establishes exact value construction for all six operational
    codes.

    Limitations: Construction does not execute an operation or establish failure
    correctness.
    """
    assert SUT(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param(
            "UNAVAILABLE", ExternalFailureCode.UNAVAILABLE, id="unavailable_code"
        ),
        pytest.param(
            "NOT_AUTHORIZED",
            ExternalFailureCode.NOT_AUTHORIZED,
            id="not_authorized_code",
        ),
        pytest.param("REJECTED", ExternalFailureCode.REJECTED, id="rejected_code"),
        pytest.param(
            "INTERRUPTED", ExternalFailureCode.INTERRUPTED, id="interrupted_code"
        ),
        pytest.param(
            "MALFORMED_RESULT",
            ExternalFailureCode.MALFORMED_RESULT,
            id="malformed_result_code",
        ),
        pytest.param(
            "INTERNAL_ERROR",
            ExternalFailureCode.INTERNAL_ERROR,
            id="internal_error_code",
        ),
    ],
)
def test_method__getitem__returns_each_code_from_declared_name(
    name: str, expected: ExternalFailureCode
) -> None:
    """Evidence ID: SV-PROV-286

    Requirement: Each declared name resolves to its corresponding canonical failure
    code.

    Method: Apply public name lookup for each explicit pair. A narrow typing cast
    exposes
    runtime enum subscription to mypy without changing behavior.

    Oracle: The expected values are literal public ``ExternalFailureCode`` members.

    Acceptance: Every lookup result is the supplied expected member by identity.

    Interpretation: Passing establishes exact declared-name lookup for all six
    operational codes.

    Limitations: Lookup does not establish external-execution correctness or provenance
    truth.
    """
    assert cast(Any, SUT)[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID: SV-PROV-189

    Requirement: Unknown text cannot construct a member of the closed code vocabulary.

    Method: Call value construction with the fixed absent string ``unknown``.

    Oracle: The accepted six-value vocabulary contains no ``unknown`` value.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Passing establishes rejection of unknown textual external-failure
    codes.

    Limitations: Wrong semantic types and name lookup are separate evidence owners.
    """
    with pytest.raises(ValueError):
        SUT("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-287

    Requirement: Integer input cannot construct a member of the string-valued code
    vocabulary.

    Method: Call value construction with integer one through the invalid public
    boundary.

    Oracle: Python enum construction finds no integer among the six string wire values.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Passing establishes rejection of the independent wrong-type input
    partition.

    Limitations: This records enum behavior, not record-constructor semantic-type
    policy.
    """
    with pytest.raises(ValueError):
        SUT(cast(Any, 1))


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID: SV-PROV-190

    Requirement: An undeclared member name cannot resolve through bracketed name lookup.

    Method: Apply name lookup to ``UNKNOWN``. A narrow typing cast exposes runtime enum
    subscription to mypy without changing behavior.

    Oracle: The six declared names do not include ``UNKNOWN``.

    Acceptance: Name lookup raises exactly ``KeyError``.

    Interpretation: Passing establishes rejection of names outside the closed code
    declaration.

    Limitations: This does not test value construction or case normalization.
    """
    with pytest.raises(KeyError):
        cast(Any, SUT)["UNKNOWN"]
