r"""Software verification of ``CapabilityKind``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies the exact closed wire vocabulary and Python ``StrEnum`` lookup behavior..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``CapabilityKind``; collaborators only supply public constructor
inputs or expose declared Python value semantics. Oracles are the accepted
field, enum, dataclass, tuple, and exception contracts. Values are synthetic,
dimensionless metadata at ordinary lexical scales; no warnings are expected.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated software contract. Failure indicates a
production, test-input, or accepted-contract mismatch. This evidence does not
establish numerical verification, physical correctness, scientific validation,
uncertainty quantification, portability, or cross-language agreement.
"""

# ruff: noqa: E501

from enum import StrEnum
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import CapabilityKind

SUT = CapabilityKind
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__is_exact_ordered_alias_free_strenum() -> None:
    """Evidence ID
    SV-PROV-030
    Requirement
    The enum has the exact versioned names, values, declaration order, no aliases, and is a StrEnum subclass.
    Method
    Inspect public iteration, ``__members__``, and subclass identity without invoking production reachability.
    Oracle
    The accepted literal name/value sequence is independent version-1 vocabulary.
    Acceptance
    Names, values, order, member keys, member count, and StrEnum inheritance match exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    expected = (
        ("EXECUTE", "execute"),
        ("PARSE", "parse"),
        ("RENDER", "render"),
        ("TRANSFER", "transfer"),
    )
    assert issubclass(SUT, StrEnum)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == (
        "EXECUTE",
        "PARSE",
        "RENDER",
        "TRANSFER",
    )
    assert len(SUT.__members__) == len(tuple(SUT))


@pytest.mark.parametrize(
    ("value", "name"),
    [
        pytest.param("execute", "EXECUTE", id="execute"),
        pytest.param("parse", "PARSE", id="parse"),
        pytest.param("render", "RENDER", id="render"),
        pytest.param("transfer", "TRANSFER", id="transfer"),
    ],
)
def test_protocol__value_and_name_lookup__return_member_identity(
    value: str, name: str
) -> None:
    """Evidence ID
    SV-PROV-176
    Requirement
    Every accepted value and name lookup resolves to the same canonical enum member.
    Method
    Perform public value construction and bracketed name lookup for each explicitly identified vocabulary member.
    Oracle
    Python Enum identity semantics plus the accepted literal mapping determine the member.
    Acceptance
    Both lookup forms are identical to ``SUT.__members__[name]`` for every case.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    expected = SUT.__members__[name]
    assert SUT(value) is expected
    assert cast(Any, SUT)[name] is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param("unknown", id="unknown_value"),
        pytest.param(1, id="integer_wrong_type"),
    ],
)
def test_protocol__invalid_value_lookup__raises_value_error(
    invalid_value: object,
) -> None:
    """Evidence ID
    SV-PROV-177
    Requirement
    Values outside the closed vocabulary cannot construct a member.
    Method
    Call the public enum constructor with semantic unknown-text and wrong-type partitions.
    Oracle
    Python Enum lookup rejects values absent from the accepted literal vocabulary.
    Acceptance
    Each value raises ValueError and no member is returned.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(ValueError):
        SUT(cast(Any, invalid_value))


def test_protocol__invalid_name_lookup__raises_key_error() -> None:
    """Evidence ID
    SV-PROV-178
    Requirement
    Names outside the closed vocabulary cannot resolve a member.
    Method
    Use public bracketed name lookup with a fixed absent name.
    Oracle
    The accepted literal member-name set excludes ``UNKNOWN``.
    Acceptance
    Lookup raises KeyError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(KeyError):
        cast(Any, SUT)["UNKNOWN"]
