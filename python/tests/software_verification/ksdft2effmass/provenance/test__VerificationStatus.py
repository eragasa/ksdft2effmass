r"""Software verification of ``VerificationStatus``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies the exact ``StrEnum`` vocabulary and its
public value-construction and name-lookup surfaces.

Intrinsic and cross-object scope
--------------------------------
The sole SUT is ``VerificationStatus``. Literal version-1 names and values plus
Python enum semantics provide independent exact oracles; no collaborator is a
co-owner, and no warnings are expected.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated software vocabulary and lookup behavior.
It does not establish tool execution, numerical verification, physical
correctness, scientific validation, UQ, portability, or cross-language agreement.
"""

from enum import StrEnum
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import VerificationStatus

SUT = VerificationStatus
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID
    SV-PROV-036
    Requirement
    The wire vocabulary is an alias-free StrEnum with three ordered members.
    Method
    Inspect public iteration, member mapping, values, type, and counts.
    Oracle
    The accepted sequence pairs each declared name with its lowercase wire value.
    Acceptance
    Type, order, names, values, key order, alias absence, and count match exactly.
    Interpretation
    Failure identifies a vocabulary, enum-type, ordering, alias, or test-oracle defect.
    Limitations
    This does not exercise lookup, serialization, execution, validation, or UQ.
    """
    expected = (
        ("VERIFIED", "verified"),
        ("REJECTED", "rejected"),
        ("UNAVAILABLE", "unavailable"),
    )
    assert SUT.__bases__ == (StrEnum,)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == tuple(name for name, _ in expected)
    assert len(SUT.__members__) == 3
    assert len(tuple(SUT)) == 3


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("verified", SUT.VERIFIED, id="verified_wire_value"),
        pytest.param("rejected", SUT.REJECTED, id="rejected_wire_value"),
        pytest.param("unavailable", SUT.UNAVAILABLE, id="unavailable_wire_value"),
    ],
)
def test_method__call__constructs_member_from_each_wire_value(
    value: str, expected: VerificationStatus
) -> None:
    """Evidence ID
    SV-PROV-179
    Requirement
    Each accepted wire value constructs its canonical enum member.
    Method
    Call the public enum value-construction surface for one named value partition.
    Oracle
    The accepted literal value-to-member mapping fixes the expected identity.
    Acceptance
    Construction returns the exact expected member by identity without warnings.
    Interpretation
    Failure identifies value lookup, vocabulary, parameter, or oracle drift.
    Limitations
    Name lookup, invalid values, tools, scientific validation, and UQ are excluded.
    """
    assert SUT(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("VERIFIED", SUT.VERIFIED, id="verified_member_name"),
        pytest.param("REJECTED", SUT.REJECTED, id="rejected_member_name"),
        pytest.param("UNAVAILABLE", SUT.UNAVAILABLE, id="unavailable_member_name"),
    ],
)
def test_method__getitem__returns_member_for_each_declared_name(
    name: str, expected: VerificationStatus
) -> None:
    """Evidence ID
    SV-PROV-239
    Requirement
    Each declared member name resolves to its canonical enum member.
    Method
    Apply bracketed enum-name lookup to one explicit name partition.
    Oracle
    The accepted literal name-to-member mapping fixes the expected identity.
    Acceptance
    Lookup returns the exact expected member by identity without warnings.
    Interpretation
    Failure identifies name lookup, vocabulary, parameter, or oracle drift.
    Limitations
    Value construction, invalid names, execution, validation, and UQ are excluded.
    """
    assert cast(Any, SUT)[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID
    SV-PROV-180
    Requirement
    Text outside the closed wire vocabulary cannot construct a member.
    Method
    Call value construction with the fixed absent string ``unknown``.
    Oracle
    The accepted three-value vocabulary contains no ``unknown`` value.
    Acceptance
    Construction raises exactly the public ValueError category.
    Interpretation
    Failure identifies accidental vocabulary widening or exception-contract drift.
    Limitations
    Wrong semantic types, name lookup, execution, validation, and UQ are excluded.
    """
    with pytest.raises(ValueError):
        SUT("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID
    SV-PROV-240
    Requirement
    A non-string integer is not an accepted enum wire value.
    Method
    Call value construction with integer one through the deliberate invalid boundary.
    Oracle
    The closed vocabulary contains strings only; Python Enum reports absent values.
    Acceptance
    Construction raises exactly ValueError and returns no member.
    Interpretation
    Failure identifies accidental coercion or enum exception-contract drift.
    Limitations
    This records Enum rejection, not record-constructor TypeError policy.
    """
    with pytest.raises(ValueError):
        SUT(cast(Any, 1))


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID
    SV-PROV-181
    Requirement
    A name outside the declared member-name set cannot resolve a member.
    Method
    Apply bracketed name lookup to the fixed absent name ``UNKNOWN``.
    Oracle
    The accepted name set contains exactly VERIFIED, REJECTED, and UNAVAILABLE.
    Acceptance
    Lookup raises exactly KeyError and returns no member.
    Interpretation
    Failure identifies accidental aliasing, name widening, or exception drift.
    Limitations
    Value construction, case normalization, execution, validation, and UQ are excluded.
    """
    with pytest.raises(KeyError):
        cast(Any, SUT)["UNKNOWN"]
