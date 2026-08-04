"""Software verification for ``TokenOutcome`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

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
def test_cpn_sv_p1_004_scoped_terminal_outcomes_are_reachable(
    scope: OutcomeScope,
) -> None:
    """SV-CPN-004: reachable terminal outcomes at every declared scope.

    Requirement
    -----------
    The version-1 P1 contract requires reachable terminal outcomes at every declared
    scope.

    Method
    ------
    For every ``OutcomeScope``, construct ``TokenOutcome`` for accepted, rejected,
    and failed terminal states.

    Independent oracle
    ------------------
    The approved outcome matrix permits each of those statuses only with terminal
    terminality at attempt, branch, gate, or workflow scope.

    Acceptance criterion
    --------------------
    All twelve public constructions succeed and preserve the exact parameterized
    scope.

    Failure interpretation
    ----------------------
    Failure makes a documented valid outcome state unreachable.

    Limitations
    -----------
    Workflow status reachability is software evidence, not scientific acceptance.
    """
    for status in (
        OutcomeStatus.ACCEPTED,
        OutcomeStatus.REJECTED,
        OutcomeStatus.FAILED,
    ):
        outcome = TokenOutcome(status, scope, "scope-1", OutcomeTerminality.TERMINAL)
        assert outcome.scope is scope


def test_cpn_sv_p1_005_only_blocked_may_be_recoverable() -> None:
    """SV-CPN-005: recoverability restricted to blocked outcomes.

    Requirement
    -----------
    The version-1 P1 contract requires recoverability restricted to blocked
    outcomes.

    Method
    ------
    Construct a recoverable blocked branch outcome, then attempt a recoverable
    failed attempt outcome.

    Independent oracle
    ------------------
    The outcome matrix admits both terminalities for blocked but only terminal for
    failed.

    Acceptance criterion
    --------------------
    Blocked construction succeeds exactly; failed/recoverable raises ``ValueError``
    mentioning terminality.

    Failure interpretation
    ----------------------
    A failure would broaden or narrow the explicit recovery-state contract.

    Limitations
    -----------
    No recovery transition or external operation is performed.
    """
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


def test_cpn_sv_p1_076_outcome_fields_have_exact_public_types_and_identity() -> None:
    """SV-CPN-076: require enum-owned outcome state and nonempty scope identity.

    Public construction across controlled invalid fields is the method; exact enum
    classes and nonempty identity are the oracle. Acceptance distinguishes type and
    value failures. Status/terminality combinations remain owned by prior evidence.
    """
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
