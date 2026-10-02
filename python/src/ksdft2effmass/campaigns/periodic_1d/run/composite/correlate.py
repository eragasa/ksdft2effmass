"""Correlation Actionizer for retained composite periodic-1D payloads."""

from dataclasses import dataclass

from ...model.retained.composite import Periodic1DCompositeCampaignModel
from ...wilson_workflows import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignCorrelationRequest:
    """Request typed correlation of one composite retained-wire model.

    Parameters
    ----------
    model
        Exact version-one composite input and result payloads.
    """

    model: Periodic1DCompositeCampaignModel

    def __post_init__(self) -> None:
        """Require the exact composite campaign model type."""
        if type(self.model) is not Periodic1DCompositeCampaignModel:
            raise TypeError("model must be Periodic1DCompositeCampaignModel")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignCorrelationResult:
    """Retain the typed composite definition, result, and payload identities.

    Parameters
    ----------
    campaign_correlation
        Result of version-one deserialization and input/result correlation.
    """

    campaign_correlation: Periodic1DCompositeCampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact composite correlation ResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")


class Periodic1DCompositeCampaignCorrelator:
    """Deserialize and correlate one composite retained-wire model."""

    __slots__ = ()

    workflow = Periodic1DCompositeCampaignWorkflow()

    def execute(
        self, request: Periodic1DCompositeCampaignCorrelationRequest
    ) -> Periodic1DCompositeCampaignCorrelationResult:
        """Return typed composite records after complete available correlation."""
        if type(request) is not Periodic1DCompositeCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DCompositeCampaignCorrelationRequest"
            )
        model = request.model
        correlation = self.workflow.execute(
            Periodic1DCompositeCampaignWorkflowRequest(
                model.input_payload,
                model.result_payload,
            )
        )
        return Periodic1DCompositeCampaignCorrelationResult(correlation)
