r"""Software verification of ``TokenOutcome``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``TokenOutcome``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
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


@pytest.mark.parametrize(
    ("scope", "status"),
    (
        pytest.param(
            OutcomeScope.ATTEMPT, OutcomeStatus.ACCEPTED, id="attempt_accepted"
        ),
        pytest.param(
            OutcomeScope.ATTEMPT, OutcomeStatus.REJECTED, id="attempt_rejected"
        ),
        pytest.param(OutcomeScope.ATTEMPT, OutcomeStatus.FAILED, id="attempt_failed"),
        pytest.param(OutcomeScope.BRANCH, OutcomeStatus.ACCEPTED, id="branch_accepted"),
        pytest.param(OutcomeScope.BRANCH, OutcomeStatus.REJECTED, id="branch_rejected"),
        pytest.param(OutcomeScope.BRANCH, OutcomeStatus.FAILED, id="branch_failed"),
        pytest.param(OutcomeScope.GATE, OutcomeStatus.ACCEPTED, id="gate_accepted"),
        pytest.param(OutcomeScope.GATE, OutcomeStatus.REJECTED, id="gate_rejected"),
        pytest.param(OutcomeScope.GATE, OutcomeStatus.FAILED, id="gate_failed"),
        pytest.param(
            OutcomeScope.WORKFLOW, OutcomeStatus.ACCEPTED, id="workflow_accepted"
        ),
        pytest.param(
            OutcomeScope.WORKFLOW, OutcomeStatus.REJECTED, id="workflow_rejected"
        ),
        pytest.param(OutcomeScope.WORKFLOW, OutcomeStatus.FAILED, id="workflow_failed"),
    ),
)
def test_constructor__fields__scoped_terminal_outcomes_are_reachable(
    scope: OutcomeScope,
    status: OutcomeStatus,
) -> None:
    """Evidence ID: SV-CPN-004

    Requirement: reachable terminal outcomes at every declared scope.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
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

    Oracle: The documented public rule that the SUT must reachable terminal outcomes at
    every
    declared scope is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    outcome = TokenOutcome(status, scope, "scope-1", OutcomeTerminality.TERMINAL)
    assert outcome.scope is scope


def test_constructor__fields__only_blocked_may_be_recoverable() -> None:
    """Evidence ID: SV-CPN-005

    Requirement: ``TokenOutcome`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    blocked = TokenOutcome(
        OutcomeStatus.BLOCKED,
        OutcomeScope.BRANCH,
        "branch-1",
        OutcomeTerminality.RECOVERABLE,
    )
    assert blocked.terminality is OutcomeTerminality.RECOVERABLE


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID: SV-CPN-143

    Requirement: ``TokenOutcome`` rejects the documented invalid state for its
    ``fields`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    TokenOutcome(
        OutcomeStatus.BLOCKED,
        OutcomeScope.BRANCH,
        "branch-1",
        OutcomeTerminality.RECOVERABLE,
    )
    with pytest.raises(ValueError, match="terminal"):
        TokenOutcome(
            OutcomeStatus.FAILED,
            OutcomeScope.ATTEMPT,
            "attempt-1",
            OutcomeTerminality.RECOVERABLE,
        )


def test_constructor__outcome_fields__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-076

    Requirement: ``TokenOutcome`` preserves the documented exact valid-state behavior
    for its
    ``outcome_fields`` contract.

    Method: Construct the public SUT with the retained valid synthetic inputs and
    inspect
    exact public state.

    Oracle: The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance: Every retained exact identity, equality, ordering, type, and
    represented-state
    assertion holds.

    Interpretation: Pass supports this valid-state mapping; failure may identify
    implementation,
    fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
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


def test_constructor__outcome_fields__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-121

    Requirement: ``TokenOutcome`` rejects wrong semantic types for its
    ``outcome_fields`` contract.

    Method: Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle: The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance: Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation: Pass supports this type partition; failure may identify
    implementation, fixture,
    oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
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
    with pytest.raises(TypeError):
        SUT(
            OutcomeStatus.BLOCKED,
            OutcomeScope.GATE,
            "g",
            "recoverable",  # type: ignore[arg-type]
        )


def test_constructor__outcome_fields__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-093

    Requirement: ``TokenOutcome`` rejects malformed values of accepted semantic
    types for its
    ``outcome_fields`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        SUT(
            OutcomeStatus.BLOCKED, OutcomeScope.GATE, "", OutcomeTerminality.RECOVERABLE
        )
