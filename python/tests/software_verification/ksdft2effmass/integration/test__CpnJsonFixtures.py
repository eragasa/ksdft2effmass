"""Artifact-owned interoperability verification for declared CPN JSON fixtures.

Evidence class: software verification. The tests use synthetic contract artifacts and
independent language/runtime or static-structure oracles. Passing is not numerical
verification, scientific validation, uncertainty quantification, engine execution,
persistence, or Rust conformance evidence.
Fixture values are synthetic workflow-routing examples, not scientific data.
"""

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
    """Load strict JSON and reject nonstandard nonfinite numeric constants."""

    def reject_constant(value: str) -> object:
        """Reject JSON constants excluded by the language-neutral contract."""
        raise ValueError(f"nonstandard JSON constant: {value}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def _validate(schema_name: str, fixture: Path) -> None:
    """Validate one fixture against one local schema entry point."""
    schema = json.loads((ROOT / schema_name).read_text())
    jsonschema.Draft202012Validator(schema, registry=REGISTRY).validate(
        _strict_load(fixture)
    )


def test_cpn_sv_p1_029_all_valid_fixtures_are_schema_conformant() -> None:
    """SV-CPN-029: schema conformance of all declared valid fixtures.

    Requirement
    -----------
    The version-1 P1 contract requires schema conformance of all declared valid
    fixtures.

    Method
    ------
    Validate the five files under ``valid/`` through their net, marking, or firing
    schema entry points.

    Independent oracle
    ------------------
    The versioned valid-fixture inventory explicitly declares which narrow schema
    owns each instance.

    Acceptance criterion
    --------------------
    Every fixture validates without network resolution or exception.

    Failure interpretation
    ----------------------
    A failure means fixture/schema drift in a declared valid contract example.

    Limitations
    -----------
    Schema success alone does not execute graph relations or scientific behavior.
    """
    mapping = {
        "minimal-net.json": "cpn-net.schema.json",
        "multiset-marking.json": "cpn-marking.schema.json",
        "synchronized-firing.json": "cpn-firing.schema.json",
        "retry-recovery-iteration.json": "cpn-marking.schema.json",
        "scoped-outcomes.json": "cpn-marking.schema.json",
    }
    for fixture_name, schema_name in mapping.items():
        _validate(schema_name, ROOT / "valid" / fixture_name)


def test_cpn_sv_p1_030_structural_invalid_fixtures_are_rejected() -> None:
    """SV-CPN-030: structural rejection of invalid fixtures.

    Requirement
    -----------
    The version-1 P1 contract requires structural rejection of invalid fixtures.

    Method
    ------
    Validate four structurally invalid fixtures and strictly parse the nonfinite
    ``NaN`` fixture.

    Independent oracle
    ------------------
    Draft 2020-12 rules and RFC-compatible JSON parsing independently reject invalid
    terminality, Boolean-as-integer, lambda shape, unsupported version, and NaN.

    Acceptance criterion
    --------------------
    Each schema case raises ``ValidationError`` and strict parsing raises
    ``ValueError`` only for the designated NaN file.

    Failure interpretation
    ----------------------
    Acceptance would broaden the fixed wire shape unexpectedly.

    Limitations
    -----------
    Relational invalidity requiring another object is covered by SV-CPN-031.
    """
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
    """Construct one routing token from a language-neutral fixture object."""
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
    """Construct a complete marking from a language-neutral fixture object."""
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
    """Construct the closed guard shapes used by relational net fixtures."""
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
    """Construct the bounded no-arc net shapes used by relational fixtures."""
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
    """Build the minimal valid net needed to evaluate an existing-ID collision."""

    def literal(
        kind: ContractValueKind,
        value: None | bool | int | float | str | tuple[str, ...],
    ) -> ValueExpression:
        """Construct one explicitly tagged literal output expression."""
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


def test_cpn_sv_p1_031_relational_invalid_fixtures_reach_public_oracles() -> None:
    """SV-CPN-031: public ActionObject rejection of relational fixtures.

    Requirement
    -----------
    The version-1 P1 contract requires public ActionObject rejection of relational
    fixtures.

    Method
    ------
    Parse schema-valid relational fixtures into public objects and invoke
    ``CpnDefinitionValidator``, ``CpnMarkingValidator``, or ``TransitionFirer``.

    Independent oracle
    ------------------
    The fixture README fixes expected codes for unknown color, unbound variable,
    duplicate token, wrong place set, and existing output ID.

    Acceptance criterion
    --------------------
    Each public owner emits its exact ``CpnIssueCode`` or ``OUTPUT_ID_COLLISION``
    error code.

    Failure interpretation
    ----------------------
    Failure means a fixture's claimed relational oracle is not executable.

    Limitations
    -----------
    The local test parser is not a production serializer or persistence layer.
    """
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
