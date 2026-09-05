r"""Software verification of dispatch-obligation correlation agreement.

Evidence profile: routine

Bounded artifact scope: simulation request correlation and immutable dispatch-obligation
records.

Facet and represented meaning

The artifact verifies that request correlation and pending dispatch state name one
obligation while retaining canonical resource scope.

Intrinsic and cross-object scope

The participating records retain their intrinsic class-owned modules; this artifact
owns only their cross-record agreement.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ObligationIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchObligation,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestCorrelation,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification


class TestDispatchObligationCorrelation:
    """Own cross-record agreement evidence."""

    def test_constructor__dispatch_obligation__retains_effect_free_scope(self) -> None:
        """Retain exact request and resource scope without dispatch behavior.

        Evidence ID: SV-WFR-CONTROL-003

        Requirement: A dispatch obligation is immutable pending-work state with one
        exact destination, canonical resource identities, and creation idempotency.

        Acceptance: Canonically ordered scopes construct and reversed scopes raise
        ``ValueError``.
        """
        correlation = self.make_request_correlation()
        obligation = self.make_obligation()

        assert correlation.obligation_identity == obligation.identity
        assert obligation.resource_scope_identities == (
            DispatchResourceScopeIdentity("resource.cpu"),
            DispatchResourceScopeIdentity("resource.memory"),
        )
        with pytest.raises(ValueError):
            replace(
                obligation,
                resource_scope_identities=tuple(
                    reversed(obligation.resource_scope_identities)
                ),
            )

    @staticmethod
    def make_request_correlation() -> SimulationExecutionRequestCorrelation:
        """Construct one exact request-to-WorkflowRun correlation."""
        return SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity("correlation.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.one")
            ),
            input_result_reference_identities=(),
        )

    @staticmethod
    def make_obligation() -> SimulationDispatchObligation:
        """Construct one immutable synthetic dispatch obligation."""
        return SimulationDispatchObligation(
            identity=ObligationIdentity("obligation.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            destination_identity=DispatchDestinationIdentity("destination.one"),
            resource_scope_identities=(
                DispatchResourceScopeIdentity("resource.cpu"),
                DispatchResourceScopeIdentity("resource.memory"),
            ),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )
