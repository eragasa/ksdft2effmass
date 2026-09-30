"""Typed retained-correlation Actionizer for a Wannier90 integration."""

from dataclasses import dataclass

from ...model.integrations import Periodic1DWannier90IntegrationModel
from ...wilson_workflows import (
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
    Periodic1DWannier90CampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationRequest:
    """Request retained correlation for one integration model."""

    model: Periodic1DWannier90IntegrationModel

    def __post_init__(self) -> None:
        """Require the exact integration model type."""
        if type(self.model) is not Periodic1DWannier90IntegrationModel:
            raise TypeError("model must be Periodic1DWannier90IntegrationModel")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationResult:
    """Retain typed composite/result correlation and exact wire identities."""

    campaign_correlation: Periodic1DWannier90CampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact correlation ResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DWannier90CampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")


class Periodic1DWannier90IntegrationCorrelator:
    """Correlate composite controls with a retained Wannier90 result."""

    __slots__ = ()

    workflow = Periodic1DWannier90CampaignWorkflow()

    def execute(
        self, request: Periodic1DWannier90IntegrationCorrelationRequest
    ) -> Periodic1DWannier90IntegrationCorrelationResult:
        """Return typed retained records without making a numerical claim.

        Parameters
        ----------
        request
            Immutable integration model to correlate.

        Returns
        -------
        Periodic1DWannier90IntegrationCorrelationResult
            Correlated composite controls, retained result, and wire identities.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If retained schemas, identities, or band-group inventories disagree.
        """
        if type(request) is not Periodic1DWannier90IntegrationCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DWannier90IntegrationCorrelationRequest"
            )
        model = request.model
        correlation = self.workflow.execute(
            Periodic1DWannier90CampaignWorkflowRequest(
                model.composite_input_payload,
                model.result_payload,
                model.result_kind,
            )
        )
        return Periodic1DWannier90IntegrationCorrelationResult(correlation)


__all__ = [
    "Periodic1DWannier90CampaignWorkflow",
    "Periodic1DWannier90CampaignWorkflowRequest",
    "Periodic1DWannier90CampaignWorkflowResult",
    "Periodic1DWannier90IntegrationCorrelationRequest",
    "Periodic1DWannier90IntegrationCorrelationResult",
    "Periodic1DWannier90IntegrationCorrelator",
]
