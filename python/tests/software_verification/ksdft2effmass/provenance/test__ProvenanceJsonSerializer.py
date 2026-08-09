r"""Software verification of ``ProvenanceJsonSerializer``.

Facet and represented meaning

-----------------------------
The evidence verifies canonical version-1 JSON serialization, representative exact
deserialization, strict input rejection, public exception translation,
deterministic round trips, and unsupported-record rejection.

Intrinsic and cross-object scope

--------------------------------
``ProvenanceJsonSerializer`` is the sole primary SUT. ``ProvenanceJsonError`` and
supported public records are collaborators and expected outputs. Fixed version-1
wire members, Python JSON semantics, public record constructors, and exact text
literals provide the bounded software oracles.

VVUQ and scientific exclusions

------------------------------
The evidence does not establish filesystem storage, artifact existence, complete
schema-family agreement, Rust conformance, numerical verification, scientific
validation, uncertainty quantification, physical correctness, or provenance truth.
"""

import json
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ArtifactSpecification,
    ProvenanceJsonError,
    ProvenanceJsonSerializer,
)

SUT = ProvenanceJsonSerializer
pytestmark = pytest.mark.software_verification


def test_method__serialize__emits_exact_sorted_compact_utf8_json_with_one_lf() -> None:
    """Evidence ID: SV-PROV-058

    Requirement: serialize emits the exact version-1 mapping as sorted, compact JSON
    text,
    preserves non-ASCII Unicode, and appends exactly one line feed.

    Method: Serialize an ArtifactSpecification containing ``café`` and compare with a
    manually ordered literal before parsing that literal with standard-library JSON.

    Oracle: The accepted field mapping and lexicographic key order determine the
    literal;
    compact separators, unescaped Unicode, and one terminal LF are exact contracts.

    Acceptance: Text equals the fixed literal, contains ``café``, ends in one but not
    two LFs,
    and ``json.loads`` returns the independently written expected mapping.

    Interpretation: Failure identifies serializer field-map, ordering, separator,
    Unicode, LF, or
    ordinary JSON syntax drift.

    Limitations: This representative record does not establish every record-family
    mapping,
    schema-family agreement, storage behavior, or cross-language conformance.
    """
    text = SUT().serialize(
        ArtifactSpecification("café/out", "json", "result", "retain")
    )
    expected = (
        '{"format":"json","logical_path":"café/out","record_type":'
        '"artifact_specification","retention_policy":"retain","schema_version":1,'
        '"semantic_role":"result"}\n'
    )
    assert text == expected
    assert "café" in text
    assert text.endswith("\n")
    assert not text.endswith("\n\n")
    assert json.loads(text) == {
        "format": "json",
        "logical_path": "café/out",
        "record_type": "artifact_specification",
        "retention_policy": "retain",
        "schema_version": 1,
        "semantic_role": "result",
    }


def test_method__deserialize__constructs_exact_public_record_from_valid_mapping() -> (
    None
):
    """Evidence ID: SV-PROV-059

    Requirement: deserialize maps an exact valid artifact-identity object to the
    corresponding
    public record, including the accepted maximum unsigned 64-bit byte size.

    Method: Decode an independently assembled JSON literal with byte_size equal to
    ``2**64 - 1`` and compare exact runtime type and represented value.

    Oracle: The version-1 artifact-identity vocabulary and public ArtifactIdentity
    constructor establish the expected record independently of deserialization.

    Acceptance: The result type is exactly ArtifactIdentity and the value equals
    ``ArtifactIdentity("a", "b" * 64, 2**64 - 1)``.

    Interpretation: Failure identifies record selection, member mapping, digest,
    identifier, or
    accepted maximum-integer boundary drift.

    Limitations: This one mapping does not replace later fixture and wire-contract
    evidence for
    the complete supported record family.
    """
    text = (
        '{"artifact_id":"a","byte_size":18446744073709551615,'
        '"record_type":"artifact_identity","schema_version":1,"sha256":"'
        + "b" * 64
        + '"}'
    )
    result = SUT().deserialize(text)
    assert type(result) is ArtifactIdentity
    assert result == ArtifactIdentity("a", "b" * 64, 2**64 - 1)


def test_method__deserialize__rejects_bytes_input_semantic_type() -> None:
    """Evidence ID: SV-PROV-378

    Requirement: deserialize accepts only built-in string text and rejects bytes without
    attempting JSON decoding.

    Method: Pass the bytes value ``b"{}"`` through the public method using a static-only
    cast that does not alter its runtime type.

    Oracle: The public signature and strict runtime contract admit built-in str only.

    Acceptance: The exact raised exception type is TypeError.

    Interpretation: Failure identifies input semantic-type enforcement drift at the
    public method.

    Limitations: This case does not classify malformed string syntax or other non-string
    types.
    """
    with pytest.raises(TypeError) as error:
        SUT().deserialize(cast(Any, b"{}"))
    assert type(error.value) is TypeError


def test_method__deserialize__translates_malformed_json_to_public_error() -> None:
    """Evidence ID: SV-PROV-057

    Requirement: deserialize translates syntactically incomplete JSON to the exact
    public
    ProvenanceJsonError boundary without leaking json.JSONDecodeError.

    Method: Decode the incomplete object text ``{`` through the public serializer.

    Oracle: Standard JSON grammar independently classifies an unclosed object as
    malformed,
    while the accepted API requires public error translation.

    Acceptance: The exact raised type is ProvenanceJsonError and is not JSONDecodeError.

    Interpretation: Failure identifies malformed-syntax acceptance or public
    exception-translation
    drift.

    Limitations: This controlled malformed literal does not verify every JSON syntax
    failure or
    the correctness of the standard-library decoder.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize("{")
    assert type(error.value) is ProvenanceJsonError
    assert not isinstance(error.value, json.JSONDecodeError)


def test_method__deserialize__rejects_duplicate_object_member() -> None:
    """Evidence ID: SV-PROV-060

    Requirement: deserialize rejects an exact duplicate member through the public
    ProvenanceJsonError boundary.

    Method: Decode an otherwise valid artifact identity containing two ``byte_size``
    members.

    Oracle: The strict version-1 input contract prohibits duplicate JSON object names.

    Acceptance: The exact raised type is ProvenanceJsonError, with no private exception
    exposed.

    Interpretation: Failure identifies duplicate detection or public error-boundary
    drift.

    Limitations: This case covers one duplicate root member and not all duplicate
    positions.
    """
    text = (
        '{"artifact_id":"a","byte_size":1,"byte_size":2,'
        '"record_type":"artifact_identity","schema_version":1,"sha256":"'
        + "a" * 64
        + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_unknown_root_member() -> None:
    """Evidence ID: SV-PROV-379

    Requirement: deserialize rejects a root member outside the exact artifact-identity
    vocabulary.

    Method: Decode an otherwise valid mapping with the additional member ``unknown``.

    Oracle: The accepted version-1 artifact-identity mapping has exactly five root
    members.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies permissive unknown-member handling or
    record-vocabulary drift.

    Limitations: This case covers an unknown root member, not unknown members in nested
    records.
    """
    text = (
        '{"artifact_id":"a","byte_size":1,"record_type":"artifact_identity",'
        '"schema_version":1,"sha256":"' + "a" * 64 + '","unknown":0}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_leading_unicode_byte_order_mark() -> None:
    """Evidence ID: SV-PROV-380

    Requirement: deserialize rejects a leading U+FEFF byte-order mark in Python text.

    Method: Prefix a minimal JSON object with the Unicode BOM character and call
    deserialize.

    Oracle: The accepted strict-input contract explicitly prohibits a leading text BOM.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies BOM-boundary enforcement drift.

    Limitations: The Python API receives text, so this case does not exercise byte
    decoding.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize("\ufeff{}")
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_floating_point_json_number() -> None:
    """Evidence ID: SV-PROV-381

    Requirement: deserialize rejects ordinary floating-point JSON numbers in version-1
    records.

    Method: Supply ``1.0`` where artifact-identity byte_size requires an integer.

    Oracle: The strict parser prohibits every decoded float and byte_size requires an
    integer.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies floating-point acceptance or strict scalar-check
    drift.

    Limitations: This case covers one finite float spelling and makes no numerical
    claim.
    """
    text = (
        '{"artifact_id":"a","byte_size":1.0,"record_type":"artifact_identity",'
        '"schema_version":1,"sha256":"' + "a" * 64 + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


@pytest.mark.parametrize(
    "constant",
    [
        pytest.param("NaN", id="nan_constant"),
        pytest.param("Infinity", id="positive_infinity_constant"),
        pytest.param("-Infinity", id="negative_infinity_constant"),
    ],
)
def test_method__deserialize__rejects_nonfinite_json_constant(constant: str) -> None:
    """Evidence ID: SV-PROV-382

    Requirement: deserialize rejects each non-finite constant spelling accepted as an
    extension by
    the standard-library JSON decoder.

    Method: Parameterize NaN, positive Infinity, and negative Infinity as ``byte_size``
    with
    explicit semantic case IDs.

    Oracle: The strict version-1 JSON contract prohibits all three non-finite constants.

    Acceptance: Every parameter raises exactly ProvenanceJsonError.

    Interpretation: Failure identifies a specific non-finite constant escaping public
    rejection.

    Limitations: The cases verify rejection only and do not assign numerical meaning to
    constants.
    """
    text = (
        '{"artifact_id":"a","byte_size":'
        + constant
        + ',"record_type":"artifact_identity","schema_version":1,"sha256":"'
        + "a" * 64
        + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_boolean_as_integer_field() -> None:
    """Evidence ID: SV-PROV-383

    Requirement: deserialize rejects JSON true where byte_size requires a built-in
    integer.

    Method: Decode an artifact identity whose byte_size member is the JSON boolean
    ``true``.

    Oracle: The public ArtifactIdentity contract rejects bool despite Python bool
    subclassing int.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies boolean-lookalike coercion or error-translation
    drift.

    Limitations: This case covers byte_size and does not inventory every integer field.
    """
    text = (
        '{"artifact_id":"a","byte_size":true,"record_type":"artifact_identity",'
        '"schema_version":1,"sha256":"' + "a" * 64 + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_numeric_string_as_integer_field() -> None:
    """Evidence ID: SV-PROV-384

    Requirement: deserialize rejects a numeric string where byte_size requires a
    built-in integer.

    Method: Decode an artifact identity whose byte_size member is the JSON string
    ``"1"``.

    Oracle: The public ArtifactIdentity contract does not coerce numeric strings to
    integers.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies prohibited numeric-string coercion or translation
    drift.

    Limitations: This case covers one positive numeric string in byte_size only.
    """
    text = (
        '{"artifact_id":"a","byte_size":"1","record_type":"artifact_identity",'
        '"schema_version":1,"sha256":"' + "a" * 64 + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_unsupported_integer_schema_version() -> None:
    """Evidence ID: SV-PROV-385

    Requirement: deserialize rejects an integer schema version other than version 1.

    Method: Decode a discriminator mapping with schema_version equal to integer 2.

    Oracle: The accepted serializer wire contract supports exactly schema version 1.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies unsupported-version acceptance or discriminator
    drift.

    Limitations: This case does not define migration behavior for future schema
    versions.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":"artifact_identity","schema_version":2}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_schema_version_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-386

    Requirement: deserialize rejects a string lookalike for the integer schema
    discriminator.

    Method: Decode a discriminator mapping with schema_version equal to JSON string
    ``"1"``.

    Oracle: The wire contract requires schema_version to have built-in integer
    semantics.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies schema-version type coercion or discriminator
    drift.

    Limitations: This case covers the numeric-string lookalike and not all JSON semantic
    types.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":"artifact_identity","schema_version":"1"}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_boolean_schema_version_lookalike() -> None:
    """Evidence ID: SV-PROV-387

    Requirement: deserialize rejects JSON true as a bool lookalike for integer schema
    version 1.

    Method: Decode a discriminator mapping with schema_version equal to JSON ``true``.

    Oracle: The contract requires exact built-in int type and excludes bool subclass
    behavior.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies bool-as-integer acceptance at the schema
    discriminator.

    Limitations: This case is specific to the schema-version discriminator.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":"artifact_identity","schema_version":true}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_missing_record_type_discriminator() -> None:
    """Evidence ID: SV-PROV-388

    Requirement: deserialize requires the root record_type discriminator.

    Method: Decode an object containing schema_version but no record_type member.

    Oracle: Every supported version-1 root mapping requires both discriminators.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies missing-discriminator acceptance or root
    validation drift.

    Limitations: The case stops before record-specific field completeness is evaluated.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"schema_version":1}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_missing_schema_version_discriminator() -> None:
    """Evidence ID: SV-PROV-394

    Requirement: deserialize requires the root schema_version discriminator
    independently of
    the record_type discriminator.

    Method: Decode ``{"record_type":"artifact_identity"}``, which contains record_type
    but omits schema_version.

    Oracle: Every supported version-1 root object requires both discriminators; this
    literal isolates the missing-schema_version partition.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies asymmetric missing-discriminator enforcement; a
    pass
    complements rather than duplicates the missing-record_type evidence.

    Limitations: This case does not test record-specific required fields or future
    schema
    migration behavior.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":"artifact_identity"}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_record_type_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-389

    Requirement: deserialize requires record_type to be a built-in JSON string.

    Method: Decode a root object whose record_type discriminator is integer 1.

    Oracle: The version-1 discriminator contract defines record_type as a string.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies record-type coercion or semantic-type enforcement
    drift.

    Limitations: This case covers one non-string semantic type.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":1,"schema_version":1}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_unsupported_record_type_value() -> None:
    """Evidence ID: SV-PROV-390

    Requirement: deserialize rejects a string record_type outside the supported public
    record set.

    Method: Decode a root mapping with the syntactically valid string ``unsupported``.

    Oracle: The accepted version-1 record-type vocabulary does not contain
    ``unsupported``.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies unintended expansion or unsupported-discriminator
    acceptance.

    Limitations: Complete supported-family agreement remains owned by fixture and wire
    artifacts.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize('{"record_type":"unsupported","schema_version":1}')
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_non_object_root() -> None:
    """Evidence ID: SV-PROV-391

    Requirement: deserialize requires the decoded JSON root to be an object.

    Method: Decode the valid JSON array literal ``[]`` through the public method.

    Oracle: Every supported version-1 provenance record has an object root.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies root-boundary acceptance of a non-record JSON
    value.

    Limitations: This representative case covers an array root rather than every scalar
    root type.
    """
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize("[]")
    assert type(error.value) is ProvenanceJsonError


def test_method__deserialize__rejects_decoded_unicode_surrogate() -> None:
    """Evidence ID: SV-PROV-392

    Requirement: deserialize rejects JSON text that decodes to a string containing a
    Unicode
    surrogate code point.

    Method: Supply an artifact_id encoded as the JSON escape ``\\ud800`` in an otherwise
    valid artifact-identity mapping.

    Oracle: U+D800 is in the surrogate range prohibited by the strict version-1 text
    contract.

    Acceptance: The exact raised type is ProvenanceJsonError.

    Interpretation: Failure identifies surrogate scanning or public strict-Unicode
    enforcement drift.

    Limitations: This case covers one high-surrogate code point in a root string value.
    """
    text = (
        '{"artifact_id":"\\ud800","byte_size":1,'
        '"record_type":"artifact_identity","schema_version":1,"sha256":"'
        + "a" * 64
        + '"}'
    )
    with pytest.raises(ProvenanceJsonError) as error:
        SUT().deserialize(text)
    assert type(error.value) is ProvenanceJsonError


def test_method__serialize__rejects_unsupported_record_type() -> None:
    """Evidence ID: SV-PROV-393

    Requirement: serialize rejects objects outside the explicitly supported public
    record union.

    Method: Pass a fresh built-in object through a static-only cast to the public
    method.

    Oracle: The accepted serializer contract does not include bare object instances.

    Acceptance: The exact raised type is TypeError.

    Interpretation: Failure identifies unintended record-set broadening or wrong error
    taxonomy.

    Limitations: This case does not enumerate every unsupported Python class.
    """
    with pytest.raises(TypeError) as error:
        SUT().serialize(cast(Any, object()))
    assert type(error.value) is TypeError


def test_method__serialize_deserialize__preserves_exact_record_and_canonical_text() -> (
    None
):
    """Evidence ID: SV-PROV-061

    Requirement: Composing serialize, deserialize, and serialize preserves one exact
    public record
    and its canonical Python text including the single terminal LF.

    Method: Serialize a maximum-byte-size ArtifactIdentity, deserialize it, and
    serialize the
    result again through the two public methods whose composition defines round trip.

    Oracle: Exact immutable-record equality and the first canonical text are independent
    exact
    acceptance values for the decoded record and second serialization.

    Acceptance: The decoded record equals the original, reserialized text is
    byte-for-byte equal
    as Python text, and both texts end in exactly one LF.

    Interpretation: Failure identifies lossy representative mapping, nondeterministic
    text, or LF drift.

    Limitations: One representative composed round trip is not complete record-family,
    schema,
    fixture, Rust, numerical, scientific-validation, or UQ evidence.
    """
    record = ArtifactIdentity("artifact-1", "f" * 64, 2**64 - 1)
    text = SUT().serialize(record)
    decoded = SUT().deserialize(text)
    reserialized = SUT().serialize(decoded)
    assert decoded == record
    assert reserialized == text
    assert text.endswith("\n") and not text.endswith("\n\n")
    assert reserialized.endswith("\n") and not reserialized.endswith("\n\n")
