"""Software verification for ``TransitionFirer`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows.cpn import (
    ArcDirection,
    CpnErrorCode,
    CpnFiringError,
    CpnMarking,
    CpnNetDefinition,
    CpnToken,
    FiringRequest,
    GuardExpression,
    GuardOperator,
    InputArcMode,
    InputInscription,
    OutcomeScope,
    OutcomeStatus,
    OutcomeTerminality,
    PlaceMarking,
    TokenField,
    TokenFieldAssignment,
    TokenOutcome,
    TransitionBinding,
    TransitionEnabler,
    TransitionFirer,
    TransitionNotEnabledError,
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = TransitionFirer


def _replace_ready(net: CpnNetDefinition, token: CpnToken) -> CpnNetDefinition:
    """Return a net whose ready place contains one independently valid token."""
    marking = CpnMarking(
        1,
        net.model_id,
        0,
        tuple(
            PlaceMarking(
                place.place_id,
                (token,) if place.place_id == "ready" else place.tokens,
            )
            for place in net.initial_marking.places
        ),
    )
    return replace(net, initial_marking=marking)


def _iteration_net(net: CpnNetDefinition) -> CpnNetDefinition:
    """Build two firings whose routing data explicitly retains iteration index 7."""
    work = replace(
        net.initial_marking.places[2].tokens[0],
        attempt_id="attempt-0",
        retry_parent_attempt_id=None,
        iteration_index=7,
    )
    authorization_1 = replace(
        net.initial_marking.places[0].tokens[0],
        token_id="authorization-1",
        attempt_id="attempt-1",
        retry_parent_attempt_id="attempt-0",
        iteration_index=7,
    )
    authorization_2 = replace(
        authorization_1,
        token_id="authorization-2",
        attempt_id="attempt-2",
        retry_parent_attempt_id="attempt-1",
        iteration_index=7,
    )
    retry_parent_assignment = TokenFieldAssignment(
        TokenField.RETRY_PARENT_ATTEMPT_ID,
        ValueExpression(
            ValueExpressionKind.TOKEN_FIELD,
            variable="work",
            field=TokenField.ATTEMPT_ID,
        ),
    )
    arcs = []
    for arc in net.arcs:
        if arc.direction is ArcDirection.INPUT and arc.place_id == "authorization":
            assert arc.input_inscription is not None
            arcs.append(
                replace(
                    arc,
                    input_inscription=InputInscription(
                        InputArcMode.CONSUME,
                        arc.input_inscription.patterns,
                    ),
                )
            )
        elif arc.direction is ArcDirection.OUTPUT:
            assert arc.output_inscription is not None
            template = arc.output_inscription.templates[0]
            arcs.append(
                replace(
                    arc,
                    place_id="ready",
                    output_inscription=replace(
                        arc.output_inscription,
                        templates=(
                            replace(
                                template,
                                color_id="work",
                                assignments=template.assignments
                                + (retry_parent_assignment,),
                            ),
                        ),
                    ),
                )
            )
        else:
            arcs.append(arc)
    transition = replace(
        net.transitions[0],
        guard=GuardExpression(
            GuardOperator.EQUAL,
            left=ValueExpression(
                ValueExpressionKind.TOKEN_FIELD,
                variable="work",
                field=TokenField.ATTEMPT_ID,
            ),
            right=ValueExpression(
                ValueExpressionKind.TOKEN_FIELD,
                variable="authorization",
                field=TokenField.RETRY_PARENT_ATTEMPT_ID,
            ),
        ),
    )
    marking = CpnMarking(
        1,
        net.model_id,
        0,
        (
            PlaceMarking("authorization", (authorization_1, authorization_2)),
            PlaceMarking("completed", ()),
            PlaceMarking("ready", (work,)),
        ),
    )
    return replace(
        net,
        transitions=(transition,),
        arcs=tuple(arcs),
        initial_marking=marking,
    )


def test_cpn_sv_p1_017_firing_consumes_reads_produces_and_revises(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-017: read/consume/output firing and revision audit.

    Requirement
    -----------
    The version-1 P1 contract requires read/consume/output firing and revision
    audit.

    Method
    ------
    Enable then call ``TransitionFirer.execute`` with output ID ``done-1`` on the
    base net.

    Independent oracle
    ------------------
    Arc inscriptions prescribe consuming work-1, retaining authorization-1,
    producing one lineage token, and advancing revision 0 to 1.

    Acceptance criterion
    --------------------
    The result exactly matches those consumed/read IDs, parent IDs, final token set,
    and revisions.

    Failure interpretation
    ----------------------
    Any mismatch means firing did not implement the declared multiset inscriptions.

    Limitations
    -----------
    The produced token is routing state, not a scientific result.
    """
    binding = (
        TransitionEnabler()
        .execute(executable_net, executable_net.initial_marking, "execute")
        .bindings[0]
    )
    result = TransitionFirer().execute(
        executable_net,
        executable_net.initial_marking,
        FiringRequest("execute", binding, ("done-1",)),
    )
    assert result.previous_revision == 0
    assert result.marking.revision == 1
    assert result.consumed_token_ids == ("work-1",)
    assert result.read_token_ids == ("authorization-1",)
    assert result.produced_tokens[0].parent_token_ids == (
        "authorization-1",
        "work-1",
    )
    all_ids = {
        token.token_id for place in result.marking.places for token in place.tokens
    }
    assert all_ids == {"authorization-1", "done-1"}


def test_cpn_sv_p1_086_maximum_revision_returns_structured_overflow(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-086: fail stably before constructing an overflowing successor.

    Requirement: firing a valid marking at revision ``2**63 - 1`` returns the
    stable ``REVISION_OVERFLOW`` structured error before successor construction.
    Method: retain the independently enabled synthetic net/binding, replace only
    the marking revision, and call the public ActionObject. Oracle: no nonnegative
    signed-i64 successor exists for the endpoint. Acceptance raises
    ``CpnFiringError`` with the exact enum code and model/transition identities.
    Failure either leaks integer overflow or constructs invalid state. The test
    does not validate execution engines, persistence, or scientific semantics.
    """
    maximum = 2**63 - 1
    marking = replace(executable_net.initial_marking, revision=maximum)
    binding = (
        TransitionEnabler().execute(executable_net, marking, "execute").bindings[0]
    )
    with pytest.raises(CpnFiringError) as error:
        SUT().execute(
            executable_net,
            marking,
            FiringRequest("execute", binding, ("never-constructed",)),
        )
    assert error.value.detail.code is CpnErrorCode.REVISION_OVERFLOW
    assert error.value.detail.model_id == executable_net.model_id
    assert error.value.detail.transition_id == "execute"


def test_cpn_sv_p1_018_output_count_and_collision_are_structured(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-018: intrinsic output IDs versus marking collisions.

    Requirement
    -----------
    The version-1 P1 contract requires intrinsic output IDs versus marking
    collisions.

    Method
    ------
    Exercise ``TransitionFirer.execute`` with zero output IDs and an existing
    marking ID using independently valid requests.

    Independent oracle
    ------------------
    One template requires one ID and ``work-1`` already exists in the marking.

    Acceptance criterion
    --------------------
    The firer reports ``OUTPUT_ID_COUNT_MISMATCH`` and ``OUTPUT_ID_COLLISION``
    respectively.

    Failure interpretation
    ----------------------
    Failure confuses intrinsic identifier validity with current-marking firing
    policy.

    Limitations
    -----------
    Identity generation policy remains caller-owned.
    """
    binding = (
        TransitionEnabler()
        .execute(executable_net, executable_net.initial_marking, "execute")
        .bindings[0]
    )
    with pytest.raises(CpnFiringError) as count_error:
        TransitionFirer().execute(
            executable_net,
            executable_net.initial_marking,
            FiringRequest("execute", binding, ()),
        )
    assert count_error.value.detail.code is CpnErrorCode.OUTPUT_ID_COUNT_MISMATCH
    with pytest.raises(CpnFiringError) as collision_error:
        TransitionFirer().execute(
            executable_net,
            executable_net.initial_marking,
            FiringRequest("execute", binding, ("work-1",)),
        )
    assert collision_error.value.detail.code is CpnErrorCode.OUTPUT_ID_COLLISION


def test_cpn_sv_p1_019_binding_is_explicit_and_current(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-019: current binding and intrinsic ResultObject consistency.

    Requirement
    -----------
    The version-1 P1 contract requires current binding and intrinsic ResultObject
    consistency.

    Method
    ------
    Fire an explicit empty binding against the valid enabled-binding set.

    Independent oracle
    ------------------
    The independently enumerated enabled-binding set contains one nonempty binding,
    so the empty binding is not current.

    Acceptance criterion
    --------------------
    The firer raises ``TRANSITION_NOT_ENABLED`` with its exact structured code.

    Failure interpretation
    ----------------------
    Acceptance would allow firing without a current enabled binding.

    Limitations
    -----------
    This does not bypass invariants or test persistence.
    """
    with pytest.raises(TransitionNotEnabledError) as error:
        TransitionFirer().execute(
            executable_net,
            executable_net.initial_marking,
            FiringRequest("execute", TransitionBinding("execute", ()), ("done-1",)),
        )
    assert error.value.detail.code is CpnErrorCode.TRANSITION_NOT_ENABLED


def test_cpn_sv_p1_020_terminal_failure_is_read_for_retry_and_retained(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-020: retained retry history and repeated nonnumeric firing.

    Requirement
    -----------
    The version-1 P1 contract permits repeated transition execution while treating
    ``iteration_index`` as explicitly supplied/copied routing data; firing does not
    automatically advance that index.

    Method
    ------
    First fire a retry pattern that reads a terminal failure. Then run the same
    two-firing sequence twice to prove determinism, with both chained authorizations
    explicitly supplying the same nonzero iteration index 7.

    Independent oracle
    ------------------
    Read arcs retain failure history. The two authorization tokens independently
    prescribe attempts 1/2, retry parents 0/1, and the unchanged index 7, while the
    marking contract advances revision once per firing from 0 through 1 to 2.

    Acceptance criterion
    --------------------
    The retry retains all three identities. Both repeated-firing runs yield equal
    markings; each produced token retains index 7, and marking revision advances
    exactly 0 to 1 to 2. The final lineage is attempt-2 with parent attempt-1.

    Failure interpretation
    ----------------------
    Failure means terminal retention, explicit routing-data copying, revision
    advance, or deterministic repeated execution regressed. A result index other
    than 7 would incorrectly conflate repeated firing with index advancement.

    Limitations
    -----------
    The test supplies synthetic control authorizations. It proves neither arithmetic
    nor automatic increment semantics, which the version-1 expression language does
    not provide, and it does not establish convergence or scientific iteration
    policy, scientific validation, or uncertainty quantification.
    """
    original = executable_net.initial_marking.places[2].tokens[0]
    failure = replace(
        original,
        outcome=TokenOutcome(
            OutcomeStatus.FAILED,
            OutcomeScope.ATTEMPT,
            original.attempt_id,
            OutcomeTerminality.TERMINAL,
        ),
    )
    authorization = replace(
        executable_net.initial_marking.places[0].tokens[0],
        attempt_id="attempt-2",
        retry_parent_attempt_id="attempt-1",
        iteration_index=1,
    )
    retry_parent_assignment = TokenFieldAssignment(
        TokenField.RETRY_PARENT_ATTEMPT_ID,
        ValueExpression(
            ValueExpressionKind.TOKEN_FIELD,
            variable="work",
            field=TokenField.ATTEMPT_ID,
        ),
    )
    arcs = []
    for arc in executable_net.arcs:
        if (
            arc.direction is ArcDirection.INPUT
            and arc.place_id == "ready"
            and arc.input_inscription is not None
        ):
            arcs.append(
                replace(
                    arc,
                    input_inscription=InputInscription(
                        InputArcMode.READ,
                        arc.input_inscription.patterns,
                    ),
                )
            )
        elif (
            arc.direction is ArcDirection.OUTPUT and arc.output_inscription is not None
        ):
            template = arc.output_inscription.templates[0]
            arcs.append(
                replace(
                    arc,
                    output_inscription=replace(
                        arc.output_inscription,
                        templates=(
                            replace(
                                template,
                                assignments=template.assignments
                                + (retry_parent_assignment,),
                            ),
                        ),
                    ),
                )
            )
        else:
            arcs.append(arc)
    initial_marking = CpnMarking(
        1,
        executable_net.model_id,
        0,
        tuple(
            PlaceMarking(
                place.place_id,
                (failure,)
                if place.place_id == "ready"
                else (authorization,)
                if place.place_id == "authorization"
                else place.tokens,
            )
            for place in executable_net.initial_marking.places
        ),
    )
    net = replace(executable_net, arcs=tuple(arcs), initial_marking=initial_marking)
    binding = (
        TransitionEnabler().execute(net, net.initial_marking, "execute").bindings[0]
    )
    result = TransitionFirer().execute(
        net, net.initial_marking, FiringRequest("execute", binding, ("retry-attempt",))
    )
    all_ids = {
        token.token_id for place in result.marking.places for token in place.tokens
    }
    assert {"work-1", "authorization-1", "retry-attempt"} <= all_ids
    produced = result.produced_tokens[0]
    assert produced.authorization_id == "authorization-1"
    assert produced.attempt_id == "attempt-2"
    assert produced.retry_parent_attempt_id == "attempt-1"
    assert produced.iteration_index == 1

    iteration_net = _iteration_net(executable_net)

    def execute_two_cycles() -> CpnMarking:
        """Execute twice with explicit index 7 and return immutable state."""
        first_binding = (
            TransitionEnabler()
            .execute(
                iteration_net,
                iteration_net.initial_marking,
                "execute",
            )
            .bindings[0]
        )
        first = TransitionFirer().execute(
            iteration_net,
            iteration_net.initial_marking,
            FiringRequest("execute", first_binding, ("iteration-token-1",)),
        )
        assert first.previous_revision == 0
        assert first.marking.revision == 1
        assert first.produced_tokens[0].iteration_index == 7
        second_binding = (
            TransitionEnabler()
            .execute(
                iteration_net,
                first.marking,
                "execute",
            )
            .bindings[0]
        )
        second = TransitionFirer().execute(
            iteration_net,
            first.marking,
            FiringRequest("execute", second_binding, ("iteration-token-2",)),
        )
        assert second.previous_revision == 1
        assert second.marking.revision == 2
        assert second.produced_tokens[0].iteration_index == 7
        return second.marking

    marking_a = execute_two_cycles()
    marking_b = execute_two_cycles()
    assert marking_a == marking_b
    assert marking_a.revision == 2
    final = next(
        token
        for place in marking_a.places
        for token in place.tokens
        if token.token_id == "iteration-token-2"
    )
    assert final.attempt_id == "attempt-2"
    assert final.retry_parent_attempt_id == "attempt-1"
    assert final.iteration_index == 7


def test_cpn_sv_p1_021_terminal_consume_is_rejected(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-021: terminal outcome consumption prohibition.

    Requirement
    -----------
    The version-1 P1 contract requires terminal outcome consumption prohibition.

    Method
    ------
    Place a terminal failed work token on a consume arc and call
    ``TransitionFirer.execute`` with the otherwise valid binding.

    Independent oracle
    ------------------
    Terminal history is immutable workflow evidence and may only participate through
    read arcs.

    Acceptance criterion
    --------------------
    A ``CpnFiringError`` is raised with code ``TERMINAL_TOKEN_CONSUMPTION``.

    Failure interpretation
    ----------------------
    Any successful firing would erase retained terminal history.

    Limitations
    -----------
    No retry authorization semantics are evaluated here.
    """
    original = executable_net.initial_marking.places[2].tokens[0]
    terminal = replace(
        original,
        outcome=TokenOutcome(
            OutcomeStatus.FAILED,
            OutcomeScope.ATTEMPT,
            "attempt-1",
            OutcomeTerminality.TERMINAL,
        ),
    )
    net = _replace_ready(executable_net, terminal)
    normal_binding = (
        TransitionEnabler()
        .execute(executable_net, executable_net.initial_marking, "execute")
        .bindings[0]
    )
    with pytest.raises(CpnFiringError) as error:
        TransitionFirer().execute(
            net,
            net.initial_marking,
            FiringRequest("execute", normal_binding, ("new",)),
        )
    assert error.value.detail.code is CpnErrorCode.TERMINAL_TOKEN_CONSUMPTION


def test_cpn_sv_p1_022_recoverable_blocked_token_can_be_consumed(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-022: consumption of recoverable blocked state.

    Requirement
    -----------
    The version-1 P1 contract requires consumption of recoverable blocked state.

    Method
    ------
    Replace work with a recoverable blocked branch token, enable, and fire the
    consume transition.

    Independent oracle
    ------------------
    The outcome matrix permits recovery to consume recoverable blocked state, unlike
    terminal outcomes.

    Acceptance criterion
    --------------------
    Consumed IDs equal ``('work-1',)`` and successor revision is exactly 1.

    Failure interpretation
    ----------------------
    Failure would make the documented recovery path unrepresentable.

    Limitations
    -----------
    The test does not decide when a real branch should be blocked.
    """
    original = executable_net.initial_marking.places[2].tokens[0]
    blocked = replace(
        original,
        iteration_index=2,
        outcome=TokenOutcome(
            OutcomeStatus.BLOCKED,
            OutcomeScope.BRANCH,
            "branch-1",
            OutcomeTerminality.RECOVERABLE,
        ),
    )
    net = _replace_ready(executable_net, blocked)
    binding = (
        TransitionEnabler().execute(net, net.initial_marking, "execute").bindings[0]
    )
    result = TransitionFirer().execute(
        net, net.initial_marking, FiringRequest("execute", binding, ("recovered",))
    )
    assert result.consumed_token_ids == ("work-1",)
    assert result.marking.revision == 1


def test_cpn_sv_p1_034_firer_rejects_wrong_public_argument_types(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-034: wrong-type validation at the TransitionFirer boundary.

    Requirement
    -----------
    The version-1 P1 contract requires wrong-type validation at the TransitionFirer
    boundary.

    Method
    ------
    Call ``TransitionFirer.execute`` with wrong-type net, marking, and request
    arguments individually and all together, while using valid counterparts for each
    isolated case.

    Independent oracle
    ------------------
    The public signature and documented error taxonomy require semantic
    ``TypeError`` before any attribute dereference or firing work.

    Acceptance criterion
    --------------------
    Each call raises ``TypeError`` naming the first invalid argument: net, marking,
    or request; the all-invalid call names net.

    Failure interpretation
    ----------------------
    ``AttributeError`` or operational work would prove precondition validation
    occurs too late.

    Limitations
    -----------
    This checks Python semantic types only and does not alter protected wire-number
    or integer-width rules.
    """
    binding = (
        TransitionEnabler()
        .execute(executable_net, executable_net.initial_marking, "execute")
        .bindings[0]
    )
    request = FiringRequest("execute", binding, ("done-1",))
    firer = TransitionFirer()
    with pytest.raises(TypeError, match="net must be CpnNetDefinition"):
        firer.execute(object(), executable_net.initial_marking, request)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="marking must be CpnMarking"):
        firer.execute(executable_net, object(), request)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="request must be FiringRequest"):
        firer.execute(executable_net, executable_net.initial_marking, object())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="net must be CpnNetDefinition"):
        firer.execute(object(), object(), object())  # type: ignore[arg-type]
