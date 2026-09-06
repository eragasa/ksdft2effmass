r"""Software verification of ``SimulationDispatchReconciliationResult``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-reconciliation ResultObject.

Facet and represented meaning

This module verifies exact request, observation, outcome, and diagnostic variants.

Intrinsic and cross-object scope

Result discrimination belongs here; production from observations belongs to the
reconciler.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, scientific
validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    DispatchObservationRecordIdentity,
    SimulationDispatchReconciler,
    SimulationDispatchReconciliationOutcomeKind,
    SimulationDispatchReconciliationRequest,
    SimulationDispatchReconciliationResult,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchReconciliationResult


class TestSimulationDispatchReconciliationResult:
    """Own software evidence for closed reconciliation results."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose result kind, request, outcome, observations, and diagnostics.

        Evidence ID: SV-WCI-RECONCILIATION-RESULT-001

        Requirement: The result declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "kind",
            "request",
            "outcome",
            "observation_record",
            "observed_outcome_identities",
            "diagnostics",
        )

    def test_constructor__confirmed__requires_matching_outcome(self) -> None:
        """Prohibit a confirmed reconciliation without a confirmed envelope.

        Evidence ID: SV-WCI-RECONCILIATION-RESULT-002

        Requirement: Established result kinds carry an outcome of the same kind.

        Acceptance: The exact confirmed variant constructs and removing its outcome
        raises ``ValueError``.
        """
        outcome = ControlScenarioFactory.outcome()
        dispatch = ControlScenarioFactory.dispatch_request()
        request = SimulationDispatchReconciliationRequest(
            dispatch_request=dispatch,
            dispatch_entry_receipt=(
                ControlScenarioFactory.dispatch_entry_receipt(dispatch)
            ),
            observation_record_identity=DispatchObservationRecordIdentity(
                "observation-record.confirmed"
            ),
            observations=(outcome,),
            reconciliation_identity_values=("read.one",),
        )
        reconciled = SimulationDispatchReconciler.execute(request)
        result = SUT(
            kind=SimulationDispatchReconciliationOutcomeKind.CONFIRMED,
            request=request,
            outcome=outcome,
            observation_record=reconciled.observation_record,
            observed_outcome_identities=(outcome.observation_identity,),
            diagnostics=(),
        )
        with pytest.raises(ValueError):
            replace(result, outcome=None)
