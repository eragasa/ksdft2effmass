r"""Software verification of OperatorRecordJsonSchema.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This artifact-owned module owns the operator record json schema facet. Object:
language-neutral schema and its interoperability with Python serializer
output and golden classifications. Evidence class: software verification, kept
distinct from runtime ``SV-ORJS`` behavior. Requirement: draft 2020-12 schema is
well formed, admits serializer output and valid fixtures, and rejects structurally
invalid fixtures it can express. Strategy: use the explicitly declared optional-
development ``jsonschema`` verification dependency. Oracle: approved public
schema/fixture contract plus independent validator. Acceptance is validator
agreement within documented
cross-field exclusions. Passing is not scientific validation, UQ, serializer-
internal validation, or Rust conformance; failure indicates artifact/runtime drift.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordJsonSchema``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
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
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Schema evidence needs decoded JSON values from the named repository
    artifact without
    changing their bytes or meaning.

    Method: Construct or inspect only the named synthetic fixture operation (load json);
    the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def test_artifact__public_schema_is_valid_draft_2020_12__agrees_exactly() -> None:
    r"""Evidence ID: SV-ORJSC-001

    Requirement: The public version-1 JSON Schema has this exact structural property:
    public schema
    is valid draft 2020 12: agrees exactly.

    Method: Load the public schema and named literal fixture partition (public schema is
    valid
    draft 2020 12: agrees exactly), then apply Draft 2020-12 validation without invoking
    serializer private helpers.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: Schema validity, exact fixture membership, and acceptance or rejection
    by Draft
    2020-12 validation agree exactly with the declared fixture class.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    assert validator_class is jsonschema.Draft202012Validator
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"] == {"const": 1}


def test_artifact__serializer_output_and_valid_fixtures__agrees_exactly() -> None:
    r"""Evidence ID: SV-ORJSC-002

    Requirement: The public version-1 JSON Schema has this exact structural property:
    serializer
    output and valid fixtures: agrees exactly.

    Method: Load the public schema and named literal fixture partition (serializer
    output and
    valid fixtures: agrees exactly), then apply Draft 2020-12 validation without
    invoking serializer private helpers.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: Schema validity, exact fixture membership, and acceptance or rejection
    by Draft
    2020-12 validation agree exactly with the declared fixture class.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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
    assert all(
        validator.is_valid(load_json(path))
        for path in sorted((SPEC / "valid").glob("*.json"))
    )


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("duplicate-basis-label.json", id="duplicate_basis_label_json"),
        pytest.param("empty-string.json", id="empty_string_json"),
        pytest.param("energy-reference-value.json", id="energy_reference_value_json"),
        pytest.param("missing-field.json", id="missing_field_json"),
        pytest.param("nonorthogonal-basis.json", id="nonorthogonal_basis_json"),
    ],
)
def test_artifact__schema_rejects_expressible_invalid_fixture__agrees_exactly(
    name: str,
) -> None:
    r"""Evidence ID: SV-ORJSC-003

    Requirement: The public version-1 JSON Schema has this exact structural property:
    schema rejects
    expressible invalid fixture: agrees exactly.

    Method: Load the public schema and named literal fixture partition (schema rejects
    expressible invalid fixture: agrees exactly), then apply Draft 2020-12 validation
    without invoking serializer private helpers.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: The named partition raises exactly jsonschema.ValidationError with the
    asserted
    public message, code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(load_json(SPEC / "invalid" / name))


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("unknown-field.json", id="unknown_field_json"),
        pytest.param("unsupported-version.json", id="unsupported_version_json"),
    ],
)
def test_artifact__schema_rejects_unknown_value_fixtures__agrees_exactly(
    name: str,
) -> None:
    r"""Evidence ID: SV-ORJSC-005

    Requirement: The public version-1 JSON Schema has this exact structural property:
    schema rejects
    unknown value fixtures: agrees exactly.

    Method: Load the public schema and named literal fixture partition (schema rejects
    unknown
    value fixtures: agrees exactly), then apply Draft 2020-12 validation without
    invoking serializer private helpers.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: The named partition raises exactly jsonschema.ValidationError with the
    asserted
    public message, code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(load_json(SPEC / "invalid" / name))


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("boolean-as-number.json", id="boolean_as_number_json"),
        pytest.param("numeric-string.json", id="numeric_string_json"),
    ],
)
def test_artifact__schema_rejects_wrong_semantic_type_fixtures__agrees_exactly(
    name: str,
) -> None:
    r"""Evidence ID: SV-ORJSC-004

    Requirement: The public version-1 JSON Schema has this exact structural property:
    schema rejects
    wrong semantic type fixtures: agrees exactly.

    Method: Load the public schema and named literal fixture partition (schema rejects
    wrong
    semantic type fixtures: agrees exactly), then apply Draft 2020-12 validation without
    invoking serializer private helpers.

    Oracle: The checked-in Draft 2020-12 schema, its literal required-field vocabulary,
    and the
    classified valid/invalid fixture manifest define the expected structural result.

    Acceptance: The named partition raises exactly jsonschema.ValidationError with the
    asserted
    public message, code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    schema = load_json(SPEC / "operator-record.schema.json")
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(load_json(SPEC / "invalid" / name))
