"""Public operator-record JSON Schema software-verification integration evidence.

Object: language-neutral schema and its interoperability with Python serializer
output and golden classifications. Evidence class: software verification, kept
distinct from runtime ``SV-ORJS`` behavior. Requirement: draft 2020-12 schema is
well formed, admits serializer output and valid fixtures, and rejects structurally
invalid fixtures it can express. Strategy: use the explicitly declared optional-
development ``jsonschema`` verification dependency. Oracle: approved public
schema/fixture contract plus independent validator. Acceptance is validator
agreement within documented
cross-field exclusions. Passing is not scientific validation, UQ, serializer-
internal validation, or Rust conformance; failure indicates artifact/runtime drift.
"""

import json
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification
SPEC = Path(__file__).resolve().parents[5] / "specification/operator-record/v1"


def load_json(path: Path) -> Any:
    """Support SV-ORJSC-001 through SV-ORJSC-003 by loading one public artifact.

    Evidence ID: supporting helper (no executable owner). Requirement: schema and
    fixture files contain standard JSON. Method: UTF-8 text plus standard parser.
    Oracle: JSON syntax. Interpretation: returns unmodified decoded content.
    Limitations: it does not validate schema semantics, scientific validity, UQ,
    serializer behavior, or Rust conformance.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def test_public_schema_is_valid_draft_2020_12() -> None:
    """Evidence ID: SV-ORJSC-001.

    Requirement: the public artifact is a valid draft-2020-12 JSON Schema with
    fixed version-one identity. Method: select the validator from ``$schema``, run
    that dialect validator's schema checker, and inspect public declarations.
    Oracle: the published metamodel and
    approved schema ID/version. Acceptance is no SchemaError and exact declarations.
    Interpretation: failure makes the conformance artifact unusable. Limitations:
    validator dependency correctness, scientific validation, UQ, and Rust
    conformance are not established.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    assert validator_class is jsonschema.Draft202012Validator
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"] == {"const": 1}


def test_serializer_output_and_valid_fixtures_conform_to_schema() -> None:
    """Evidence ID: SV-ORJSC-002.

    Requirement: Python serializer output and every valid golden artifact satisfy
    the public schema. Method: validate minimal serializer output and enumerated
    valid files with the validator selected from the schema's declared dialect.
    Oracle: public schema, independently executed by jsonschema. Acceptance is no
    ValidationError. Interpretation:
    failure indicates schema/serializer/fixture divergence. Limitations: this does
    not prove cross-field semantics, scientific validation, UQ, dependency
    correctness, or Rust conformance.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    serializer_payload = json.loads((SPEC / "valid/minimal.json").read_text())
    # Deserialize/reserialize ensures the checked object is actual serializer output.
    serializer_payload = json.loads(
        OperatorRecordJsonSerializer().serialize(
            OperatorRecordJsonSerializer().deserialize(json.dumps(serializer_payload))
        )
    )
    validator.validate(serializer_payload)
    for path in sorted((SPEC / "valid").glob("*.json")):
        validator.validate(load_json(path))


@pytest.mark.parametrize(
    "name",
    [
        "boolean-as-number.json",
        "duplicate-basis-label.json",
        "empty-string.json",
        "energy-reference-value.json",
        "missing-field.json",
        "nonorthogonal-basis.json",
        "numeric-string.json",
        "unknown-field.json",
        "unsupported-version.json",
    ],
)
def test_schema_rejects_expressible_invalid_fixture_classes(name: str) -> None:
    """Evidence ID: SV-ORJSC-003.

    Requirement: schema rejects every golden invalid class expressible by its
    structural keywords. Method: validate the explicitly enumerated subset with
    the validator selected from ``$schema``. Oracle: independent jsonschema
    evaluation of approved constraints. Acceptance
    is ValidationError. Interpretation: failure indicates schema weakening.
    Limitations: dimension agreement, matrix squareness/raggedness, cell linear
    independence, and finite-number parser policy require runtime validation;
    scientific validation, UQ, and Rust conformance are not performed.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(load_json(SPEC / "invalid" / name))
