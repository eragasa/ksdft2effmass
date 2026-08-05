"""Evidence class and represented meaning
Software verification of the provenance version-1 Python/JSON Schema boundary.
Owned contract, oracle, and scope
The Python runtime and Draft 2020-12 schema agreement is the artifact owner; fixed
definitions and enums are exact oracles.
VVUQ and scientific exclusions
Evidence excludes storage, numerical verification, scientific validation, UQ, physical
correctness, and unimplemented cross-language runtimes.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest

from ksdft2effmass import provenance

REPO_ROOT = Path(__file__).resolve().parents[5]
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


def _schema() -> dict[str, Any]:
    """Evidence ID
    Supports SV-PROV-064 and SV-PROV-065 and owns no separate identifier.
    Requirement
    Load the single authorized public version-1 schema without transformation.
    Method
    Read UTF-8 and decode standard JSON from the fixed repository path.
    Oracle
    The ownership manifest and P2 specification path select the artifact.
    Acceptance
    Return a JSON object.
    Interpretation
    Helper failure is artifact setup failure only.
    Limitations
    Loading alone establishes no schema validity.
    """
    value = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_artifact__draft_and_definition_inventory__compiles_exact_schema() -> None:
    """Evidence ID
    SV-PROV-064
    Requirement
    The public provenance schema is valid Draft 2020-12 and contains exactly one
    definition per serializable public record.
    Method
    Apply the external metaschema checker and compare $defs plus oneOf references with
    fixed inventories.
    Oracle
    Draft 2020-12 metaschema and the accepted eighteen serializable record families are
    independent.
    Acceptance
    check_schema succeeds; definition names and oneOf references equal the fixed sets
    exactly.
    Interpretation
    Failure may indicate malformed schema, inventory drift, or validator-library
    behavior.
    Limitations
    Metaschema compilation does not prove Python runtime agreement or fixture validity.
    """
    schema = _schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    definitions = schema["$defs"]
    assert isinstance(definitions, dict)
    assert set(definitions) == EXPECTED_DEFINITIONS
    assert {
        item["$ref"].removeprefix("#/$defs/") for item in schema["oneOf"]
    } == EXPECTED_DEFINITIONS


def test_artifact__schema_enum_values__agree_with_python_enums() -> None:
    """Evidence ID
    SV-PROV-065
    Requirement
    Stored closed vocabularies agree exactly, while artifact/correlation statuses remain
    derived Python relations and are absent from structural wire records.
    Method
    Compare stored schema enum locations with Python enums, assert derived status fields
    are absent, and derive statuses from valid public records.
    Oracle
    The corrected structural schema and public derived-property contracts independently
    define their divided responsibilities.
    Acceptance
    Stored sets are equal, completed const matches, derived fields are absent, and
    representative Python properties derive VERIFIED and CORRELATED.
    Interpretation
    Failure indicates Python/schema vocabulary drift.
    Limitations
    Representative derived relations are not exhaustive and no external execution is
    validated.
    """
    defs = _schema()["$defs"]
    assert isinstance(defs, dict)
    comparisons = (
        ("ArtifactLocation", "kind", provenance.ArtifactLocationKind),
        ("DeclaredCapability", "kind", provenance.CapabilityKind),
        ("ExternalExecutionFailure", "stage", provenance.ExternalFailureStage),
        ("ExternalExecutionFailure", "code", provenance.ExternalFailureCode),
        ("LineageRelation", "kind", provenance.LineageKind),
        ("RunManifest", "state", provenance.ManifestState),
        ("VerificationObservation", "status", provenance.VerificationStatus),
    )
    for definition, field, enum_type in comparisons:
        assert set(defs[definition]["properties"][field]["enum"]) == {
            item.value for item in enum_type
        }
    assert (
        defs["ExternalExecutionResult"]["properties"]["status"]["const"] == "completed"
    )
    assert {item.value for item in provenance.ExternalExecutionStatus} == {"completed"}
    assert "status" not in defs["ArtifactIdentityVerificationResult"]["properties"]
    assert "status" not in defs["ExecutionCorrelationResult"]["properties"]
    assert (
        provenance.ArtifactIdentityVerificationResult(
            "a", "a" * 64, "a" * 64, 1, 1
        ).status
        is provenance.ArtifactIdentityVerificationStatus.VERIFIED
    )
    assert (
        provenance.ExecutionCorrelationResult("r", "o", ()).status
        is provenance.CorrelationStatus.CORRELATED
    )


def test_artifact__nfc_format_contract__is_asserted_by_runtime_format_checker() -> None:
    """Evidence ID
    SV-PROV-066
    Requirement
    Schema format=nfc is actively assertable and distinguishes NFC from canonically
    decomposed text.
    Method
    Register an explicit Unicode-normalization checker and validate representative
    valid/invalid logical paths.
    Oracle
    Python unicodedata NFC normalization is independent of production path validation.
    Acceptance
    NFC input validates and decomposed input raises jsonschema.ValidationError.
    Interpretation
    Failure may indicate schema, format-checker, Unicode database, or evidence drift.
    Limitations
    Other lexical path restrictions are covered by fixtures and constructor evidence.
    """
    checker = jsonschema.FormatChecker()

    @checker.checks("nfc")
    def is_nfc(value: object) -> bool:
        return type(value) is str and unicodedata.normalize("NFC", value) == value

    definition = _schema()["$defs"]["ArtifactSpecification"]
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
