r"""Software verification of workflow cpn v1 json fixtures python runtime contract.

Facet and represented meaning
--------------------------------------
Software verification of the version-1 CPN JSON fixture family <-> Python runtime
contract, using synthetic routing representations rather than scientific data.

Intrinsic and cross-object scope
--------------------------------
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


def strict_load_json(path: Path) -> object:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-029, SV-CPN-030, SV-CPN-031, SV-CPN-170,
    SV-CPN-171, SV-CPN-172, SV-CPN-173.
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
        -----------
        Owns no identifier; supports SV-CPN-029, SV-CPN-030, SV-CPN-031, SV-CPN-170,
        SV-CPN-171, SV-CPN-172, and SV-CPN-173.

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


def validate_fixture_document(schema_name: str, fixture: Path) -> None:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-029, SV-CPN-030, SV-CPN-031, SV-CPN-171,
    SV-CPN-172, SV-CPN-173.
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
        strict_load_json(fixture)
    )


VALID_FIXTURE_CASES = (
    pytest.param("minimal-net.json", "cpn-net.schema.json", id="minimal_net"),
    pytest.param(
        "multiset-marking.json", "cpn-marking.schema.json", id="multiset_marking"
    ),
    pytest.param(
        "synchronized-firing.json", "cpn-firing.schema.json", id="synchronized_firing"
    ),
    pytest.param(
        "retry-recovery-iteration.json",
        "cpn-marking.schema.json",
        id="retry_recovery_iteration",
    ),
    pytest.param(
        "scoped-outcomes.json", "cpn-marking.schema.json", id="scoped_outcomes"
    ),
)


@pytest.mark.parametrize(("fixture_name", "schema_name"), VALID_FIXTURE_CASES)
def test_artifact__valid_json_fixtures__conform_to_declared_schemas(
    fixture_name: str, schema_name: str
) -> None:
    """Evidence ID
    -----------
    SV-CPN-029

    Requirement
    -----------
    Each declared valid fixture conforms to its declared narrow schema entry point.

    Method
    ------
    Validate one explicit fixture/schema pair through the local registry and strict
    loader.

    Oracle
    ------
    The versioned fixture inventory explicitly fixes the accepted schema classification.

    Acceptance
    ----------
    Validation completes without exception, warning, or network resolution.

    Interpretation
    --------------
    Failure may identify fixture, mapping, schema, registry, parser, or library drift.

    Limitations
    -----------
    Schema success does not establish runtime semantics, science, UQ, or Rust agreement.
    """
    validate_fixture_document(schema_name, ROOT / "valid" / fixture_name)


def fixture_validation_succeeds(schema_name: str, path: Path) -> bool:
    """Evidence ID
    -----------
    Owns no identifier; supports no collected evidence owner.
    Requirement
    -----------
    Expose repeated fixture-validation mechanics without an independent claim.

    Method
    ------
    Validate one named repository fixture against its supplied public schema.

    Oracle
    ------
    The supported artifact tests own fixture classification; this helper owns none.

    Acceptance
    ----------
    Return ``True`` after validation and propagate every validation failure.

    Interpretation
    --------------
    Helper failure invalidates the supported artifact evidence execution.

    Limitations
    -----------
    This does not establish runtime semantics, scientific validation, or UQ.
    """
    validate_fixture_document(schema_name, path)
    return True


def fixture_is_rejected(schema_name: str, path: Path) -> bool:
    """Evidence ID
    -----------
    Owns no identifier; supports no collected evidence owner.
    Requirement
    -----------
    Expose deterministic structural-rejection mechanics without an independent claim.

    Method
    ------
    Validate one supplied fixture and translate only JSON-Schema rejection to ``True``.

    Oracle
    ------
    The supported artifact test owns the schema oracle; this helper owns none.

    Acceptance
    ----------
    Return ``True`` exactly when ``jsonschema.ValidationError`` is raised.

    Interpretation
    --------------
    Helper failure invalidates the supported artifact evidence setup.

    Limitations
    -----------
    This does not validate schema meaning, runtime semantics, science, or UQ.
    """
    try:
        validate_fixture_document(schema_name, path)
    except jsonschema.ValidationError:
        return True
    return False


STRUCTURAL_INVALID_CASES = (
    pytest.param(
        "invalid-outcome-terminality.json",
        "cpn-marking.schema.json",
        id="invalid_outcome_terminality",
    ),
    pytest.param(
        "lambda-like-expression.json",
        "cpn-contract.schema.json",
        id="lambda_like_expression",
    ),
    pytest.param(
        "unsupported-version.json", "cpn-net.schema.json", id="unsupported_version"
    ),
)


@pytest.mark.parametrize(("fixture_name", "schema_name"), STRUCTURAL_INVALID_CASES)
def test_artifact__structural_invalid_json_fixtures__are_rejected(
    fixture_name: str, schema_name: str
) -> None:
    """Evidence ID
    -----------
    SV-CPN-030

    Requirement
    -----------
    Each declared structurally invalid fixture is rejected by its public schema layer.

    Method
    ------
    Validate one explicit invalid fixture/schema pair through the local registry.

    Oracle
    ------
    The versioned invalid-fixture classification fixes schema rejection.

    Acceptance
    ----------
    Validation raises exactly ``jsonschema.ValidationError``.

    Interpretation
    --------------
    Failure may identify fixture, schema, registry, parser, library, or evidence drift.

    Limitations
    -----------
    Relational invalidity, runtime semantics, science, UQ, and Rust are excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        validate_fixture_document(schema_name, ROOT / "invalid" / fixture_name)


def test_artifact__boolean_integer_fixture__rejects_wrong_semantic_type() -> None:
    """Evidence ID
    -----------
    SV-CPN-173

    Requirement
    -----------
    The marking schema rejects Boolean in an integer control field.

    Method
    ------
    Validate the explicit ``boolean-as-integer`` fixture through the marking schema.

    Oracle
    ------
    JSON Boolean and integer are distinct semantic wire types under the public contract.

    Acceptance
    ----------
    Validation raises exactly ``jsonschema.ValidationError``.

    Interpretation
    --------------
    Failure permits wrong-semantic-type coercion or indicates fixture/schema drift.

    Limitations
    -----------
    Other wrong types, runtime construction, science, UQ, and Rust are excluded.
    """
    with pytest.raises(jsonschema.ValidationError):
        validate_fixture_document(
            "cpn-marking.schema.json", ROOT / "invalid" / "boolean-as-integer.json"
        )


def test_artifact__strict_json_fixture__rejects_nonfinite_real() -> None:
    """Evidence ID
    -----------
    SV-CPN-170

    Requirement
    -----------
    The designated nonfinite REAL fixture is rejected during strict JSON parsing.

    Method
    ------
    Load ``nonfinite-real.json`` with the controlled strict loader.

    Oracle
    ------
    Standard strict JSON excludes the fixture's nonfinite numeric token.

    Acceptance
    ----------
    Parsing raises exactly ``ValueError``.

    Interpretation
    --------------
    Failure admits a nonstandard JSON value or indicates fixture/parser drift.

    Limitations
    -----------
    Schema in-memory NaN behavior, runtime construction, science, UQ, and Rust are
    excluded.
    """
    with pytest.raises(ValueError):
        strict_load_json(ROOT / "invalid" / "nonfinite-real.json")


def make_wire_token(data: dict[str, Any]) -> CpnToken:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-031, SV-CPN-171, SV-CPN-172.
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


def make_wire_marking(data: dict[str, Any]) -> CpnMarking:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-031, SV-CPN-171, SV-CPN-172.
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
                tuple(make_wire_token(token) for token in place["tokens"]),
            )
            for place in places
        ),
    )


def make_wire_guard(data: dict[str, Any]) -> GuardExpression:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-031, SV-CPN-171.
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


def make_wire_net(data: dict[str, Any]) -> CpnNetDefinition:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-031, SV-CPN-171.
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
                make_wire_guard(transition["guard"]),
            )
            for transition in transitions
        ),
        (),
        make_wire_marking(initial),
    )


def make_collision_net() -> CpnNetDefinition:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-172.
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
        -----------
        Owns no identifier; supports SV-CPN-172.

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
    token_data = strict_load_json(ROOT / "valid" / "multiset-marking.json")
    assert isinstance(token_data, dict)
    token = make_wire_marking(token_data).places[0].tokens[0]
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


DEFINITION_RELATIONAL_CASES = (
    pytest.param("unknown-color.json", CpnIssueCode.UNKNOWN_COLOR, id="unknown_color"),
    pytest.param(
        "unbound-guard-variable.json",
        CpnIssueCode.UNBOUND_VARIABLE,
        id="unbound_guard_variable",
    ),
)


@pytest.mark.parametrize(("fixture_name", "expected_code"), DEFINITION_RELATIONAL_CASES)
def test_artifact__definition_relational_fixtures__reach_public_issue_code(
    fixture_name: str, expected_code: CpnIssueCode
) -> None:
    """Evidence ID
    -----------
    SV-CPN-031

    Requirement
    -----------
    Each schema-valid definition-relational fixture reaches its declared public issue.

    Method
    ------
    Validate, strictly load, construct, and execute ``CpnDefinitionValidator``.

    Oracle
    ------
    The fixture classification fixes the exact expected ``CpnIssueCode``.

    Acceptance
    ----------
    Schema succeeds and the runtime issue set contains the exact expected code.

    Interpretation
    --------------
    Failure may identify fixture, schema, parser, constructor, validator, or oracle
    drift.

    Limitations
    -----------
    The local parser is not persistence; science, UQ, engine execution, and Rust are
    excluded.
    """
    path = ROOT / "invalid" / fixture_name
    validate_fixture_document("cpn-net.schema.json", path)
    data = strict_load_json(path)
    assert isinstance(data, dict)
    result = CpnDefinitionValidator().execute(
        make_wire_net(cast("dict[str, Any]", data))
    )
    assert expected_code in {issue.code for issue in result.issues}


MARKING_RELATIONAL_CASES = (
    pytest.param(
        "duplicate-token-id.json",
        CpnIssueCode.DUPLICATE_TOKEN_ID,
        id="duplicate_token_id",
    ),
    pytest.param(
        "wrong-place-set.json", CpnIssueCode.PLACE_SET_MISMATCH, id="wrong_place_set"
    ),
)


@pytest.mark.parametrize(("fixture_name", "expected_code"), MARKING_RELATIONAL_CASES)
def test_artifact__marking_relational_fixtures__reach_public_issue_code(
    fixture_name: str, expected_code: CpnIssueCode
) -> None:
    """Evidence ID
    -----------
    SV-CPN-171

    Requirement
    -----------
    Each schema-valid marking-relational fixture reaches its declared public issue.

    Method
    ------
    Validate, strictly load, construct, and execute ``CpnMarkingValidator``.

    Oracle
    ------
    The fixture classification fixes the exact expected ``CpnIssueCode``.

    Acceptance
    ----------
    Schema succeeds and the runtime issue set contains the exact expected code.

    Interpretation
    --------------
    Failure may identify fixture, schema, parser, constructor, validator, or oracle
    drift.

    Limitations
    -----------
    The local parser is not persistence; science, UQ, engine execution, and Rust are
    excluded.
    """
    path = ROOT / "invalid" / fixture_name
    validate_fixture_document("cpn-marking.schema.json", path)
    data = strict_load_json(path)
    minimal = strict_load_json(ROOT / "valid" / "minimal-net.json")
    assert isinstance(data, dict)
    assert isinstance(minimal, dict)
    net = make_wire_net(cast("dict[str, Any]", minimal))
    result = CpnMarkingValidator().execute(
        net, make_wire_marking(cast("dict[str, Any]", data))
    )
    assert expected_code in {issue.code for issue in result.issues}


def test_artifact__output_collision_fixture__reaches_public_error_code() -> None:
    """Evidence ID
    -----------
    SV-CPN-172

    Requirement
    -----------
    The schema-valid output-collision fixture reaches ``OUTPUT_ID_COLLISION``.

    Method
    ------
    Validate, load, construct the public request, and execute ``TransitionFirer``.

    Oracle
    ------
    The fixture classification fixes the exact public collision error code.

    Acceptance
    ----------
    Schema succeeds and firing raises ``CpnFiringError`` with the exact code.

    Interpretation
    --------------
    Failure may identify fixture, schema, parser, constructor, firer, or oracle drift.

    Limitations
    -----------
    The local parser is not persistence; science, UQ, external engines, and Rust are
    excluded.
    """
    path = ROOT / "invalid" / "output-id-collision.json"
    validate_fixture_document("cpn-firing.schema.json", path)
    request_data = strict_load_json(path)
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
        request_data["transition_id"], binding, tuple(request_data["output_token_ids"])
    )
    net = make_collision_net()
    with pytest.raises(CpnFiringError) as collision:
        TransitionFirer().execute(net, net.initial_marking, request)
    assert collision.value.detail.code is CpnErrorCode.OUTPUT_ID_COLLISION
