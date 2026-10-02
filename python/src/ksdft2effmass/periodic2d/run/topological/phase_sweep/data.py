"""Encapsulating DataObject for the retained topological phase sweep."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from .correlate import (
    Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest,
    Periodic2DTopologicalPhaseSweepCampaignCorrelationResult,
    Periodic2DTopologicalPhaseSweepCampaignCorrelator,
)
from .encoded_documents import Periodic2DTopologicalPhaseSweepEncodedDocuments
from .verify import (
    Periodic2DTopologicalPhaseSweepCampaignVerificationRequest,
    Periodic2DTopologicalPhaseSweepCampaignVerificationResult,
    Periodic2DTopologicalPhaseSweepCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaign(Periodic2DCampaign):
    """Encapsulate one retained three-model parameter sweep."""

    encoded_documents: Periodic2DTopologicalPhaseSweepEncodedDocuments
    correlator = Periodic2DTopologicalPhaseSweepCampaignCorrelator()
    verifier = Periodic2DTopologicalPhaseSweepCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact phase-sweep encoded-document type."""
        if (
            type(self.encoded_documents)
            is not Periodic2DTopologicalPhaseSweepEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DTopologicalPhaseSweepEncodedDocuments"
            )

    def correlate(self) -> Periodic2DTopologicalPhaseSweepCampaignCorrelationResult:
        """Correlate retained and maintained sweep documents."""
        return self.correlator.execute(
            Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest(
                self.encoded_documents
            )
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalPhaseSweepCampaignVerificationResult:
        """Independently verify every retained sweep sample."""
        return self.verifier.execute(
            Periodic2DTopologicalPhaseSweepCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
