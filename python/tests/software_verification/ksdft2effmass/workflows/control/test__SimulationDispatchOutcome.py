r"""Software verification of ``SimulationDispatchOutcome``.

Evidence profile: routine

Bounded artifact scope: the public runtime specialized dispatch outcome.

Facet and represented meaning

This module verifies exact dispatch correlations and closed confirmed, rejected, and
indeterminate payloads.

Intrinsic and cross-object scope

Runtime-envelope invariants belong here; durable aggregate admission belongs to later
ingress and persistence owners.

VVUQ and scientific exclusions

This is software verification only. Synthetic outcomes are not calculated physical
results and establish no scientific validation, UQ, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    DispatchOutcomeKind,
    SimulationDispatchOutcome,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchOutcome


class TestSimulationDispatchOutcome:
    """Own software evidence for runtime dispatch outcomes."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose exact dispatch, result, manifest, failure, and reconciliation state.

        Evidence ID: SV-WCI-DISPATCH-OUTCOME-001

        Requirement: The outcome declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "observation_identity",
            "request_identity",
            "workflow_run_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "executor_identity",
            "obligation_identity",
            "grant_identity",
            "kind",
            "result",
            "native_output_manifest_identity",
            "native_output_manifest_entry_identities",
            "failure",
            "reconciliation_identity_values",
        )

    def test_constructor__variants__separate_result_failure_and_uncertainty(
        self,
    ) -> None:
        """Keep result, failure, and reconciliation payloads mutually exclusive.

        Evidence ID: SV-WCI-DISPATCH-OUTCOME-002

        Requirement: Confirmed alone carries a result and manifest, rejected alone a
        failure, and indeterminate alone reconciliation identities.

        Acceptance: All three exact variants construct and removing the confirmed
        manifest raises ``ValueError``.
        """
        confirmed = ControlScenarioFactory.outcome(kind=DispatchOutcomeKind.CONFIRMED)
        rejected = ControlScenarioFactory.outcome(kind=DispatchOutcomeKind.REJECTED)
        indeterminate = ControlScenarioFactory.outcome(
            kind=DispatchOutcomeKind.INDETERMINATE
        )
        assert confirmed.result is not None
        assert rejected.failure is not None
        assert indeterminate.reconciliation_identity_values == ("observation.one",)
        with pytest.raises(ValueError):
            replace(confirmed, native_output_manifest_identity=None)
