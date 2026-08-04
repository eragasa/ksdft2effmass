"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TransitionFirer``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TransitionFirer`` is the sole primary SUT. Tests exercise its documented public
contract with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions
------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-021, SV-CPN-022 and owns no independent evidence
    ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Return a net whose ready place contains one
    independently valid token.

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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-020 and owns no independent evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Build two firings whose routing data explicitly
    retains iteration index 7.

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


def test_method__contract__firing_consumes_reads_produces_and_revises(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-017

    Requirement
    -----------
    read/consume/output firing and revision audit.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: read/consume/output firing and revision
    audit. Prior requirement detail: The version-1 P1 contract requires
    read/consume/output firing and revision audit. Prior method detail: Enable then call
    ``TransitionFirer.execute`` with output ID ``done-1`` on the base net. Prior
    independent oracle detail: Arc inscriptions prescribe consuming work-1, retaining
    authorization-1, producing one lineage token, and advancing revision 0 to 1. Prior
    acceptance criterion detail: The result exactly matches those consumed/read IDs,
    parent IDs, final token set, and revisions. Prior failure interpretation detail: Any
    mismatch means firing did not implement the declared multiset inscriptions. Prior
    limitations detail: The produced token is routing state, not a scientific result.

    Oracle
    ------
    The documented public rule that the SUT must read/consume/output firing and revision
    audit is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__contract__maximum_revision_returns_structured_overflow(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-086

    Requirement
    -----------
    maximum-revision firing raises the stable structured overflow error before successor
    construction.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: fail stably before constructing an
    overflowing successor. Requirement: firing a valid marking at revision ``2**63 - 1``
    returns the stable ``REVISION_OVERFLOW`` structured error before successor
    construction. Method: retain the independently enabled synthetic net/binding,
    replace only the marking revision, and call the public ActionObject. Oracle: no
    nonnegative signed-i64 successor exists for the endpoint. Acceptance raises
    ``CpnFiringError`` with the exact enum code and model/transition identities. Failure
    either leaks integer overflow or constructs invalid state. The test does not
    validate execution engines, persistence, or scientific semantics.

    Oracle
    ------
    The documented public rule that the SUT must maximum-revision firing raises the
    stable structured overflow error before successor construction is the contract
    oracle; fixed synthetic values, Python exact type/value semantics, and the public
    error taxonomy provide independently inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__contract__output_count_and_collision_are_structured(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-018

    Requirement
    -----------
    intrinsic output IDs versus marking collisions.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: intrinsic output IDs versus marking
    collisions. Prior requirement detail: The version-1 P1 contract requires intrinsic
    output IDs versus marking collisions. Prior method detail: Exercise
    ``TransitionFirer.execute`` with zero output IDs and an existing marking ID using
    independently valid requests. Prior independent oracle detail: One template requires
    one ID and ``work-1`` already exists in the marking. Prior acceptance criterion
    detail: The firer reports ``OUTPUT_ID_COUNT_MISMATCH`` and ``OUTPUT_ID_COLLISION``
    respectively. Prior failure interpretation detail: Failure confuses intrinsic
    identifier validity with current-marking firing policy. Prior limitations detail:
    Identity generation policy remains caller-owned.

    Oracle
    ------
    The documented public rule that the SUT must intrinsic output IDs versus marking
    collisions is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__contract__binding_is_explicit_and_current(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-019

    Requirement
    -----------
    current binding and intrinsic ResultObject consistency.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: current binding and intrinsic ResultObject
    consistency. Prior requirement detail: The version-1 P1 contract requires current
    binding and intrinsic ResultObject consistency. Prior method detail: Fire an
    explicit empty binding against the valid enabled-binding set. Prior independent
    oracle detail: The independently enumerated enabled-binding set contains one
    nonempty binding, so the empty binding is not current. Prior acceptance criterion
    detail: The firer raises ``TRANSITION_NOT_ENABLED`` with its exact structured code.
    Prior failure interpretation detail: Acceptance would allow firing without a current
    enabled binding. Prior limitations detail: This does not bypass invariants or test
    persistence.

    Oracle
    ------
    The documented public rule that the SUT must current binding and intrinsic
    ResultObject consistency is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(TransitionNotEnabledError) as error:
        TransitionFirer().execute(
            executable_net,
            executable_net.initial_marking,
            FiringRequest("execute", TransitionBinding("execute", ()), ("done-1",)),
        )
    assert error.value.detail.code is CpnErrorCode.TRANSITION_NOT_ENABLED


def test_method__contract__terminal_failure_is_read_for_retry_and_retained(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-020

    Requirement
    -----------
    retained retry history and deterministic repeated firing with the same explicitly
    supplied iteration index; no automatic index advancement.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: retained retry history and repeated
    nonnumeric firing. Prior requirement detail: The version-1 P1 contract permits
    repeated transition execution while treating ``iteration_index`` as explicitly
    supplied/copied routing data; firing does not automatically advance that index.
    Prior method detail: First fire a retry pattern that reads a terminal failure. Then
    run the same two-firing sequence twice to prove determinism, with both chained
    authorizations explicitly supplying the same nonzero iteration index 7. Prior
    independent oracle detail: Read arcs retain failure history. The two authorization
    tokens independently prescribe attempts 1/2, retry parents 0/1, and the unchanged
    index 7, while the marking contract advances revision once per firing from 0 through
    1 to 2. Prior acceptance criterion detail: The retry retains all three identities.
    Both repeated-firing runs yield equal markings; each produced token retains index 7,
    and marking revision advances exactly 0 to 1 to 2. The final lineage is attempt-2
    with parent attempt-1. Prior failure interpretation detail: Failure means terminal
    retention, explicit routing-data copying, revision advance, or deterministic
    repeated execution regressed. A result index other than 7 would incorrectly conflate
    repeated firing with index advancement. Prior limitations detail: The test supplies
    synthetic control authorizations. It proves neither arithmetic nor automatic
    increment semantics, which the version-1 expression language does not provide, and
    it does not establish convergence or scientific iteration policy, scientific
    validation, or uncertainty quantification.

    Oracle
    ------
    The documented public rule that the SUT must retained retry history and
    deterministic repeated firing with the same explicitly supplied iteration index; no
    automatic index advancement is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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
        """Evidence ID
        -----------
        This helper supports exactly SV-CPN-020 and owns no independent evidence ID.

        Requirement
        -----------
        Provide explicit synthetic setup or assertion mechanics without creating an
        independent pass claim.

        Method
        ------
        Construct or transform the public CPN test inputs required by the listed
        evidence owners. Prior helper description: Execute twice with explicit index 7
        and return immutable state.

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


def test_method__contract__terminal_consume_is_rejected(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-021

    Requirement
    -----------
    terminal outcome consumption prohibition.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: terminal outcome consumption prohibition.
    Prior requirement detail: The version-1 P1 contract requires terminal outcome
    consumption prohibition. Prior method detail: Place a terminal failed work token on
    a consume arc and call ``TransitionFirer.execute`` with the otherwise valid binding.
    Prior independent oracle detail: Terminal history is immutable workflow evidence and
    may only participate through read arcs. Prior acceptance criterion detail: A
    ``CpnFiringError`` is raised with code ``TERMINAL_TOKEN_CONSUMPTION``. Prior failure
    interpretation detail: Any successful firing would erase retained terminal history.
    Prior limitations detail: No retry authorization semantics are evaluated here.

    Oracle
    ------
    The documented public rule that the SUT must terminal outcome consumption
    prohibition is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__contract__recoverable_blocked_token_can_be_consumed(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-022

    Requirement
    -----------
    consumption of recoverable blocked state.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: consumption of recoverable blocked state.
    Prior requirement detail: The version-1 P1 contract requires consumption of
    recoverable blocked state. Prior method detail: Replace work with a recoverable
    blocked branch token, enable, and fire the consume transition. Prior independent
    oracle detail: The outcome matrix permits recovery to consume recoverable blocked
    state, unlike terminal outcomes. Prior acceptance criterion detail: Consumed IDs
    equal ``('work-1',)`` and successor revision is exactly 1. Prior failure
    interpretation detail: Failure would make the documented recovery path
    unrepresentable. Prior limitations detail: The test does not decide when a real
    branch should be blocked.

    Oracle
    ------
    The documented public rule that the SUT must consumption of recoverable blocked
    state is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__contract__firer_rejects_wrong_public_argument_types(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-034

    Requirement
    -----------
    wrong-type validation at the TransitionFirer boundary.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: wrong-type validation at the
    TransitionFirer boundary. Prior requirement detail: The version-1 P1 contract
    requires wrong-type validation at the TransitionFirer boundary. Prior method detail:
    Call ``TransitionFirer.execute`` with wrong-type net, marking, and request arguments
    individually and all together, while using valid counterparts for each isolated
    case. Prior independent oracle detail: The public signature and documented error
    taxonomy require semantic ``TypeError`` before any attribute dereference or firing
    work. Prior acceptance criterion detail: Each call raises ``TypeError`` naming the
    first invalid argument: net, marking, or request; the all-invalid call names net.
    Prior failure interpretation detail: ``AttributeError`` or operational work would
    prove precondition validation occurs too late. Prior limitations detail: This checks
    Python semantic types only and does not alter protected wire-number or integer-width
    rules.

    Oracle
    ------
    The documented public rule that the SUT must wrong-type validation at the
    TransitionFirer boundary is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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
