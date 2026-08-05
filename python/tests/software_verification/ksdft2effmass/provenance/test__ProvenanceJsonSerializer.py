"""Evidence class and represented meaning
Software verification of the stateless version-1 provenance JSON ActionObject.
Owned contract, oracle, and scope
ProvenanceJsonSerializer is the SUT; fixed wire fields, RFC JSON rules, and canonical
text are the oracle.
VVUQ and scientific exclusions
Evidence excludes storage I/O, numerical verification, scientific validation, UQ,
physical correctness, and cross-language conformance.
"""

import json

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ProvenanceJsonError,
    ProvenanceJsonSerializer,
)

SUT = ProvenanceJsonSerializer
pytestmark = pytest.mark.software_verification


def test_method__serialize_canonical_text__emits_exact_sorted_compact_utf8_json() -> (
    None
):
    """Evidence ID
    SV-PROV-058
    Requirement
    Serialization emits fixed fields as compact sorted-key Unicode JSON with exactly one
    LF.
    Method
    Serialize a public artifact specification with non-ASCII path text and compare the
    literal text.
    Oracle
    The version-1 field map and manual lexical key ordering provide an independent exact
    string.
    Acceptance
    Output equals the expected literal, has one terminal LF, and round-trips through
    standard JSON parsing.
    Interpretation
    Failure indicates canonicalization or field-map drift.
    Limitations
    P2 has no floating-point output and cross-language byte conformance is not claimed
    here.
    """
    from ksdft2effmass.provenance import ArtifactSpecification

    text = SUT().serialize(
        ArtifactSpecification("café/out", "json", "result", "retain")
    )
    expected = (
        '{"format":"json","logical_path":"café/out","record_type":'
        '"artifact_specification","retention_policy":"retain","schema_version":1,'
        '"semantic_role":"result"}\n'
    )
    assert text == expected
    assert text.endswith("\n") and not text.endswith("\n\n")
    assert json.loads(text)["logical_path"] == "café/out"


def test_method__deserialize_exact_mapping__constructs_public_record() -> None:
    """Evidence ID
    SV-PROV-059
    Requirement
    Deserialization maps exact version-1 artifact identity members to their public
    record fields.
    Method
    Decode an independently assembled valid JSON literal and inspect type and value
    equality.
    Oracle
    The fixed schema field vocabulary and public constructor values determine the
    expected object.
    Acceptance
    Result is exactly ArtifactIdentity('a', digest, 2**64-1).
    Interpretation
    Failure indicates record selection, field mapping, or u64 decoding drift.
    Limitations
    Other record families are covered by fixture-wide integration evidence.
    """
    text = (
        '{"artifact_id":"a","byte_size":18446744073709551615,"record_type":"artifact_identity","schema_version":1,"sha256":"'
        + "b" * 64
        + '"}'
    )
    assert SUT().deserialize(text) == ArtifactIdentity("a", "b" * 64, 2**64 - 1)


def test_method__strict_input__rejects_prohibited_json_forms() -> None:
    """Evidence ID
    SV-PROV-060
    Requirement
    Input rejects duplicate/unknown keys, BOM, floats/nonfinite numbers,
    bool-as-integer, numeric strings, and unsupported version/type.
    Method
    Decode one representative literal from each strict invalid partition; warnings are
    not emitted or accepted.
    Oracle
    RFC 8259 plus the accepted stricter P2 parser and schema field contract classify
    every literal as invalid.
    Acceptance
    Every literal raises ProvenanceJsonError; bytes input raises TypeError.
    Interpretation
    Failure indicates a strict decoding regression or stale literal.
    Limitations
    Golden invalid fixtures provide broader lexical/path coverage.
    """
    base = (
        '"record_type":"artifact_identity","schema_version":1,"artifact_id":"a","sha256":"'
        + "a" * 64
        + '"'
    )
    invalid = (
        "\ufeff{" + base + ',"byte_size":1}',
        "{" + base + ',"byte_size":1,"byte_size":2}',
        "{" + base + ',"byte_size":1,"unknown":0}',
        "{" + base + ',"byte_size":1.0}',
        "{" + base + ',"byte_size":NaN}',
        "{" + base + ',"byte_size":true}',
        "{" + base + ',"byte_size":"1"}',
        "{"
        + base.replace('"schema_version":1', '"schema_version":2')
        + ',"byte_size":1}',
    )
    for text in invalid:
        with pytest.raises(ProvenanceJsonError):
            SUT().deserialize(text)
    with pytest.raises(TypeError):
        SUT().deserialize(b"{}")  # type: ignore[arg-type]


def test_method__canonical_round_trip__preserves_exact_value_and_text() -> None:
    """Evidence ID
    SV-PROV-061
    Requirement
    Canonical serialize-deserialize-serialize round trips preserve exact record value
    and canonical text.
    Method
    Apply both public actions to a boundary-sized ArtifactIdentity and repeat
    serialization.
    Oracle
    Exact dataclass equality and deterministic canonical text are accepted software
    contracts.
    Acceptance
    Decoded value equals the original exactly and both serialized strings are identical.
    Interpretation
    Failure indicates lossy mapping or nondeterministic output.
    Limitations
    This representative class-owned case does not replace fixture-family integration.
    """
    record = ArtifactIdentity("artifact-1", "f" * 64, 2**64 - 1)
    text = SUT().serialize(record)
    decoded = SUT().deserialize(text)
    assert decoded == record
    assert SUT().serialize(decoded) == text
