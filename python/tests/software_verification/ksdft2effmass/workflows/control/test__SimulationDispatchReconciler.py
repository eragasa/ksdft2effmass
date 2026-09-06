r"""Software verification of ``SimulationDispatchReconciler``.

Evidence profile: routine

Bounded artifact scope: the public effect-free dispatch reconciler ActionObject.

Facet and represented meaning

This module verifies duplicate, absent, conflicting, and uncorrelated observation
semantics without redispatch.

Intrinsic and cross-object scope

Observation comparison and closed reconciliation belong here. External reads,
persistence, result ingress, retry, and calculation remain excluded.

VVUQ and scientific exclusions

This is software verification only using synthetic observations. It establishes no
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import (
    DispatchObservationRecordIdentity,
    DispatchOutcomeKind,
    ScientificExecutorIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationDispatchReconciler,
    SimulationDispatchReconciliationOutcomeKind,
    SimulationDispatchReconciliationRequest,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchReconciler


class TestSimulationDispatchReconciler:
    """Own software evidence for deterministic dispatch reconciliation."""

    def test_methods__execute__treats_exact_duplicates_as_idempotent(self) -> None:
        """Return one established outcome for repeated equal observations.

        Evidence ID: SV-WCI-RECONCILER-001

        Requirement: Exact duplicate observations are idempotent and never cause
        another dispatch.

        Acceptance: Two equal confirmed observations return the first exact outcome as
        confirmed while retaining both observed identities.
        """
        outcome = ControlScenarioFactory.outcome()
        request = SimulationDispatchReconciliationRequest(
            dispatch_request=ControlScenarioFactory.dispatch_request(),
            dispatch_entry_receipt=ControlScenarioFactory.dispatch_entry_receipt(
                ControlScenarioFactory.dispatch_request()
            ),
            observation_record_identity=DispatchObservationRecordIdentity(
                "observation-record.duplicate"
            ),
            observations=(outcome, outcome),
            reconciliation_identity_values=("read.one", "read.two"),
        )
        result = SUT.execute(request)
        assert result.kind is SimulationDispatchReconciliationOutcomeKind.CONFIRMED
        assert result.outcome is outcome
        assert result.observed_outcome_identities == (
            outcome.observation_identity,
            outcome.observation_identity,
        )

    def test_methods__execute__keeps_absence_indeterminate(self) -> None:
        """Construct no result or failure when completion cannot be observed.

        Evidence ID: SV-WCI-RECONCILER-002

        Requirement: Absence of a dispatch observation is indeterminate and never
        authorizes redispatch.

        Acceptance: No observations returns an indeterminate outcome carrying only the
        supplied reconciliation identities.
        """
        request = SimulationDispatchReconciliationRequest(
            dispatch_request=ControlScenarioFactory.dispatch_request(),
            dispatch_entry_receipt=ControlScenarioFactory.dispatch_entry_receipt(
                ControlScenarioFactory.dispatch_request()
            ),
            observation_record_identity=DispatchObservationRecordIdentity(
                "observation-record.absent"
            ),
            observations=(),
            reconciliation_identity_values=("read.one",),
        )
        result = SUT.execute(request)
        assert result.kind is SimulationDispatchReconciliationOutcomeKind.INDETERMINATE
        assert result.outcome is None
        assert result.observation_record.kind.value == "indeterminate"
        assert result.observation_record.observed_outcomes == ()

    def test_methods__execute__does_not_select_between_conflicts(self) -> None:
        """Return conflict for unequal observations of the same request.

        Evidence ID: SV-WCI-RECONCILER-003

        Requirement: Distinct correlated outcomes never select a winner.

        Acceptance: Confirmed and rejected observations return conflict with no
        reconciled outcome.
        """
        confirmed = ControlScenarioFactory.outcome(kind=DispatchOutcomeKind.CONFIRMED)
        rejected = ControlScenarioFactory.outcome(kind=DispatchOutcomeKind.REJECTED)
        request = SimulationDispatchReconciliationRequest(
            dispatch_request=ControlScenarioFactory.dispatch_request(),
            dispatch_entry_receipt=ControlScenarioFactory.dispatch_entry_receipt(
                ControlScenarioFactory.dispatch_request()
            ),
            observation_record_identity=DispatchObservationRecordIdentity(
                "observation-record.conflict"
            ),
            observations=(confirmed, rejected),
            reconciliation_identity_values=("read.one", "read.two"),
        )
        result = SUT.execute(request)
        assert result.kind is SimulationDispatchReconciliationOutcomeKind.CONFLICT
        assert result.outcome is None

        reused_identity = replace(
            rejected,
            observation_identity=confirmed.observation_identity,
        )
        collision = SUT.execute(
            replace(
                request,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "observation-record.identity-collision"
                ),
                observations=(confirmed, reused_identity),
            )
        )
        assert collision.kind is SimulationDispatchReconciliationOutcomeKind.ERROR
        assert collision.outcome is None

    def test_methods__execute__rejects_uncorrelated_observation(self) -> None:
        """Fail closed when an observation names another executor.

        Evidence ID: SV-WCI-RECONCILER-004

        Requirement: Every observed outcome closes over the exact claimed request.

        Acceptance: An executor mismatch returns error with no reconciled outcome.
        """
        mismatch = replace(
            ControlScenarioFactory.outcome(),
            executor_identity=ScientificExecutorIdentity("executor.other"),
        )
        request = SimulationDispatchReconciliationRequest(
            dispatch_request=ControlScenarioFactory.dispatch_request(),
            dispatch_entry_receipt=ControlScenarioFactory.dispatch_entry_receipt(
                ControlScenarioFactory.dispatch_request()
            ),
            observation_record_identity=DispatchObservationRecordIdentity(
                "observation-record.error"
            ),
            observations=(mismatch,),
            reconciliation_identity_values=("read.one",),
        )
        result = SUT.execute(request)
        assert result.kind is SimulationDispatchReconciliationOutcomeKind.ERROR
        assert result.outcome is None

        outcome_identity_mismatch = replace(
            mismatch,
            identity=SimulationDispatchOutcomeIdentity("outcome.other"),
        )
        identity_result = SUT.execute(
            replace(
                request,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "observation-record.outcome-identity-error"
                ),
                observations=(outcome_identity_mismatch,),
            )
        )
        assert identity_result.kind is (
            SimulationDispatchReconciliationOutcomeKind.ERROR
        )
        assert identity_result.outcome is None
