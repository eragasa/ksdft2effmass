r"""Software verification of ``DispatchObservationRecord``.

Evidence profile: routine

Bounded artifact scope: the public append-only dispatch observation DataObject.

Facet and represented meaning

This module verifies the nonterminal indeterminate observation variant.

Intrinsic and cross-object scope

Aggregate lifecycle and final-outcome correlation remain with replay evidence.

VVUQ and scientific exclusions

This is software verification of append-only observation structure only. It establishes
no persistence, external execution, scientific validation, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import WorkflowRunIdentity
from ksdft2effmass.workflows.runs import (
    DispatchObservationKind,
    DispatchObservationRecord,
    DispatchObservationRecordIdentity,
    ObligationIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionRequestIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = DispatchObservationRecord


class TestDispatchObservationRecord:
    """Own software evidence for append-only dispatch observations."""

    @staticmethod
    def observation() -> DispatchObservationRecord:
        """Construct synthetic no-observation indeterminate evidence."""
        return SUT(
            identity=DispatchObservationRecordIdentity("observation-record.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            dispatch_entry_identity=SimulationDispatchEntryIdentity("entry.one"),
            dispatch_entry_receipt_identity=SimulationDispatchEntryReceiptIdentity(
                "entry-receipt.one"
            ),
            outcome_identity=SimulationDispatchOutcomeIdentity("outcome.one"),
            kind=DispatchObservationKind.INDETERMINATE,
            observed_outcomes=(),
            reconciliation_identity_values=("read.one",),
        )

    def test_constructor__indeterminate__retains_nonterminal_observation(self) -> None:
        """Permit empty indeterminate evidence and reject terminal reclassification.

        Evidence ID: SV-WFR-DISPATCH-OBSERVATION-RECORD-001
        """
        observation = self.observation()
        assert observation.observed_outcomes == ()
        with pytest.raises(ValueError):
            replace(observation, kind=DispatchObservationKind.CONFIRMED)
