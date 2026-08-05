"""Evidence class and represented meaning
Software verification of version-1 golden fixtures against schema and Python runtime.
Owned contract, oracle, and scope
The valid/invalid fixture families and runtime/schema interoperability are the artifact
owner and classification oracle.
VVUQ and scientific exclusions
Evidence excludes scientific truth, numerical verification, scientific validation, UQ,
storage behavior, and cross-language conformance.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import jsonschema  # type: ignore[import-untyped]
import pytest

from ksdft2effmass.provenance import ProvenanceJsonError, ProvenanceJsonSerializer

REPO_ROOT = Path(__file__).resolve().parents[5]
ROOT = REPO_ROOT / "specification/provenance/v1"
VALID = tuple(sorted((ROOT / "fixtures/valid").glob("*.json")))
INVALID = tuple(sorted((ROOT / "fixtures/invalid").glob("*.json")))
pytestmark = pytest.mark.software_verification


def _validator() -> jsonschema.Draft202012Validator:
    """Evidence ID
    Supports SV-PROV-067 and owns no separate identifier.
    Requirement
    Build a local Draft 2020-12 validator that actively checks NFC.
    Method
    Load the fixed schema and register Unicode NFC normalization as the format oracle.
    Oracle
    Python unicodedata and the public schema independently define the checker.
    Acceptance
    Return a validator without network access.
    Interpretation
    Helper failure is schema setup failure only.
    Limitations
    Strict lexical JSON features remain owned by the runtime parser.
    """
    schema = json.loads(
        (ROOT / "provenance-v1.schema.json").read_text(encoding="utf-8")
    )
    checker = jsonschema.FormatChecker()

    @checker.checks("nfc")
    def is_nfc(value: object) -> bool:
        return type(value) is str and unicodedata.normalize("NFC", value) == value

    return jsonschema.Draft202012Validator(schema, format_checker=checker)


def test_artifact__valid_fixtures__pass_schema_runtime_and_round_trip() -> None:
    """Evidence ID
    SV-PROV-067
    Requirement
    Every maintained valid fixture satisfies the public schema, decodes to a public
    record, and is canonical round-trip text.
    Method
    Discover the semantic valid family, validate decoded JSON, deserialize strict text,
    and serialize the record again.
    Oracle
    Directory classification, public schema, and checked-in canonical fixture text are
    independent artifacts.
    Acceptance
    The family is nonempty; each schema validation succeeds and serializer output equals
    original text exactly.
    Interpretation
    Failure may indicate schema, fixture, runtime, canonicalization, or library drift.
    Limitations
    Fixture quantity is not an acceptance condition and represented metadata is
    synthetic.
    """
    assert VALID
    validator = _validator()
    serializer = ProvenanceJsonSerializer()
    for path in VALID:
        text = path.read_text(encoding="utf-8")
        validator.validate(json.loads(text))
        record = serializer.deserialize(text)
        assert serializer.serialize(record) == text, path


def test_artifact__invalid_fixture_family__is_rejected_by_strict_runtime() -> None:
    """Evidence ID
    SV-PROV-068
    Requirement
    Every maintained invalid fixture is rejected at the strict public Python JSON
    boundary.
    Method
    Discover the semantic invalid family and deserialize each raw UTF-8 text without
    permissive preprocessing.
    Oracle
    The checked-in invalid classification covers duplicate, unknown, BOM, malformed,
    Unicode, numeric, path, ordering, and legacy-field cases.
    Acceptance
    The family is nonempty and each fixture raises ProvenanceJsonError.
    Interpretation
    Failure may indicate runtime permissiveness, fixture misclassification, or contract
    drift.
    Limitations
    Fixture quantity is not an acceptance condition; JSON Schema alone cannot detect
    every raw-text defect.
    """
    assert INVALID
    serializer = ProvenanceJsonSerializer()
    for path in INVALID:
        with pytest.raises(ProvenanceJsonError):
            serializer.deserialize(path.read_text(encoding="utf-8"))


def test_artifact__fixture_types__cover_serializable_schema_inventory() -> None:
    """Evidence ID
    SV-PROV-069
    Requirement
    Valid fixtures provide one canonical runtime representative for every schema record
    definition.
    Method
    Extract record_type from each valid fixture and compare with record_type constants
    in every schema definition.
    Oracle
    Fixed schema constants and independently maintained fixture objects define both
    inventories.
    Acceptance
    Record-type sets are equal and fixture stems equal their record_type values.
    Interpretation
    Failure indicates missing, extra, or misnamed interoperability fixtures.
    Limitations
    One representative does not exhaust each record's input domain.
    """
    schema = json.loads(
        (ROOT / "provenance-v1.schema.json").read_text(encoding="utf-8")
    )
    fixture_types = set()
    for path in VALID:
        record_type = json.loads(path.read_text(encoding="utf-8"))["record_type"]
        assert path.stem == record_type
        fixture_types.add(record_type)
    schema_types = {
        definition["properties"]["record_type"]["const"]
        for definition in schema["$defs"].values()
    }
    assert fixture_types == schema_types


def test_artifact__corrected_invalid_fixtures__reject_legacy_channels() -> None:
    """Evidence ID
    SV-PROV-079
    Requirement
    Golden invalid fixtures explicitly retain rejection evidence for removed
    environment/argument/detail/message channels, raw versions, impossible dates, and
    missing attempts.
    Method
    Require the fixed semantic fixture stems, then pass each raw text to the strict
    public deserializer.
    Oracle
    The corrected version-1 contract classifies each named legacy or unsafe shape as
    invalid independently of discovery count.
    Acceptance
    Every required fixture exists and each raises ProvenanceJsonError.
    Interpretation
    Failure indicates missing retained evidence, unknown-key permissiveness, or
    runtime/schema correction drift.
    Limitations
    Credential detection inside arbitrary opaque external artifacts is excluded.
    """
    required = {
        "impossible-calendar-date",
        "legacy-environment-record",
        "legacy-failure-message",
        "legacy-manifest-arguments",
        "legacy-manifest-environment",
        "legacy-verification-detail",
        "missing-attempt-id",
        "raw-observed-version",
        "raw-requested-version",
        "unknown-key",
    }
    by_stem = {path.stem: path for path in INVALID}
    assert required <= set(by_stem)
    serializer = ProvenanceJsonSerializer()
    for stem in sorted(required):
        with pytest.raises(ProvenanceJsonError):
            serializer.deserialize(by_stem[stem].read_text(encoding="utf-8"))
