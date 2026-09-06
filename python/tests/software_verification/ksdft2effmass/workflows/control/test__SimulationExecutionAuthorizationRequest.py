r"""Software verification of ``SimulationExecutionAuthorizationRequest``.

Evidence profile: routine

Bounded artifact scope: the public simulation authorization-request DataObject.

Facet and represented meaning

This module verifies the exact authority, operation, resource, input, and time scope.

Intrinsic and cross-object scope

Request field types and ordering belong here; grant compatibility belongs to the
authorizer.

VVUQ and scientific exclusions

This is software verification only. It performs no authorization or execution and
establishes no scientific validation, UQ, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    DispatchResourceScopeIdentity,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionAuthorizationRequest


class TestSimulationExecutionAuthorizationRequest:
    """Own software evidence for an exact authorization request."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose every operation and authority correlation.

        Evidence ID: SV-WCI-AUTHORIZATION-REQUEST-001

        Requirement: The request declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "result_identity",
            "phase",
            "grant",
            "snapshot",
            "request_identity",
            "workflow_run_identity",
            "task_definition_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "executor_identity",
            "destination_identity",
            "obligation_identity",
            "resource_scope_identities",
            "input_result_reference_identities",
            "input_artifact_entry_identities",
            "evaluated_at",
        )

    def test_constructor__resource_scope__requires_canonical_order(self) -> None:
        """Reject a noncanonical externally authorized resource scope.

        Evidence ID: SV-WCI-AUTHORIZATION-REQUEST-002

        Requirement: Resource scopes are unique and lexically sorted.

        Acceptance: Reversing a two-member scope raises ``ValueError``.
        """
        request = ControlScenarioFactory.authorization_request(
            phase=SimulationExecutionAuthorizationPhase.PREPARATION,
            state=ScientificExecutionGrantState.UNUSED,
            result_identity="authorization.prepare",
        )
        with pytest.raises(ValueError):
            replace(
                request,
                resource_scope_identities=(
                    DispatchResourceScopeIdentity("resource.z"),
                    DispatchResourceScopeIdentity("resource.a"),
                ),
            )
