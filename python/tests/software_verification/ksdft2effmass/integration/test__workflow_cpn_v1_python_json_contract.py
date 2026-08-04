"""Evidence class and represented meaning
--------------------------------------
Software verification of the version-1 CPN Python runtime <-> version-1 CPN JSON
Schema and wire contract, a represented software boundary rather than a physical or
numerical model.

Owned contract, oracle, and scope
---------------------------------
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
    """Evidence ID
    Supports exactly SV-CPN-027, SV-CPN-028, SV-CPN-087, and SV-CPN-088; owns no
    independent Evidence ID.

    Requirement
    Load a repository JSON artifact without transforming its represented values.

    Method
    Read UTF-8 text and apply the standard JSON decoder.

    Oracle
    Standard JSON decoding and the supplied repository path define the expected
    operation.

    Acceptance
    Return the decoded object or propagate the decoder/read failure.

    Interpretation
    This helper supports the named evidence and owns no separate pass claim.

    Limitations
    It does not validate schema meaning, file inventory, or scientific content."""
    return json.loads(path.read_text(encoding="utf-8"))


def _registry() -> Registry:
    """Evidence ID
    Supports exactly SV-CPN-028, SV-CPN-087, and SV-CPN-088; owns no independent
    Evidence ID.

    Requirement
    Provide a local-only registry containing every discovered version-1 schema under its
    public ``$id``.

    Method
    Load discovered schemas and register each resource by its declared identifier.

    Oracle
    The discovered schema documents and referencing registry contract define the
    mapping.

    Acceptance
    Return a registry containing each loaded ``$id`` without network resolution.

    Interpretation
    This helper supports the named evidence and owns no separate pass claim.

    Limitations
    It does not assert the exact schema inventory or validate schema semantics."""
    registry = Registry()
    for path in SCHEMAS:
        contents = _load(path)
        assert isinstance(contents, dict)
        registry = registry.with_resource(
            contents["$id"], Resource.from_contents(contents)
        )
    return registry


def test_artifact__json_schemas__satisfy_draft_2020_12_metaschema() -> None:
    """Evidence ID
    SV-CPN-027

    Requirement
    Every discovered version-1 CPN schema satisfies JSON Schema Draft 2020-12.

    Method
    Load each ``*.schema.json`` file and apply its selected validator class
    ``check_schema``; no warnings are expected.

    Oracle
    The official Draft 2020-12 metaschema implemented by ``jsonschema`` is external to
    the project schemas.

    Acceptance
    Every discovered schema completes metaschema checking without exception.

    Interpretation
    Pass supports syntax/keyword validity; failure may indicate malformed schemas,
    unsupported keywords, discovery drift, or library behavior.

    Limitations
    The exact seven-file inventory is not asserted. Runtime agreement, numerical
    verification, scientific validation, UQ, and cross-language conformance are
    excluded."""
    for path in SCHEMAS:
        schema = _load(path)
        validator = jsonschema.validators.validator_for(schema)
        validator.check_schema(schema)


def test_artifact__schema_entry_points__resolve_locally_and_match_public_enums() -> (
    None
):
    """Evidence ID
    SV-CPN-028

    Requirement
    As one accepted conjunctive nonnumeric boundary requirement, version-1 entry points
    resolve locally, required public definitions exist, closed schema enums equal Python
    enums, representative valid wire values pass, and prohibited empty/duplicate values
    fail.

    Method
    Build a local registry; validate representative net, marking, firing,
    contract-value, result, validation, and firing-request instances; compare public
    enum value sets. No warnings or network resolution are expected.

    Oracle
    Version-1 schemas and fixture classifications fix wire structure; the public
    ``CpnIssueCode`` and ``CpnErrorCode`` enums fix the Python closed sets.

    Acceptance
    All local references resolve; representative valid values pass; required definitions
    are present; enum sets are exactly equal; empty string sequences and duplicate
    output IDs raise ``ValidationError``.

    Interpretation
    Pass supports all conjunctive nonnumeric facets of the accepted Python/JSON
    boundary; failure may indicate schema, fixture, runtime-enum, registry, library, or
    evidence drift.

    Limitations
    SV-CPN-028 remains one broad requirement and is not split. Numeric bounds are owned
    by SV-CPN-087/088. Exhaustive wire behavior, scientific validation, UQ, and Rust
    conformance are excluded."""
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
        """Evidence ID
        Supports exactly SV-CPN-028; owns no independent Evidence ID.

        Requirement
        Resolve one named contract definition through the already controlled local
        registry.

        Method
        Construct a Draft 2020-12 validator whose sole reference targets the supplied
        definition name.

        Oracle
        The fixed contract ``$id`` and supplied definition name define the expected
        local reference.

        Acceptance
        Return the validator; resolution/validation outcomes remain owned by SV-CPN-028.

        Interpretation
        This nested helper supports SV-CPN-028 and owns no separate pass claim.

        Limitations
        It does not independently validate the registry, definition, or library."""
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


def test_artifact__numeric_wire_contract__matches_python_runtime() -> None:
    """Evidence ID
    SV-CPN-087

    Requirement
    Tagged INTEGER and REAL wire values match Python runtime domains, strict JSON
    excludes nonfinite values, and no unsigned ``ContractValue`` kind exists.

    Method
    Validate/construct signed-i64 endpoints, binary64 rounding and overflow boundaries,
    huge integers, infinities, NaN strict encoding, and an unsupported unsigned tag; no
    warnings are expected.

    Oracle
    Accepted signed-i64 endpoints, exact binary64 boundary integers, Python binary64
    conversion semantics, strict JSON semantics, and the fixed enum inventory are
    independent constants/rules.

    Acceptance
    Schema and runtime classifications match for every body case; retained values are
    exact; specified invalid cases raise the asserted exceptions; unsigned kind is
    absent.

    Interpretation
    Pass supports the exercised numeric wire/runtime agreement; failure may indicate
    schema, runtime, JSON library, validator, platform, or evidence drift.

    Limitations
    This is interoperability software evidence, not numerical verification. In-memory
    validator NaN behavior is intentionally excluded, as are scientific validation, UQ,
    and Rust conformance."""
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


def test_artifact__control_field_bounds__match_python_runtime() -> None:
    """Evidence ID
    SV-CPN-088

    Requirement
    Expression-visible token controls admit exactly the exercised nonnegative signed-i64
    boundary in version-1 schema and Python construction.

    Method
    Construct complete synthetic wire/runtime tokens at zero, ``2**63 - 1``, and
    ``2**63``; no warnings are expected.

    Oracle
    The approved inclusive interval ``[0, 2**63 - 1]`` and complete token shape are
    fixed contract inputs independent of production validation.

    Acceptance
    Both valid endpoints are accepted and retained exactly; ``2**63`` raises schema
    ``ValidationError`` and runtime ``ValueError``.

    Interpretation
    Pass supports exercised control-field agreement; failure may indicate schema,
    runtime, fixture-shape, library, or evidence drift.

    Limitations
    Only the selected boundary values and two controls are exercised. Scientific
    validation, UQ, persistence, and cross-language conformance are excluded."""
    contract_id = (
        "https://github.com/eragasa/ksdft2effmass/"
        "specification/workflow-cpn/v1/cpn-contract.schema.json"
    )
    validator = jsonschema.Draft202012Validator(
        {"$ref": f"{contract_id}#/$defs/token"}, registry=_registry()
    )

    def runtime_token(value: int) -> CpnToken:
        """Evidence ID
        Supports exactly SV-CPN-088; owns no independent Evidence ID.

        Requirement
        Construct the complete synthetic Python token counterpart for one control value.

        Method
        Pass fixed synthetic identities and the supplied integer to both
        expression-visible controls.

        Oracle
        The accepted complete token field mapping fixes the counterpart.

        Acceptance
        Return a public ``CpnToken`` or propagate its contract error.

        Interpretation
        This nested helper supports SV-CPN-088 and owns no separate pass claim.

        Limitations
        Synthetic identities have no scientific meaning; the constructor itself is not
        independently validated here."""
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
        """Evidence ID
        Supports exactly SV-CPN-088; owns no independent Evidence ID.

        Requirement
        Construct the exact version-1 wire counterpart of ``runtime_token`` for one
        control value.

        Method
        Return the fixed JSON object with the supplied integer in both control fields.

        Oracle
        The accepted token wire field mapping fixes every key and value.

        Acceptance
        Return the exact mapping used by SV-CPN-088.

        Interpretation
        This nested helper supports SV-CPN-088 and owns no separate pass claim.

        Limitations
        It is test construction, not a production serializer or cross-language proof."""
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
