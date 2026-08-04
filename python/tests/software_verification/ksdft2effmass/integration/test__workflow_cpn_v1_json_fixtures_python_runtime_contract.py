"""Evidence class and represented meaning
--------------------------------------
Software verification of the version-1 CPN JSON fixture family <-> Python runtime
contract, using synthetic routing representations rather than scientific data.

Owned contract, oracle, and scope
---------------------------------
The version-1 CPN JSON fixture family <-> Python runtime contract is the primary
artifact owner. Declared fixture classifications, version-1 schemas, and public Python
error/result surfaces are the exact oracles.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the exercised fixture/schema/runtime contract; failure may
indicate fixture, schema, parser, runtime, or evidence drift. Numerical verification,
scientific validation, uncertainty quantification, physical correctness, persistence,
and cross-language conformance are excluded."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import jsonschema  # type: ignore[import-untyped]
import pytest
from referencing import Registry, Resource

from ksdft2effmass.workflows.cpn import (
    ArcDefinition,
    ArcDirection,
    ColorDefinition,
    ContractValue,
    ContractValueKind,
    CpnDefinitionValidator,
    CpnErrorCode,
    CpnFiringError,
    CpnIssueCode,
    CpnMarking,
    CpnMarkingValidator,
    CpnNetDefinition,
    CpnToken,
    FiringRequest,
    GuardExpression,
    GuardOperator,
    OutputInscription,
    PlaceDefinition,
    PlaceMarking,
    TokenBinding,
    TokenField,
    TokenFieldAssignment,
    TokenTemplate,
    TransitionBinding,
    TransitionDefinition,
    TransitionFirer,
    ValueExpression,
    ValueExpressionKind,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
ROOT = REPO_ROOT / "specification" / "workflow-cpn" / "v1"
CONTRACT = json.loads((ROOT / "cpn-contract.schema.json").read_text())
REGISTRY = Registry().with_resource(CONTRACT["$id"], Resource.from_contents(CONTRACT))
pytestmark = pytest.mark.software_verification


def _strict_load(path: Path) -> object:
    """Evidence ID
    Supports exactly SV-CPN-029, SV-CPN-030, and SV-CPN-031; owns no independent
    Evidence ID.

    Requirement
    Load fixture JSON while rejecting nonstandard nonfinite constants.

    Method
    Read repository text and decode with a controlled ``parse_constant`` callback.

    Oracle
    Standard JSON excludes NaN and infinities; the supplied fixture path fixes the
    input.

    Acceptance
    Return decoded data or raise ``ValueError`` for a nonstandard constant.

    Interpretation
    This helper supports the named fixture evidence and owns no separate pass claim.

    Limitations
    It is not a production serializer and does not validate fixture semantics."""

    def reject_constant(value: str) -> object:
        """Evidence ID
        Supports exactly SV-CPN-030; owns no independent Evidence ID.

        Requirement
        Translate any decoder-supplied nonstandard JSON constant into deterministic
        rejection.

        Method
        Raise ``ValueError`` containing the supplied constant text.

        Oracle
        Strict JSON language rules exclude every such callback value.

        Acceptance
        Always raise ``ValueError``.

        Interpretation
        This nested helper supports SV-CPN-030 and owns no separate pass claim.

        Limitations
        The controlled decoder callback is not itself validated."""
        raise ValueError(f"nonstandard JSON constant: {value}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def _validate(schema_name: str, fixture: Path) -> None:
    """Evidence ID
    Supports exactly SV-CPN-029, SV-CPN-030, and SV-CPN-031; owns no independent
    Evidence ID.

    Requirement
    Validate one fixture through one named local version-1 schema entry point.

    Method
    Load schema and fixture locally, then invoke Draft 2020-12 validation with the fixed
    registry.

    Oracle
    The caller-supplied schema/fixture pairing and local registry define the check.

    Acceptance
    Complete without exception for conforming data or propagate exact validation/load
    failure.

    Interpretation
    This helper supports the named fixture evidence and owns no separate pass claim.

    Limitations
    It does not independently classify fixtures or test network behavior."""
    schema = json.loads((ROOT / schema_name).read_text())
    jsonschema.Draft202012Validator(schema, registry=REGISTRY).validate(
        _strict_load(fixture)
    )


def test_artifact__valid_json_fixtures__conform_to_declared_schemas() -> None:
    """Evidence ID
    SV-CPN-029

    Requirement
    Every declared valid version-1 fixture conforms to its declared narrow schema entry
    point.

    Method
    Validate the five explicit valid fixture filenames using the local schema mapping
    and strict loader; no warnings or network access are expected.

    Oracle
    The versioned fixture inventory and its explicit schema mapping provide the accepted
    classifications.

    Acceptance
    Every mapped fixture validates without exception.

    Interpretation
    Pass supports declared fixture/schema agreement; failure may indicate fixture,
    mapping, schema, registry, parser, or library drift.

    Limitations
    Schema success does not execute relational behavior. Scientific validation, UQ,
    physical correctness, and cross-language conformance are excluded."""
    mapping = {
        "minimal-net.json": "cpn-net.schema.json",
        "multiset-marking.json": "cpn-marking.schema.json",
        "synchronized-firing.json": "cpn-firing.schema.json",
        "retry-recovery-iteration.json": "cpn-marking.schema.json",
        "scoped-outcomes.json": "cpn-marking.schema.json",
    }
    for fixture_name, schema_name in mapping.items():
        _validate(schema_name, ROOT / "valid" / fixture_name)


def test_artifact__structural_invalid_json_fixtures__are_rejected() -> None:
    """Evidence ID
    SV-CPN-030

    Requirement
    Declared structurally invalid version-1 fixtures are rejected by schema validation
    or strict JSON parsing.

    Method
    Validate four explicit invalid fixtures and strictly parse the designated nonfinite
    fixture; no warnings are expected.

    Oracle
    Draft 2020-12 constraints and standard strict JSON exclusion of NaN independently
    define rejection for the declared cases.

    Acceptance
    Each schema case raises ``ValidationError`` and only the designated NaN parse case
    raises ``ValueError``.

    Interpretation
    Pass supports structural-invalid classifications; failure may indicate fixture,
    schema, parser, library, or evidence drift.

    Limitations
    Relational invalidity belongs to SV-CPN-031. Exhaustive invalid inputs, scientific
    validation, UQ, and cross-language conformance are excluded."""
    cases = {
        "invalid-outcome-terminality.json": "cpn-marking.schema.json",
        "boolean-as-integer.json": "cpn-marking.schema.json",
        "lambda-like-expression.json": "cpn-contract.schema.json",
        "unsupported-version.json": "cpn-net.schema.json",
    }
    for fixture_name, schema_name in cases.items():
        try:
            _validate(schema_name, ROOT / "invalid" / fixture_name)
        except jsonschema.ValidationError:
            continue
        raise AssertionError(f"{fixture_name} unexpectedly passed schema validation")
    try:
        _strict_load(ROOT / "invalid" / "nonfinite-real.json")
    except ValueError:
        pass
    else:
        raise AssertionError("nonfinite-real.json unexpectedly parsed as strict JSON")


def _token(data: dict[str, Any]) -> CpnToken:
    """Evidence ID
    Supports exactly SV-CPN-031; owns no independent Evidence ID.

    Requirement
    Construct one public routing token from the bounded relational fixture shape.

    Method
    Require no outcome and map every fixture field to the public constructor.

    Oracle
    The version-1 token wire/runtime field correspondence fixes the mapping.

    Acceptance
    Return the matching ``CpnToken`` or raise for unsupported/out-of-contract input.

    Interpretation
    This helper supports SV-CPN-031 and owns no separate pass claim.

    Limitations
    It is a local test parser, not a production serializer; outcomes are excluded."""
    outcome_data = data["outcome"]
    if outcome_data is not None:
        raise ValueError("relational marking fixtures do not use outcomes")
    return CpnToken(
        token_id=data["token_id"],
        color_id=data["color_id"],
        workflow_id=data["workflow_id"],
        run_id=data["run_id"],
        parent_run_id=data["parent_run_id"],
        attempt_id=data["attempt_id"],
        retry_parent_attempt_id=data["retry_parent_attempt_id"],
        iteration_index=data["iteration_index"],
        payload_type_id=data["payload_type_id"],
        payload_id=data["payload_id"],
        payload_schema_version=data["payload_schema_version"],
        provenance_ids=tuple(data["provenance_ids"]),
        parent_token_ids=tuple(data["parent_token_ids"]),
        correlation_id=data["correlation_id"],
        authorization_id=data["authorization_id"],
    )


def _marking(data: dict[str, Any]) -> CpnMarking:
    """Evidence ID
    Supports exactly SV-CPN-031; owns no independent Evidence ID.

    Requirement
    Construct one complete public marking from the bounded fixture shape.

    Method
    Map places and tokens in fixture order through public constructors.

    Oracle
    The version-1 marking wire/runtime field correspondence fixes the mapping.

    Acceptance
    Return the matching ``CpnMarking``.

    Interpretation
    This helper supports SV-CPN-031 and owns no separate pass claim.

    Limitations
    It is a local test parser and assumes list-shaped places."""
    places = data["places"]
    assert isinstance(places, list)
    return CpnMarking(
        data["schema_version"],
        data["model_id"],
        data["revision"],
        tuple(
            PlaceMarking(
                place["place_id"],
                tuple(_token(token) for token in place["tokens"]),
            )
            for place in places
        ),
    )


def _guard(data: dict[str, Any]) -> GuardExpression:
    """Evidence ID
    Supports exactly SV-CPN-031; owns no independent Evidence ID.

    Requirement
    Construct only the closed guard shapes used by relational net fixtures.

    Method
    Map TRUE directly or map one token-field/literal comparison through public enums and
    objects.

    Oracle
    The bounded relational fixture grammar fixes the supported branches.

    Acceptance
    Return the corresponding ``GuardExpression``.

    Interpretation
    This helper supports SV-CPN-031 and owns no separate pass claim.

    Limitations
    Other valid guard/expression shapes are intentionally excluded."""
    operator = GuardOperator(data["operator"])
    if operator is GuardOperator.TRUE:
        return GuardExpression(operator)
    left_data = data["left"]
    right_data = data["right"]
    assert isinstance(left_data, dict) and isinstance(right_data, dict)
    left = ValueExpression(
        ValueExpressionKind.TOKEN_FIELD,
        variable=left_data["variable"],
        field=TokenField(left_data["field"]),
    )
    literal_data = right_data["literal"]
    assert isinstance(literal_data, dict)
    right = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(
            ContractValueKind(literal_data["kind"]), literal_data["value"]
        ),
    )
    return GuardExpression(operator, left=left, right=right)


def _net(data: dict[str, Any]) -> CpnNetDefinition:
    """Evidence ID
    Supports exactly SV-CPN-031; owns no independent Evidence ID.

    Requirement
    Construct the bounded no-arc public net shapes used by relational fixtures.

    Method
    Map colors, places, transitions, guards, and initial marking through public
    constructors.

    Oracle
    The bounded fixture wire/runtime correspondence fixes the mapping.

    Acceptance
    Return the corresponding ``CpnNetDefinition`` with an empty arc tuple.

    Interpretation
    This helper supports SV-CPN-031 and owns no separate pass claim.

    Limitations
    It is not a general parser and excludes arc-bearing nets."""
    colors = data["colors"]
    places = data["places"]
    transitions = data["transitions"]
    assert isinstance(colors, list)
    assert isinstance(places, list)
    assert isinstance(transitions, list)
    initial = data["initial_marking"]
    assert isinstance(initial, dict)
    return CpnNetDefinition(
        data["schema_version"],
        data["model_id"],
        tuple(
            ColorDefinition(
                color["color_id"],
                color["description"],
                tuple(color["allowed_payload_type_ids"]),
            )
            for color in colors
        ),
        tuple(
            PlaceDefinition(
                place["place_id"],
                place["description"],
                tuple(place["allowed_color_ids"]),
            )
            for place in places
        ),
        tuple(
            TransitionDefinition(
                transition["transition_id"],
                transition["description"],
                _guard(transition["guard"]),
            )
            for transition in transitions
        ),
        (),
        _marking(initial),
    )


def _collision_net() -> CpnNetDefinition:
    """Evidence ID
    Supports exactly SV-CPN-031; owns no independent Evidence ID.

    Requirement
    Build the minimal valid public net required to exercise an existing-output-ID
    collision.

    Method
    Compose fixed synthetic public objects and a token loaded from the declared valid
    marking fixture.

    Oracle
    The public firing preconditions and fixture token fix the controlled setup.

    Acceptance
    Return a valid net whose initial marking already owns the tested output ID.

    Interpretation
    This helper supports SV-CPN-031 and owns no separate pass claim.

    Limitations
    The setup is synthetic and validates neither general firing correctness nor
    scientific behavior."""

    def literal(
        kind: ContractValueKind,
        value: None | bool | int | float | str | tuple[str, ...],
    ) -> ValueExpression:
        """Evidence ID
        Supports exactly SV-CPN-031; owns no independent Evidence ID.

        Requirement
        Construct one explicitly tagged literal expression used by the controlled
        collision net.

        Method
        Wrap the supplied accepted kind/value in public ``ContractValue`` and
        ``ValueExpression`` objects.

        Oracle
        The fixed collision-net assignment list supplies each expected kind/value pair.

        Acceptance
        Return the tagged literal or propagate public-constructor rejection.

        Interpretation
        This nested helper supports SV-CPN-031 and owns no separate pass claim.

        Limitations
        It does not independently validate literal semantics or general expression
        evaluation."""
        return ValueExpression(
            ValueExpressionKind.LITERAL,
            literal=ContractValue(kind, value),
        )

    assignments = (
        TokenFieldAssignment(
            TokenField.WORKFLOW_ID,
            literal(ContractValueKind.STRING, "workflow-1"),
        ),
        TokenFieldAssignment(
            TokenField.RUN_ID, literal(ContractValueKind.STRING, "run-1")
        ),
        TokenFieldAssignment(
            TokenField.ATTEMPT_ID, literal(ContractValueKind.STRING, "attempt-1")
        ),
        TokenFieldAssignment(
            TokenField.ITERATION_INDEX, literal(ContractValueKind.INTEGER, 0)
        ),
        TokenFieldAssignment(
            TokenField.PROVENANCE_IDS,
            literal(ContractValueKind.STRING_SEQUENCE, ("provenance-1",)),
        ),
        TokenFieldAssignment(
            TokenField.PARENT_TOKEN_IDS,
            literal(ContractValueKind.STRING_SEQUENCE, ()),
        ),
    )
    token_data = _strict_load(ROOT / "valid" / "multiset-marking.json")
    assert isinstance(token_data, dict)
    token = _marking(token_data).places[0].tokens[0]
    marking = CpnMarking(1, "minimal-model", 0, (PlaceMarking("ready", (token,)),))
    return CpnNetDefinition(
        1,
        "minimal-model",
        (ColorDefinition("control", "control", ()),),
        (PlaceDefinition("ready", "ready", ("control",)),),
        (TransitionDefinition("t", "produce", GuardExpression(GuardOperator.TRUE)),),
        (
            ArcDefinition(
                "output",
                "ready",
                "t",
                ArcDirection.OUTPUT,
                output_inscription=OutputInscription(
                    (TokenTemplate("control", assignments),)
                ),
            ),
        ),
        marking,
    )


def test_artifact__relational_invalid_json_fixtures__reach_public_runtime_oracles() -> (
    None
):
    """Evidence ID
    SV-CPN-031

    Requirement
    Schema-valid relational-invalid fixtures reach public Python owners and produce
    their declared issue/error codes.

    Method
    Validate and parse explicit fixtures, construct public CPN objects, then execute
    public definition/marking validators or firer; no warnings are expected.

    Oracle
    The fixture contract fixes the exact ``CpnIssueCode`` and ``OUTPUT_ID_COLLISION``
    outcomes independently of the exercised ActionObjects.

    Acceptance
    Each fixture is schema-valid and each public owner emits the exact asserted issue or
    error code.

    Interpretation
    Pass supports fixture/runtime relational agreement; failure may indicate fixture
    parser, schema, runtime owner, oracle, or evidence drift.

    Limitations
    The local parser is not a production serializer or persistence layer. Scientific
    validation, UQ, and cross-language conformance are excluded."""
    cases = {
        "unknown-color.json": "cpn-net.schema.json",
        "duplicate-token-id.json": "cpn-marking.schema.json",
        "wrong-place-set.json": "cpn-marking.schema.json",
        "unbound-guard-variable.json": "cpn-net.schema.json",
        "output-id-collision.json": "cpn-firing.schema.json",
    }
    for fixture_name, schema_name in cases.items():
        _validate(schema_name, ROOT / "invalid" / fixture_name)

    unknown_data = _strict_load(ROOT / "invalid" / "unknown-color.json")
    unbound_data = _strict_load(ROOT / "invalid" / "unbound-guard-variable.json")
    minimal_data = _strict_load(ROOT / "valid" / "minimal-net.json")
    duplicate_data = _strict_load(ROOT / "invalid" / "duplicate-token-id.json")
    wrong_places_data = _strict_load(ROOT / "invalid" / "wrong-place-set.json")
    assert all(
        isinstance(item, dict)
        for item in (
            unknown_data,
            unbound_data,
            minimal_data,
            duplicate_data,
            wrong_places_data,
        )
    )
    unknown_result = CpnDefinitionValidator().execute(
        _net(cast("dict[str, Any]", unknown_data))
    )
    assert CpnIssueCode.UNKNOWN_COLOR in {issue.code for issue in unknown_result.issues}
    unbound_result = CpnDefinitionValidator().execute(
        _net(cast("dict[str, Any]", unbound_data))
    )
    assert CpnIssueCode.UNBOUND_VARIABLE in {
        issue.code for issue in unbound_result.issues
    }
    minimal_net = _net(cast("dict[str, Any]", minimal_data))
    duplicate_result = CpnMarkingValidator().execute(
        minimal_net,
        _marking(cast("dict[str, Any]", duplicate_data)),
    )
    assert CpnIssueCode.DUPLICATE_TOKEN_ID in {
        issue.code for issue in duplicate_result.issues
    }
    place_result = CpnMarkingValidator().execute(
        minimal_net,
        _marking(cast("dict[str, Any]", wrong_places_data)),
    )
    assert CpnIssueCode.PLACE_SET_MISMATCH in {
        issue.code for issue in place_result.issues
    }

    request_data = _strict_load(ROOT / "invalid" / "output-id-collision.json")
    assert isinstance(request_data, dict)
    binding_data = request_data["binding"]
    assert isinstance(binding_data, dict)
    binding = TransitionBinding(
        binding_data["transition_id"],
        tuple(
            TokenBinding(item["variable"], item["token_id"])
            for item in binding_data["assignments"]
        ),
    )
    request = FiringRequest(
        request_data["transition_id"],
        binding,
        tuple(request_data["output_token_ids"]),
    )
    collision_net = _collision_net()
    with pytest.raises(CpnFiringError) as collision:
        TransitionFirer().execute(collision_net, collision_net.initial_marking, request)
    assert collision.value.detail.code is CpnErrorCode.OUTPUT_ID_COLLISION
