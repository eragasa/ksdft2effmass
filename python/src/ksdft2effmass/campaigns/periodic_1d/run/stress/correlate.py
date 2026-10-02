"""Correlation Actionizer for retained adversarial periodic-1D payloads."""

from dataclasses import dataclass

from ...model.retained.stress import Periodic1DStressCampaignModel
from ...workflows import (
    Periodic1DStressCampaignWorkflow,
    Periodic1DStressCampaignWorkflowRequest,
    Periodic1DStressCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignCorrelationRequest:
    """Request typed correlation of one stress retained-wire model.

    Parameters
    ----------
    model
        Exact version-one stress input and result payloads.
    """

    model: Periodic1DStressCampaignModel

    def __post_init__(self) -> None:
        """Require the exact stress campaign model type."""
        if type(self.model) is not Periodic1DStressCampaignModel:
            raise TypeError("model must be Periodic1DStressCampaignModel")


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignCorrelationResult:
    """Retain the typed stress definition, result, and payload identities.

    Parameters
    ----------
    campaign_correlation
        Result of version-one deserialization and input/result correlation.
    """

    campaign_correlation: Periodic1DStressCampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact stress correlation ResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DStressCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")


class Periodic1DStressCampaignCorrelator:
    """Deserialize and correlate one stress retained-wire model."""

    __slots__ = ()

    workflow = Periodic1DStressCampaignWorkflow()

    def execute(
        self, request: Periodic1DStressCampaignCorrelationRequest
    ) -> Periodic1DStressCampaignCorrelationResult:
        """Return typed stress records after complete available correlation."""
        if type(request) is not Periodic1DStressCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DStressCampaignCorrelationRequest"
            )
        model = request.model
        correlation = self.workflow.execute(
            Periodic1DStressCampaignWorkflowRequest(
                model.input_payload,
                model.result_payload,
            )
        )
        return Periodic1DStressCampaignCorrelationResult(correlation)
