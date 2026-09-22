r"""Software verification of schema fixture family v1.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This artifact-owned module verifies corrected schema pattern inventory,
trailing-line-feed rejection, and isolated invalid-fixture meanings as exact software
wire evidence.

Intrinsic and cross-object scope

--------------------------------
The version-1 schema plus canonical valid and strict invalid fixture families are
primary. The Draft 2020-12 metaschema, Python regex behavior used by jsonschema, and
public strict serializer are independently exercised collaborators.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the declared schema/fixture software boundary. It excludes
provenance truth, numerical verification, scientific validation, UQ, persistence-system
reliability, execution validity, future-schema compatibility, portability, and
implemented Rust or other cross-language conformance.
"""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest

from ksdft2effmass import provenance

REPO_ROOT = Path(__file__).resolve().parents[6]
ROOT = REPO_ROOT / "specification/provenance/v1"
SCHEMA_PATH = ROOT / "provenance-v1.schema.json"
INVALID_ROOT = ROOT / "fixtures/invalid"
pytestmark = pytest.mark.software_verification

IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}(?![\s\S])"
SHA256_PATTERN = r"^[0-9a-f]{64}(?![\s\S])"
VERSION_PATTERN = r"^[0-9A-Za-z][0-9A-Za-z._+-]{0,63}(?![\s\S])"
VULNERABLE_IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"
VULNERABLE_SHA256_PATTERN = r"^[0-9a-f]{64}$"
VULNERABLE_VERSION_PATTERN = r"^[0-9A-Za-z][0-9A-Za-z._+-]{0,63}$"
EXPECTED_DEFINITIONS = {
    "ArtifactIdentity",
    "ArtifactIdentityVerificationResult",
    "ArtifactLocation",
    "ArtifactReference",
    "ArtifactSpecification",
    "DeclaredCapability",
    "ExecutionCorrelationResult",
    "ExternalExecutionFailure",
    "ExternalExecutionRequest",
    "ExternalExecutionResult",
    "ExternalToolIdentity",
    "ExternalToolSpecification",
    "InstallationObservation",
    "LineageRelation",
    "ProvenanceRecord",
    "RunManifest",
    "VerificationObservation",
}


def make_unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Evidence ID: Owns no identifier; supports SV-PROV-399, SV-PROV-400, and
    SV-PROV-401.

    Requirement: Construct one JSON object only when every encoded member name is
    unique.

    Method: Compare the incoming pair count with its key set before constructing a
    built-in
    dict.

    Oracle: RFC JSON object member identity and exact Python string equality define
    uniqueness.

    Acceptance: Return a dict for unique names and raise ValueError for any duplicated
    member name.

    Interpretation: Failure indicates malformed local artifact text or a strict-decoding
    oracle defect.

    Limitations: This helper does not validate schemas, fixture meaning, runtime
    records, science,
    persistence, portability, validation, or UQ.
    """
    if len(pairs) != len({key for key, _value in pairs}):
        raise ValueError("duplicate JSON object member")
    return dict(pairs)


def decode_strict_json_object(text: str) -> dict[str, Any]:
    """Evidence ID: Owns no identifier; supports SV-PROV-399, SV-PROV-400, and
    SV-PROV-401.

    Requirement: Decode one artifact as a strict finite JSON object without duplicate
    member names.

    Method: Use the standard decoder with duplicate rejection and non-finite-token
    rejection.

    Oracle: JSON object grammar excludes duplicate contract names and non-finite numeric
    tokens.

    Acceptance: Return an exact built-in dict; malformed, duplicate, non-finite, or
    nonobject input
    raises ValueError or AssertionError.

    Interpretation: Failure identifies artifact lexical/shape drift or strict-decoder
    setup failure.

    Limitations: Strict decoding establishes no schema acceptance, runtime construction,
    provenance
    truth, persistence, scientific validation, UQ, or cross-language behavior.
    """
    value = json.loads(
        text,
        object_pairs_hook=make_unique_json_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON token: {token}")
        ),
    )
    assert type(value) is dict
    return value


def collect_schema_pattern_values(value: object) -> tuple[str, ...]:
    """Evidence ID: Owns no identifier; supports SV-PROV-399.

    Requirement: Expose every decoded JSON Schema ``pattern`` value without inspecting
    raw text.

    Method: Recursively traverse object values and array elements and retain pattern
    values.

    Oracle: The decoded JSON member name ``pattern`` independently identifies regex
    locations.

    Acceptance: Return one string entry for every recursively encountered pattern
    member.

    Interpretation: Failure indicates schema traversal, decoded type, or pattern-member
    shape drift.

    Limitations: Inventory traversal does not establish regex semantics, schema
    completeness,
    runtime behavior, scientific validation, UQ, persistence, or portability.
    """
    if isinstance(value, dict):
        own_pattern = () if "pattern" not in value else (value["pattern"],)
        assert all(type(pattern) is str for pattern in own_pattern)
        descendants = tuple(
            pattern
            for child in value.values()
            for pattern in collect_schema_pattern_values(child)
        )
        return own_pattern + descendants
    if isinstance(value, list):
        return tuple(
            pattern
            for child in value
            for pattern in collect_schema_pattern_values(child)
        )
    return ()


def make_schema_fixture_validator() -> jsonschema.Draft202012Validator:
    """Evidence ID: Owns no identifier; supports SV-PROV-400 and SV-PROV-401.

    Requirement: Build the complete local Draft 2020-12 validator with the active NFC
    checker.

    Method: Strictly decode the fixed schema, compile it, and register exact Unicode NFC
    normalization with jsonschema's format-checker boundary.

    Oracle: The checked-in schema, Draft 2020-12 metaschema, and unicodedata NFC
    transform are
    independent inputs to the fixture checks.

    Acceptance: Return a compiled validator that applies built-in formats and active
    ``nfc`` checks.

    Interpretation: Failure is schema/compiler/NFC setup drift, not fixture acceptance
    evidence.

    Limitations: This helper does not prove fixture classification, runtime mapping,
    provenance
    truth,
    persistence, execution validity, scientific validation, UQ, or portability.
    """
    schema = decode_strict_json_object(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    checker = jsonschema.FormatChecker()
    checker.checks("nfc")(
        lambda value: (
            type(value) is str and unicodedata.normalize("NFC", value) == value
        )
    )
    return jsonschema.Draft202012Validator(schema, format_checker=checker)


def test_artifact__schema_patterns__use_exact_end_of_input_contract() -> None:
    """Evidence ID: SV-PROV-399

    Requirement: The version-1 schema has exact corrected pattern counts, no vulnerable
    variants, and
    unchanged record, path-pattern, and timestamp-pattern inventories.

    Method: Strictly decode and compile the schema, recursively count decoded pattern
    values,
    compare exact definitions/references, and validate ordinary and final-LF strings
    through three Draft 2020-12 pattern validators.

    Oracle: Explicit accepted counts, names, refs, regex strings, and representative
    strings are
    independent of the schema's repeated locations.

    Acceptance: Counts are 73 identifier, 5 digest, 2 version, and zero old variants;
    all 17 record
    names/refs, 5 path patterns, and 3 timestamp patterns remain exact; ordinary values
    pass and the corresponding final-LF values raise ValidationError.

    Interpretation: Failure identifies schema JSON, dialect, metaschema, inventory, or
    end-anchor drift.

    Limitations: This mechanical inventory does not establish all schema semantics,
    fixture
    classification, runtime construction, provenance truth, validation, UQ, or storage.
    """
    schema = decode_strict_json_object(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    jsonschema.Draft202012Validator.check_schema(schema)
    assert len(schema["$defs"]) == 17
    assert set(schema["$defs"]) == EXPECTED_DEFINITIONS
    references = tuple(entry["$ref"] for entry in schema["oneOf"])
    assert len(references) == 17
    assert len(references) == len(set(references))
    assert set(references) == {
        f"#/$defs/{definition}" for definition in EXPECTED_DEFINITIONS
    }

    patterns = Counter(collect_schema_pattern_values(schema))
    assert patterns[IDENTIFIER_PATTERN] == 73
    assert patterns[SHA256_PATTERN] == 5
    assert patterns[VERSION_PATTERN] == 2
    assert patterns[VULNERABLE_IDENTIFIER_PATTERN] == 0
    assert patterns[VULNERABLE_SHA256_PATTERN] == 0
    assert patterns[VULNERABLE_VERSION_PATTERN] == 0
    assert sum("(?:[cC][oO][nN]" in pattern for pattern in patterns) == 1
    assert (
        patterns[
            r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T"
            r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\dZ$"
        ]
        == 3
    )
    assert (
        sum(
            count for pattern, count in patterns.items() if "(?:[cC][oO][nN]" in pattern
        )
        == 5
    )

    identifier_validator = jsonschema.Draft202012Validator(
        {"type": "string", "pattern": IDENTIFIER_PATTERN}
    )
    digest_validator = jsonschema.Draft202012Validator(
        {"type": "string", "pattern": SHA256_PATTERN}
    )
    version_validator = jsonschema.Draft202012Validator(
        {"type": "string", "pattern": VERSION_PATTERN}
    )
    identifier_validator.validate("artifact.input")
    digest_validator.validate("0" * 64)
    version_validator.validate("1.0.0")
    with pytest.raises(jsonschema.ValidationError):
        identifier_validator.validate("artifact.input\n")
    with pytest.raises(jsonschema.ValidationError):
        digest_validator.validate("0" * 64 + "\n")
    with pytest.raises(jsonschema.ValidationError):
        version_validator.validate("1.0.0\n")


@pytest.mark.parametrize(
    ("fixture_name", "record_type", "field_name", "invalid_value"),
    (
        pytest.param(
            "trailing-line-feed-identifier.json",
            "artifact_identity",
            "artifact_id",
            "artifact.input\n",
            id="identifier",
        ),
        pytest.param(
            "trailing-line-feed-sha256.json",
            "artifact_identity",
            "sha256",
            "0" * 64 + "\n",
            id="sha256",
        ),
        pytest.param(
            "trailing-line-feed-requested-version.json",
            "external_tool_specification",
            "requested_version",
            "1.0.0\n",
            id="requested_version",
        ),
        pytest.param(
            "trailing-line-feed-observed-version.json",
            "installation_observation",
            "observed_version",
            "1.0.0\n",
            id="observed_version",
        ),
    ),
)
def test_artifact__trailing_line_feed_fixtures__fail_schema_and_runtime(
    fixture_name: str,
    record_type: str,
    field_name: str,
    invalid_value: str,
) -> None:
    """Evidence ID: SV-PROV-400

    Requirement: Each otherwise-valid trailing-LF fixture is canonical JSON rejected by
    both the
    complete schema and strict public runtime at its named pattern field.

    Method: Strictly decode original text, assert exact field and canonical bytes,
    require both
    rejection layers, then remove only the value's final LF and require both layers
    pass.

    Oracle: Four explicit record/field/value cases and canonical JSON rules
    independently define
    the controlled defect and corrected counterpart.

    Acceptance: Original text has one file LF and escaped value LF, raises schema
    ValidationError
    and ProvenanceJsonError, while the one-field counterpart passes both layers.

    Interpretation: Failure identifies fixture isolation/canonicalization, pattern,
    schema, or runtime
    strictness drift.

    Limitations: Four representatives do not exhaust string locations or establish
    provenance truth,
    persistence, execution validity, validation, UQ, or cross-language conformance.
    """
    path = INVALID_ROOT / fixture_name
    text = path.read_text(encoding="utf-8")
    payload = decode_strict_json_object(text)
    assert text.count("\n") == 1
    assert (
        text
        == json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    assert payload["record_type"] == record_type
    assert payload[field_name] == invalid_value
    validator = make_schema_fixture_validator()
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(payload)
    with pytest.raises(provenance.ProvenanceJsonError):
        provenance.ProvenanceJsonSerializer().deserialize(text)

    corrected = dict(payload)
    corrected[field_name] = invalid_value[:-1]
    corrected_text = (
        json.dumps(corrected, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    validator.validate(corrected)
    provenance.ProvenanceJsonSerializer().deserialize(corrected_text)


@pytest.mark.parametrize(
    ("fixture_name", "schema_rejects_original"),
    (
        pytest.param(
            "legacy-manifest-arguments.json",
            True,
            id="legacy_manifest_arguments",
        ),
        pytest.param(
            "legacy-manifest-environment.json",
            True,
            id="legacy_manifest_environment",
        ),
        pytest.param("missing-attempt-id.json", True, id="missing_attempt_id"),
        pytest.param(
            "impossible-calendar-date.json", True, id="impossible_calendar_date"
        ),
        pytest.param("surrogate.json", True, id="surrogate"),
    ),
)
def test_artifact__corrected_invalid_fixtures__isolate_named_defect(
    fixture_name: str,
    schema_rejects_original: bool,
) -> None:
    """Evidence ID: SV-PROV-401

    Requirement: Each retained invalid fixture contains its exact named defect and forms
    a complete
    schema-valid and runtime-valid record after one local correction.

    Method: Strictly decode canonical original text, assert and remove/change only the
    named
    feature, compare original schema classification with its explicit layer expectation,
    require runtime rejection, and pass the counterpart through both layers.

    Oracle: Explicit removed fields, required attempt ID, calendar dates, sorted roles,
    valid
    identifier, and schema-layer expectations independently define each counterpart.

    Acceptance: Each original has one exact defect and expected schema classification,
    always fails
    runtime, and has a one-feature counterpart that passes both layers.

    Interpretation: Failure identifies unrelated fixture defects, canonical drift, or
    schema/runtime
    classification disagreement.

    Limitations: The surrogate scalar also violates identifier grammar if scalar
    prechecking is
    absent; this case does not prove ordering of every runtime validation layer, nor
    provenance truth, persistence, execution validity, scientific validation, or UQ.
    """
    path = INVALID_ROOT / fixture_name
    text = path.read_text(encoding="utf-8")
    payload = decode_strict_json_object(text)
    assert text.count("\n") == 1
    assert (
        text
        == json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    corrected = dict(payload)

    if fixture_name == "legacy-manifest-arguments.json":
        assert payload["argument_vector"] == ["--password", "secret"]
        assert payload["started_at"] == "2026-08-05T15:00:00Z"
        assert payload["finished_at"] == "2026-08-05T15:01:00Z"
        corrected.pop("argument_vector")
    elif fixture_name == "legacy-manifest-environment.json":
        assert payload["environment"] == [{"name": "PASSWORD", "value": "secret"}]
        assert payload["started_at"] == "2026-08-05T15:00:00Z"
        assert payload["finished_at"] == "2026-08-05T15:01:00Z"
        corrected.pop("environment")
    elif fixture_name == "missing-attempt-id.json":
        assert "attempt_id" not in payload
        assert payload["expected_output_roles"] == ["a", "z"]
        corrected["attempt_id"] = "attempt.1"
    elif fixture_name == "impossible-calendar-date.json":
        assert payload["started_at"] == "2026-02-28T12:00:00Z"
        assert payload["finished_at"] == "2026-02-31T12:00:01Z"
        corrected["finished_at"] = "2026-02-28T12:00:01Z"
    else:
        assert fixture_name == "surrogate.json"
        assert payload["artifact_id"] == "artifact.\ud800"
        assert set(payload) == {
            "artifact_id",
            "byte_size",
            "record_type",
            "schema_version",
            "sha256",
        }
        corrected["artifact_id"] = "artifact.input"

    validator = make_schema_fixture_validator()
    assert bool(tuple(validator.iter_errors(payload))) is schema_rejects_original
    with pytest.raises(provenance.ProvenanceJsonError):
        provenance.ProvenanceJsonSerializer().deserialize(text)
    validator.validate(corrected)
    corrected_text = (
        json.dumps(corrected, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    provenance.ProvenanceJsonSerializer().deserialize(corrected_text)
