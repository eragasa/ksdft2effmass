"""Encapsulating DataObject for the portable standalone optimizer study."""

from dataclasses import dataclass
from pathlib import Path

from .....campaign.base import Periodic2DCampaign
from .encoded_documents import Periodic2DOptimizerStandaloneEncodedDocuments
from .verify import (
    Periodic2DOptimizerStandaloneCampaignVerificationRequest,
    Periodic2DOptimizerStandaloneCampaignVerificationResult,
    Periodic2DOptimizerStandaloneCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaign(Periodic2DCampaign):
    """Encapsulate retained initial, continuation, and basin outcomes."""

    encoded_documents: Periodic2DOptimizerStandaloneEncodedDocuments
    verifier = Periodic2DOptimizerStandaloneCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerStandaloneCampaignVerificationResult:
        """Verify retained outcomes without accessing native execution files."""
        return self.verifier.execute(
            Periodic2DOptimizerStandaloneCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
