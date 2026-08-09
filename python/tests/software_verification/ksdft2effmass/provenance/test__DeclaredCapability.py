r"""Software verification of ``DeclaredCapability``.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies capability construction, strict enum typing,
identifier invariants, immutability, complete equality, and durable state.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``DeclaredCapability``; ``CapabilityKind`` is a typed
constructor collaborator. Accepted field contracts provide exact oracles for
synthetic, dimensionless metadata at identifier lengths 0 through 129.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated declaration contract; failure indicates a
source, test-oracle, or accepted-contract mismatch. This evidence does not
invoke capabilities, establish numerical verification, validate science,
quantify uncertainty, or prove portability or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import CapabilityKind, DeclaredCapability

SUT = DeclaredCapability
pytestmark = pytest.mark.software_verification

VALID_VALUES: dict[str, Any] = {
    "capability_id": "cap-1",
    "tool_id": "qe",
    "kind": CapabilityKind.EXECUTE,
    "name": "run-pw",
    "specification_version": "v1",
}
TEXT_FIELDS = ("capability_id", "tool_id", "name", "specification_version")


def test_constructor__field_mapping__stores_exact_declaration() -> None:
    """Evidence ID: SV-PROV-028

    Requirement: Construction stores five exact fields, including the semantic enum
    member.

    Method: Construct fixed valid metadata and inspect public dataclass state.

    Oracle: The accepted signature and literals define exact field order, values, and
    types.

    Acceptance: Names, the complete stored tuple, string types, and enum identity match
    exactly.

    Interpretation: A pass confirms constructor mapping; a failure indicates source,
    input, or
    contract drift.

    Limitations: Synthetic metadata only; no invocation, validation, UQ, portability, or
    cross-
    language claim is made.
    """
    record = SUT(**VALID_VALUES)
    assert tuple(field.name for field in fields(record)) == (
        "capability_id",
        "tool_id",
        "kind",
        "name",
        "specification_version",
    )
    assert astuple(record) == (
        "cap-1",
        "qe",
        CapabilityKind.EXECUTE,
        "run-pw",
        "v1",
    )
    assert all(type(getattr(record, name)) is str for name in TEXT_FIELDS)
    assert record.kind is CapabilityKind.EXECUTE


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("capability_id", id="capability_id"),
        pytest.param("tool_id", id="tool_id"),
        pytest.param("name", id="capability_name"),
        pytest.param("specification_version", id="specification_version"),
    ],
)
def test_constructor__text_semantic_type__rejects_non_string(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-029

    Requirement: Each capability text field requires an exact built-in string.

    Method: Replace the named valid field with bytes while retaining all other fields.

    Oracle: The public type contract excludes bytes from every textual field.

    Acceptance: Every field partition raises ``TypeError`` without a warning.

    Interpretation: A pass confirms strict typing; a failure identifies an accepted
    lookalike.

    Limitations: Only bytes represents wrong types; no invocation, validation, UQ,
    portability,
    or cross-language claim is made.
    """
    kwargs = dict(VALID_VALUES)
    kwargs[field_name] = b"wrong"
    with pytest.raises(TypeError):
        SUT(**kwargs)


def test_constructor__kind_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID: SV-PROV-200

    Requirement: Capability kind requires a ``CapabilityKind`` member, not its wire
    string.

    Method: Pass ``execute`` with otherwise valid declaration fields.

    Oracle: The accepted semantic type is the public enum class, not built-in ``str``.

    Acceptance: Construction raises ``TypeError`` and emits no warning.

    Interpretation: A pass confirms enum typing; a failure identifies coercion of a
    string lookalike.

    Limitations: This tests one lookalike, not invocation, validation, UQ, portability,
    or cross-
    language agreement.
    """
    kwargs = dict(VALID_VALUES)
    kwargs["kind"] = cast(Any, "execute")
    with pytest.raises(TypeError):
        SUT(**kwargs)


@pytest.mark.parametrize(
    ("field_name", "invalid_text"),
    [
        pytest.param("capability_id", "", id="capability_id_empty_identifier"),
        pytest.param("capability_id", "bad id", id="capability_id_embedded_space"),
        pytest.param("capability_id", "e\u0301", id="capability_id_non_nfc_identifier"),
        pytest.param(
            "capability_id", chr(0xD800), id="capability_id_unicode_surrogate"
        ),
        pytest.param(
            "capability_id", "x" * 129, id="capability_id_overlength_identifier"
        ),
        pytest.param("tool_id", "", id="tool_id_empty_identifier"),
        pytest.param("tool_id", "bad id", id="tool_id_embedded_space"),
        pytest.param("tool_id", "e\u0301", id="tool_id_non_nfc_identifier"),
        pytest.param("tool_id", chr(0xD800), id="tool_id_unicode_surrogate"),
        pytest.param("tool_id", "x" * 129, id="tool_id_overlength_identifier"),
        pytest.param("name", "", id="name_empty_identifier"),
        pytest.param("name", "bad id", id="name_embedded_space"),
        pytest.param("name", "e\u0301", id="name_non_nfc_identifier"),
        pytest.param("name", chr(0xD800), id="name_unicode_surrogate"),
        pytest.param("name", "x" * 129, id="name_overlength_identifier"),
        pytest.param(
            "specification_version",
            "",
            id="specification_version_empty_identifier",
        ),
        pytest.param(
            "specification_version",
            "bad id",
            id="specification_version_embedded_space",
        ),
        pytest.param(
            "specification_version",
            "e\u0301",
            id="specification_version_non_nfc_identifier",
        ),
        pytest.param(
            "specification_version",
            chr(0xD800),
            id="specification_version_unicode_surrogate",
        ),
        pytest.param(
            "specification_version",
            "x" * 129,
            id="specification_version_overlength_identifier",
        ),
    ],
)
def test_constructor__portable_text_value__rejects_invalid_identifier(
    field_name: str, invalid_text: str
) -> None:
    """Evidence ID: SV-PROV-201

    Requirement: Every capability identifier is nonempty, NFC, surrogate-free,
    grammar-valid, and
    at most 128 characters.

    Method: Replace each text field with empty, spaced, non-NFC, surrogate, and
    overlength
    partitions.

    Oracle: The literal portable-identifier grammar and Unicode invariants reject every
    table entry.

    Acceptance: Every field-and-partition case raises ``ValueError`` without a warning.

    Interpretation: A pass confirms complete field-wise rejection; a failure identifies
    an unchecked
    field or partition.

    Limitations: This finite set does not exhaust Unicode or establish invocation,
    validation,
    UQ, portability, or cross-language agreement.
    """
    assert field_name in TEXT_FIELDS
    kwargs = dict(VALID_VALUES)
    kwargs[field_name] = invalid_text
    with pytest.raises(ValueError):
        SUT(**kwargs)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-202

    Requirement: A capability declaration is operationally immutable after construction.

    Method: Assign a different valid value to the public ``name`` field.

    Oracle: Frozen dataclass assignment semantics require ``FrozenInstanceError``.

    Acceptance: Assignment raises that exception and cannot mutate the record.

    Interpretation: A pass confirms reassignment protection; a failure identifies
    mutable state.

    Limitations: This excludes hostile reflection, invocation, validation, UQ,
    portability, and
    cross-language agreement.
    """
    record = SUT(**VALID_VALUES)
    with pytest.raises(FrozenInstanceError):
        field_name = "name"
        setattr(record, field_name, "other")


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("capability_id", "cap-2", id="capability_id"),
        pytest.param("tool_id", "abinit", id="tool_id"),
        pytest.param("kind", CapabilityKind.PARSE, id="kind"),
        pytest.param("name", "parse-output", id="name"),
        pytest.param("specification_version", "v2", id="specification_version"),
    ],
)
def test_method__eq__compares_complete_represented_state(
    field_name: str, replacement: object
) -> None:
    """Evidence ID: SV-PROV-203

    Requirement: Exact equality includes each of the five represented capability fields.

    Method: Compare equal records, then independently vary the named field with a valid
    value.

    Oracle: Dataclass equality is exact over the complete accepted field tuple.

    Acceptance: Equal state compares true and every single-field variation compares
    unequal.

    Interpretation: A pass confirms complete equality; a failure identifies an omitted
    or distorted
    field.

    Limitations: This does not test ordering, invocation, validation, UQ, portability,
    or cross-
    language agreement.
    """
    left = SUT(**VALID_VALUES)
    changed = dict(VALID_VALUES)
    changed[field_name] = replacement
    assert left == SUT(**VALID_VALUES)
    assert left != SUT(**changed)


def test_field__durable_surface__excludes_runtime_state() -> None:
    """Evidence ID: SV-PROV-204

    Requirement: The durable capability surface excludes named runtime and credential
    state.

    Method: Compare public field names with the accepted prohibited-name vocabulary.

    Oracle: The durable boundary excludes commands, credentials, clients, processes, and
    handles.

    Acceptance: The public and prohibited field-name sets are disjoint.

    Interpretation: A pass confirms this named boundary; a failure identifies prohibited
    durable state.

    Limitations: Name inspection does not prove secret absence elsewhere or establish
    validation,
    UQ, portability, or cross-language agreement.
    """
    assert {field.name for field in fields(SUT)}.isdisjoint(
        {"command", "credential", "client", "process", "handle"}
    )
