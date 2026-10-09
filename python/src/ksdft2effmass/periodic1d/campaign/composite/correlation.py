"""Correlation action for retained composite periodic-1D payloads."""

from dataclasses import dataclass

from .correlation_workflow import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeCampaignWorkflowResult,
)
from .encoded_documents import Periodic1DCompositeEncodedDocuments


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignCorrelationRequest:
    """Request typed correlation of composite encoded documents.

    Parameters
    ----------
    encoded_documents
        Exact version-one composite input and result payloads.
    """

    encoded_documents: Periodic1DCompositeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact composite encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DCompositeEncodedDocuments"
            )


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
        """Require the exact composite correlation AbstractResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation uses the wrong AbstractResultObject type"
            )


class Periodic1DCompositeCampaignCorrelator:
    """Deserialize and correlate composite encoded documents.

    Notes
    -----
    This Action derives a typed value from one explicit request. It creates a fresh
    correlation Workflow for each invocation and retains no request or result state.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeCampaignCorrelationRequest
    ) -> Periodic1DCompositeCampaignCorrelationResult:
        """Return typed composite records after complete available correlation.

        Parameters
        ----------
        request
            Exact composite encoded-document correlation request.

        Returns
        -------
        Periodic1DCompositeCampaignCorrelationResult
            Typed definition/result correlation and exact source identities.

        Raises
        ------
        TypeError
            If ``request`` or a decoded field has the wrong exact representation.
        ValueError
            If schema, intrinsic values, or cross-document correlations are invalid.
        """
        if type(request) is not Periodic1DCompositeCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DCompositeCampaignCorrelationRequest"
            )
        encoded_documents = request.encoded_documents
        correlation = Periodic1DCompositeCampaignWorkflow().execute(
            Periodic1DCompositeCampaignWorkflowRequest(
                encoded_documents.input_payload,
                encoded_documents.result_payload,
            )
        )
        return Periodic1DCompositeCampaignCorrelationResult(correlation)
