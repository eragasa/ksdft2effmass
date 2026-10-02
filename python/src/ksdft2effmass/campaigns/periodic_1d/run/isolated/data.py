"""Encapsulating DataObject for the retained isolated periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...encoded_documents import Periodic1DIsolatedBandEncodedDocuments
from .correlate import (
    Periodic1DIsolatedBandCampaignCorrelationRequest,
    Periodic1DIsolatedBandCampaignCorrelationResult,
    Periodic1DIsolatedBandCampaignCorrelator,
)
from .verify import (
    Periodic1DIsolatedBandCampaignVerificationRequest,
    Periodic1DIsolatedBandCampaignVerificationResult,
    Periodic1DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaign:
    """Encapsulate one retained isolated-band campaign.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and result bytes delegated to campaign operations.
    """

    encoded_documents: Periodic1DIsolatedBandEncodedDocuments

    correlator = Periodic1DIsolatedBandCampaignCorrelator()
    verifier = Periodic1DIsolatedBandCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact isolated encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DIsolatedBandEncodedDocuments"
            )

    def correlate(self) -> Periodic1DIsolatedBandCampaignCorrelationResult:
        """Delegate retained-wire binding and validation to the correlator."""
        return self.correlator.execute(
            Periodic1DIsolatedBandCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self,
        *,
        absolute_tolerance: ScalarQuantity,
        curvature_absolute_tolerance: ScalarQuantity,
    ) -> Periodic1DIsolatedBandCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for ordinary reconstruction diagnostics.
        curvature_absolute_tolerance
            Separate inclusive unitless tolerance for zone-center curvature.

        Returns
        -------
        Periodic1DIsolatedBandCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DIsolatedBandCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
                curvature_absolute_tolerance,
            )
        )
