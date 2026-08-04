"""Artifact-owned verification of version-1 CPN JSON schemas.

Evidence class: software verification. The tests use synthetic contract artifacts and
independent language/runtime or static-structure oracles. Passing is not numerical
verification, scientific validation, uncertainty quantification, engine execution,
persistence, or Rust conformance evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

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


def _load(path: Path) -> object:
    """Load one strict JSON schema or fixture from repository storage."""
    return json.loads(path.read_text(encoding="utf-8"))


def _registry() -> Registry:
    """Build a local-only registry keyed by each schema's fixed public ID."""
    registry = Registry()
    for path in SCHEMAS:
        contents = _load(path)
        assert isinstance(contents, dict)
        registry = registry.with_resource(
            contents["$id"], Resource.from_contents(contents)
        )
    return registry


def test_cpn_sv_p1_027_schemas_satisfy_their_metaschema() -> None:
    """SV-CPN-027: Draft 2020-12 schema validity.

    Requirement
    -----------
    The version-1 P1 contract requires Draft 2020-12 schema validity.

    Method
    ------
    Load each ``*.schema.json`` and invoke the validator class's ``check_schema``
    method.

    Independent oracle
    ------------------
    The official Draft 2020-12 metaschema implemented by jsonschema is independent
    of the project schemas.

    Acceptance criterion
    --------------------
    All seven version-1 schema documents satisfy their metaschema without exception.

    Failure interpretation
    ----------------------
    Failure identifies malformed schema syntax or unsupported keywords.

    Limitations
    -----------
    Metaschema validity does not establish Python/runtime relational agreement.
    """
    for path in SCHEMAS:
        schema = _load(path)
        validator = jsonschema.validators.validator_for(schema)
        validator.check_schema(schema)


def test_cpn_sv_p1_028_narrow_schema_entry_points_resolve_locally() -> None:
    """SV-CPN-028: local schema entry points and Python enum agreement.

    Requirement
    -----------
    The version-1 P1 contract requires local schema entry points and Python enum
    agreement.

    Method
    ------
    Resolve net/marking/firing fixtures through a local registry, then validate
    string sequences, exported result/validation definitions, enum sets, and
    duplicate firing IDs.

    Independent oracle
    ------------------
    Fixture classification plus exact Python ``CpnIssueCode``/``CpnErrorCode`` value
    sets are independent expected inventories.

    Acceptance criterion
    --------------------
    Valid instances pass; empty string sequences and duplicate output IDs fail;
    schema enums equal Python enums exactly.

    Failure interpretation
    ----------------------
    Failure means a broken local reference or Python/schema surface divergence.

    Limitations
    -----------
    Numeric boundary agreement is exercised separately by focused boundary cases.
    """
    registry = _registry()
    cases = (
        ("cpn-net.schema.json", "minimal-net.json"),
        ("cpn-marking.schema.json", "multiset-marking.json"),
        ("cpn-firing.schema.json", "synchronized-firing.json"),
    )
    for schema_name, fixture_name in cases:
        schema = _load(ROOT / schema_name)
        jsonschema.Draft202012Validator(schema, registry=registry).validate(
            _load(ROOT / "valid" / fixture_name)
        )

    contract_id = (
        "https://github.com/eragasa/ksdft2effmass/"
        "specification/workflow-cpn/v1/cpn-contract.schema.json"
    )

    def definition_validator(name: str) -> jsonschema.Draft202012Validator:
        """Return a local validator for one named contract definition."""
        return jsonschema.Draft202012Validator(
            {"$ref": f"{contract_id}#/$defs/{name}"}, registry=registry
        )

    # Ordered duplicate string values are required for repeated read bindings;
    # empty strings remain invalid at both Python and wire boundaries.
    string_sequence = {"kind": "string_sequence", "value": ["token-1", "token-1"]}
    definition_validator("contractValue").validate(string_sequence)
    with pytest.raises(jsonschema.ValidationError):
        definition_validator("contractValue").validate(
            {"kind": "string_sequence", "value": [""]}
        )
    definition_validator("guardEvaluationResult").validate({"value": True})
    definition_validator("transitionEnablementResult").validate(
        {"transition_id": "t", "bindings": []}
    )
    definition_validator("validationIssue").validate(
        {
            "code": "unknown_color",
            "path": ["places", "p"],
            "related_ids": ["missing"],
            "message": "unknown color",
        }
    )
    definition_validator("validationResult").validate({"issues": []})
    contract = _load(ROOT / "cpn-contract.schema.json")
    assert isinstance(contract, dict)
    definitions = contract["$defs"]
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
    assert {item.value for item in CpnIssueCode} == set(
        definitions["validationIssueCode"]["enum"]
    )
    assert {item.value for item in CpnErrorCode} == set(
        definitions["errorCode"]["enum"]
    )
    with pytest.raises(jsonschema.ValidationError):
        definition_validator("firingRequest").validate(
            {
                "transition_id": "t",
                "binding": {"transition_id": "t", "assignments": []},
                "output_token_ids": ["duplicate", "duplicate"],
            }
        )


def test_cpn_sv_p1_087_numeric_schema_matches_runtime_and_has_no_unsigned_kind() -> (
    None
):
    """SV-CPN-087: align tagged numeric schema with the runtime closed union.

    Requirement: schema INTEGER uses signed i64; REAL admits JSON integers and
    fractional numbers exactly when their runtime conversion is finite binary64;
    and no unsigned ContractValue kind exists. Integer inputs slightly above the
    largest finite binary64 value remain admissible when round-to-nearest,
    ties-to-even canonicalizes them to that finite value. Method: validate tagged
    boundary objects, construct runtime equivalents, and exercise strict JSON
    encoding for nonfinite values. Oracle: fixed enum inventory, signed-i64
    endpoints, the exact largest finite binary64 integer, the exact preserved
    integer-conversion boundary ``L = 2**1024 - 2**970 - 1``, and Python's
    independently specified binary64 conversion. Acceptance requires ordinary and
    rounding REAL cases, ``MAX_BINARY64 + 1``, and ``L`` to remain admitted while
    both signs of ``L + 1`` and ``10**400``, validator-supplied infinities, and
    runtime overflow/nonfinite values are rejected. Strict JSON has no NaN or
    Infinity values. The jsonschema library may admit an in-memory NaN
    because ordered bounds do not match it, so this test does not assert unsupported
    NaN validator behavior; strict encoding and runtime rejection own that boundary.
    This is interoperability software evidence, not numerical verification,
    scientific validation, or uncertainty quantification.
    """
    contract_id = (
        "https://github.com/eragasa/ksdft2effmass/"
        "specification/workflow-cpn/v1/cpn-contract.schema.json"
    )
    validator = jsonschema.Draft202012Validator(
        {"$ref": f"{contract_id}#/$defs/contractValue"}, registry=_registry()
    )
    minimum = -(2**63)
    maximum = 2**63 - 1
    for value in (minimum, 0, maximum):
        instance = {"kind": "integer", "value": value}
        validator.validate(instance)
        assert ContractValue(ContractValueKind.INTEGER, value).value == value
    for value in (minimum - 1, maximum + 1):
        with pytest.raises(jsonschema.ValidationError):
            validator.validate({"kind": "integer", "value": value})
        with pytest.raises(ValueError):
            ContractValue(ContractValueKind.INTEGER, value)
    for real_value in (0, 2**53 + 1, 1.5):
        validator.validate({"kind": "real", "value": real_value})
        runtime = ContractValue(ContractValueKind.REAL, real_value)
        assert type(runtime.value) is float
    assert ContractValue(ContractValueKind.REAL, 2**53 + 1).value == float(2**53)

    max_binary64_integer = (2**53 - 1) * 2**971
    max_binary64 = float.fromhex("0x1.fffffffffffffp+1023")
    last_finite_integer = 2**1024 - 2**970 - 1
    for preserved_integer in (max_binary64_integer + 1, last_finite_integer):
        validator.validate({"kind": "real", "value": preserved_integer})
        runtime = ContractValue(ContractValueKind.REAL, preserved_integer)
        assert runtime.value == max_binary64
        assert runtime.value != float("inf")

    for overflow_boundary in (last_finite_integer + 1, -(last_finite_integer + 1)):
        with pytest.raises(jsonschema.ValidationError):
            validator.validate({"kind": "real", "value": overflow_boundary})
        with pytest.raises(ValueError, match="overflows binary64"):
            ContractValue(ContractValueKind.REAL, overflow_boundary)

    for enormous_integer in (10**400, -(10**400)):
        with pytest.raises(jsonschema.ValidationError):
            validator.validate({"kind": "real", "value": enormous_integer})
        with pytest.raises(ValueError, match="overflows binary64"):
            ContractValue(ContractValueKind.REAL, enormous_integer)

    for infinity in (float("inf"), float("-inf")):
        with pytest.raises(jsonschema.ValidationError):
            validator.validate({"kind": "real", "value": infinity})
        with pytest.raises(ValueError, match="must be finite binary64"):
            ContractValue(ContractValueKind.REAL, infinity)

    for nonfinite in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError, match="Out of range float values"):
            json.dumps(
                {"kind": "real", "value": nonfinite},
                allow_nan=False,
            )
        with pytest.raises(ValueError, match="must be finite binary64"):
            ContractValue(ContractValueKind.REAL, nonfinite)

    with pytest.raises(jsonschema.ValidationError):
        validator.validate({"kind": "unsigned_integer", "value": maximum})
    assert "unsigned_integer" not in {kind.value for kind in ContractValueKind}


def test_cpn_sv_p1_088_control_schema_boundaries_match_runtime() -> None:
    """SV-CPN-088: align expression-visible token controls at both i64 bounds.

    Requirement: iteration and payload/schema controls admit zero through
    ``2**63 - 1`` and reject ``2**63`` in both public runtime construction and the
    version-1 JSON Schema. Method: build a complete synthetic payload token and its
    wire object for each boundary. Oracle: the approved nonnegative signed-i64
    interval, with no unsigned route. Acceptance requires identical classification
    and exact retained values. Failure exposes a cross-language contract split.
    Payload identities are synthetic and no persistence/scientific evidence follows.
    """
    contract_id = (
        "https://github.com/eragasa/ksdft2effmass/"
        "specification/workflow-cpn/v1/cpn-contract.schema.json"
    )
    validator = jsonschema.Draft202012Validator(
        {"$ref": f"{contract_id}#/$defs/token"}, registry=_registry()
    )

    def runtime_token(value: int) -> CpnToken:
        """Construct one complete synthetic token with both controls equal."""
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

    def wire_token(value: int) -> dict[str, object]:
        """Return the exact wire counterpart of ``runtime_token``."""
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

    maximum = 2**63 - 1
    for value in (0, maximum):
        validator.validate(wire_token(value))
        token = runtime_token(value)
        assert token.iteration_index == value
        assert token.payload_schema_version == value
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(wire_token(maximum + 1))
    with pytest.raises(ValueError):
        runtime_token(maximum + 1)
