r"""Software verification of ``ExternalToolIdentity``.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies construction, portable identifier fields,
immutability, complete exact equality, and the durable field boundary.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``ExternalToolIdentity``. Accepted field definitions
and fixed literals provide exact oracles for synthetic, dimensionless metadata
at identifier lengths 0 through 129. No warnings are expected.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated immutable-record contract; failure indicates
a source, test-oracle, or accepted-contract mismatch. This evidence does not
establish tool availability, numerical verification, physical correctness,
scientific validation, UQ, portability, or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import ExternalToolIdentity

SUT = ExternalToolIdentity
pytestmark = pytest.mark.software_verification

VALID_VALUES = {
    "tool_id": "qe",
    "implementation_family": "quantum-espresso",
}


def test_constructor__field_mapping__stores_exact_declared_types_and_values() -> None:
    """Evidence ID: SV-PROV-024

    Requirement: Construction stores both declared fields unchanged as built-in strings.

    Method: Construct from fixed valid metadata and inspect public dataclass fields.

    Oracle: The accepted signature and supplied literals define exact order, values, and
    types.

    Acceptance: The field sequence, stored tuple, and exact types match the two
    literals.

    Interpretation: A pass confirms constructor mapping; a failure indicates source,
    input, or
    contract drift.

    Limitations: Synthetic metadata only; this does not establish tool availability,
    validation,
    UQ, portability, or cross-language agreement.
    """
    record = SUT(**VALID_VALUES)
    assert tuple(field.name for field in fields(record)) == (
        "tool_id",
        "implementation_family",
    )
    assert tuple(getattr(record, field.name) for field in fields(record)) == (
        "qe",
        "quantum-espresso",
    )
    assert all(type(getattr(record, field.name)) is str for field in fields(record))


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("tool_id", id="tool_id"),
        pytest.param("implementation_family", id="implementation_family"),
    ],
)
def test_constructor__text_semantic_type__rejects_non_builtin_string(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-025

    Requirement: Each textual field requires an exact built-in string.

    Method: Replace the named valid field with bytes while retaining the other field.

    Oracle: The public type contract excludes bytes from both string fields.

    Acceptance: Every field partition raises ``TypeError`` and emits no warning.

    Interpretation: A pass confirms strict field typing; a failure identifies an
    accepted lookalike.

    Limitations: Only bytes represents wrong types; no availability, validation, UQ,
    portability,
    or cross-language claim is made.
    """
    kwargs: dict[str, Any] = dict(VALID_VALUES)
    kwargs[field_name] = b"wrong"
    with pytest.raises(TypeError):
        SUT(**kwargs)


@pytest.mark.parametrize(
    ("field_name", "invalid_text"),
    [
        pytest.param("tool_id", "", id="tool_id_empty_identifier"),
        pytest.param("tool_id", "bad id", id="tool_id_embedded_space"),
        pytest.param("tool_id", "e\u0301", id="tool_id_non_nfc_identifier"),
        pytest.param("tool_id", chr(0xD800), id="tool_id_unicode_surrogate"),
        pytest.param("tool_id", "x" * 129, id="tool_id_overlength_identifier"),
        pytest.param(
            "implementation_family",
            "",
            id="implementation_family_empty_identifier",
        ),
        pytest.param(
            "implementation_family",
            "bad id",
            id="implementation_family_embedded_space",
        ),
        pytest.param(
            "implementation_family",
            "e\u0301",
            id="implementation_family_non_nfc_identifier",
        ),
        pytest.param(
            "implementation_family",
            chr(0xD800),
            id="implementation_family_unicode_surrogate",
        ),
        pytest.param(
            "implementation_family",
            "x" * 129,
            id="implementation_family_overlength_identifier",
        ),
    ],
)
def test_constructor__portable_text_value__rejects_invalid_grammar(
    field_name: str, invalid_text: str
) -> None:
    """Evidence ID: SV-PROV-191

    Requirement: Each identifier is nonempty, NFC, surrogate-free, grammar-valid, and at
    most 128
    characters.

    Method: Replace each field with empty, spaced, non-NFC, surrogate, and 129-character
    partitions.

    Oracle: The literal ``[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`` grammar and Unicode
    invariants
    reject every table entry.

    Acceptance: Every field-and-partition case raises ``ValueError`` without a warning.

    Interpretation: A pass confirms field-wise malformed-value rejection; a failure
    identifies an
    unchecked field or partition.

    Limitations: This finite boundary set does not exhaust Unicode or establish
    availability,
    validation, UQ, portability, or cross-language agreement.
    """
    kwargs = dict(VALID_VALUES)
    kwargs[field_name] = invalid_text
    with pytest.raises(ValueError):
        SUT(**kwargs)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-192

    Requirement: The identity record is operationally immutable after construction.

    Method: Assign a different valid value to the public ``tool_id`` field.

    Oracle: Frozen dataclass assignment semantics require ``FrozenInstanceError``.

    Acceptance: Assignment raises that exception and does not mutate the record.

    Interpretation: A pass confirms reassignment protection; a failure identifies
    mutable state.

    Limitations: This does not test hostile reflection, availability, validation, UQ,
    portability, or cross-language agreement.
    """
    record = SUT(**VALID_VALUES)
    with pytest.raises(FrozenInstanceError):
        field_name = "tool_id"
        setattr(record, field_name, "replacement")


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("tool_id", "abinit", id="tool_id"),
        pytest.param(
            "implementation_family",
            "qe-distribution",
            id="implementation_family",
        ),
    ],
)
def test_method__eq__compares_complete_represented_state(
    field_name: str, replacement: str
) -> None:
    """Evidence ID: SV-PROV-193

    Requirement: Exact equality includes each of the two represented fields.

    Method: Compare equal records, then independently vary the named field with a valid
    value.

    Oracle: Dataclass equality is exact over the complete accepted field tuple.

    Acceptance: Equal state compares true and every single-field variation compares
    unequal.

    Interpretation: A pass confirms complete equality; a failure identifies an omitted
    or distorted
    field.

    Limitations: This does not establish ordering, hashing, availability, validation,
    UQ,
    portability, or cross-language agreement.
    """
    left = SUT(**VALID_VALUES)
    changed = dict(VALID_VALUES)
    changed[field_name] = replacement
    assert left == SUT(**VALID_VALUES)
    assert left != SUT(**changed)


def test_field__durable_surface__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID: SV-PROV-194

    Requirement: The durable identity surface excludes named runtime and credential
    state.

    Method: Compare public field names with the accepted prohibited-name vocabulary.

    Oracle: The durable-token boundary excludes commands, secrets, clients, processes,
    handles, and schedulers.

    Acceptance: The public and prohibited field-name sets are disjoint.

    Interpretation: A pass confirms this named surface boundary; a failure identifies
    prohibited
    durable state.

    Limitations: Name inspection does not prove secret absence elsewhere or establish
    validation,
    UQ, portability, or cross-language agreement.
    """
    prohibited = {
        "command",
        "credential",
        "password",
        "token",
        "client",
        "process",
        "handle",
        "scheduler",
    }
    assert {field.name for field in fields(SUT)}.isdisjoint(prohibited)
