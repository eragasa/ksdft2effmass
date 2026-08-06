r"""Software verification of ``CapabilityKind``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies the closed wire vocabulary and the public
``StrEnum`` value- and name-lookup surfaces.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``CapabilityKind``. Fixed version-1 names and values
provide the oracle for synthetic, dimensionless metadata. No warnings are
expected, and no collaborator is a co-owner.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated enum contract; failure indicates a source,
test-oracle, or accepted-contract mismatch. This evidence does not establish
numerical verification, physical correctness, scientific validation, UQ,
portability, or cross-language agreement.
"""

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
    The enum exposes the exact ordered version-1 names and values without aliases.
    Method
    Inspect iteration, the public member mapping, and ``StrEnum`` inheritance.
    Oracle
    The accepted vocabulary is EXECUTE/execute, PARSE/parse, RENDER/render, and
    TRANSFER/transfer in that order.
    Acceptance
    Names, values, order, member keys, member count, and inheritance match exactly.
    Interpretation
    A pass confirms the closed vocabulary; a failure identifies source, oracle, or
    contract drift.
    Limitations
    This does not test lookup errors, external behavior, numerical verification,
    validation, UQ, portability, or cross-language agreement.
    """
    expected = (
        ("EXECUTE", "execute"),
        ("PARSE", "parse"),
        ("RENDER", "render"),
        ("TRANSFER", "transfer"),
    )
    assert issubclass(SUT, StrEnum)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == tuple(name for name, _ in expected)
    assert len(SUT.__members__) == len(tuple(SUT))


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("execute", CapabilityKind.EXECUTE, id="execute_value"),
        pytest.param("parse", CapabilityKind.PARSE, id="parse_value"),
        pytest.param("render", CapabilityKind.RENDER, id="render_value"),
        pytest.param("transfer", CapabilityKind.TRANSFER, id="transfer_value"),
    ],
)
def test_method__call__resolves_each_wire_value(
    value: str, expected: CapabilityKind
) -> None:
    """Evidence ID
    SV-PROV-176
    Requirement
    Calling the enum class with each accepted wire value returns its canonical member.
    Method
    Call the public enum constructor for each explicitly named version-1 value.
    Oracle
    The fixed value-to-member pairs are declared independently in the parameter table.
    Acceptance
    Each call returns the expected member by identity and emits no warning.
    Interpretation
    A pass confirms value lookup; a failure identifies constructor or vocabulary drift.
    Limitations
    This does not test name lookup, external behavior, validation, UQ, portability,
    or cross-language agreement.
    """
    assert SUT(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("EXECUTE", CapabilityKind.EXECUTE, id="execute_name"),
        pytest.param("PARSE", CapabilityKind.PARSE, id="parse_name"),
        pytest.param("RENDER", CapabilityKind.RENDER, id="render_name"),
        pytest.param("TRANSFER", CapabilityKind.TRANSFER, id="transfer_name"),
    ],
)
def test_method__getitem__resolves_each_member_name(
    name: str, expected: CapabilityKind
) -> None:
    """Evidence ID
    SV-PROV-238
    Requirement
    Bracketed enum lookup resolves every accepted member name to its canonical member.
    Method
    Apply the public class subscription surface to each explicit version-1 name.
    Oracle
    The fixed name-to-member pairs are declared independently in the parameter table.
    Acceptance
    Each lookup returns the expected member by identity and emits no warning.
    Interpretation
    A pass confirms name lookup; a failure identifies subscription or name-
    vocabulary drift.
    Limitations
    This new owner does not test value construction, external behavior, validation,
    UQ, portability, or cross-language agreement.
    """
    assert cast(Any, SUT)[name] is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param("unknown", id="unknown_value"),
        pytest.param(1, id="integer_wrong_type"),
    ],
)
def test_method__call__rejects_values_outside_vocabulary(
    invalid_value: object,
) -> None:
    """Evidence ID
    SV-PROV-177
    Requirement
    Calling the enum class with a value outside its vocabulary fails.
    Method
    Call the public constructor with unknown-text and integer partitions.
    Oracle
    Neither value occurs in the accepted four-value vocabulary.
    Acceptance
    Each call raises ``ValueError`` and returns no member.
    Interpretation
    A pass confirms closed value lookup; a failure indicates an unexpectedly
    accepted value.
    Limitations
    This does not characterize every Python type or establish external behavior,
    validation, UQ, portability, or cross-language agreement.
    """
    with pytest.raises(ValueError):
        SUT(cast(Any, invalid_value))


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID
    SV-PROV-178
    Requirement
    Bracketed enum lookup rejects names outside the closed member-name set.
    Method
    Look up the fixed absent name ``UNKNOWN`` through class subscription.
    Oracle
    The accepted member names are exactly EXECUTE, PARSE, RENDER, and TRANSFER.
    Acceptance
    Lookup raises ``KeyError`` and returns no member.
    Interpretation
    A pass confirms closed name lookup; a failure indicates name-vocabulary drift.
    Limitations
    This tests one representative absent name, not external behavior, validation,
    UQ, portability, or cross-language agreement.
    """
    with pytest.raises(KeyError):
        cast(Any, SUT)["UNKNOWN"]
