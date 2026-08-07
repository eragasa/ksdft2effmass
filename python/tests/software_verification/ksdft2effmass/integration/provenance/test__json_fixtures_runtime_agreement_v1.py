r"""Software verification of version-1 provenance JSON fixture/runtime interoperability.

Facet and represented meaning
-----------------------------
This artifact-owned module verifies checked-in version-1 fixture classification,
strict public runtime mapping, and canonical serialization as distinct software layers.

Intrinsic and cross-object scope
--------------------------------
The fixture families are primary. The Draft 2020-12 schema, public provenance record
classes, and public JSON serializer are independently named collaborators and oracles.

VVUQ and scientific exclusions
------------------------------
Pass/failure concerns nonnumerical software interoperability only. Evidence excludes
provenance truth, numerical verification, scientific validation, UQ, persistence,
physical correctness, released-package compatibility, future-version compatibility,
and cross-language conformance.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest

import ksdft2effmass.provenance as provenance

REPO_ROOT = Path(__file__).resolve().parents[6]
ROOT = REPO_ROOT / "specification/provenance/v1"
VALID = tuple(sorted((ROOT / "fixtures/valid").glob("*.json")))
INVALID = tuple(sorted((ROOT / "fixtures/invalid").glob("*.json")))
pytestmark = pytest.mark.software_verification

ValidFixtureCase = tuple[Path, type[object]]

VALID_FIXTURE_CASES = (
    pytest.param(
        (ROOT / "fixtures/valid/artifact_identity.json", provenance.ArtifactIdentity),
        id="artifact_identity",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/artifact_identity_verification_result.json",
            provenance.ArtifactIdentityVerificationResult,
        ),
        id="artifact_identity_verification_result",
    ),
    pytest.param(
        (ROOT / "fixtures/valid/artifact_location.json", provenance.ArtifactLocation),
        id="artifact_location",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/artifact_reference.json",
            provenance.ArtifactReference,
        ),
        id="artifact_reference",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/artifact_specification.json",
            provenance.ArtifactSpecification,
        ),
        id="artifact_specification",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/declared_capability.json",
            provenance.DeclaredCapability,
        ),
        id="declared_capability",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/execution_correlation_result.json",
            provenance.ExecutionCorrelationResult,
        ),
        id="execution_correlation_result",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/external_execution_failure.json",
            provenance.ExternalExecutionFailure,
        ),
        id="external_execution_failure",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/external_execution_request.json",
            provenance.ExternalExecutionRequest,
        ),
        id="external_execution_request",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/external_execution_result.json",
            provenance.ExternalExecutionResult,
        ),
        id="external_execution_result",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/external_tool_identity.json",
            provenance.ExternalToolIdentity,
        ),
        id="external_tool_identity",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/external_tool_specification.json",
            provenance.ExternalToolSpecification,
        ),
        id="external_tool_specification",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/installation_observation.json",
            provenance.InstallationObservation,
        ),
        id="installation_observation",
    ),
    pytest.param(
        (ROOT / "fixtures/valid/lineage_relation.json", provenance.LineageRelation),
        id="lineage_relation",
    ),
    pytest.param(
        (ROOT / "fixtures/valid/provenance_record.json", provenance.ProvenanceRecord),
        id="provenance_record",
    ),
    pytest.param(
        (ROOT / "fixtures/valid/run_manifest.json", provenance.RunManifest),
        id="run_manifest",
    ),
    pytest.param(
        (
            ROOT / "fixtures/valid/verification_observation.json",
            provenance.VerificationObservation,
        ),
        id="verification_observation",
    ),
)

INVALID_FIXTURE_CASES = (
    pytest.param(ROOT / "fixtures/invalid/bom.json", id="bom"),
    pytest.param(
        ROOT / "fixtures/invalid/boolean-byte-size.json", id="boolean_byte_size"
    ),
    pytest.param(ROOT / "fixtures/invalid/c1-control-path.json", id="c1_control_path"),
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
    pytest.param(
        ROOT / "fixtures/invalid/trailing-line-feed-identifier.json",
        id="trailing_line_feed_identifier",
    ),
    pytest.param(
        ROOT / "fixtures/invalid/trailing-line-feed-observed-version.json",
        id="trailing_line_feed_observed_version",
    ),
    pytest.param(
        ROOT / "fixtures/invalid/trailing-line-feed-requested-version.json",
        id="trailing_line_feed_requested_version",
    ),
    pytest.param(
        ROOT / "fixtures/invalid/trailing-line-feed-sha256.json",
        id="trailing_line_feed_sha256",
    ),
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
)


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
    Load the fixed public schema and register Python NFC normalization without network
    access.
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


def extract_declared_fixture_paths(
    parameter_cases: tuple[Any, ...],
) -> tuple[Path, ...]:
    """Evidence ID
    Owns no identifier; supports SV-PROV-396 and SV-PROV-397.
    Requirement
    Derive declared fixture paths directly from one local pytest.param inventory.
    Method
    Read the first declared value from each static local parameter entry in order.
    Oracle
    The explicit module-local pytest.param tuple is the sole declared-case source.
    Acceptance
    Every entry supplies a Path first value and returned paths preserve declared order.
    Interpretation
    Failure indicates a malformed local parameter inventory rather than fixture drift.
    Limitations
    This helper performs no discovery, execution, schema validation, deserialization,
    scientific validation, UQ, persistence, or cross-language checking.
    """
    values = tuple(parameter_case.values[0] for parameter_case in parameter_cases)
    paths = tuple(value[0] if isinstance(value, tuple) else value for value in values)
    assert all(isinstance(path, Path) for path in paths)
    return paths


def assert_exact_declared_fixture_family(
    declared_paths: tuple[Path, ...],
    discovered_paths: tuple[Path, ...],
) -> None:
    """Evidence ID
    Owns no identifier; supports SV-PROV-396 and SV-PROV-397.
    Requirement
    Compare one declared fixture-path inventory bidirectionally with one discovered
    family.
    Method
    Require declared-path uniqueness and exact set equality without performing
    discovery.
    Oracle
    Explicit declared paths and the caller-supplied checked-in directory inventory are
    independent sides of the artifact relation.
    Acceptance
    Every declared path is unique and declared and discovered path sets are exactly
    equal.
    Interpretation
    Failure identifies duplicate declarations, omissions, nonexistent declarations, or
    wrong-family placement.
    Limitations
    Exact path agreement does not establish fixture contents, runtime behavior,
    provenance truth, numerical verification, scientific validation, UQ, or portability.
    """
    assert len(declared_paths) == len(set(declared_paths))
    assert set(declared_paths) == set(discovered_paths)


@pytest.mark.parametrize("fixture_case", VALID_FIXTURE_CASES)
def test_artifact__valid_fixture_parameters__belong_to_maintained_family(
    fixture_case: ValidFixtureCase,
) -> None:
    """Evidence ID
    SV-PROV-140
    Requirement
    Every declared valid-fixture parameter belongs to the maintained valid family.
    Method
    Extract the declared path from the named valid case and compare it with VALID.
    Oracle
    The checked-in valid fixture directory independently defines membership.
    Acceptance
    The declared path is present in VALID exactly.
    Interpretation
    Failure indicates a stale parameter entry or wrong-family classification.
    Limitations
    Membership establishes no completeness, schema, runtime, scientific, UQ, or
    cross-language result.
    """
    path, _expected_type = fixture_case
    assert path in VALID


def test_artifact__valid_fixture_inventory__matches_declared_parameter_family_exactly(  # noqa: E501
) -> None:
    """Evidence ID
    SV-PROV-396
    Requirement
    Declared valid cases and discovered valid fixtures form one exact unique family.
    Method
    Extract paths from VALID_FIXTURE_CASES, compare them exactly with VALID, and inject
    controlled omitted, nonexistent, and duplicate declarations through the same helper.
    Oracle
    The static named inventory and checked-in valid directory are independent
    inventories.
    Acceptance
    Real inventories agree exactly; omission, nonexistent declaration, and duplication
    each raise AssertionError under the same exact-family mechanism.
    Interpretation
    Failure identifies valid-family inventory drift or a completeness oracle defect.
    Limitations
    Path completeness does not establish fixture contents, schema semantics, runtime
    mapping, canonical text, provenance truth, validation, UQ, or portability.
    """
    declared_paths = extract_declared_fixture_paths(VALID_FIXTURE_CASES)
    assert_exact_declared_fixture_family(declared_paths, VALID)
    with pytest.raises(AssertionError):
        assert_exact_declared_fixture_family(declared_paths[:-1], VALID)
    nonexistent = ROOT / "fixtures/valid/declared-but-missing.json"
    with pytest.raises(AssertionError):
        assert_exact_declared_fixture_family((*declared_paths, nonexistent), VALID)
    with pytest.raises(AssertionError):
        assert_exact_declared_fixture_family(
            (*declared_paths, declared_paths[0]), VALID
        )


@pytest.mark.parametrize("fixture_case", VALID_FIXTURE_CASES)
def test_artifact__valid_fixtures__pass_schema_validation(
    fixture_case: ValidFixtureCase,
) -> None:
    """Evidence ID
    SV-PROV-067
    Requirement
    Every maintained valid fixture satisfies the public version-1 JSON Schema.
    Method
    Decode the named fixture with json and validate it using the configured local schema
    validator.
    Oracle
    The checked-in schema plus active NFC format checker independently define structural
    acceptance.
    Acceptance
    Schema validation completes without an exception for all 17 valid cases.
    Interpretation
    Failure identifies schema, fixture classification, NFC oracle, or jsonschema drift.
    Limitations
    Schema acceptance does not establish strict runtime mapping, canonical text,
    provenance truth, scientific validation, UQ, persistence, or cross-language
    behavior.
    """
    path, _expected_type = fixture_case
    make_provenance_schema_validator().validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


@pytest.mark.parametrize("fixture_case", VALID_FIXTURE_CASES)
def test_artifact__valid_fixtures__deserialize_to_exact_public_record_type(
    fixture_case: ValidFixtureCase,
) -> None:
    """Evidence ID
    SV-PROV-135
    Requirement
    Every maintained valid fixture maps to its exact intended public provenance class.
    Method
    Deserialize original UTF-8 fixture text through the public serializer and compare
    exact result type identity with the class declared in the canonical named case.
    Oracle
    The explicit public class in VALID_FIXTURE_CASES independently fixes each mapping.
    Acceptance
    For all 17 fixtures, ``type(record) is expected_type``.
    Interpretation
    Failure identifies fixture classification, runtime constructor, serializer mapping,
    or public-class oracle drift.
    Limitations
    Exact class mapping does not establish canonical serialization, provenance truth,
    scientific validation, UQ, persistence, portability, or cross-language conformance.
    """
    path, expected_type = fixture_case
    record = provenance.ProvenanceJsonSerializer().deserialize(
        path.read_text(encoding="utf-8")
    )
    assert type(record) is expected_type


@pytest.mark.parametrize("fixture_case", VALID_FIXTURE_CASES)
def test_artifact__valid_fixtures__serialize_to_canonical_round_trip_text(
    fixture_case: ValidFixtureCase,
) -> None:
    """Evidence ID
    SV-PROV-136
    Requirement
    Each valid fixture is the exact canonical serialization of its represented record.
    Method
    Deserialize the named fixture and serialize the resulting public record.
    Oracle
    The checked-in original UTF-8 fixture text is the independent canonical-text oracle.
    Acceptance
    Serialized output equals original text exactly for all 17 valid cases.
    Interpretation
    Failure identifies runtime serialization, canonicalization, or fixture-text drift.
    Limitations
    Canonical text agreement does not establish schema completeness, provenance truth,
    scientific validation, UQ, persistence, portability, or cross-language behavior.
    """
    path, _expected_type = fixture_case
    text = path.read_text(encoding="utf-8")
    record = provenance.ProvenanceJsonSerializer().deserialize(text)
    assert provenance.ProvenanceJsonSerializer().serialize(record) == text


@pytest.mark.parametrize("path", INVALID_FIXTURE_CASES)
def test_artifact__invalid_fixture_parameters__belong_to_maintained_family(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-141
    Requirement
    Every declared invalid-fixture parameter belongs to the maintained invalid family.
    Method
    Compare each path from INVALID_FIXTURE_CASES with the discovered INVALID tuple.
    Oracle
    The checked-in invalid fixture directory independently defines membership.
    Acceptance
    The declared path is present in INVALID exactly.
    Interpretation
    Failure indicates a stale parameter entry or wrong-family classification.
    Limitations
    Membership establishes no completeness, runtime rejection, scientific, UQ,
    persistence, or cross-language result.
    """
    assert path in INVALID


def test_artifact__invalid_fixture_inventory__matches_declared_parameter_family_exactly(  # noqa: E501
) -> None:
    """Evidence ID
    SV-PROV-397
    Requirement
    Declared invalid cases and discovered invalid fixtures form one exact unique family.
    Method
    Extract paths from INVALID_FIXTURE_CASES, compare them exactly with INVALID, and
    inject one controlled omitted declaration through the same exact-family helper.
    Oracle
    The static named inventory and checked-in invalid directory are independent
    inventories.
    Acceptance
    Real inventories agree exactly and an undeclared discovered invalid path raises
    AssertionError under the same mechanism.
    Interpretation
    Failure identifies invalid-family inventory drift or a completeness oracle defect.
    Limitations
    Path completeness does not establish runtime rejection, fixture meaning, provenance
    truth, scientific validation, UQ, persistence, or cross-language behavior.
    """
    declared_paths = extract_declared_fixture_paths(INVALID_FIXTURE_CASES)
    assert_exact_declared_fixture_family(declared_paths, INVALID)
    with pytest.raises(AssertionError):
        assert_exact_declared_fixture_family(declared_paths[:-1], INVALID)


@pytest.mark.parametrize("path", INVALID_FIXTURE_CASES)
def test_artifact__invalid_fixture_family__is_rejected_by_strict_runtime(
    path: Path,
) -> None:
    """Evidence ID
    SV-PROV-068
    Requirement
    Each maintained invalid fixture is rejected at the strict public Python JSON
    boundary.
    Method
    Pass each original UTF-8 fixture directly to public deserialization without
    permissive preprocessing.
    Oracle
    Its checked-in invalid-family classification independently declares rejection.
    Acceptance
    All 31 cases raise ProvenanceJsonError.
    Interpretation
    Failure may indicate runtime permissiveness, fixture misclassification, or contract
    drift.
    Limitations
    Runtime rejection does not establish schema rejection, provenance truth, scientific
    validation, UQ, persistence, portability, or cross-language behavior.
    """
    with pytest.raises(provenance.ProvenanceJsonError):
        provenance.ProvenanceJsonSerializer().deserialize(
            path.read_text(encoding="utf-8")
        )


def test_artifact__fixture_types__cover_serializable_schema_inventory() -> None:
    """Evidence ID
    SV-PROV-069
    Requirement
    Valid fixtures provide one canonically named representative for every schema record
    definition.
    Method
    Compare fixture record_type values and stems with schema record_type constants using
    fixed artifacts.
    Oracle
    Independently maintained fixture objects and schema definitions supply the
    inventories.
    Acceptance
    Record-type sets are exactly equal and every fixture stem equals its record_type.
    Interpretation
    Failure indicates missing, extra, misnamed, or schema-divergent interoperability
    fixtures.
    Limitations
    One synthetic representative does not exhaust domains or establish provenance truth,
    validation, UQ, persistence, portability, or cross-language conformance.
    """
    schema = json.loads(
        (ROOT / "provenance-v1.schema.json").read_text(encoding="utf-8")
    )
    fixture_pairs = tuple(
        (
            path.stem,
            json.loads(path.read_text(encoding="utf-8"))["record_type"],
        )
        for path in VALID
    )
    assert all(stem == record_type for stem, record_type in fixture_pairs)
    fixture_types = {record_type for _stem, record_type in fixture_pairs}
    schema_types = {
        definition["properties"]["record_type"]["const"]
        for definition in schema["$defs"].values()
    }
    assert fixture_types == schema_types


def test_artifact__corrected_invalid_fixture_inventory__contains_required_stems() -> (
    None
):
    """Evidence ID
    SV-PROV-142
    Requirement
    The corrected invalid family retains every required legacy and unsafe fixture stem,
    including the removed ``retryable`` field channel.
    Method
    Compare the fixed required stem set with stems discovered in INVALID.
    Oracle
    The corrected version-1 contract independently fixes the required stem set.
    Acceptance
    The required set, including ``legacy-retryable-field``, is a subset of discovered
    invalid fixture stems.
    Interpretation
    Failure identifies missing retained correction evidence or fixture inventory drift.
    Limitations
    Existence establishes no runtime rejection, provenance truth, scientific validation,
    UQ, persistence, portability, or cross-language result.
    """
    required = {
        "impossible-calendar-date",
        "legacy-environment-record",
        "legacy-failure-message",
        "legacy-manifest-arguments",
        "legacy-manifest-environment",
        "legacy-retryable-field",
        "legacy-verification-detail",
        "missing-attempt-id",
        "raw-observed-version",
        "raw-requested-version",
        "unknown-key",
    }
    assert required <= {path.stem for path in INVALID}


@pytest.mark.parametrize(
    "stem",
    (
        pytest.param("impossible-calendar-date", id="impossible_calendar_date"),
        pytest.param("legacy-environment-record", id="legacy_environment_record"),
        pytest.param("legacy-failure-message", id="legacy_failure_message"),
        pytest.param("legacy-manifest-arguments", id="legacy_manifest_arguments"),
        pytest.param("legacy-manifest-environment", id="legacy_manifest_environment"),
        pytest.param("legacy-retryable-field", id="legacy_retryable_field"),
        pytest.param("legacy-verification-detail", id="legacy_verification_detail"),
        pytest.param("missing-attempt-id", id="missing_attempt_id"),
        pytest.param("raw-observed-version", id="raw_observed_version"),
        pytest.param("raw-requested-version", id="raw_requested_version"),
        pytest.param("unknown-key", id="unknown_key"),
    ),
)
def test_artifact__corrected_invalid_fixtures__reject_legacy_channels(
    stem: str,
) -> None:
    """Evidence ID
    SV-PROV-079
    Requirement
    Named invalid fixtures retain rejection evidence for removed environment, argument,
    message, verification-detail, and ``retryable`` channels plus corrected invalid
    forms.
    Method
    Require each semantic fixture stem and pass original text to the strict
    deserializer.
    Oracle
    The corrected version-1 contract independently classifies every named shape as
    invalid.
    Acceptance
    Every named fixture exists in INVALID and raises ProvenanceJsonError, including
    ``legacy-retryable-field``.
    Interpretation
    Failure indicates missing retained evidence, parser permissiveness, or contract
    drift.
    Limitations
    Credential detection, provenance truth, scientific validation, UQ, persistence,
    portability, and cross-language claims are excluded.
    """
    path = ROOT / "fixtures/invalid" / f"{stem}.json"
    assert path in INVALID
    with pytest.raises(provenance.ProvenanceJsonError):
        provenance.ProvenanceJsonSerializer().deserialize(
            path.read_text(encoding="utf-8")
        )


def test_artifact__direct_self_dependency_fixture__has_layered_classification() -> None:
    """Evidence ID
    SV-PROV-103
    Requirement
    The self-dependency fixture is runtime-invalid although its unrelated wire structure
    is schema-valid.
    Method
    Validate decoded structure, compare manifest and dependency identities, then
    strictly deserialize original text.
    Oracle
    Fixture classification and exact identifier equality independently supply structural
    and runtime expectations.
    Acceptance
    Schema validation succeeds, identifiers are equal, and deserialization raises
    ProvenanceJsonError.
    Interpretation
    Failure indicates fixture, schema-layer, runtime-relation, or classification drift.
    Limitations
    Indirect cycles, provenance truth, scientific validation, UQ, persistence,
    portability, and cross-language conformance are excluded.
    """
    path = ROOT / "fixtures/invalid/direct-self-dependent-run-manifest.json"
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    make_provenance_schema_validator().validate(payload)
    assert payload["manifest_id"] == payload["dependency_manifest_ids"][0]
    with pytest.raises(provenance.ProvenanceJsonError):
        provenance.ProvenanceJsonSerializer().deserialize(text)
