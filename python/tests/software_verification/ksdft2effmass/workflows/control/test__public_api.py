r"""Software verification of Workflow control-ingress public API.

Evidence profile: routine

Bounded artifact scope: ``ksdft2effmass.workflows.control`` and package-root exports.

Facet and represented meaning

This module verifies the exact architecture-facing authority and dispatch-effect
contract selected by the resolved human decision.

Intrinsic and cross-object scope

Package export agreement belongs here. Individual class behavior belongs to each
class-owned module.

VVUQ and scientific exclusions

This is structural software verification only. Export presence establishes no real
authority, execution, persistence, scientific validation, UQ, or human acceptance.
"""

import pytest

import ksdft2effmass.workflows as api
import ksdft2effmass.workflows.control as control_api

pytestmark = pytest.mark.software_verification


class TestControlIngressPublicApi:
    """Own package-boundary evidence for the control-ingress slice."""

    def test_public_api__package__exports_exact_control_contract(self) -> None:
        """Expose the complete authority and dispatch-effect inventory.

        Evidence ID: SV-WCI-PUBLIC-001

        Requirement: The control package and Workflow root expose exactly the selected
        architecture-facing control names without an application-specific wrapper.

        Acceptance: ``control.__all__`` equals the approved inventory and every name
        resolves to the identical root export.
        """
        expected = [
            "ScientificExecutionAuthorityGrant",
            "ScientificExecutionAuthoritySnapshot",
            "ScientificExecutionAuthorityVerificationKind",
            "ScientificExecutionGrantState",
            "SimulationDispatchAdapter",
            "SimulationDispatchAdapterResult",
            "SimulationDispatchAdapterResultKind",
            "SimulationDispatchClaimOutcomeKind",
            "SimulationDispatchClaimPreparer",
            "SimulationDispatchClaimRequest",
            "SimulationDispatchClaimResult",
            "SimulationDispatchEffect",
            "SimulationDispatchEffectRequest",
            "SimulationDispatchEntryCommitter",
            "SimulationDispatchEntryOutcomeKind",
            "SimulationDispatchEntryResult",
            "SimulationDispatchOutcome",
            "SimulationDispatchPreparationOutcomeKind",
            "SimulationDispatchPreparationRequest",
            "SimulationDispatchPreparationResult",
            "SimulationDispatchPreparer",
            "SimulationDispatchReconciler",
            "SimulationDispatchReconciliationOutcomeKind",
            "SimulationDispatchReconciliationRequest",
            "SimulationDispatchReconciliationResult",
            "SimulationDispatchRequest",
            "SimulationDispatchResultIngressOutcomeKind",
            "SimulationDispatchResultIngressPreparer",
            "SimulationDispatchResultIngressRequest",
            "SimulationDispatchResultIngressResult",
            "SimulationExecutionAuthorizationOutcomeKind",
            "SimulationExecutionAuthorizationPhase",
            "SimulationExecutionAuthorizationRequest",
            "SimulationExecutionAuthorizationResult",
            "SimulationExecutionAuthorizer",
            "SimulationExecutionRequest",
            "WorkflowRunDispatchEntryCommitter",
        ]
        assert control_api.__all__ == expected
        for name in expected:
            assert getattr(api, name) is getattr(control_api, name)
