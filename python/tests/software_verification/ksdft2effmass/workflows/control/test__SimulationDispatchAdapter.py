r"""Software verification of ``SimulationDispatchAdapter``.

Evidence profile: routine

Bounded artifact scope: the public Workflow-owned simulation dispatch adapter.

Facet and represented meaning

This module verifies immediate authorization, exact claim correlation, at-most-once
effect entry, and fail-closed post-invocation uncertainty.

Intrinsic and cross-object scope

Dispatch orchestration belongs to this ActionObject. Persistence CAS, application
calculator adaptation, result ingress, CPN firing, retry, and science remain separate.

VVUQ and scientific exclusions

This is software verification only using a synthetic effect. It performs no external
calculation and establishes no scientific validation, UQ, authority, or acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import (
    ScientificExecutionAuthorityVerificationKind,
    ScientificExecutorIdentity,
    SimulationDispatchAdapter,
    SimulationDispatchAdapterResultKind,
    SimulationExecutionAuthorizer,
)

from .resources.scenarios import (
    ControlScenarioFactory,
    RecordingSimulationDispatchEffect,
    RecordingSimulationDispatchEntryCommitter,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchAdapter


class TestSimulationDispatchAdapter:
    """Own software evidence for the selected dispatch-effect boundary."""

    def test_methods__execute__invokes_exact_authorized_effect_once(self) -> None:
        """Enter the selected effect once after exact claim-phase authorization.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-001

        Requirement: An exact authorized and claimed request invokes the matching
        application effect once and preserves its runtime outcome.

        Acceptance: The result is dispatched, retains the configured outcome, and the
        recording effect observes exactly one call.
        """
        request = ControlScenarioFactory.dispatch_request()
        outcome = ControlScenarioFactory.outcome()
        effect = RecordingSimulationDispatchEffect(
            executor_identity=outcome.executor_identity,
            outcome=outcome,
        )
        result = SUT(
            authorizer=SimulationExecutionAuthorizer(),
            entry_committer=RecordingSimulationDispatchEntryCommitter(),
            effect=effect,
        ).execute(request)
        assert result.kind is SimulationDispatchAdapterResultKind.DISPATCHED
        assert result.outcome is outcome
        assert effect.call_count == 1

    def test_method__execute__repeated_request_does_not_reenter_effect(self) -> None:
        """Require every call to win durable entry before effect invocation.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-005

        Requirement: Repeating the same committed-claim request calls the
        persistence-owned compare-and-swap again and only its first winner enters the
        effect.

        Acceptance: The first call dispatches, the second reports already entered,
        and the effect call count remains exactly one.
        """
        request = ControlScenarioFactory.dispatch_request()
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ScientificExecutorIdentity("executor.one"),
            outcome=ControlScenarioFactory.outcome(),
        )
        adapter = SUT(
            authorizer=SimulationExecutionAuthorizer(),
            entry_committer=RecordingSimulationDispatchEntryCommitter(),
            effect=effect,
        )

        first = adapter.execute(request)
        second = adapter.execute(request)

        assert first.kind is SimulationDispatchAdapterResultKind.DISPATCHED
        assert second.kind is SimulationDispatchAdapterResultKind.ALREADY_ENTERED
        assert second.effect_invoked is False
        assert effect.call_count == 1

    def test_methods__execute__denial_performs_no_effect(self) -> None:
        """Stop before the effect when claim-phase authorization is denied.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-002

        Requirement: A revoked authority snapshot returns denial without entering the
        external effect boundary.

        Acceptance: The result is denied, ``effect_invoked`` is false, and call count
        remains zero.
        """
        request = ControlScenarioFactory.dispatch_request()
        denied_authorization = replace(
            request.claim_authorization_request,
            snapshot=replace(
                request.claim_authorization_request.snapshot,
                revocation_closure=(
                    ScientificExecutionAuthorityVerificationKind.FAILED
                ),
            ),
        )
        denied_request = replace(
            request,
            claim_authorization_request=denied_authorization,
        )
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ScientificExecutorIdentity("executor.one"),
            outcome=ControlScenarioFactory.outcome(),
        )
        result = SUT(
            authorizer=SimulationExecutionAuthorizer(),
            entry_committer=RecordingSimulationDispatchEntryCommitter(),
            effect=effect,
        ).execute(denied_request)
        assert result.kind is SimulationDispatchAdapterResultKind.DENIED
        assert result.effect_invoked is False
        assert effect.call_count == 0

    def test_methods__execute__propagates_exception_after_effect_entry(self) -> None:
        """Never reinterpret an effect exception as a safe rejection.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-003

        Requirement: Unexpected effect exceptions remain exceptions; entering the
        effect supplies no no-effect claim and no automatic redispatch authority.

        Acceptance: ``RuntimeError`` propagates and the recording effect was called
        exactly once.
        """
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ScientificExecutorIdentity("executor.one"),
            outcome=None,
            raises=True,
        )
        adapter = SUT(
            authorizer=SimulationExecutionAuthorizer(),
            entry_committer=RecordingSimulationDispatchEntryCommitter(),
            effect=effect,
        )
        with pytest.raises(RuntimeError):
            adapter.execute(ControlScenarioFactory.dispatch_request())
        assert effect.call_count == 1

    def test_methods__execute__executor_mismatch_performs_no_effect(self) -> None:
        """Reject a mismatched injected executor before entering the effect.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-004

        Requirement: The effect executor identity must equal the authorized request.

        Acceptance: A mismatch returns pre-effect error and leaves call count zero.
        """
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ScientificExecutorIdentity("executor.other"),
            outcome=ControlScenarioFactory.outcome(),
        )
        result = SUT(
            authorizer=SimulationExecutionAuthorizer(),
            entry_committer=RecordingSimulationDispatchEntryCommitter(),
            effect=effect,
        ).execute(ControlScenarioFactory.dispatch_request())
        assert result.kind is SimulationDispatchAdapterResultKind.ERROR
        assert result.effect_invoked is False
        assert effect.call_count == 0
