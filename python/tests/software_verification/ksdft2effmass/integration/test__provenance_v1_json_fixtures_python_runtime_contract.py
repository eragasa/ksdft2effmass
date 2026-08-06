r"""Software verification of version-1 provenance JSON fixture/runtime interoperability.

Facet and represented meaning
-----------------------------
This artifact-owned module verifies version-1 golden JSON fixtures against the public
schema and Python runtime serializer boundary.

Intrinsic and cross-object scope
--------------------------------
The fixture families, schema, and Python runtime relation are primary; public schema
validation, strict deserialization, and canonical serialization are collaborators.

VVUQ and scientific exclusions
------------------------------
Pass/failure concerns nonnumerical software interoperability only. Evidence excludes
numerical verification, scientific validation, UQ, physical correctness, portability,
filesystem behavior beyond reading checked-in fixtures, and cross-language conformance.
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


def is_nfc_text(value: object) -> bool:
    """Evidence ID
    Owns no identifier; supports SV-PROV-067.
    Requirement
    Provide the active NFC predicate used by valid-fixture schema evidence.
    Method
    Accept one decoded schema value and compare it with Unicode NFC normalization.
    Oracle
    Python unicodedata.normalize defines NFC independently of the production serializer.
    Acceptance
    Return true exactly for built-in strings already in NFC.
    Interpretation
    Failure is schema-evidence setup/oracle failure, not an independent runtime result.
    Limitations
    This helper does not validate JSON parsing, record construction, scientific
    meaning, UQ, portability, or cross-language behavior.
    """
    return type(value) is str and unicodedata.normalize("NFC", value) == value


def make_provenance_schema_validator() -> jsonschema.Draft202012Validator:
    """Evidence ID
    Owns no identifier; supports SV-PROV-067 and SV-PROV-103.
    Requirement
    Provide local Draft 2020-12 schema checking with active Unicode NFC format checks.
    Method
    Load the fixed public schema and register Python NFC normalization without
    network access.
    Oracle
    The checked-in schema and Python unicodedata definition independently define checks.
    Acceptance
    Return a configured validator for the two named artifact evidence owners.
    Interpretation
    Failure is evidence setup failure, not an independent schema/runtime test result.
    Limitations
    The helper does not validate strict lexical JSON, scientific meaning, UQ,
    portability, or cross-language behavior.
    """
    schema = json.loads(
        (ROOT / "provenance-v1.schema.json").read_text(encoding="utf-8")
    )
    checker = jsonschema.FormatChecker()

    checker.checks("nfc")(is_nfc_text)
    return jsonschema.Draft202012Validator(schema, format_checker=checker)


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity.json", id="artifact_identity"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity_verification_result.json",
            id="artifact_identity_verification_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_location.json", id="artifact_location"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_reference.json", id="artifact_reference"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_specification.json",
            id="artifact_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/declared_capability.json", id="declared_capability"
        ),
        pytest.param(
            ROOT / "fixtures/valid/execution_correlation_result.json",
            id="execution_correlation_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_failure.json",
            id="external_execution_failure",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_request.json",
            id="external_execution_request",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_result.json",
            id="external_execution_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_identity.json",
            id="external_tool_identity",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_specification.json",
            id="external_tool_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/installation_observation.json",
            id="installation_observation",
        ),
        pytest.param(
            ROOT / "fixtures/valid/lineage_relation.json", id="lineage_relation"
        ),
        pytest.param(
            ROOT / "fixtures/valid/provenance_record.json", id="provenance_record"
        ),
        pytest.param(ROOT / "fixtures/valid/run_manifest.json", id="run_manifest"),
        pytest.param(
            ROOT / "fixtures/valid/verification_observation.json",
            id="verification_observation",
        ),
    ],
)
def test_artifact__valid_fixture_parameters__belong_to_maintained_family(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-140
    Requirement
    Every named valid-fixture parameter belongs to the maintained valid family.
    Method
    Compare the named fixed fixture path with the discovered VALID tuple.
    Oracle
    The checked-in valid fixture directory independently defines membership.
    Acceptance
    The path is present in VALID exactly.
    Interpretation
    Failure indicates stale parameter inventory or fixture-family drift.
    Limitations
    Membership establishes no schema, runtime, scientific, UQ, or cross-language result.
    """
    assert path in VALID


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity.json", id="artifact_identity"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity_verification_result.json",
            id="artifact_identity_verification_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_location.json", id="artifact_location"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_reference.json", id="artifact_reference"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_specification.json",
            id="artifact_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/declared_capability.json", id="declared_capability"
        ),
        pytest.param(
            ROOT / "fixtures/valid/execution_correlation_result.json",
            id="execution_correlation_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_failure.json",
            id="external_execution_failure",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_request.json",
            id="external_execution_request",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_result.json",
            id="external_execution_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_identity.json",
            id="external_tool_identity",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_specification.json",
            id="external_tool_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/installation_observation.json",
            id="installation_observation",
        ),
        pytest.param(
            ROOT / "fixtures/valid/lineage_relation.json", id="lineage_relation"
        ),
        pytest.param(
            ROOT / "fixtures/valid/provenance_record.json", id="provenance_record"
        ),
        pytest.param(ROOT / "fixtures/valid/run_manifest.json", id="run_manifest"),
        pytest.param(
            ROOT / "fixtures/valid/verification_observation.json",
            id="verification_observation",
        ),
    ],
)
def test_artifact__valid_fixtures__pass_schema_validation(path: Path) -> None:
    """Evidence ID
    SV-PROV-067
    Requirement
    Every maintained valid fixture satisfies the public version-1 JSON Schema.
    Method
    Decode the named fixture with json and validate it using the configured local
    schema validator.
    Oracle
    The checked-in schema plus active NFC format checker independently define
    structural acceptance.
    Acceptance
    Schema validation completes without an exception.
    Interpretation
    Failure identifies schema, fixture classification, NFC oracle, or jsonschema drift.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    make_provenance_schema_validator().validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity.json", id="artifact_identity"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity_verification_result.json",
            id="artifact_identity_verification_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_location.json", id="artifact_location"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_reference.json", id="artifact_reference"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_specification.json",
            id="artifact_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/declared_capability.json", id="declared_capability"
        ),
        pytest.param(
            ROOT / "fixtures/valid/execution_correlation_result.json",
            id="execution_correlation_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_failure.json",
            id="external_execution_failure",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_request.json",
            id="external_execution_request",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_result.json",
            id="external_execution_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_identity.json",
            id="external_tool_identity",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_specification.json",
            id="external_tool_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/installation_observation.json",
            id="installation_observation",
        ),
        pytest.param(
            ROOT / "fixtures/valid/lineage_relation.json", id="lineage_relation"
        ),
        pytest.param(
            ROOT / "fixtures/valid/provenance_record.json", id="provenance_record"
        ),
        pytest.param(ROOT / "fixtures/valid/run_manifest.json", id="run_manifest"),
        pytest.param(
            ROOT / "fixtures/valid/verification_observation.json",
            id="verification_observation",
        ),
    ],
)
def test_artifact__valid_fixtures__deserialize_at_runtime(path: Path) -> None:
    """Evidence ID
    SV-PROV-135
    Requirement
    Every maintained valid fixture constructs a public record through strict runtime
    deserialization.
    Method
    Pass the named original UTF-8 fixture text to ProvenanceJsonSerializer.deserialize.
    Oracle
    The maintained valid classification independently declares runtime acceptance.
    Acceptance
    Deserialization returns without ProvenanceJsonError.
    Interpretation
    Failure identifies fixture classification, runtime constructor, or deserializer
    drift.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    ProvenanceJsonSerializer().deserialize(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity.json", id="artifact_identity"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_identity_verification_result.json",
            id="artifact_identity_verification_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_location.json", id="artifact_location"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_reference.json", id="artifact_reference"
        ),
        pytest.param(
            ROOT / "fixtures/valid/artifact_specification.json",
            id="artifact_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/declared_capability.json", id="declared_capability"
        ),
        pytest.param(
            ROOT / "fixtures/valid/execution_correlation_result.json",
            id="execution_correlation_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_failure.json",
            id="external_execution_failure",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_request.json",
            id="external_execution_request",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_execution_result.json",
            id="external_execution_result",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_identity.json",
            id="external_tool_identity",
        ),
        pytest.param(
            ROOT / "fixtures/valid/external_tool_specification.json",
            id="external_tool_specification",
        ),
        pytest.param(
            ROOT / "fixtures/valid/installation_observation.json",
            id="installation_observation",
        ),
        pytest.param(
            ROOT / "fixtures/valid/lineage_relation.json", id="lineage_relation"
        ),
        pytest.param(
            ROOT / "fixtures/valid/provenance_record.json", id="provenance_record"
        ),
        pytest.param(ROOT / "fixtures/valid/run_manifest.json", id="run_manifest"),
        pytest.param(
            ROOT / "fixtures/valid/verification_observation.json",
            id="verification_observation",
        ),
    ],
)
def test_artifact__valid_fixtures__serialize_to_canonical_round_trip_text(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-136
    Requirement
    Each valid fixture is the exact canonical serialization of its represented
    public record.
    Method
    Deserialize the named fixture and serialize the resulting public record.
    Oracle
    The checked-in UTF-8 fixture text is the independent canonical-text oracle.
    Acceptance
    Serialized output equals original text exactly.
    Interpretation
    Failure identifies runtime serialization, canonicalization, or fixture-text drift.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    text = path.read_text(encoding="utf-8")
    record = ProvenanceJsonSerializer().deserialize(text)
    assert ProvenanceJsonSerializer().serialize(record) == text


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(ROOT / "fixtures/invalid/bom.json", id="bom"),
        pytest.param(
            ROOT / "fixtures/invalid/boolean-byte-size.json", id="boolean_byte_size"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/c1-control-path.json", id="c1_control_path"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/direct-self-dependent-run-manifest.json",
            id="direct_self_dependency",
        ),
        pytest.param(ROOT / "fixtures/invalid/duplicate-key.json", id="duplicate_key"),
        pytest.param(
            ROOT / "fixtures/invalid/floating-byte-size.json", id="floating_byte_size"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/impossible-calendar-date.json",
            id="impossible_calendar_date",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-environment-record.json",
            id="legacy_environment_record",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-failure-message.json",
            id="legacy_failure_message",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-manifest-arguments.json",
            id="legacy_manifest_arguments",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-manifest-environment.json",
            id="legacy_manifest_environment",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-retryable-field.json",
            id="legacy_retryable_field",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-verification-detail.json",
            id="legacy_verification_detail",
        ),
        pytest.param(ROOT / "fixtures/invalid/malformed.json", id="malformed_json"),
        pytest.param(
            ROOT / "fixtures/invalid/missing-attempt-id.json", id="missing_attempt_id"
        ),
        pytest.param(ROOT / "fixtures/invalid/non-nfc-path.json", id="non_nfc_path"),
        pytest.param(ROOT / "fixtures/invalid/nonfinite.json", id="nonfinite_number"),
        pytest.param(
            ROOT / "fixtures/invalid/numeric-string-byte-size.json",
            id="numeric_string_byte_size",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/raw-observed-version.json",
            id="raw_observed_version",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/raw-requested-version.json",
            id="raw_requested_version",
        ),
        pytest.param(ROOT / "fixtures/invalid/surrogate.json", id="unicode_surrogate"),
        pytest.param(ROOT / "fixtures/invalid/u64-overflow.json", id="u64_overflow"),
        pytest.param(ROOT / "fixtures/invalid/unknown-key.json", id="unknown_key"),
        pytest.param(
            ROOT / "fixtures/invalid/unsorted-identifiers.json",
            id="unsorted_identifiers",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/uppercase-sha256.json", id="uppercase_sha256"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/windows-device-path.json", id="windows_device_path"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/windows-drive-path.json", id="windows_drive_path"
        ),
    ],
)
def test_artifact__invalid_fixture_parameters__belong_to_maintained_family(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-141
    Requirement
    Every named invalid-fixture parameter belongs to the maintained invalid family.
    Method
    Compare the named fixed fixture path with the discovered INVALID tuple.
    Oracle
    The checked-in invalid fixture directory independently defines membership.
    Acceptance
    The path is present in INVALID exactly.
    Interpretation
    Failure indicates stale parameter inventory or fixture-family drift.
    Limitations
    Membership establishes no runtime rejection, scientific, UQ, or cross-language
    result.
    """
    assert path in INVALID


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(ROOT / "fixtures/invalid/bom.json", id="bom"),
        pytest.param(
            ROOT / "fixtures/invalid/boolean-byte-size.json", id="boolean_byte_size"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/c1-control-path.json", id="c1_control_path"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/direct-self-dependent-run-manifest.json",
            id="direct_self_dependency",
        ),
        pytest.param(ROOT / "fixtures/invalid/duplicate-key.json", id="duplicate_key"),
        pytest.param(
            ROOT / "fixtures/invalid/floating-byte-size.json", id="floating_byte_size"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/impossible-calendar-date.json",
            id="impossible_calendar_date",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-environment-record.json",
            id="legacy_environment_record",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-failure-message.json",
            id="legacy_failure_message",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-manifest-arguments.json",
            id="legacy_manifest_arguments",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-manifest-environment.json",
            id="legacy_manifest_environment",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-retryable-field.json",
            id="legacy_retryable_field",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/legacy-verification-detail.json",
            id="legacy_verification_detail",
        ),
        pytest.param(ROOT / "fixtures/invalid/malformed.json", id="malformed_json"),
        pytest.param(
            ROOT / "fixtures/invalid/missing-attempt-id.json", id="missing_attempt_id"
        ),
        pytest.param(ROOT / "fixtures/invalid/non-nfc-path.json", id="non_nfc_path"),
        pytest.param(ROOT / "fixtures/invalid/nonfinite.json", id="nonfinite_number"),
        pytest.param(
            ROOT / "fixtures/invalid/numeric-string-byte-size.json",
            id="numeric_string_byte_size",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/raw-observed-version.json",
            id="raw_observed_version",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/raw-requested-version.json",
            id="raw_requested_version",
        ),
        pytest.param(ROOT / "fixtures/invalid/surrogate.json", id="unicode_surrogate"),
        pytest.param(ROOT / "fixtures/invalid/u64-overflow.json", id="u64_overflow"),
        pytest.param(ROOT / "fixtures/invalid/unknown-key.json", id="unknown_key"),
        pytest.param(
            ROOT / "fixtures/invalid/unsorted-identifiers.json",
            id="unsorted_identifiers",
        ),
        pytest.param(
            ROOT / "fixtures/invalid/uppercase-sha256.json", id="uppercase_sha256"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/windows-device-path.json", id="windows_device_path"
        ),
        pytest.param(
            ROOT / "fixtures/invalid/windows-drive-path.json", id="windows_drive_path"
        ),
    ],
)
def test_artifact__invalid_fixture_family__is_rejected_by_strict_runtime(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-068
    Requirement
    Each maintained invalid fixture is rejected at the strict public Python JSON
    boundary.
    Method
    Pass the named raw UTF-8 fixture directly to public deserialization without
    permissive preprocessing.
    Oracle
    Its checked-in invalid-family classification independently declares rejection.
    Acceptance
    The path belongs to INVALID and deserialization raises ProvenanceJsonError.
    Interpretation
    Failure may indicate runtime permissiveness, fixture misclassification, or
    contract drift.
    Limitations
    Schema alone cannot detect all raw-text defects; scientific validation, UQ,
    portability, and cross-language claims are excluded.
    """
    with pytest.raises(ProvenanceJsonError):
        ProvenanceJsonSerializer().deserialize(path.read_text(encoding="utf-8"))


def test_artifact__fixture_types__cover_serializable_schema_inventory() -> None:
    """Evidence ID
    SV-PROV-069
    Requirement
    Valid fixtures provide one canonically named representative for every schema
    record definition.
    Method
    Compare fixture record_type values and stems with schema record_type constants
    using fixed artifacts.
    Oracle
    Independently maintained fixture objects and schema definitions supply the two
    inventories.
    Acceptance
    Record-type sets are exactly equal and every fixture stem equals its record_type.
    Interpretation
    Failure indicates missing, extra, misnamed, or schema-divergent interoperability
    fixtures.
    Limitations
    One synthetic representative does not exhaust domains or establish validation,
    UQ, portability, or cross-language conformance.
    """
    schema = json.loads(
        (ROOT / "provenance-v1.schema.json").read_text(encoding="utf-8")
    )
    fixture_pairs = tuple(
        map(
            lambda path: (
                path.stem,
                json.loads(path.read_text(encoding="utf-8"))["record_type"],
            ),
            VALID,
        )
    )
    assert all(map(lambda pair: pair[0] == pair[1], fixture_pairs))
    fixture_types = set(map(lambda pair: pair[1], fixture_pairs))
    schema_types = set(
        map(
            lambda definition: definition["properties"]["record_type"]["const"],
            schema["$defs"].values(),
        )
    )
    assert fixture_types == schema_types


def test_artifact__corrected_invalid_fixture_inventory__contains_required_stems() -> (
    None
):
    """Evidence ID
    SV-PROV-142
    Requirement
    The corrected invalid family retains every required legacy/unsafe fixture stem.
    Method
    Compare the fixed required stem set with stems discovered in INVALID.
    Oracle
    The corrected version-1 contract independently fixes the required stem set.
    Acceptance
    The required set is a subset of discovered invalid fixture stems.
    Interpretation
    Failure identifies missing retained correction evidence or fixture inventory drift.
    Limitations
    Existence establishes no runtime rejection, scientific, UQ, or cross-language
    result.
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
    assert required <= {path.stem for path in INVALID}


@pytest.mark.parametrize(
    "stem",
    [
        pytest.param("impossible-calendar-date", id="impossible_calendar_date"),
        pytest.param("legacy-environment-record", id="legacy_environment_record"),
        pytest.param("legacy-failure-message", id="legacy_failure_message"),
        pytest.param("legacy-manifest-arguments", id="legacy_manifest_arguments"),
        pytest.param("legacy-manifest-environment", id="legacy_manifest_environment"),
        pytest.param("legacy-verification-detail", id="legacy_verification_detail"),
        pytest.param("missing-attempt-id", id="missing_attempt_id"),
        pytest.param("raw-observed-version", id="raw_observed_version"),
        pytest.param("raw-requested-version", id="raw_requested_version"),
        pytest.param("unknown-key", id="unknown_key"),
    ],
)
def test_artifact__corrected_invalid_fixtures__reject_legacy_channels(
    stem: str,
) -> None:
    """Evidence ID
    SV-PROV-079
    Requirement
    Named invalid fixtures retain rejection evidence for removed channels, raw
    versions, impossible dates, and missing attempts.
    Method
    Require the semantic fixture stem and pass its raw text to the strict public
    deserializer.
    Oracle
    The corrected version-1 contract independently classifies each named shape as
    invalid.
    Acceptance
    The fixture exists in INVALID and deserialization raises ProvenanceJsonError.
    Interpretation
    Failure indicates missing retained evidence, parser permissiveness, or contract
    drift.
    Limitations
    Credential detection, scientific validation, UQ, portability, and cross-language
    claims are excluded.
    """
    path = ROOT / "fixtures/invalid" / f"{stem}.json"
    with pytest.raises(ProvenanceJsonError):
        ProvenanceJsonSerializer().deserialize(path.read_text(encoding="utf-8"))


def test_artifact__direct_self_dependency_fixture__has_layered_classification() -> None:
    """Evidence ID
    SV-PROV-103
    Requirement
    The self-dependency fixture is runtime-invalid although its unrelated wire
    structure is schema-valid.
    Method
    Validate decoded structure, compare manifest/dependency identities, then
    strictly deserialize original text.
    Oracle
    Fixture classification and exact identifier equality independently supply
    structural and runtime expectations.
    Acceptance
    Schema validation succeeds, identifiers are equal, and deserialization raises
    ProvenanceJsonError.
    Interpretation
    Failure indicates fixture, schema-layer, runtime-relation, or classification drift.
    Limitations
    Indirect cycles, scientific validation, UQ, portability, and cross-language
    conformance are excluded.
    """
    path = ROOT / "fixtures/invalid/direct-self-dependent-run-manifest.json"
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    make_provenance_schema_validator().validate(payload)
    assert payload["manifest_id"] == payload["dependency_manifest_ids"][0]
    with pytest.raises(ProvenanceJsonError):
        ProvenanceJsonSerializer().deserialize(text)
