"""Correlation Action for retained reduction-challenge payloads."""

from dataclasses import dataclass

from .correlation_workflow import (
    Periodic1DReductionChallengeCampaignWorkflow,
    Periodic1DReductionChallengeCampaignWorkflowRequest,
    Periodic1DReductionChallengeCampaignWorkflowResult,
)
from .encoded_documents import Periodic1DReductionChallengeEncodedDocuments


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignCorrelationRequest:
    """Request typed correlation of exact challenge documents.

    Parameters
    ----------
    encoded_documents
        Exact historical schema-one input and result payloads.

    Raises
    ------
    TypeError
        If ``encoded_documents`` has the wrong exact semantic type.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact reduction-challenge document owner."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignCorrelationResult:
    """Retain typed challenge records and exact payload identities.

    Parameters
    ----------
    campaign_correlation
        Result of strict deserialization, input authentication, and cross-document
        correlation.
    """

    campaign_correlation: Periodic1DReductionChallengeCampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact correlation Result type."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DReductionChallengeCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation must be "
                "Periodic1DReductionChallengeCampaignWorkflowResult"
            )


class Periodic1DReductionChallengeCampaignCorrelator:
    """Deserialize, authenticate, and correlate exact challenge documents.

    Notes
    -----
    This stateless Action creates a fresh Workflow for each request. Correlation makes
    no numerical-reconstruction, convergence, validation, UQ, or acceptance claim.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DReductionChallengeCampaignCorrelationRequest
    ) -> Periodic1DReductionChallengeCampaignCorrelationResult:
        """Return typed challenge records after complete available correlation.

        Parameters
        ----------
        request
            Exact encoded-document correlation request.

        Returns
        -------
        Periodic1DReductionChallengeCampaignCorrelationResult
            Typed correlation and exact source identities.

        Raises
        ------
        TypeError
            If ``request`` or a decoded field has the wrong exact representation.
        ValueError
            If strict wire structure, intrinsic values, or correlations are invalid.
        OverflowError
            If a retained diagnostic is not finite binary64.
        """
        if type(request) is not Periodic1DReductionChallengeCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic1DReductionChallengeCampaignCorrelationRequest"
            )
        documents = request.encoded_documents
        correlation = Periodic1DReductionChallengeCampaignWorkflow().execute(
            Periodic1DReductionChallengeCampaignWorkflowRequest(
                documents.input_payload,
                documents.result_payload,
            )
        )
        return Periodic1DReductionChallengeCampaignCorrelationResult(correlation)
