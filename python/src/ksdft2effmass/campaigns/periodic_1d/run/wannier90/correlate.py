"""Typed retained-correlation Actionizer for a Wannier90 integration."""

from dataclasses import dataclass

from ...encoded_documents import Periodic1DWannier90EncodedDocuments
from ...wilson_workflows import (
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
    Periodic1DWannier90CampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationRequest:
    """Request binding for one set of Wannier90 encoded documents."""

    encoded_documents: Periodic1DWannier90EncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DWannier90EncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DWannier90EncodedDocuments"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationResult:
    """Retain typed composite/result correlation and exact wire identities."""

    campaign_correlation: Periodic1DWannier90CampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact correlation AbstractResultObject type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DWannier90CampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation uses the wrong AbstractResultObject type"
            )


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
            Immutable encoded documents to bind and validate.

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
        encoded_documents = request.encoded_documents
        correlation = self.workflow.execute(
            Periodic1DWannier90CampaignWorkflowRequest(
                encoded_documents.composite_input_payload,
                encoded_documents.result_payload,
                encoded_documents.result_kind,
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
