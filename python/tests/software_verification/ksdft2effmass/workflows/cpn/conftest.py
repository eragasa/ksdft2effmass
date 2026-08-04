"""Synthetic CPN fixtures shared by P1 software-verification tests.

The fixtures exercise the public contract without scientific payloads. They are
not numerical verification, scientific validation, or uncertainty quantification.
"""

from collections.abc import Callable

import pytest

from ksdft2effmass.workflows.cpn import (
    ArcDefinition,
    ArcDirection,
    ColorDefinition,
    CpnMarking,
    CpnNetDefinition,
    CpnToken,
    GuardExpression,
    GuardOperator,
    InputArcMode,
    InputInscription,
    OutputInscription,
    PlaceDefinition,
    PlaceMarking,
    TokenField,
    TokenFieldAssignment,
    TokenPattern,
    TokenTemplate,
    TransitionDefinition,
    ValueExpression,
    ValueExpressionKind,
)

TokenFactory = Callable[..., CpnToken]


@pytest.fixture
def token_factory() -> TokenFactory:
    """Return a factory for independently valid synthetic routing tokens."""

    def create(token_id: str, color_id: str = "work", **overrides: object) -> CpnToken:
        values: dict[str, object] = {
            "token_id": token_id,
            "color_id": color_id,
            "workflow_id": "workflow-1",
            "run_id": "run-1",
            "parent_run_id": None,
            "attempt_id": "attempt-1",
            "retry_parent_attempt_id": None,
            "iteration_index": 0,
            "payload_type_id": None,
            "payload_id": None,
            "payload_schema_version": None,
            "provenance_ids": ("provenance-1",),
            "parent_token_ids": (),
            "correlation_id": "correlation-1",
            "authorization_id": "authorization-1",
            "outcome": None,
        }
        values.update(overrides)
        return CpnToken(**values)  # type: ignore[arg-type]

    return create


def _field(variable: str, field: TokenField) -> ValueExpression:
    """Build one declarative bound-token field expression."""
    return ValueExpression(
        ValueExpressionKind.TOKEN_FIELD, variable=variable, field=field
    )


@pytest.fixture
def executable_net(token_factory: TokenFactory) -> CpnNetDefinition:
    """Return a two-input synchronized consume/read net with one output."""
    work = token_factory("work-1")
    authorization = token_factory("authorization-1", "authorization")
    initial = CpnMarking(
        1,
        "execution-model",
        0,
        (
            PlaceMarking("authorization", (authorization,)),
            PlaceMarking("completed", ()),
            PlaceMarking("ready", (work,)),
        ),
    )
    assignments = (
        TokenFieldAssignment(
            TokenField.WORKFLOW_ID, _field("work", TokenField.WORKFLOW_ID)
        ),
        TokenFieldAssignment(TokenField.RUN_ID, _field("work", TokenField.RUN_ID)),
        TokenFieldAssignment(
            TokenField.ATTEMPT_ID, _field("authorization", TokenField.ATTEMPT_ID)
        ),
        TokenFieldAssignment(
            TokenField.ITERATION_INDEX,
            _field("authorization", TokenField.ITERATION_INDEX),
        ),
        TokenFieldAssignment(
            TokenField.PROVENANCE_IDS, _field("work", TokenField.PROVENANCE_IDS)
        ),
        TokenFieldAssignment(
            TokenField.PARENT_TOKEN_IDS,
            ValueExpression(
                ValueExpressionKind.BOUND_TOKEN_IDS, variables=("work", "authorization")
            ),
        ),
        TokenFieldAssignment(
            TokenField.AUTHORIZATION_ID,
            _field("authorization", TokenField.AUTHORIZATION_ID),
        ),
    )
    return CpnNetDefinition(
        1,
        "execution-model",
        (
            ColorDefinition("authorization", "authorization routing", ()),
            ColorDefinition("done", "completed routing", ()),
            ColorDefinition("work", "work routing", ()),
        ),
        (
            PlaceDefinition(
                "authorization", "authorization inputs", ("authorization",)
            ),
            PlaceDefinition("completed", "completed outputs", ("done",)),
            PlaceDefinition("ready", "ready inputs", ("work",)),
        ),
        (
            TransitionDefinition(
                "execute",
                "synchronize work and authorization",
                GuardExpression(
                    GuardOperator.EQUAL,
                    left=_field("work", TokenField.RUN_ID),
                    right=_field("authorization", TokenField.RUN_ID),
                ),
            ),
        ),
        (
            ArcDefinition(
                "a-consume",
                "ready",
                "execute",
                ArcDirection.INPUT,
                input_inscription=InputInscription(
                    InputArcMode.CONSUME, (TokenPattern("work", ("work",)),)
                ),
            ),
            ArcDefinition(
                "b-read",
                "authorization",
                "execute",
                ArcDirection.INPUT,
                input_inscription=InputInscription(
                    InputArcMode.READ,
                    (TokenPattern("authorization", ("authorization",)),),
                ),
            ),
            ArcDefinition(
                "c-output",
                "completed",
                "execute",
                ArcDirection.OUTPUT,
                output_inscription=OutputInscription(
                    (TokenTemplate("done", assignments),)
                ),
            ),
        ),
        initial,
    )
