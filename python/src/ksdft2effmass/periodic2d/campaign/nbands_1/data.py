"""Encapsulating DataObject for the retained isolated periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from ..base import Periodic2DCampaign
from .correlate import (
    Periodic2DIsolatedBandCampaignCorrelationRequest,
    Periodic2DIsolatedBandCampaignCorrelationResult,
    Periodic2DIsolatedBandCampaignCorrelator,
)
from .encoded_documents import Periodic2DIsolatedBandEncodedDocuments
from .verify import (
    Periodic2DIsolatedBandCampaignVerificationRequest,
    Periodic2DIsolatedBandCampaignVerificationResult,
    Periodic2DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaign(Periodic2DCampaign):
    """Encapsulate one retained isolated-band campaign DataObjectModel."""

    encoded_documents: Periodic2DIsolatedBandEncodedDocuments

    correlator = Periodic2DIsolatedBandCampaignCorrelator()
    verifier = Periodic2DIsolatedBandCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact isolated campaign document type."""
        if type(self.encoded_documents) is not Periodic2DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DIsolatedBandEncodedDocuments"
            )

    def correlate(self) -> Periodic2DIsolatedBandCampaignCorrelationResult:
        """Delegate retained-wire correlation to the correlation Actionizer."""
        return self.correlator.execute(
            Periodic2DIsolatedBandCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DIsolatedBandCampaignVerificationResult:
        """Delegate independent verification through a complete typed request."""
        return self.verifier.execute(
            Periodic2DIsolatedBandCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
