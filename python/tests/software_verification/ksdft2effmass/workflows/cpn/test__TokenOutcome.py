"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TokenOutcome``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TokenOutcome`` is the sole primary SUT. Tests exercise its documented public contract
with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions
------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

import pytest

from ksdft2effmass.workflows.cpn import (
    OutcomeScope,
    OutcomeStatus,
    OutcomeTerminality,
    TokenOutcome,
)

pytestmark = pytest.mark.software_verification

SUT = TokenOutcome


@pytest.mark.parametrize("scope", list(OutcomeScope))
def test_constructor__contract__scoped_terminal_outcomes_are_reachable(
    scope: OutcomeScope,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-004

    Requirement
    -----------
    reachable terminal outcomes at every declared scope.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reachable terminal outcomes at every
    declared scope. Prior requirement detail: The version-1 P1 contract requires
    reachable terminal outcomes at every declared scope. Prior method detail: For every
    ``OutcomeScope``, construct ``TokenOutcome`` for accepted, rejected, and failed
    terminal states. Prior independent oracle detail: The approved outcome matrix
    permits each of those statuses only with terminal terminality at attempt, branch,
    gate, or workflow scope. Prior acceptance criterion detail: All twelve public
    constructions succeed and preserve the exact parameterized scope. Prior failure
    interpretation detail: Failure makes a documented valid outcome state unreachable.
    Prior limitations detail: Workflow status reachability is software evidence, not
    scientific acceptance.

    Oracle
    ------
    The documented public rule that the SUT must reachable terminal outcomes at every
    declared scope is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
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
    for status in (
        OutcomeStatus.ACCEPTED,
        OutcomeStatus.REJECTED,
        OutcomeStatus.FAILED,
    ):
        outcome = TokenOutcome(status, scope, "scope-1", OutcomeTerminality.TERMINAL)
        assert outcome.scope is scope


def test_constructor__contract__only_blocked_may_be_recoverable() -> None:
    """Evidence ID
    -----------
    SV-CPN-005

    Requirement
    -----------
    recoverability restricted to blocked outcomes.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: recoverability restricted to blocked
    outcomes. Prior requirement detail: The version-1 P1 contract requires
    recoverability restricted to blocked outcomes. Prior method detail: Construct a
    recoverable blocked branch outcome, then attempt a recoverable failed attempt
    outcome. Prior independent oracle detail: The outcome matrix admits both
    terminalities for blocked but only terminal for failed. Prior acceptance criterion
    detail: Blocked construction succeeds exactly; failed/recoverable raises
    ``ValueError`` mentioning terminality. Prior failure interpretation detail: A
    failure would broaden or narrow the explicit recovery-state contract. Prior
    limitations detail: No recovery transition or external operation is performed.

    Oracle
    ------
    The documented public rule that the SUT must recoverability restricted to blocked
    outcomes is the contract oracle; fixed synthetic values, Python exact type/value
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
    blocked = TokenOutcome(
        OutcomeStatus.BLOCKED,
        OutcomeScope.BRANCH,
        "branch-1",
        OutcomeTerminality.RECOVERABLE,
    )
    assert blocked.terminality is OutcomeTerminality.RECOVERABLE
    with pytest.raises(ValueError, match="terminal"):
        TokenOutcome(
            OutcomeStatus.FAILED,
            OutcomeScope.ATTEMPT,
            "attempt-1",
            OutcomeTerminality.RECOVERABLE,
        )


def test_constructor__contract__outcome_fields_have_exact_public_types_and_identity\
() -> None:
    """Evidence ID
    -----------
    SV-CPN-076

    Requirement
    -----------
    require enum-owned outcome state and nonempty scope identity.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: require enum-owned outcome state and
    nonempty scope identity. Public construction across controlled invalid fields is the
    method; exact enum classes and nonempty identity are the oracle. Acceptance
    distinguishes type and value failures. Status/terminality combinations remain owned
    by prior evidence.

    Oracle
    ------
    The documented public rule that the SUT must require enum-owned outcome state and
    nonempty scope identity is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
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
    assert (
        SUT(
            OutcomeStatus.BLOCKED,
            OutcomeScope.GATE,
            "g",
            OutcomeTerminality.RECOVERABLE,
        ).scope_id
        == "g"
    )
    with pytest.raises(TypeError):
        SUT("blocked", OutcomeScope.GATE, "g", OutcomeTerminality.RECOVERABLE)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(OutcomeStatus.BLOCKED, "gate", "g", OutcomeTerminality.RECOVERABLE)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(
            OutcomeStatus.BLOCKED,
            OutcomeScope.GATE,
            1,  # type: ignore[arg-type]
            OutcomeTerminality.RECOVERABLE,
        )
    with pytest.raises(ValueError):
        SUT(
            OutcomeStatus.BLOCKED, OutcomeScope.GATE, "", OutcomeTerminality.RECOVERABLE
        )
    with pytest.raises(TypeError):
        SUT(
            OutcomeStatus.BLOCKED,
            OutcomeScope.GATE,
            "g",
            "recoverable",  # type: ignore[arg-type]
        )
