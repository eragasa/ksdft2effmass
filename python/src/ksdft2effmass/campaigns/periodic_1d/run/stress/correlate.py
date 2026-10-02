"""Correlation action for periodic-1D reduction-challenge payloads."""

from dataclasses import dataclass

from ...encoded_documents import Periodic1DReductionChallengeEncodedDocuments
from ...workflows import (
    Periodic1DStressCampaignWorkflow,
    Periodic1DStressCampaignWorkflowRequest,
    Periodic1DStressCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignCorrelationRequest:
    """Request typed correlation of reduction-challenge encoded documents.

    Parameters
    ----------
    encoded_documents
        Exact version-one reduction-challenge input and result payloads.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact reduction-challenge document type."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )


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
    """Deserialize, bind, and validate reduction-challenge documents."""

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
        encoded_documents = request.encoded_documents
        correlation = self.workflow.execute(
            Periodic1DStressCampaignWorkflowRequest(
                encoded_documents.input_payload,
                encoded_documents.result_payload,
            )
        )
        return Periodic1DStressCampaignCorrelationResult(correlation)
