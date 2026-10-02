"""Encapsulating DataObject for the retained adversarial periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...encoded_documents import Periodic1DReductionChallengeEncodedDocuments
from .correlate import (
    Periodic1DStressCampaignCorrelationRequest,
    Periodic1DStressCampaignCorrelationResult,
    Periodic1DStressCampaignCorrelator,
)
from .verify import (
    Periodic1DStressCampaignVerificationRequest,
    Periodic1DStressCampaignVerificationResult,
    Periodic1DStressCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaign:
    """Encapsulate one retained adversarial stress campaign.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and result bytes delegated to campaign operations.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments

    correlator = Periodic1DStressCampaignCorrelator()
    verifier = Periodic1DStressCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact reduction-challenge document type."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )

    def correlate(self) -> Periodic1DStressCampaignCorrelationResult:
        """Delegate retained-wire binding and validation to the correlator."""
        return self.correlator.execute(
            Periodic1DStressCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DStressCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance applied to each reconstructed stress channel.

        Returns
        -------
        Periodic1DStressCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DStressCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
            )
        )
