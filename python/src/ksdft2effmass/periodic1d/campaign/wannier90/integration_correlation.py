"""Typed document-correlation Action for the Wannier90 integration facade.

This module adapts the cohesive integration DataObject to the canonical result-first
campaign Workflow. It adds no schema, numerical method, native-file inference,
provenance claim, or execution authority.
"""

from dataclasses import dataclass

from .correlation import (
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
    Periodic1DWannier90CampaignWorkflowResult,
)
from .encoded_documents import Periodic1DWannier90EncodedDocuments


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationRequest:
    """Bind exact encoded documents to one correlation operation.

    Parameters
    ----------
    encoded_documents
        Immutable composite-input bytes, retained result bytes, and explicit result
        kind.

    Raises
    ------
    TypeError
        If another semantic record is supplied.
    """

    encoded_documents: Periodic1DWannier90EncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DWannier90EncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DWannier90EncodedDocuments"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationCorrelationResult:
    """Retain typed composite/result correlation and exact wire identities.

    Parameters
    ----------
    campaign_correlation
        Result-first authenticated campaign Workflow result.

    Raises
    ------
    TypeError
        If the nested Result has the wrong exact semantic type.

    Notes
    -----
    This wrapper establishes no additional numerical or scientific claim.
    """

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
    """Correlate composite controls with one retained Wannier90 result.

    The Action delegates to the canonical result-first Workflow and retains its typed
    Result unchanged. It does not require native artifacts and makes no numerical,
    convergence, provenance, or scientific-acceptance claim.
    """

    __slots__ = ()

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
        correlation = Periodic1DWannier90CampaignWorkflow().execute(
            Periodic1DWannier90CampaignWorkflowRequest(
                encoded_documents.composite_input_payload,
                encoded_documents.result_payload,
                encoded_documents.result_kind,
            )
        )
        return Periodic1DWannier90IntegrationCorrelationResult(correlation)


__all__ = [
    "Periodic1DWannier90IntegrationCorrelationRequest",
    "Periodic1DWannier90IntegrationCorrelationResult",
    "Periodic1DWannier90IntegrationCorrelator",
]
