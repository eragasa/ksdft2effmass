"""Encapsulating DataObject for the retained composite periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from ...campaign.base import Periodic2DCampaign
from .correlate import (
    Periodic2DCompositeCampaignCorrelationRequest,
    Periodic2DCompositeCampaignCorrelationResult,
    Periodic2DCompositeCampaignCorrelator,
)
from .encoded_documents import Periodic2DCompositeEncodedDocuments
from .verify import (
    Periodic2DCompositeCampaignVerificationRequest,
    Periodic2DCompositeCampaignVerificationResult,
    Periodic2DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DCompositeCampaign(Periodic2DCampaign):
    """Encapsulate one retained composite campaign document set."""

    encoded_documents: Periodic2DCompositeEncodedDocuments
    correlator = Periodic2DCompositeCampaignCorrelator()
    verifier = Periodic2DCompositeCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact composite encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DCompositeEncodedDocuments"
            )

    def correlate(self) -> Periodic2DCompositeCampaignCorrelationResult:
        """Correlate the retained composite document."""
        return self.correlator.execute(
            Periodic2DCompositeCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DCompositeCampaignVerificationResult:
        """Independently verify the retained composite document."""
        return self.verifier.execute(
            Periodic2DCompositeCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
