"""Encapsulating DataObject for the retained topological benchmark."""

from dataclasses import dataclass
from pathlib import Path

from ...campaign.base import Periodic2DCampaign
from .correlate import (
    Periodic2DTopologicalCampaignCorrelationRequest,
    Periodic2DTopologicalCampaignCorrelationResult,
    Periodic2DTopologicalCampaignCorrelator,
)
from .encoded_documents import Periodic2DTopologicalEncodedDocuments
from .verify import (
    Periodic2DTopologicalCampaignVerificationRequest,
    Periodic2DTopologicalCampaignVerificationResult,
    Periodic2DTopologicalCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalCampaign(Periodic2DCampaign):
    """Encapsulate one retained three-model benchmark."""

    encoded_documents: Periodic2DTopologicalEncodedDocuments
    correlator = Periodic2DTopologicalCampaignCorrelator()
    verifier = Periodic2DTopologicalCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact topological encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DTopologicalEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DTopologicalEncodedDocuments"
            )

    def correlate(self) -> Periodic2DTopologicalCampaignCorrelationResult:
        """Correlate the retained document with the maintained route."""
        return self.correlator.execute(
            Periodic2DTopologicalCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalCampaignVerificationResult:
        """Independently verify all retained model families."""
        return self.verifier.execute(
            Periodic2DTopologicalCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
