"""Correlation Actionizer for retained isolated periodic-1D payloads."""

from dataclasses import dataclass

from ...model.retained.isolated import Periodic1DIsolatedBandCampaignModel
from ...workflows import (
    Periodic1DIsolatedBandCampaignWorkflow,
    Periodic1DIsolatedBandCampaignWorkflowRequest,
    Periodic1DIsolatedBandCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignCorrelationRequest:
    """Request typed correlation of one isolated retained-wire model.

    Parameters
    ----------
    model
        Exact version-one isolated input and result payloads.
    """

    model: Periodic1DIsolatedBandCampaignModel

    def __post_init__(self) -> None:
        """Require the exact isolated campaign model type."""
        if type(self.model) is not Periodic1DIsolatedBandCampaignModel:
            raise TypeError("model must be Periodic1DIsolatedBandCampaignModel")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignCorrelationResult:
    """Retain the typed isolated definition, result, and payload identities.

    Parameters
    ----------
    campaign_correlation
        Result of version-one deserialization and input/result correlation.
    """

    campaign_correlation: Periodic1DIsolatedBandCampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact isolated correlation ResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DIsolatedBandCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")


class Periodic1DIsolatedBandCampaignCorrelator:
    """Deserialize and correlate one isolated retained-wire model."""

    __slots__ = ()

    workflow = Periodic1DIsolatedBandCampaignWorkflow()

    def execute(
        self, request: Periodic1DIsolatedBandCampaignCorrelationRequest
    ) -> Periodic1DIsolatedBandCampaignCorrelationResult:
        """Return typed isolated records after complete available correlation."""
        if type(request) is not Periodic1DIsolatedBandCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DIsolatedBandCampaignCorrelationRequest"
            )
        model = request.model
        correlation = self.workflow.execute(
            Periodic1DIsolatedBandCampaignWorkflowRequest(
                model.input_payload,
                model.result_payload,
            )
        )
        return Periodic1DIsolatedBandCampaignCorrelationResult(correlation)
