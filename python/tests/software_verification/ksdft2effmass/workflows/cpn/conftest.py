"""Evidence class and represented meaning
--------------------------------------
This module provides synthetic helper and fixture support for P1 CPN
software-verification evidence. It represents exact software-routing setup rather than a
physical model, mathematical result, or independent evidence owner.

Owned contract, oracle, and scope
---------------------------------
The helpers support only the complete evidence-ID lists in their function docstrings and
own no independent evidence IDs. They construct public CPN inputs
without fabricating a class SUT, oracle, acceptance result, or separate pass claim.

VVUQ and scientific exclusions
------------------------------
Helper success only permits supported tests to run; failure can invalidate those tests'
setup. This module provides no numerical verification, scientific validation,
uncertainty quantification, physical-correctness, engine-adapter, persistence, or
cross-language-conformance evidence."""

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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-001, SV-CPN-002, SV-CPN-003, SV-CPN-010,
    SV-CPN-011, SV-CPN-012, SV-CPN-013, SV-CPN-014, SV-CPN-015, SV-CPN-016, SV-CPN-017,
    SV-CPN-018, SV-CPN-019, SV-CPN-020, SV-CPN-021, SV-CPN-022, SV-CPN-024, SV-CPN-025,
    SV-CPN-026, SV-CPN-034, SV-CPN-036, SV-CPN-039, SV-CPN-044, SV-CPN-051, SV-CPN-063,
    SV-CPN-064, SV-CPN-065, SV-CPN-066, SV-CPN-067, SV-CPN-070, SV-CPN-071, SV-CPN-072,
    SV-CPN-073, SV-CPN-082, SV-CPN-084, SV-CPN-085, SV-CPN-086 and owns no independent
    evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Return a factory for independently valid synthetic
    routing tokens.

    Oracle
    ------
    The helper has no independent oracle; each supported test owns and documents the
    applicable contract oracle.

    Acceptance
    ----------
    Return the exact public object or deterministic setup consumed by every listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation
    --------------
    A helper failure blocks or invalidates its listed evidence owners but is not an
    independent evidence failure.

    Limitations
    -----------
    The helper is synthetic, supports only the complete identifier list above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""

    def create(token_id: str, color_id: str = "work", **overrides: object) -> CpnToken:
        """Evidence ID
        -----------
        This helper supports exactly SV-CPN-001, SV-CPN-002, SV-CPN-003, SV-CPN-010,
        SV-CPN-011, SV-CPN-012, SV-CPN-013, SV-CPN-014, SV-CPN-015, SV-CPN-016,
        SV-CPN-017, SV-CPN-018, SV-CPN-019, SV-CPN-020, SV-CPN-021, SV-CPN-022,
        SV-CPN-024, SV-CPN-025, SV-CPN-026, SV-CPN-034, SV-CPN-036, SV-CPN-039,
        SV-CPN-044, SV-CPN-051, SV-CPN-063, SV-CPN-064, SV-CPN-065, SV-CPN-066,
        SV-CPN-067, SV-CPN-070, SV-CPN-071, SV-CPN-072, SV-CPN-073, SV-CPN-082,
        SV-CPN-084, SV-CPN-085, SV-CPN-086 and owns no independent evidence ID.

        Requirement
        -----------
        Provide explicit synthetic setup or assertion mechanics without creating an
        independent pass claim.

        Method
        ------
        Construct or transform the public CPN test inputs required by the listed
        evidence owners. Prior helper description: local synthetic setup only.

        Oracle
        ------
        The helper has no independent oracle; each supported test owns and documents the
        applicable contract oracle.

        Acceptance
        ----------
        Return the exact public object or deterministic setup consumed by every listed
        evidence owner, without swallowing exceptions or asserting a separate result.

        Interpretation
        --------------
        A helper failure blocks or invalidates its listed evidence owners but is not an
        independent evidence failure.

        Limitations
        -----------
        The helper is synthetic, supports only the complete identifier list above, owns
        no independent evidence ID, and establishes no numerical verification,
        scientific validation, uncertainty quantification, physical meaning, or
        cross-language conformance."""
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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-011, SV-CPN-085, SV-CPN-010, SV-CPN-012,
    SV-CPN-036, SV-CPN-013, SV-CPN-014, SV-CPN-044, SV-CPN-039, SV-CPN-070, SV-CPN-071,
    SV-CPN-084, SV-CPN-072, SV-CPN-073, SV-CPN-015, SV-CPN-016, SV-CPN-024, SV-CPN-025,
    SV-CPN-026, SV-CPN-017, SV-CPN-086, SV-CPN-018, SV-CPN-019, SV-CPN-020, SV-CPN-021,
    SV-CPN-022, SV-CPN-034 and owns no independent evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Build one declarative bound-token field
    expression.

    Oracle
    ------
    The helper has no independent oracle; each supported test owns and documents the
    applicable contract oracle.

    Acceptance
    ----------
    Return the exact public object or deterministic setup consumed by every listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation
    --------------
    A helper failure blocks or invalidates its listed evidence owners but is not an
    independent evidence failure.

    Limitations
    -----------
    The helper is synthetic, supports only the complete identifier list above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
    return ValueExpression(
        ValueExpressionKind.TOKEN_FIELD, variable=variable, field=field
    )


@pytest.fixture
def executable_net(token_factory: TokenFactory) -> CpnNetDefinition:
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-011, SV-CPN-085, SV-CPN-010, SV-CPN-012,
    SV-CPN-036, SV-CPN-013, SV-CPN-014, SV-CPN-044, SV-CPN-039, SV-CPN-070, SV-CPN-071,
    SV-CPN-084, SV-CPN-072, SV-CPN-073, SV-CPN-015, SV-CPN-016, SV-CPN-024, SV-CPN-025,
    SV-CPN-026, SV-CPN-017, SV-CPN-086, SV-CPN-018, SV-CPN-019, SV-CPN-020, SV-CPN-021,
    SV-CPN-022, SV-CPN-034 and owns no independent evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Return a two-input synchronized consume/read net
    with one output.

    Oracle
    ------
    The helper has no independent oracle; each supported test owns and documents the
    applicable contract oracle.

    Acceptance
    ----------
    Return the exact public object or deterministic setup consumed by every listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation
    --------------
    A helper failure blocks or invalidates its listed evidence owners but is not an
    independent evidence failure.

    Limitations
    -----------
    The helper is synthetic, supports only the complete identifier list above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
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
