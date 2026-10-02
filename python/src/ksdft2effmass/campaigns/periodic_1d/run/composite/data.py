"""Encapsulating DataObject for the retained composite periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...encoded_documents import Periodic1DCompositeEncodedDocuments
from .correlate import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignCorrelator,
)
from .verify import (
    Periodic1DCompositeCampaignVerificationRequest,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaign:
    """Encapsulate one retained composite-band campaign.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and result bytes delegated to campaign operations.
    """

    encoded_documents: Periodic1DCompositeEncodedDocuments

    correlator = Periodic1DCompositeCampaignCorrelator()
    verifier = Periodic1DCompositeCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact composite encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DCompositeEncodedDocuments"
            )

    def correlate(self) -> Periodic1DCompositeCampaignCorrelationResult:
        """Delegate retained-wire binding and validation to the correlator."""
        return self.correlator.execute(
            Periodic1DCompositeCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DCompositeCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for reconstructable numerical diagnostics.

        Returns
        -------
        Periodic1DCompositeCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DCompositeCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
            )
        )
