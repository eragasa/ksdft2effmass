"""Correlation action for retained isolated periodic-1D payloads."""

from dataclasses import dataclass

from ...encoded_documents import Periodic1DIsolatedBandEncodedDocuments
from ...workflows import (
    Periodic1DIsolatedBandCampaignWorkflow,
    Periodic1DIsolatedBandCampaignWorkflowRequest,
    Periodic1DIsolatedBandCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignCorrelationRequest:
    """Request typed correlation of isolated encoded documents.

    Parameters
    ----------
    encoded_documents
        Exact version-one isolated input and result payloads.
    """

    encoded_documents: Periodic1DIsolatedBandEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact isolated encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DIsolatedBandEncodedDocuments"
            )


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
    """Deserialize and correlate isolated encoded documents."""

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
        encoded_documents = request.encoded_documents
        correlation = self.workflow.execute(
            Periodic1DIsolatedBandCampaignWorkflowRequest(
                encoded_documents.input_payload,
                encoded_documents.result_payload,
            )
        )
        return Periodic1DIsolatedBandCampaignCorrelationResult(correlation)
