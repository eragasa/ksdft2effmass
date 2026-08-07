r"""Software verification of json contract v1.

Facet and represented meaning
-----------------------------
This artifact-owned module verifies the declared version-1 JSON Schema dialect,
record inventory, stored vocabularies, unstored derived statuses, and active NFC format.

Intrinsic and cross-object scope
--------------------------------
The version-1 Python/JSON relation is primary. The checked-in schema and public Python
classes are independent sides. Fixture-family classification is owned by P2-A09;
complete schema/fixture-family content is owned separately by P2-A11.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the declared software wire contract. It excludes provenance
truth, numerical verification, scientific validation, UQ, persistence, external
execution validity, released-package compatibility, and implemented cross-language
conformance.
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import fields
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest

from ksdft2effmass import provenance

REPO_ROOT = Path(__file__).resolve().parents[6]
SCHEMA_PATH = REPO_ROOT / "specification/provenance/v1/provenance-v1.schema.json"
pytestmark = pytest.mark.software_verification

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


def load_provenance_v1_schema() -> dict[str, Any]:
    """Evidence ID
    Owns no identifier; supports SV-PROV-064, SV-PROV-065, SV-PROV-066, and
    SV-PROV-398.
    Requirement
    Load the exact checked-in public version-1 schema as one JSON object.
    Method
    Read SCHEMA_PATH as UTF-8 and decode it through the standard JSON parser without
    caching or transformation.
    Oracle
    The fixed repository path and JSON object grammar independently define the input.
    Acceptance
    Decoding returns a built-in dict for every call.
    Interpretation
    Failure indicates schema-path, UTF-8, JSON syntax, or object-shape setup drift.
    Limitations
    Loading establishes no schema validity, Python agreement, fixture classification,
    provenance truth, scientific validation, UQ, persistence, or portability.
    """
    value = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert type(value) is dict
    return value


def assert_exact_top_level_references(references: tuple[str, ...]) -> None:
    """Evidence ID
    Owns no identifier; supports SV-PROV-064.
    Requirement
    Require the top-level schema references to be exactly the unique 17-record family.
    Method
    Compare count, unique count, and unordered reference set with EXPECTED_DEFINITIONS.
    Oracle
    The explicit accepted definition inventory independently fixes every expected ref.
    Acceptance
    There are exactly 17 references, all are unique, and their set is exact.
    Interpretation
    Failure identifies a missing, extra, duplicated, or misdirected top-level reference.
    Limitations
    This helper does not compile schema content, inspect fixtures, execute Python
    records, or establish scientific, persistence, or cross-language behavior.
    """
    assert len(references) == 17
    assert len(references) == len(set(references))
    assert set(references) == {
        f"#/$defs/{definition}" for definition in EXPECTED_DEFINITIONS
    }


def is_nfc_text(value: object) -> bool:
    """Evidence ID
    Owns no identifier; supports SV-PROV-066.
    Requirement
    Identify exact built-in strings already represented in Unicode NFC.
    Method
    Require exact built-in str type and compare with unicodedata NFC normalization.
    Oracle
    Python unicodedata.normalize independently defines the NFC transformation.
    Acceptance
    Return true exactly for built-in strings unchanged by NFC normalization.
    Interpretation
    Failure indicates format-checker oracle or Unicode-database behavior drift.
    Limitations
    This representative predicate does not establish full path grammar, fixtures,
    provenance truth, scientific validation, UQ, persistence, or portability.
    """
    return type(value) is str and unicodedata.normalize("NFC", value) == value


def test_artifact__schema_declaration__matches_draft_and_record_inventory() -> None:
    """Evidence ID
    SV-PROV-064
    Requirement
    The schema declares Draft 2020-12, compiles under that metaschema, and contains the
    exact 17-definition family with exactly 17 unique top-level references.
    Method
    Load the schema, assert its dialect, invoke Draft202012Validator.check_schema,
    compare definitions, apply the exact reference helper, and replace one reference
    with a valid duplicate while preserving the 17-element count.
    Oracle
    The Draft 2020-12 URI, metaschema, and explicit EXPECTED_DEFINITIONS are
    independent.
    Acceptance
    The dialect is exact; compilation succeeds; definitions and unique references are
    exact; and a 17-element inventory containing one duplicate causes the same helper
    to fail at the uniqueness guard.
    Interpretation
    Failure identifies dialect, schema compilation, definition inventory, reference
    inventory, or duplicate-detection drift.
    Limitations
    This does not establish Python record behavior, fixture-family validity, provenance
    truth, scientific validation, UQ, persistence, or cross-language implementation.
    """
    schema = load_provenance_v1_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    jsonschema.Draft202012Validator.check_schema(schema)
    definitions = schema["$defs"]
    assert type(definitions) is dict
    assert len(definitions) == 17
    assert set(definitions) == EXPECTED_DEFINITIONS
    references = tuple(item["$ref"] for item in schema["oneOf"])
    assert_exact_top_level_references(references)
    duplicate_references = (*references[:-1], references[0])
    assert len(duplicate_references) == 17
    with pytest.raises(AssertionError):
        assert_exact_top_level_references(duplicate_references)


def test_artifact__stored_vocabularies__agree_with_public_python_enums() -> None:
    """Evidence ID
    SV-PROV-065
    Requirement
    All eight stored schema vocabularies agree exactly with public Python enums, and the
    stored execution-result status equals the public COMPLETED value.
    Method
    Build literal-key schema and Python mappings from eight explicit locations, compare
    them exactly, and compare the explicit completed constant.
    Oracle
    The checked-in schema locations and public enum iteration are independent sides.
    Acceptance
    The two eight-key mappings are exactly equal and completed const equals
    COMPLETED.value.
    Interpretation
    Failure identifies a missing location or stored Python/schema vocabulary drift.
    Limitations
    Enum construction and lookup semantics remain class-owned; this does not establish
    derived status storage, provenance truth, execution validity, validation, or UQ.
    """
    defs = load_provenance_v1_schema()["$defs"]
    assert type(defs) is dict
    observed_schema_vocabularies = {
        "ArtifactLocation.kind": frozenset(
            defs["ArtifactLocation"]["properties"]["kind"]["enum"]
        ),
        "DeclaredCapability.kind": frozenset(
            defs["DeclaredCapability"]["properties"]["kind"]["enum"]
        ),
        "ExecutionCorrelationResult.issues.items": frozenset(
            defs["ExecutionCorrelationResult"]["properties"]["issues"]["items"]["enum"]
        ),
        "ExternalExecutionFailure.stage": frozenset(
            defs["ExternalExecutionFailure"]["properties"]["stage"]["enum"]
        ),
        "ExternalExecutionFailure.code": frozenset(
            defs["ExternalExecutionFailure"]["properties"]["code"]["enum"]
        ),
        "LineageRelation.kind": frozenset(
            defs["LineageRelation"]["properties"]["kind"]["enum"]
        ),
        "RunManifest.state": frozenset(
            defs["RunManifest"]["properties"]["state"]["enum"]
        ),
        "VerificationObservation.status": frozenset(
            defs["VerificationObservation"]["properties"]["status"]["enum"]
        ),
    }
    public_python_vocabularies = {
        "ArtifactLocation.kind": frozenset(
            member.value for member in provenance.ArtifactLocationKind
        ),
        "DeclaredCapability.kind": frozenset(
            member.value for member in provenance.CapabilityKind
        ),
        "ExecutionCorrelationResult.issues.items": frozenset(
            member.value for member in provenance.CorrelationIssue
        ),
        "ExternalExecutionFailure.stage": frozenset(
            member.value for member in provenance.ExternalFailureStage
        ),
        "ExternalExecutionFailure.code": frozenset(
            member.value for member in provenance.ExternalFailureCode
        ),
        "LineageRelation.kind": frozenset(
            member.value for member in provenance.LineageKind
        ),
        "RunManifest.state": frozenset(
            member.value for member in provenance.ManifestState
        ),
        "VerificationObservation.status": frozenset(
            member.value for member in provenance.VerificationStatus
        ),
    }
    assert observed_schema_vocabularies == public_python_vocabularies
    assert (
        defs["ExternalExecutionResult"]["properties"]["status"]["const"]
        == provenance.ExternalExecutionStatus.COMPLETED.value
    )


def test_artifact__derived_statuses__remain_unstored_public_properties() -> None:
    """Evidence ID
    SV-PROV-398
    Requirement
    Verification and correlation statuses remain public derived properties absent from
    dataclass storage, schema properties, and serialized version-1 JSON.
    Method
    Inspect public dataclass fields and property descriptors, inspect two explicit
    schema property maps, serialize valid representative records, and compare one map.
    Oracle
    Dataclass reflection, explicit schema definitions, Python property semantics, and
    public serializer output independently expose the four storage relations.
    Acceptance
    For both classes, status is absent from fields, schema, and JSON but is a property.
    Interpretation
    Failure identifies derived-property exposure or duplicated wire/storage state drift.
    Limitations
    This does not retest derived outcomes, prove persistence, establish provenance
    truth, validate science, quantify uncertainty, or implement cross-language
    conformance.
    """
    defs = load_provenance_v1_schema()["$defs"]
    assert type(defs) is dict
    verification_result = provenance.ArtifactIdentityVerificationResult(
        "artifact-1", "a" * 64, "a" * 64, 1, 1
    )
    correlation_result = provenance.ExecutionCorrelationResult(
        "request-1", "outcome-1", ()
    )
    serializer = provenance.ProvenanceJsonSerializer()
    observed_relations = {
        "ArtifactIdentityVerificationResult": {
            "dataclass_field": "status"
            in {
                field.name
                for field in fields(provenance.ArtifactIdentityVerificationResult)
            },
            "schema_property": "status"
            in defs["ArtifactIdentityVerificationResult"]["properties"],
            "public_property": isinstance(
                provenance.ArtifactIdentityVerificationResult.status, property
            ),
            "serialized_key": "status"
            in json.loads(serializer.serialize(verification_result)),
        },
        "ExecutionCorrelationResult": {
            "dataclass_field": "status"
            in {field.name for field in fields(provenance.ExecutionCorrelationResult)},
            "schema_property": "status"
            in defs["ExecutionCorrelationResult"]["properties"],
            "public_property": isinstance(
                provenance.ExecutionCorrelationResult.status, property
            ),
            "serialized_key": "status"
            in json.loads(serializer.serialize(correlation_result)),
        },
    }
    expected_relations = {
        "ArtifactIdentityVerificationResult": {
            "dataclass_field": False,
            "schema_property": False,
            "public_property": True,
            "serialized_key": False,
        },
        "ExecutionCorrelationResult": {
            "dataclass_field": False,
            "schema_property": False,
            "public_property": True,
            "serialized_key": False,
        },
    }
    assert observed_relations == expected_relations


def test_artifact__nfc_format__distinguishes_normalized_text() -> None:
    """Evidence ID
    SV-PROV-066
    Requirement
    The schema NFC format checker accepts normalized text and rejects a canonically
    equivalent decomposed representative.
    Method
    Register is_nfc_text for format ``nfc`` and validate explicit composed and
    decomposed logical paths against ArtifactSpecification.
    Oracle
    Python unicodedata NFC normalization independently predicts the two outcomes.
    Acceptance
    ``é/result.json`` validates and ``e\u0301/result.json`` raises ValidationError.
    Interpretation
    Failure identifies schema format wiring, Unicode oracle, or checker activation
    drift.
    Limitations
    This representative pair does not establish full path grammar, fixture-family
    classification, provenance truth, scientific validation, UQ, or persistence.
    """
    checker = jsonschema.FormatChecker()
    checker.checks("nfc")(is_nfc_text)
    definition = load_provenance_v1_schema()["$defs"]["ArtifactSpecification"]
    validator = jsonschema.Draft202012Validator(definition, format_checker=checker)
    base = {
        "record_type": "artifact_specification",
        "schema_version": 1,
        "format": "json",
        "retention_policy": "retain",
        "semantic_role": "result",
    }
    validator.validate(base | {"logical_path": "é/result.json"})
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(base | {"logical_path": "e\u0301/result.json"})
