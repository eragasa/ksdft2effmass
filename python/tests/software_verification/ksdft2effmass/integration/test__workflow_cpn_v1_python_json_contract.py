r"""Software verification of workflow cpn v1 python json contract.

Facet and represented meaning

--------------------------------------
Software verification of the version-1 CPN Python runtime <-> version-1 CPN JSON
Schema and wire contract, a represented software boundary rather than a physical or
numerical model.

Intrinsic and cross-object scope

--------------------------------
The version-1 CPN Python runtime <-> version-1 CPN JSON Schema and wire contract is the
primary boundary owner. Draft 2020-12, fixed schema definitions, public Python enums,
and accepted version-1 numeric/control boundaries provide the exact contract oracles.

VVUQ and scientific exclusions

------------------------------
Passing confirms only the exercised Python/JSON agreement facets; failure may indicate
runtime, schema, library, or evidence drift. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, persistence, engine
execution, and Rust conformance are excluded."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
import pytest
from referencing import Registry, Resource

from ksdft2effmass.workflows.cpn import (
    ContractValue,
    ContractValueKind,
    CpnErrorCode,
    CpnIssueCode,
    CpnToken,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
ROOT = REPO_ROOT / "specification" / "workflow-cpn" / "v1"
SCHEMAS = tuple(sorted(ROOT.glob("*.schema.json")))
pytestmark = pytest.mark.software_verification


def load_schema_json(path: Path) -> Any:
    """Evidence ID: Owns no identifier; supports SV-CPN-027, SV-CPN-028, SV-CPN-087,
    SV-CPN-088,
    SV-CPN-153, SV-CPN-154, SV-CPN-155, SV-CPN-156, SV-CPN-157, SV-CPN-158,
    SV-CPN-159, SV-CPN-161, SV-CPN-162, SV-CPN-163, SV-CPN-164, SV-CPN-166,
    SV-CPN-167.

    Requirement: Load a repository JSON artifact without transforming its represented
    values.

    Method: Read UTF-8 text and apply the standard JSON decoder.

    Oracle: Standard JSON decoding and the supplied repository path define the expected
    operation.

    Acceptance: Return the decoded object or propagate the decoder/read failure.

    Interpretation: This helper supports the named evidence and owns no separate pass
    claim.

    Limitations: It does not validate schema meaning, file inventory, or scientific
    content."""
    return json.loads(path.read_text(encoding="utf-8"))


def make_schema_registry() -> Registry:
    """Evidence ID: Owns no identifier; supports SV-CPN-028, SV-CPN-087, SV-CPN-088,
    SV-CPN-153,
    SV-CPN-156, SV-CPN-157, SV-CPN-158, SV-CPN-159, SV-CPN-161, SV-CPN-162,
    SV-CPN-163, SV-CPN-164, SV-CPN-166, SV-CPN-167.

    Requirement: Provide a local-only registry containing every discovered version-1
    schema under its
    public ``$id``.

    Method: Load discovered schemas and register each resource by its declared
    identifier.

    Oracle: The discovered schema documents and referencing registry contract define the
    mapping.

    Acceptance: Return a registry containing each loaded ``$id`` without network
    resolution.

    Interpretation: This helper supports the named evidence and owns no separate pass
    claim.

    Limitations: It does not assert the exact schema inventory or validate schema
    semantics."""
    contents_by_path = tuple(load_schema_json(path) for path in SCHEMAS)
    assert all(isinstance(contents, dict) for contents in contents_by_path)
    return Registry().with_resources(
        (contents["$id"], Resource.from_contents(contents))
        for contents in contents_by_path
    )


def schema_validation_succeeds(validator: Any, instance: Any) -> bool:
    """Evidence ID: Owns no identifier; supports SV-CPN-028, SV-CPN-087, SV-CPN-088,
    SV-CPN-153,
    SV-CPN-159, SV-CPN-161.

    Requirement: Expose repeated schema-validation mechanics without an independent
    evidence claim.

    Method: Invoke the supplied public validator on one synthetic schema or instance.

    Oracle: Each supported artifact test owns its schema oracle; this helper owns none.

    Acceptance: Return ``True`` after validation completes and propagate every
    validation failure.

    Interpretation: Helper failure invalidates the supported artifact evidence
    execution.

    Limitations: This helper does not establish schema meaning, runtime semantics,
    science, or UQ.
    """
    validator.validate(instance)
    return True


def schema_check_succeeds(schema: Any) -> bool:
    """Evidence ID: Owns no identifier; supports SV-CPN-027.

    Requirement: Expose metaschema-check mechanics without an independent evidence
    claim.

    Method: Select the declared validator and check one discovered schema.

    Oracle: The supported artifact test owns the metaschema oracle; this helper owns
    none.

    Acceptance: Return ``True`` after checking and propagate every schema error.

    Interpretation: Helper failure invalidates the supported metaschema evidence
    execution.

    Limitations: This helper does not assert inventory completeness, science,
    validation, or UQ.
    """
    jsonschema.validators.validator_for(schema).check_schema(schema)
    return True


def test_artifact__json_schemas__satisfy_draft_2020_12_metaschema() -> None:
    """Evidence ID: SV-CPN-027

    Requirement: Every discovered version-1 CPN schema satisfies JSON Schema Draft
    2020-12.

    Method: Load each ``*.schema.json`` file and apply its selected validator class
    ``check_schema``; no warnings are expected.

    Oracle: The official Draft 2020-12 metaschema implemented by ``jsonschema`` is
    external to
    the project schemas.

    Acceptance: Every discovered schema completes metaschema checking without exception.

    Interpretation: Pass supports syntax/keyword validity; failure may indicate
    malformed schemas,
    unsupported keywords, discovery drift, or library behavior.

    Limitations: The exact seven-file inventory is not asserted. Runtime agreement,
    numerical
    verification, scientific validation, UQ, and cross-language conformance are
    excluded."""
    schemas = tuple(load_schema_json(path) for path in SCHEMAS)
    assert all(schema_check_succeeds(schema) for schema in schemas)


CONTRACT_ID = (
    "https://github.com/eragasa/ksdft2effmass/"
    "specification/workflow-cpn/v1/cpn-contract.schema.json"
)


def definition_validator(registry: Registry, name: str) -> Any:
    """Evidence ID: Owns no identifier; supports SV-CPN-087, SV-CPN-088, SV-CPN-153,
    SV-CPN-156,
    SV-CPN-157, SV-CPN-158, SV-CPN-159, SV-CPN-161, SV-CPN-162, SV-CPN-163,
    SV-CPN-164, SV-CPN-166, SV-CPN-167.

    Requirement: Provide local definition-validator setup without an independent
    evidence claim.

    Method: Construct a Draft 2020-12 validator referencing one named public definition.

    Oracle: The fixed contract identifier and caller-supplied definition name fix the
    reference.

    Acceptance: Return the validator without network resolution or swallowed errors.

    Interpretation: Failure invalidates the supported artifact evidence setup.

    Limitations: The helper does not validate the registry, definition meaning, science,
    or UQ.
    """
    return jsonschema.Draft202012Validator(
        {"$ref": f"{CONTRACT_ID}#/$defs/{name}"}, registry=registry
    )


def contract_value_validator() -> Any:
    """Evidence ID: Owns no identifier; supports SV-CPN-087, SV-CPN-158, SV-CPN-159,
    SV-CPN-161,
    SV-CPN-162, SV-CPN-163, SV-CPN-164, SV-CPN-166.

    Requirement: Provide local contract-value validator setup without an independent
    claim.

    Method: Resolve the public contract-value definition through the local schema
    registry.

    Oracle: The fixed version-1 contract-value reference defines the setup.

    Acceptance: Return a validator without network resolution or swallowed errors.

    Interpretation: Failure invalidates the supported numeric interoperability evidence
    setup.

    Limitations: Setup alone establishes no wire agreement, numerical verification,
    science, or UQ.
    """
    return definition_validator(make_schema_registry(), "contractValue")


def token_validator() -> Any:
    """Evidence ID: Owns no identifier; supports SV-CPN-088, SV-CPN-167.

    Requirement: Provide local token-validator setup without an independent evidence
    claim.

    Method: Resolve the public token definition through the local schema registry.

    Oracle: The fixed version-1 token reference defines the setup.

    Acceptance: Return a validator without network resolution or swallowed errors.

    Interpretation: Failure invalidates supported control-field boundary evidence.

    Limitations: Setup alone establishes no persistence, cross-language, science, or UQ
    claim.
    """
    return definition_validator(make_schema_registry(), "token")


def make_runtime_token(value: int) -> CpnToken:
    """Evidence ID: Owns no identifier; supports SV-CPN-088, SV-CPN-167.

    Requirement: Construct the complete synthetic runtime token for one control value.

    Method: Pass fixed identities and the supplied integer to both expression-visible
    controls.

    Oracle: The accepted complete public token field mapping fixes the counterpart.

    Acceptance: Return the exact public token or propagate its public contract error.

    Interpretation: Failure invalidates the supported boundary evidence setup.

    Limitations: Synthetic identities have no scientific meaning and provide no UQ.
    """
    return CpnToken(
        "token",
        "color",
        "workflow",
        "run",
        None,
        "attempt",
        None,
        value,
        "payload-type",
        "payload",
        value,
        (),
        (),
        None,
        None,
    )


def make_wire_token(value: int) -> dict[str, object]:
    """Evidence ID: Owns no identifier; supports SV-CPN-088, SV-CPN-167.

    Requirement: Construct the exact version-1 wire token counterpart for one control
    value.

    Method: Return fixed JSON fields with the supplied value in both public controls.

    Oracle: The accepted token wire mapping fixes every key and value.

    Acceptance: Return the exact mapping consumed by the supported schema evidence.

    Interpretation: Failure invalidates supported boundary evidence setup.

    Limitations: This helper does not validate schema meaning, persistence, science, or
    UQ.
    """
    return {
        "token_id": "token",
        "color_id": "color",
        "workflow_id": "workflow",
        "run_id": "run",
        "parent_run_id": None,
        "attempt_id": "attempt",
        "retry_parent_attempt_id": None,
        "iteration_index": value,
        "payload_type_id": "payload-type",
        "payload_id": "payload",
        "payload_schema_version": value,
        "provenance_ids": [],
        "parent_token_ids": [],
        "correlation_id": None,
        "authorization_id": None,
        "outcome": None,
    }


ENTRY_POINT_CASES = (
    pytest.param("cpn-net.schema.json", "minimal-net.json", id="net_entry_point"),
    pytest.param(
        "cpn-marking.schema.json", "multiset-marking.json", id="marking_entry_point"
    ),
    pytest.param(
        "cpn-firing.schema.json", "synchronized-firing.json", id="firing_entry_point"
    ),
)


@pytest.mark.parametrize(("schema_name", "fixture_name"), ENTRY_POINT_CASES)
def test_artifact__schema_entry_points__resolve_valid_fixtures_locally(
    schema_name: str, fixture_name: str
) -> None:
    """Evidence ID: SV-CPN-028

    Requirement: Each version-1 schema entry point resolves locally for its declared
    valid fixture.

    Method: Validate one explicit fixture through a registry containing only repository
    schemas.

    Oracle: The public schema entry point and declared valid fixture classification fix
    success.

    Acceptance: Validation completes without exception or network resolution.

    Interpretation: Failure may identify schema, fixture, registry, library, or evidence
    drift.

    Limitations: This checks wire shape, not runtime semantics, scientific validation,
    UQ, or Rust.
    """
    validator = jsonschema.Draft202012Validator(
        load_schema_json(ROOT / schema_name), registry=make_schema_registry()
    )
    assert schema_validation_succeeds(
        validator, load_schema_json(ROOT / "valid" / fixture_name)
    )


DEFINITION_CASES = (
    pytest.param(
        "contractValue",
        {"kind": "string_sequence", "value": ["a", "a"]},
        id="contract_value",
    ),
    pytest.param("guardEvaluationResult", {"value": True}, id="guard_result"),
    pytest.param(
        "transitionEnablementResult",
        {"transition_id": "t", "bindings": []},
        id="enablement_result",
    ),
    pytest.param(
        "validationIssue",
        {
            "code": "unknown_color",
            "path": ["places", "p"],
            "related_ids": ["missing"],
            "message": "unknown color",
        },
        id="validation_issue",
    ),
    pytest.param("validationResult", {"issues": []}, id="validation_result"),
)


@pytest.mark.parametrize(("definition_name", "instance"), DEFINITION_CASES)
def test_artifact__contract_definitions__accept_representative_valid_values(
    definition_name: str, instance: dict[str, object]
) -> None:
    """Evidence ID: SV-CPN-153

    Requirement: Required public contract definitions resolve locally and accept
    declared valid
    shape.

    Method: Validate one explicit synthetic instance through its named definition.

    Oracle: The version-1 definition and fixed valid instance provide the shape oracle.

    Acceptance: Definition validation completes without exception or network access.

    Interpretation: Failure may identify definition, instance, registry, library, or
    evidence drift.

    Limitations: Representative shape evidence excludes exhaustive semantics, science,
    UQ, and Rust.
    """
    assert schema_validation_succeeds(
        definition_validator(make_schema_registry(), definition_name), instance
    )


def test_artifact__contract_definitions__contain_required_inventory() -> None:
    """Evidence ID: SV-CPN-154

    Requirement: The version-1 contract contains every required public result, request,
    and error
    definition.

    Method: Inspect the decoded public ``$defs`` mapping without runtime construction.

    Oracle: A fixed literal required-name set independently defines inventory
    completeness.

    Acceptance: Every required literal name is present in ``$defs``.

    Interpretation: Failure identifies missing or renamed public wire definitions or
    evidence drift.

    Limitations: Extra definitions and definition semantics are excluded, as are science
    and UQ.
    """
    definitions = load_schema_json(ROOT / "cpn-contract.schema.json")["$defs"]
    assert {
        "guardEvaluationResult",
        "transitionEnablementResult",
        "firingRequest",
        "firingResult",
        "validationIssueCode",
        "validationIssue",
        "validationResult",
        "errorCode",
        "errorDetail",
    } <= set(definitions)


@pytest.mark.parametrize(
    ("definition_name", "runtime_values"),
    (
        pytest.param(
            "validationIssueCode",
            {item.value for item in CpnIssueCode},
            id="issue_codes",
        ),
        pytest.param(
            "errorCode", {item.value for item in CpnErrorCode}, id="error_codes"
        ),
    ),
)
def test_artifact__schema_enum_vocabularies__agree_with_python_exports(
    definition_name: str, runtime_values: set[str]
) -> None:
    """Evidence ID: SV-CPN-155

    Requirement: Closed schema error vocabularies equal their corresponding public
    Python enums.

    Method: Compare one explicit relation pair by exact set equality.

    Oracle: Agreement itself is the artifact relation; neither side is used as its own
    oracle.

    Acceptance: Schema and Python value sets are exactly equal.

    Interpretation: Failure identifies schema/runtime vocabulary drift or wrong relation
    setup.

    Limitations: Enum behavior, ordering, science, UQ, and Rust implementation are
    excluded.
    """
    definitions = load_schema_json(ROOT / "cpn-contract.schema.json")["$defs"]
    assert runtime_values == set(definitions[definition_name]["enum"])


def test_artifact__string_sequence_wire_value__rejects_empty_entry() -> None:
    """Evidence ID: SV-CPN-156

    Requirement: A contract string sequence rejects an empty entry while permitting
    duplicates
    elsewhere.

    Method: Validate the fixed single-empty-entry instance through the public
    definition.

    Oracle: The nonempty string-item schema invariant fixes rejection.

    Acceptance: Validation raises exactly ``jsonschema.ValidationError``.

    Interpretation: Failure permits an invalid routing identifier or indicates
    schema/evidence drift.

    Limitations: Other string grammar, runtime construction, science, UQ, and Rust are
    excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        definition_validator(make_schema_registry(), "contractValue").validate(
            {"kind": "string_sequence", "value": [""]}
        )


def test_artifact__firing_request_wire_value__rejects_duplicate_output_ids() -> None:
    """Evidence ID: SV-CPN-157

    Requirement: A firing request rejects duplicate output token identifiers.

    Method: Validate one fixed duplicate-ID request through the public definition.

    Oracle: The unique output-token-ID schema invariant fixes rejection.

    Acceptance: Validation raises exactly ``jsonschema.ValidationError``.

    Interpretation: Failure permits ambiguous output identity or indicates
    schema/evidence drift.

    Limitations: Runtime firing, engine behavior, science, UQ, and Rust are excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        definition_validator(make_schema_registry(), "firingRequest").validate(
            {
                "transition_id": "t",
                "binding": {"transition_id": "t", "assignments": []},
                "output_token_ids": ["duplicate", "duplicate"],
            }
        )


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(-(2**63), id="minimum_i64"),
        pytest.param(0, id="zero"),
        pytest.param(2**63 - 1, id="maximum_i64"),
    ),
)
def test_artifact__integer_wire_runtime_agreement__accepts_signed_i64(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-087

    Requirement: Tagged INTEGER wire and runtime values admit the inclusive signed-i64
    domain.

    Method: Validate and construct one explicit boundary partition without warnings.

    Oracle: Fixed signed-i64 endpoints and exact integer identity provide the
    independent
    oracle.

    Acceptance: Schema validation succeeds and runtime storage equals the exact built-in
    integer.

    Interpretation: Failure identifies schema/runtime numeric-domain disagreement or
    evidence drift.

    Limitations: This is interoperability software evidence, not numerical verification,
    science,
    or UQ.
    """
    assert schema_validation_succeeds(
        contract_value_validator(), {"kind": "integer", "value": value}
    )
    assert ContractValue(ContractValueKind.INTEGER, value).value == value


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(-(2**63) - 1, id="below_minimum_i64"),
        pytest.param(2**63, id="above_maximum_i64"),
    ),
)
def test_artifact__integer_wire_runtime_agreement__rejects_outside_signed_i64(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-158

    Requirement: Tagged INTEGER wire and runtime values reject integers outside
    signed-i64.

    Method: Validate and construct one explicit adjacent out-of-range value.

    Oracle: Fixed signed-i64 endpoints independently classify both adjacent values as
    invalid.

    Acceptance: Schema raises ``ValidationError`` and runtime construction raises
    ``ValueError``.

    Interpretation: Failure identifies numeric-domain disagreement or wrong boundary
    evidence.

    Limitations: Other values, numerical verification, science, UQ, and Rust are
    excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        contract_value_validator().validate({"kind": "integer", "value": value})
    with pytest.raises(ValueError):
        ContractValue(ContractValueKind.INTEGER, value)


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(0, id="integer_zero_to_real"),
        pytest.param(1.5, id="fractional_binary64"),
    ),
)
def test_artifact__real_wire_runtime_agreement__stores_binary64(
    value: int | float,
) -> None:
    """Evidence ID: SV-CPN-159

    Requirement: Admitted REAL wire numbers canonicalize to built-in finite binary64
    runtime values.

    Method: Validate and construct one exact synthetic REAL input.

    Oracle: Python binary64 conversion and exact built-in type semantics provide the
    oracle.

    Acceptance: Schema validation succeeds and runtime storage has exact type ``float``.

    Interpretation: Failure identifies wire/runtime REAL admission disagreement.

    Limitations: This is software interoperability evidence, not accuracy, science, or
    UQ.
    """
    assert schema_validation_succeeds(
        contract_value_validator(), {"kind": "real", "value": value}
    )
    assert type(ContractValue(ContractValueKind.REAL, value).value) is float


def test_artifact__real_runtime_canonicalization__rounds_above_exact_integer() -> None:
    """Evidence ID: SV-CPN-160

    Requirement: REAL canonicalization follows binary64 rounding above the exact-integer
    range.

    Method: Construct the fixed integer ``2**53 + 1`` through the public runtime value.

    Oracle: Python binary64 conversion fixes the exact stored result ``float(2**53)``.

    Acceptance: Stored value equals ``float(2**53)`` exactly and differs from the
    integer input.

    Interpretation: Failure identifies runtime binary64 canonicalization drift.

    Limitations: This is a software conversion check, not general numerical verification
    or science.
    """
    stored = ContractValue(ContractValueKind.REAL, 2**53 + 1).value
    assert stored == float(2**53)
    assert stored != 2**53 + 1


@pytest.mark.parametrize(
    "value",
    (
        pytest.param((2**53 - 1) * 2**971 + 1, id="rounded_to_maximum_binary64"),
        pytest.param(2**1024 - 2**970 - 1, id="last_integer_rounding_to_binary64"),
    ),
)
def test_artifact__real_wire_runtime_agreement__accepts_last_finite_integers(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-161

    Requirement: REAL wire/runtime values admit integers that round to maximum finite
    binary64.

    Method: Validate and construct one independently fixed upper-bound integer.

    Oracle: Binary64 boundary derivation fixes ``0x1.fffffffffffffp+1023`` as stored
    value.

    Acceptance: Schema succeeds; runtime equals maximum finite binary64 and is not
    infinity.

    Interpretation: Failure identifies upper-bound wire/runtime disagreement or oracle
    transcription.

    Limitations: Synthetic boundary software evidence is not numerical verification,
    science, or UQ.
    """
    assert schema_validation_succeeds(
        contract_value_validator(), {"kind": "real", "value": value}
    )
    stored = ContractValue(ContractValueKind.REAL, value).value
    assert stored == float.fromhex("0x1.fffffffffffffp+1023")
    assert stored != float("inf")


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(2**1024 - 2**970, id="positive_adjacent_binary64_overflow"),
        pytest.param(-(2**1024 - 2**970), id="negative_adjacent_binary64_overflow"),
    ),
)
def test_artifact__real_wire_runtime_agreement__rejects_adjacent_overflow(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-162

    Requirement: REAL wire/runtime values reject adjacent integers that overflow
    binary64.

    Method: Validate and construct one signed adjacent overflow boundary.

    Oracle: The independently fixed last-finite integer makes each adjacent value
    invalid.

    Acceptance: Schema raises ``ValidationError`` and runtime raises binary64
    ``ValueError``.

    Interpretation: Failure identifies boundary disagreement or oracle transcription
    drift.

    Limitations: This is boundary interoperability evidence, not numerical verification
    or science.
    """
    with pytest.raises(jsonschema.ValidationError):
        contract_value_validator().validate({"kind": "real", "value": value})
    with pytest.raises(ValueError, match="overflows binary64"):
        ContractValue(ContractValueKind.REAL, value)


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(10**400, id="positive_enormous_integer"),
        pytest.param(-(10**400), id="negative_enormous_integer"),
    ),
)
def test_artifact__real_wire_runtime_agreement__rejects_enormous_integers(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-163

    Requirement: REAL wire/runtime values reject enormous integers that overflow
    binary64.

    Method: Validate and construct one signed synthetic enormous integer.

    Oracle: Its magnitude exceeds the independently fixed maximum finite binary64 range.

    Acceptance: Schema raises ``ValidationError`` and runtime raises binary64
    ``ValueError``.

    Interpretation: Failure identifies wire/runtime overflow disagreement.

    Limitations: This is software boundary evidence, not numerical verification,
    science, or UQ.
    """
    with pytest.raises(jsonschema.ValidationError):
        contract_value_validator().validate({"kind": "real", "value": value})
    with pytest.raises(ValueError, match="overflows binary64"):
        ContractValue(ContractValueKind.REAL, value)


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(float("inf"), id="positive_infinity"),
        pytest.param(float("-inf"), id="negative_infinity"),
    ),
)
def test_artifact__real_wire_runtime_agreement__rejects_infinity(value: float) -> None:
    """Evidence ID: SV-CPN-164

    Requirement: REAL wire/runtime values reject either infinity sign.

    Method: Validate and construct one explicit IEEE infinity.

    Oracle: ``math.isfinite`` semantics independently classify both inputs as nonfinite.

    Acceptance: Schema raises ``ValidationError`` and runtime raises finite-binary64
    ``ValueError``.

    Interpretation: Failure admits a nonstandard JSON numeric state or indicates
    evidence drift.

    Limitations: NaN encoding, numerical verification, science, UQ, and Rust are
    excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        contract_value_validator().validate({"kind": "real", "value": value})
    with pytest.raises(ValueError, match="must be finite binary64"):
        ContractValue(ContractValueKind.REAL, value)


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive_infinity"),
        pytest.param(float("-inf"), id="negative_infinity"),
    ),
)
def test_artifact__strict_json_runtime_agreement__rejects_nonfinite_real(
    value: float,
) -> None:
    """Evidence ID: SV-CPN-165

    Requirement: Strict JSON encoding and runtime REAL construction reject each
    nonfinite binary64.

    Method: Encode and construct one explicit nonfinite input through independent public
    layers.

    Oracle: Strict JSON and finite REAL contracts independently classify the input as
    invalid.

    Acceptance: Both layers raise their documented exact ``ValueError``.

    Interpretation: Failure identifies JSON/runtime nonfinite disagreement or evidence
    drift.

    Limitations: In-memory schema NaN behavior, numerical verification, science, UQ, and
    Rust are
    excluded.
    """
    with pytest.raises(ValueError, match="Out of range float values"):
        json.dumps({"kind": "real", "value": value}, allow_nan=False)
    with pytest.raises(ValueError, match="must be finite binary64"):
        ContractValue(ContractValueKind.REAL, value)


def test_artifact__unsigned_contract_value_kind__is_rejected_and_unexported() -> None:
    """Evidence ID: SV-CPN-166

    Requirement: Version 1 has no unsigned contract-value tag in schema or Python
    runtime vocabulary.

    Method: Validate a fixed unsigned-tag instance and inspect the public Python enum
    vocabulary.

    Oracle: The approved closed tag set excludes the literal ``unsigned_integer``.

    Acceptance: Schema raises ``ValidationError`` and the exact literal is absent from
    Python
    values.

    Interpretation: Failure identifies wire/runtime vocabulary drift.

    Limitations: Unsigned token fields, future versions, numerical verification,
    science, and UQ
    are excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        contract_value_validator().validate(
            {"kind": "unsigned_integer", "value": 2**63 - 1}
        )
    assert "unsigned_integer" not in {kind.value for kind in ContractValueKind}


@pytest.mark.parametrize(
    "value",
    (
        pytest.param(0, id="minimum_control"),
        pytest.param(2**63 - 1, id="maximum_control"),
    ),
)
def test_artifact__control_field_bounds__accepts_inclusive_signed_i64(
    value: int,
) -> None:
    """Evidence ID: SV-CPN-088

    Requirement: Expression-visible token controls admit inclusive nonnegative
    signed-i64 endpoints.

    Method: Validate and construct complete synthetic wire/runtime tokens at one
    endpoint.

    Oracle: The approved inclusive interval ``[0, 2**63 - 1]`` fixes acceptance.

    Acceptance: Schema succeeds and both runtime controls retain the exact input.

    Interpretation: Failure identifies schema/runtime control-bound disagreement.

    Limitations: Other fields, persistence, numerical verification, science, UQ, and
    Rust are
    excluded.
    """
    assert schema_validation_succeeds(token_validator(), make_wire_token(value))
    token = make_runtime_token(value)
    assert token.iteration_index == value
    assert token.payload_schema_version == value


def test_artifact__control_field_bounds__rejects_signed_i64_overflow() -> None:
    """Evidence ID: SV-CPN-167

    Requirement: Expression-visible token controls reject ``2**63`` in wire and runtime
    forms.

    Method: Validate and construct complete synthetic tokens at the adjacent upper
    overflow.

    Oracle: The approved maximum ``2**63 - 1`` independently classifies ``2**63`` as
    invalid.

    Acceptance: Schema raises ``ValidationError`` and runtime construction raises
    ``ValueError``.

    Interpretation: Failure identifies schema/runtime control-bound disagreement.

    Limitations: Negative values, persistence, numerical verification, science, UQ, and
    Rust are
    excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        token_validator().validate(make_wire_token(2**63))
    with pytest.raises(ValueError, match="signed i64"):
        make_runtime_token(2**63)
