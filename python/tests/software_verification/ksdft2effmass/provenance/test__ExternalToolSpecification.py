r"""Software verification of ``ExternalToolSpecification``.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies constructor mapping, identifier and opaque
version grammars, immutability, complete equality, and durable field boundaries.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``ExternalToolSpecification``. Accepted field and
lexical contracts provide exact oracles for synthetic, dimensionless metadata
at identifier lengths 0 through 129 and version lengths 0 through 65.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated declaration contract; failure indicates a
source, test-oracle, or accepted-contract mismatch. This evidence does not
resolve versions, discover tools, establish numerical verification, validate
science, quantify uncertainty, or prove portability or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import ExternalToolSpecification

SUT = ExternalToolSpecification
pytestmark = pytest.mark.software_verification

VALID_VALUES = {
    "specification_id": "spec-1",
    "tool_id": "qe",
    "requested_version": "7.4",
    "executable_or_package_id": "pw.x",
}
IDENTIFIER_FIELDS = (
    "specification_id",
    "tool_id",
    "executable_or_package_id",
)


def test_constructor__field_mapping__stores_exact_declared_types_and_values() -> None:
    """Evidence ID: SV-PROV-026

    Requirement: Construction stores all four declared fields unchanged as built-in
    strings.

    Method: Construct fixed valid metadata and inspect the public dataclass fields.

    Oracle: The accepted signature and supplied literals define exact order, values, and
    types.

    Acceptance: Field names, stored values, and exact string types match the
    declaration.

    Interpretation: A pass confirms constructor mapping; a failure indicates source,
    input, or
    contract drift.

    Limitations: Synthetic metadata only; no resolution, discovery, validation, UQ,
    portability,
    or cross-language claim is made.
    """
    record = SUT(**VALID_VALUES)
    assert tuple(field.name for field in fields(record)) == (
        "specification_id",
        "tool_id",
        "requested_version",
        "executable_or_package_id",
    )
    assert tuple(getattr(record, field.name) for field in fields(record)) == (
        "spec-1",
        "qe",
        "7.4",
        "pw.x",
    )
    assert all(type(getattr(record, field.name)) is str for field in fields(record))


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("specification_id", id="specification_id"),
        pytest.param("tool_id", id="tool_id"),
        pytest.param("requested_version", id="requested_version"),
        pytest.param("executable_or_package_id", id="executable_or_package_id"),
    ],
)
def test_constructor__text_semantic_type__rejects_non_builtin_string(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-027

    Requirement: Each specification field requires an exact built-in string.

    Method: Replace the named valid field with bytes while retaining all other fields.

    Oracle: The public type contract excludes bytes from every textual field.

    Acceptance: Every field partition raises ``TypeError`` without a warning.

    Interpretation: A pass confirms strict typing; a failure identifies an accepted
    lookalike.

    Limitations: Only bytes represents wrong types; no resolution, validation, UQ,
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
        pytest.param("specification_id", "", id="specification_id_empty_identifier"),
        pytest.param(
            "specification_id", "bad id", id="specification_id_embedded_space"
        ),
        pytest.param(
            "specification_id", "e\u0301", id="specification_id_non_nfc_identifier"
        ),
        pytest.param(
            "specification_id", chr(0xD800), id="specification_id_unicode_surrogate"
        ),
        pytest.param(
            "specification_id", "x" * 129, id="specification_id_overlength_identifier"
        ),
        pytest.param("tool_id", "", id="tool_id_empty_identifier"),
        pytest.param("tool_id", "bad id", id="tool_id_embedded_space"),
        pytest.param("tool_id", "e\u0301", id="tool_id_non_nfc_identifier"),
        pytest.param("tool_id", chr(0xD800), id="tool_id_unicode_surrogate"),
        pytest.param("tool_id", "x" * 129, id="tool_id_overlength_identifier"),
        pytest.param(
            "executable_or_package_id",
            "",
            id="executable_or_package_id_empty_identifier",
        ),
        pytest.param(
            "executable_or_package_id",
            "bad id",
            id="executable_or_package_id_embedded_space",
        ),
        pytest.param(
            "executable_or_package_id",
            "e\u0301",
            id="executable_or_package_id_non_nfc_identifier",
        ),
        pytest.param(
            "executable_or_package_id",
            chr(0xD800),
            id="executable_or_package_id_unicode_surrogate",
        ),
        pytest.param(
            "executable_or_package_id",
            "x" * 129,
            id="executable_or_package_id_overlength_identifier",
        ),
    ],
)
def test_constructor__portable_text_value__rejects_invalid_grammar(
    field_name: str, invalid_text: str
) -> None:
    """Evidence ID: SV-PROV-196

    Requirement: Every identifier is nonempty, NFC, surrogate-free, grammar-valid, and
    no longer
    than 128 characters.

    Method: Replace each identifier with empty, spaced, non-NFC, surrogate, and
    overlength
    partitions.

    Oracle: The literal portable-identifier grammar and Unicode invariants reject all
    table
    entries.

    Acceptance: Every field-and-partition case raises ``ValueError`` without a warning.

    Interpretation: A pass confirms complete field-wise rejection; a failure identifies
    an unchecked
    identifier or partition.

    Limitations: This finite set does not exhaust Unicode or establish resolution,
    validation,
    UQ, portability, or cross-language agreement.
    """
    assert field_name in IDENTIFIER_FIELDS
    kwargs = dict(VALID_VALUES)
    kwargs[field_name] = invalid_text
    with pytest.raises(ValueError):
        SUT(**kwargs)


@pytest.mark.parametrize(
    "requested_version",
    [
        pytest.param("0", id="minimum_length_one"),
        pytest.param("A" + "._+-" * 15 + "xyz", id="maximum_length_64"),
    ],
)
def test_constructor__requested_version_bounds__accepts_valid_endpoints(
    requested_version: str,
) -> None:
    """Evidence ID: SV-PROV-237

    Requirement: Opaque requested versions accept valid one- and 64-character lexical
    endpoints.

    Method: Construct with independently fixed minimum- and maximum-length valid
    strings.

    Oracle: ``[0-9A-Za-z][0-9A-Za-z._+-]{0,63}`` admits both parameter values exactly.

    Acceptance: Construction succeeds, stores the exact text, and emits no warning.

    Interpretation: A pass confirms inclusive length endpoints; a failure indicates an
    off-by-one or
    grammar defect.

    Limitations: This new owner does not interpret version precedence or establish
    discovery,
    validation, UQ, portability, or cross-language agreement.
    """
    record = SUT(**(VALID_VALUES | {"requested_version": requested_version}))
    assert record.requested_version == requested_version


@pytest.mark.parametrize(
    "invalid_version",
    [
        pytest.param("", id="empty_version"),
        pytest.param("-7.4", id="leading_prohibited_character"),
        pytest.param("7 4", id="embedded_space"),
        pytest.param("7:4", id="embedded_prohibited_character"),
        pytest.param("e\u0301", id="non_nfc_version"),
        pytest.param(chr(0xD800), id="unicode_surrogate"),
        pytest.param("x" * 65, id="overlength_version"),
    ],
)
def test_constructor__requested_version_value__rejects_nonportable_text(
    invalid_version: str,
) -> None:
    """Evidence ID: SV-PROV-195

    Requirement: Requested version text satisfies the exact opaque 1-to-64-character
    grammar.

    Method: Exercise empty, leading, embedded, Unicode, surrogate, and overlength
    rejection
    partitions.

    Oracle: The literal ``[0-9A-Za-z][0-9A-Za-z._+-]{0,63}`` grammar rejects each value.

    Acceptance: Every one of the seven partitions raises ``ValueError`` without a
    warning.

    Interpretation: A pass confirms bounded lexical rejection; a failure identifies an
    unchecked
    grammar partition.

    Limitations: This does not parse or order versions or establish discovery,
    validation, UQ,
    portability, or cross-language agreement.
    """
    with pytest.raises(ValueError):
        SUT(**(VALID_VALUES | {"requested_version": invalid_version}))


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-197

    Requirement: A specification is operationally immutable after construction.

    Method: Assign a different valid value to the public specification identifier.

    Oracle: Frozen dataclass assignment semantics require ``FrozenInstanceError``.

    Acceptance: Assignment raises that exception and cannot mutate the record.

    Interpretation: A pass confirms reassignment protection; a failure identifies
    mutable state.

    Limitations: This excludes hostile reflection, resolution, validation, UQ,
    portability, and
    cross-language agreement.
    """
    record = SUT(**VALID_VALUES)
    with pytest.raises(FrozenInstanceError):
        field_name = "specification_id"
        setattr(record, field_name, "replacement")


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("specification_id", "spec-2", id="specification_id"),
        pytest.param("tool_id", "abinit", id="tool_id"),
        pytest.param("requested_version", "8.0", id="requested_version"),
        pytest.param("executable_or_package_id", "ph.x", id="executable_or_package_id"),
    ],
)
def test_method__eq__compares_complete_represented_state(
    field_name: str, replacement: str
) -> None:
    """Evidence ID: SV-PROV-198

    Requirement: Exact equality includes each of the four represented specification
    fields.

    Method: Compare equal records, then independently vary the named field with a valid
    value.

    Oracle: Dataclass equality is exact over the complete accepted field tuple.

    Acceptance: Equal state compares true and every single-field variation compares
    unequal.

    Interpretation: A pass confirms complete equality; a failure identifies an omitted
    or distorted
    field.

    Limitations: This does not test ordering, resolution, validation, UQ, portability,
    or cross-
    language agreement.
    """
    left = SUT(**VALID_VALUES)
    changed = dict(VALID_VALUES)
    changed[field_name] = replacement
    assert left == SUT(**VALID_VALUES)
    assert left != SUT(**changed)


def test_field__durable_surface__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID: SV-PROV-199

    Requirement: The durable specification surface excludes named runtime and credential
    state.

    Method: Compare public field names with the accepted prohibited-name vocabulary.

    Oracle: The durable boundary excludes commands, secrets, clients, processes,
    handles,
    and schedulers.

    Acceptance: The public and prohibited field-name sets are disjoint.

    Interpretation: A pass confirms this named boundary; a failure identifies prohibited
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
