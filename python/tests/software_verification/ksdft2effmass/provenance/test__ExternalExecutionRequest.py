r"""Software verification of ``ExternalExecutionRequest``.

Facet and represented meaning

-----------------------------
This class-owned software evidence verifies exact eleven-field construction,
identifier invariants, optional retry-parent lineage, direct self-lineage
rejection, canonical artifact and output-role tuples, frozen state, equality,
and the durable request boundary. The record stores immutable request intent
that refers to a separate authorization identity.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``ExternalExecutionRequest``. Public constructor inputs,
dataclass field semantics, and fixed valid or invalid literals provide the
oracles. Construction does not verify authorization, authorize a retry merely
because a parent ID exists, execute a tool, prove input artifacts exist, create
expected outputs, or inspect external state.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated request-record software behavior; failure
identifies a production, test-input, oracle, or accepted-contract mismatch.
Construction does not establish solver convergence, numerical acceptance,
scientific validation, uncertainty quantification, physical correctness,
portability, or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from types import NoneType
from typing import Any

import pytest

from ksdft2effmass.provenance import ExternalExecutionRequest

SUT = ExternalExecutionRequest
pytestmark = pytest.mark.software_verification

IDENTIFIER_FIELDS = (
    "request_id",
    "correlation_id",
    "attempt_id",
    "tool_id",
    "capability_id",
    "installation_id",
    "authorization_id",
    "provenance_id",
)
TUPLE_FIELDS = ("input_artifact_ids", "expected_output_roles")
PUBLIC_FIELDS = (
    "request_id",
    "correlation_id",
    "attempt_id",
    "retry_parent_request_id",
    "tool_id",
    "capability_id",
    "installation_id",
    "authorization_id",
    "input_artifact_ids",
    "expected_output_roles",
    "provenance_id",
)
FROZEN_FIELDS = (
    "request_id",
    "correlation_id",
    "attempt_id",
    "retry_parent_request_id",
    "tool_id",
    "capability_id",
    "installation_id",
    "authorization_id",
    "input_artifact_ids",
    "expected_output_roles",
    "provenance_id",
)
EQUALITY_FIELDS = (
    "request_id",
    "correlation_id",
    "attempt_id",
    "retry_parent_request_id",
    "tool_id",
    "capability_id",
    "installation_id",
    "authorization_id",
    "input_artifact_ids",
    "expected_output_roles",
    "provenance_id",
)


def make_external_execution_request(**overrides: Any) -> ExternalExecutionRequest:
    """Evidence ID: Owns no identifier; supports all evidence in this module.

    Requirement: Tests need valid baseline request state with explicit one-field
    overrides.

    Method: Merge named overrides into fixed synthetic values and call the public
    constructor.

    Oracle: The accepted constructor signature and independently valid literals define
    setup.

    Acceptance: The helper returns the constructor result without assertions or
    normalization.

    Interpretation: The helper isolates the field under test while all other request
    fields stay valid.

    Limitations: This setup helper owns no result and performs no I/O or authorization
    check.
    """
    values: dict[str, Any] = {
        "request_id": "request-1",
        "correlation_id": "correlation-1",
        "attempt_id": "attempt-1",
        "retry_parent_request_id": None,
        "tool_id": "tool-1",
        "capability_id": "capability-1",
        "installation_id": "installation-1",
        "authorization_id": "authorization-1",
        "input_artifact_ids": ("input-1", "input-2"),
        "expected_output_roles": ("log", "output"),
        "provenance_id": "provenance-1",
    }
    values.update(overrides)
    return SUT(**values)


def test_constructor__field_mapping__stores_exact_values_types_and_order() -> None:
    """Evidence ID: SV-PROV-037

    Requirement: Construction stores the exact eleven-field request payload without
    coercion.

    Method: Construct baseline state and inspect declared order, values, and exact
    built-in
    types.

    Oracle: The public inventory and fixed constructor literals are independent expected
    state.

    Acceptance: Field order and values match exactly; types are str, NoneType, and tuple
    as
    declared.

    Interpretation: Passing establishes exact request constructor mapping and absent
    retry-parent state.

    Limitations: Synthetic metadata only; storage does not validate authorization or
    external state.
    """
    record = make_external_execution_request()
    assert tuple(field.name for field in fields(record)) == PUBLIC_FIELDS
    assert astuple(record) == (
        "request-1",
        "correlation-1",
        "attempt-1",
        None,
        "tool-1",
        "capability-1",
        "installation-1",
        "authorization-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "provenance-1",
    )
    assert tuple(type(value) for value in astuple(record)) == (
        str,
        str,
        str,
        NoneType,
        str,
        str,
        str,
        str,
        tuple,
        tuple,
        str,
    )
    assert type(record.input_artifact_ids) is tuple
    assert type(record.expected_output_roles) is tuple


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "request_id", "request-ordinary", id="request_id_ordinary_valid_identifier"
        ),
        pytest.param("request_id", "a", id="request_id_minimum_length_1"),
        pytest.param(
            "request_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="request_id_maximum_length_128",
        ),
        pytest.param(
            "correlation_id",
            "correlation-ordinary",
            id="correlation_id_ordinary_valid_identifier",
        ),
        pytest.param("correlation_id", "a", id="correlation_id_minimum_length_1"),
        pytest.param(
            "correlation_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="correlation_id_maximum_length_128",
        ),
        pytest.param(
            "attempt_id", "attempt-ordinary", id="attempt_id_ordinary_valid_identifier"
        ),
        pytest.param("attempt_id", "a", id="attempt_id_minimum_length_1"),
        pytest.param(
            "attempt_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="attempt_id_maximum_length_128",
        ),
        pytest.param(
            "tool_id", "tool-ordinary", id="tool_id_ordinary_valid_identifier"
        ),
        pytest.param("tool_id", "a", id="tool_id_minimum_length_1"),
        pytest.param(
            "tool_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="tool_id_maximum_length_128",
        ),
        pytest.param(
            "capability_id",
            "capability-ordinary",
            id="capability_id_ordinary_valid_identifier",
        ),
        pytest.param("capability_id", "a", id="capability_id_minimum_length_1"),
        pytest.param(
            "capability_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="capability_id_maximum_length_128",
        ),
        pytest.param(
            "installation_id",
            "installation-ordinary",
            id="installation_id_ordinary_valid_identifier",
        ),
        pytest.param("installation_id", "a", id="installation_id_minimum_length_1"),
        pytest.param(
            "installation_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="installation_id_maximum_length_128",
        ),
        pytest.param(
            "authorization_id",
            "authorization-ordinary",
            id="authorization_id_ordinary_valid_identifier",
        ),
        pytest.param("authorization_id", "a", id="authorization_id_minimum_length_1"),
        pytest.param(
            "authorization_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="authorization_id_maximum_length_128",
        ),
        pytest.param(
            "provenance_id",
            "provenance-ordinary",
            id="provenance_id_ordinary_valid_identifier",
        ),
        pytest.param("provenance_id", "a", id="provenance_id_minimum_length_1"),
        pytest.param(
            "provenance_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="provenance_id_maximum_length_128",
        ),
    ],
)
def test_constructor__required_identifiers__accept_valid_length_partitions(
    field_name: str, value: str
) -> None:
    """Evidence ID: SV-PROV-288

    Requirement: Every required identifier accepts valid portable text at ordinary,
    minimum, and
    maximum lengths.

    Method: Override one required field for each explicit field-and-length partition.

    Oracle: The accepted grammar permits 1 through 128 ASCII portable identifier
    characters.

    Acceptance: Construction succeeds and stores the selected value exactly.

    Interpretation: Passing establishes accepted lexical-length partitions for every
    required
    identifier.

    Limitations: Does not establish identity uniqueness, authorization, or meaning
    outside lexical
    validity.
    """
    assert (
        getattr(make_external_execution_request(**{field_name: value}), field_name)
        == value
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", b"identifier", id="request_id_bytes_wrong_type"),
        pytest.param(
            "correlation_id", b"identifier", id="correlation_id_bytes_wrong_type"
        ),
        pytest.param("attempt_id", b"identifier", id="attempt_id_bytes_wrong_type"),
        pytest.param("tool_id", b"identifier", id="tool_id_bytes_wrong_type"),
        pytest.param(
            "capability_id", b"identifier", id="capability_id_bytes_wrong_type"
        ),
        pytest.param(
            "installation_id", b"identifier", id="installation_id_bytes_wrong_type"
        ),
        pytest.param(
            "authorization_id", b"identifier", id="authorization_id_bytes_wrong_type"
        ),
        pytest.param(
            "provenance_id", b"identifier", id="provenance_id_bytes_wrong_type"
        ),
    ],
)
def test_constructor__required_identifier_type__rejects_bytes_wrong_type(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-219

    Requirement: Every required identifier rejects wrong semantic type.

    Method: Override each required field independently with the wrong semantic type
    partition.

    Oracle: The accepted identifier contract assigns TypeError to this partition.

    Acceptance: Every field raises exactly TypeError.

    Interpretation: Passing establishes wrong semantic type rejection for all eight
    required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(TypeError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", "", id="request_id_empty_text"),
        pytest.param("correlation_id", "", id="correlation_id_empty_text"),
        pytest.param("attempt_id", "", id="attempt_id_empty_text"),
        pytest.param("tool_id", "", id="tool_id_empty_text"),
        pytest.param("capability_id", "", id="capability_id_empty_text"),
        pytest.param("installation_id", "", id="installation_id_empty_text"),
        pytest.param("authorization_id", "", id="authorization_id_empty_text"),
        pytest.param("provenance_id", "", id="provenance_id_empty_text"),
    ],
)
def test_constructor__required_identifier_empty__rejects_empty_text(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-289

    Requirement: Every required identifier rejects empty text.

    Method: Override each required field independently with the empty text partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes empty text rejection for all eight required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", "bad id", id="request_id_embedded_space"),
        pytest.param("correlation_id", "bad id", id="correlation_id_embedded_space"),
        pytest.param("attempt_id", "bad id", id="attempt_id_embedded_space"),
        pytest.param("tool_id", "bad id", id="tool_id_embedded_space"),
        pytest.param("capability_id", "bad id", id="capability_id_embedded_space"),
        pytest.param("installation_id", "bad id", id="installation_id_embedded_space"),
        pytest.param(
            "authorization_id", "bad id", id="authorization_id_embedded_space"
        ),
        pytest.param("provenance_id", "bad id", id="provenance_id_embedded_space"),
    ],
)
def test_constructor__required_identifier_grammar__rejects_embedded_space(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-290

    Requirement: Every required identifier rejects embedded-space grammar.

    Method: Override each required field independently with the embedded-space grammar
    partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes embedded-space grammar rejection for all eight
    required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", "-leading", id="request_id_invalid_leading_hyphen"),
        pytest.param(
            "correlation_id", "-leading", id="correlation_id_invalid_leading_hyphen"
        ),
        pytest.param("attempt_id", "-leading", id="attempt_id_invalid_leading_hyphen"),
        pytest.param("tool_id", "-leading", id="tool_id_invalid_leading_hyphen"),
        pytest.param(
            "capability_id", "-leading", id="capability_id_invalid_leading_hyphen"
        ),
        pytest.param(
            "installation_id", "-leading", id="installation_id_invalid_leading_hyphen"
        ),
        pytest.param(
            "authorization_id", "-leading", id="authorization_id_invalid_leading_hyphen"
        ),
        pytest.param(
            "provenance_id", "-leading", id="provenance_id_invalid_leading_hyphen"
        ),
    ],
)
def test_constructor__required_identifier_leading__rejects_invalid_leading_hyphen(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-291

    Requirement: Every required identifier rejects invalid leading character.

    Method: Override each required field independently with the invalid leading
    character
    partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes invalid leading character rejection for all
    eight required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", "\ud800", id="request_id_unicode_surrogate"),
        pytest.param("correlation_id", "\ud800", id="correlation_id_unicode_surrogate"),
        pytest.param("attempt_id", "\ud800", id="attempt_id_unicode_surrogate"),
        pytest.param("tool_id", "\ud800", id="tool_id_unicode_surrogate"),
        pytest.param("capability_id", "\ud800", id="capability_id_unicode_surrogate"),
        pytest.param(
            "installation_id", "\ud800", id="installation_id_unicode_surrogate"
        ),
        pytest.param(
            "authorization_id", "\ud800", id="authorization_id_unicode_surrogate"
        ),
        pytest.param("provenance_id", "\ud800", id="provenance_id_unicode_surrogate"),
    ],
)
def test_constructor__required_identifier_surrogate__rejects_unicode_surrogate(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-292

    Requirement: Every required identifier rejects Unicode surrogate.

    Method: Override each required field independently with the Unicode surrogate
    partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes Unicode surrogate rejection for all eight
    required identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("request_id", "é", id="request_id_non_nfc"),
        pytest.param("correlation_id", "é", id="correlation_id_non_nfc"),
        pytest.param("attempt_id", "é", id="attempt_id_non_nfc"),
        pytest.param("tool_id", "é", id="tool_id_non_nfc"),
        pytest.param("capability_id", "é", id="capability_id_non_nfc"),
        pytest.param("installation_id", "é", id="installation_id_non_nfc"),
        pytest.param("authorization_id", "é", id="authorization_id_non_nfc"),
        pytest.param("provenance_id", "é", id="provenance_id_non_nfc"),
    ],
)
def test_constructor__required_identifier_nfc__rejects_non_nfc(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-293

    Requirement: Every required identifier rejects non-NFC text.

    Method: Override each required field independently with the non-NFC text partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes non-NFC text rejection for all eight required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "request_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="request_id_overlength_129",
        ),
        pytest.param(
            "correlation_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="correlation_id_overlength_129",
        ),
        pytest.param(
            "attempt_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="attempt_id_overlength_129",
        ),
        pytest.param(
            "tool_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="tool_id_overlength_129",
        ),
        pytest.param(
            "capability_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="capability_id_overlength_129",
        ),
        pytest.param(
            "installation_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="installation_id_overlength_129",
        ),
        pytest.param(
            "authorization_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="authorization_id_overlength_129",
        ),
        pytest.param(
            "provenance_id",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="provenance_id_overlength_129",
        ),
    ],
)
def test_constructor__required_identifier_length__rejects_overlength_129(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-294

    Requirement: Every required identifier rejects overlength text.

    Method: Override each required field independently with the overlength text
    partition.

    Oracle: The accepted identifier contract assigns ValueError to this partition.

    Acceptance: Every field raises exactly ValueError.

    Interpretation: Passing establishes overlength text rejection for all eight required
    identifiers.

    Limitations: Other fields remain valid; this does not establish authorization or
    identifier
    uniqueness.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("parent",),
    [
        pytest.param(None, id="retry_parent_none"),
        pytest.param("parent-ordinary", id="retry_parent_distinct_ordinary"),
        pytest.param("a", id="retry_parent_minimum_length_1"),
        pytest.param(
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            id="retry_parent_maximum_length_128",
        ),
    ],
)
def test_constructor__retry_parent__accepts_optional_valid_states(
    parent: str | None,
) -> None:
    """Evidence ID: SV-PROV-078

    Requirement: Retry-parent lineage accepts None or a distinct valid identifier across
    length
    boundaries.

    Method: Override only retry_parent_request_id with four explicit accepted states.

    Oracle: The optional portable-identifier and direct inequality contracts define
    expected
    state.

    Acceptance: Construction stores each parent exactly.

    Interpretation: Passing establishes the four accepted optional retry-parent states.

    Limitations: A parent ID neither authorizes retry nor establishes graph-wide lineage
    validity.
    """
    assert (
        make_external_execution_request(
            retry_parent_request_id=parent
        ).retry_parent_request_id
        == parent
    )


def test_constructor__retry_parent_type__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-295

    Requirement: Retry-parent lineage rejects wrong semantic type.

    Method: Construct with only retry_parent_request_id set to wrong semantic type.

    Oracle: The optional identifier contract assigns TypeError to this partition.

    Acceptance: Construction raises exactly TypeError.

    Interpretation: Passing establishes retry-parent wrong semantic type rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(TypeError):
        make_external_execution_request(retry_parent_request_id=b"parent")


def test_constructor__retry_parent_empty__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-296

    Requirement: Retry-parent lineage rejects empty text.

    Method: Construct with only retry_parent_request_id set to empty text.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent empty text rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="")


def test_constructor__retry_parent_grammar__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-297

    Requirement: Retry-parent lineage rejects embedded-space grammar.

    Method: Construct with only retry_parent_request_id set to embedded-space grammar.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent embedded-space grammar rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="bad parent")


def test_constructor__retry_parent_leading__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-298

    Requirement: Retry-parent lineage rejects invalid leading character.

    Method: Construct with only retry_parent_request_id set to invalid leading
    character.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent invalid leading character
    rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="-parent")


def test_constructor__retry_parent_surrogate__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-299

    Requirement: Retry-parent lineage rejects Unicode surrogate.

    Method: Construct with only retry_parent_request_id set to Unicode surrogate.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent Unicode surrogate rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="\ud800")


def test_constructor__retry_parent_nfc__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-300

    Requirement: Retry-parent lineage rejects non-NFC text.

    Method: Construct with only retry_parent_request_id set to non-NFC text.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent non-NFC text rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="é")


def test_constructor__retry_parent_length__rejects_invalid_state() -> None:
    """Evidence ID: SV-PROV-301

    Requirement: Retry-parent lineage rejects overlength text.

    Method: Construct with only retry_parent_request_id set to overlength text.

    Oracle: The optional identifier contract assigns ValueError to this partition.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes retry-parent overlength text rejection.

    Limitations: This lexical check does not authorize retry or establish graph-wide
    acyclicity.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(
            retry_parent_request_id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        )


def test_constructor__retry_parent_relation__rejects_direct_self_reference() -> None:
    """Evidence ID: SV-PROV-217

    Requirement: A request cannot directly name its own request ID as retry parent.

    Method: Construct otherwise valid state with equal request and parent identifiers.

    Oracle: The accepted direct irreflexive lineage invariant supplies the expected
    error.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes rejection of direct self-reference.

    Limitations: Does not establish graph-wide acyclicity or retry authorization.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(retry_parent_request_id="request-1")


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids", (), id="input_artifact_ids_empty_builtin_tuple"
        ),
        pytest.param(
            "input_artifact_ids",
            ("member-1",),
            id="input_artifact_ids_singleton_builtin_tuple",
        ),
        pytest.param(
            "input_artifact_ids",
            ("member-1", "member-2"),
            id="input_artifact_ids_unique_lexically_sorted_tuple",
        ),
        pytest.param(
            "expected_output_roles", (), id="expected_output_roles_empty_builtin_tuple"
        ),
        pytest.param(
            "expected_output_roles",
            ("member-1",),
            id="expected_output_roles_singleton_builtin_tuple",
        ),
        pytest.param(
            "expected_output_roles",
            ("member-1", "member-2"),
            id="expected_output_roles_unique_lexically_sorted_tuple",
        ),
    ],
)
def test_constructor__identifier_tuples__accept_canonical_states(
    field_name: str, value: tuple[str, ...]
) -> None:
    """Evidence ID: SV-PROV-038

    Requirement: Both tuple fields accept empty, singleton, and unique sorted built-in
    tuples.

    Method: Override each tuple field independently across three canonical cardinality
    states.

    Oracle: Fixed built-in tuples already satisfy the public member grammar and tuple
    relations.

    Acceptance: Construction preserves each tuple exactly with built-in tuple type.

    Interpretation: Passing establishes canonical accepted states for both tuple fields.

    Limitations: Synthetic members do not prove artifacts exist or outputs are created.
    """
    stored = getattr(make_external_execution_request(**{field_name: value}), field_name)
    assert stored == value
    assert type(stored) is tuple


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ["member-1"],
            id="input_artifact_ids_list_wrong_container_type",
        ),
        pytest.param(
            "expected_output_roles",
            ["member-1"],
            id="expected_output_roles_list_wrong_container_type",
        ),
    ],
)
def test_constructor__tuple_container_type__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-218

    Requirement: Each request tuple field rejects a non-tuple container.

    Method: Override each tuple field independently with the non-tuple container
    partition.

    Oracle: The canonical tuple contract assigns TypeError to this invariant.

    Acceptance: Both fields raise exactly TypeError.

    Interpretation: Passing establishes non-tuple container rejection independently for
    both tuple
    fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(TypeError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            (1,),
            id="input_artifact_ids_integer_wrong_member_type",
        ),
        pytest.param(
            "expected_output_roles",
            (1,),
            id="expected_output_roles_integer_wrong_member_type",
        ),
    ],
)
def test_constructor__tuple_member_type__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-302

    Requirement: Each request tuple field rejects a non-string member.

    Method: Override each tuple field independently with the non-string member
    partition.

    Oracle: The canonical tuple contract assigns TypeError to this invariant.

    Acceptance: Both fields raise exactly TypeError.

    Interpretation: Passing establishes non-string member rejection independently for
    both tuple fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(TypeError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("input_artifact_ids", ("",), id="input_artifact_ids_empty_member"),
        pytest.param(
            "expected_output_roles", ("",), id="expected_output_roles_empty_member"
        ),
    ],
)
def test_constructor__tuple_member_nonempty__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-303

    Requirement: Each request tuple field rejects a empty member.

    Method: Override each tuple field independently with the empty member partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes empty member rejection independently for both
    tuple fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("bad member",),
            id="input_artifact_ids_embedded_space_member",
        ),
        pytest.param(
            "expected_output_roles",
            ("bad member",),
            id="expected_output_roles_embedded_space_member",
        ),
    ],
)
def test_constructor__tuple_member_grammar__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-304

    Requirement: Each request tuple field rejects a embedded-space member.

    Method: Override each tuple field independently with the embedded-space member
    partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes embedded-space member rejection independently
    for both tuple
    fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("-member",),
            id="input_artifact_ids_invalid_leading_hyphen_member",
        ),
        pytest.param(
            "expected_output_roles",
            ("-member",),
            id="expected_output_roles_invalid_leading_hyphen_member",
        ),
    ],
)
def test_constructor__tuple_member_leading_character__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-305

    Requirement: Each request tuple field rejects a invalid leading character.

    Method: Override each tuple field independently with the invalid leading character
    partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes invalid leading character rejection
    independently for both tuple
    fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("\ud800",),
            id="input_artifact_ids_unicode_surrogate_member",
        ),
        pytest.param(
            "expected_output_roles",
            ("\ud800",),
            id="expected_output_roles_unicode_surrogate_member",
        ),
    ],
)
def test_constructor__tuple_member_unicode_surrogate__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-306

    Requirement: Each request tuple field rejects a Unicode surrogate member.

    Method: Override each tuple field independently with the Unicode surrogate member
    partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes Unicode surrogate member rejection independently
    for both tuple
    fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids", ("é",), id="input_artifact_ids_non_nfc_member"
        ),
        pytest.param(
            "expected_output_roles", ("é",), id="expected_output_roles_non_nfc_member"
        ),
    ],
)
def test_constructor__tuple_member_unicode_nfc__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-307

    Requirement: Each request tuple field rejects a non-NFC member.

    Method: Override each tuple field independently with the non-NFC member partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes non-NFC member rejection independently for both
    tuple fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            (
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ),
            id="input_artifact_ids_overlength_129_member",
        ),
        pytest.param(
            "expected_output_roles",
            (
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ),
            id="expected_output_roles_overlength_129_member",
        ),
    ],
)
def test_constructor__tuple_member_length__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-308

    Requirement: Each request tuple field rejects a overlength member.

    Method: Override each tuple field independently with the overlength member
    partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes overlength member rejection independently for
    both tuple fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("member-2", "member-1"),
            id="input_artifact_ids_reverse_lexical_order",
        ),
        pytest.param(
            "expected_output_roles",
            ("member-2", "member-1"),
            id="expected_output_roles_reverse_lexical_order",
        ),
    ],
)
def test_constructor__tuple_ordering__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-309

    Requirement: Each request tuple field rejects a reverse lexical order.

    Method: Override each tuple field independently with the reverse lexical order
    partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes reverse lexical order rejection independently
    for both tuple
    fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("member-1", "member-1"),
            id="input_artifact_ids_duplicate_member",
        ),
        pytest.param(
            "expected_output_roles",
            ("member-1", "member-1"),
            id="expected_output_roles_duplicate_member",
        ),
    ],
)
def test_constructor__tuple_uniqueness__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """Evidence ID: SV-PROV-310

    Requirement: Each request tuple field rejects a duplicate member.

    Method: Override each tuple field independently with the duplicate member partition.

    Oracle: The canonical tuple contract assigns ValueError to this invariant.

    Acceptance: Both fields raise exactly ValueError.

    Interpretation: Passing establishes duplicate member rejection independently for
    both tuple fields.

    Limitations: Other tuple invariants remain outside this evidence owner; no artifact
    existence
    claim.
    """
    with pytest.raises(ValueError):
        make_external_execution_request(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("request_id", "request-2", id="request_id_frozen_reassignment"),
        pytest.param(
            "correlation_id", "correlation-2", id="correlation_id_frozen_reassignment"
        ),
        pytest.param("attempt_id", "attempt-2", id="attempt_id_frozen_reassignment"),
        pytest.param(
            "retry_parent_request_id",
            "parent-1",
            id="retry_parent_request_id_frozen_reassignment",
        ),
        pytest.param("tool_id", "tool-2", id="tool_id_frozen_reassignment"),
        pytest.param(
            "capability_id", "capability-2", id="capability_id_frozen_reassignment"
        ),
        pytest.param(
            "installation_id",
            "installation-2",
            id="installation_id_frozen_reassignment",
        ),
        pytest.param(
            "authorization_id",
            "authorization-2",
            id="authorization_id_frozen_reassignment",
        ),
        pytest.param(
            "input_artifact_ids",
            ("input-3",),
            id="input_artifact_ids_frozen_reassignment",
        ),
        pytest.param(
            "expected_output_roles",
            ("result",),
            id="expected_output_roles_frozen_reassignment",
        ),
        pytest.param(
            "provenance_id", "provenance-2", id="provenance_id_frozen_reassignment"
        ),
    ],
)
def test_field__frozen_state__rejects_every_public_field_reassignment(
    field_name: str, replacement: object
) -> None:
    """Evidence ID: SV-PROV-220

    Requirement: Every public request field rejects post-construction reassignment.

    Method: Apply setattr independently to all eleven fields of valid frozen state.

    Oracle: Frozen dataclass semantics require FrozenInstanceError for declared fields.

    Acceptance: Every case raises exactly FrozenInstanceError.

    Interpretation: Passing establishes operational frozen assignment behavior for the
    full inventory.

    Limitations: Does not inspect private mutation mechanisms or referenced external
    resources.
    """
    record = make_external_execution_request()
    with pytest.raises(FrozenInstanceError):
        setattr(record, field_name, replacement)


@pytest.mark.parametrize(
    ("field_name", "different_value"),
    [
        pytest.param("request_id", "request-2", id="request_id_affects_equality"),
        pytest.param(
            "correlation_id", "correlation-2", id="correlation_id_affects_equality"
        ),
        pytest.param("attempt_id", "attempt-2", id="attempt_id_affects_equality"),
        pytest.param(
            "retry_parent_request_id",
            "parent-1",
            id="retry_parent_request_id_affects_equality",
        ),
        pytest.param("tool_id", "tool-2", id="tool_id_affects_equality"),
        pytest.param(
            "capability_id", "capability-2", id="capability_id_affects_equality"
        ),
        pytest.param(
            "installation_id", "installation-2", id="installation_id_affects_equality"
        ),
        pytest.param(
            "authorization_id",
            "authorization-2",
            id="authorization_id_affects_equality",
        ),
        pytest.param(
            "input_artifact_ids", ("input-3",), id="input_artifact_ids_affects_equality"
        ),
        pytest.param(
            "expected_output_roles",
            ("result",),
            id="expected_output_roles_affects_equality",
        ),
        pytest.param(
            "provenance_id", "provenance-2", id="provenance_id_affects_equality"
        ),
    ],
)
def test_method__eq__compares_every_public_field(
    field_name: str, different_value: object
) -> None:
    """Evidence ID: SV-PROV-221

    Requirement: Equality includes every field in the represented request state.

    Method: Compare baseline with identical state and with each public field
    independently
    varied.

    Oracle: Accepted dataclass equality and explicit valid alternatives define expected
    results.

    Acceptance: Identical complete state is equal; every one-field variant is unequal.

    Interpretation: Passing establishes equality participation for all eleven public
    fields.

    Limitations: Equality does not imply artifact identity, authorization validity, or
    scientific
    equivalence.
    """
    baseline = make_external_execution_request()
    assert baseline == make_external_execution_request()
    assert baseline != make_external_execution_request(**{field_name: different_value})


def test_method__eq__distinguishes_retry_parent_in_both_directions() -> None:
    """Evidence ID: SV-PROV-311

    Requirement: Absent and present retry-parent states are unequal symmetrically.

    Method: Compare otherwise identical absent-parent and distinct-present-parent
    records both
    ways.

    Oracle: Python equality symmetry and the represented optional field define False in
    each
    direction.

    Acceptance: Both operand directions compare unequal.

    Interpretation: Passing establishes symmetric inequality for absent versus present
    lineage state.

    Limitations: Does not infer retry authorization or graph-wide lineage validity.
    """
    absent = make_external_execution_request()
    present = make_external_execution_request(retry_parent_request_id="parent-1")
    assert absent != present
    assert present != absent


@pytest.mark.parametrize(
    ("field_name", "different_value"),
    [
        pytest.param(
            "input_artifact_ids",
            ("input-3",),
            id="input_artifact_ids_distinct_valid_tuple_affects_equality",
        ),
        pytest.param(
            "expected_output_roles",
            ("result",),
            id="expected_output_roles_distinct_valid_tuple_affects_equality",
        ),
    ],
)
def test_method__eq__distinguishes_distinct_valid_tuple_state(
    field_name: str, different_value: tuple[str, ...]
) -> None:
    """Evidence ID: SV-PROV-312

    Requirement: Distinct valid artifact and output-role tuple states affect equality.

    Method: Vary each tuple field with a valid canonical singleton while other state is
    fixed.

    Oracle: Exact dataclass tuple equality defines the expected unequal results.

    Acceptance: Both tuple-field variants compare unequal to baseline.

    Interpretation: Passing establishes represented tuple content affects request
    equality.

    Limitations: Does not establish artifact existence, output creation, or scientific
    equivalence.
    """
    assert make_external_execution_request() != make_external_execution_request(
        **{field_name: different_value}
    )


def test_method__eq__returns_unequal_for_unrelated_object() -> None:
    """Evidence ID: SV-PROV-313

    Requirement: A request is unequal to an unrelated Python object.

    Method: Compare valid request state with a fixed unrelated object.

    Oracle: Accepted dataclass equality returns NotImplemented across unrelated types,
    yielding
    inequality.

    Acceptance: The comparison with object() is unequal.

    Interpretation: Passing establishes the public cross-type inequality boundary.

    Limitations: Does not characterize equality with subclasses or serialized
    representations.
    """
    assert make_external_execution_request() != object()


def test_field__durable_boundary__contains_authorization_identity_only() -> None:
    """Evidence ID: SV-PROV-039

    Requirement: Declared request state includes authorization identity but excludes
    runtime and
    secret state.

    Method: Inspect the exact public dataclass field-name inventory against fixed
    prohibited
    names.

    Oracle: PUBLIC_FIELDS and the accepted durable-boundary vocabulary provide the
    expected
    sets.

    Acceptance: authorization_id is present, exact fields match, and all prohibited
    names are
    absent.

    Interpretation: Passing establishes the declared stored-field boundary for durable
    request intent.

    Limitations: Field-name inspection cannot prove absence of behavior outside declared
    stored
    state.
    """
    names = tuple(field.name for field in fields(SUT))
    assert names == PUBLIC_FIELDS
    assert "authorization_id" in names
    assert set(names).isdisjoint(
        {
            "command",
            "credential",
            "password",
            "secret",
            "client",
            "process",
            "scheduler_handle",
            "open_file",
            "mutable_runtime_service",
        }
    )
