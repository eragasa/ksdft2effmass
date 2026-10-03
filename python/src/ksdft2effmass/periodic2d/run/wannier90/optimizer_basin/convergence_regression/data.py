"""Encapsulating DataObject for portable censored convergence regression."""

from dataclasses import dataclass
from pathlib import Path

from .....campaign.base import Periodic2DCampaign
from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments
from .verify import (
    Periodic2DOptimizerRegressionCampaignVerificationRequest,
    Periodic2DOptimizerRegressionCampaignVerificationResult,
    Periodic2DOptimizerRegressionCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaign(Periodic2DCampaign):
    """Encapsulate the retained right-censored log-normal regression."""

    encoded_documents: Periodic2DOptimizerRegressionEncodedDocuments
    verifier = Periodic2DOptimizerRegressionCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerRegressionCampaignVerificationResult:
        """Independently reconstruct retained estimates and diagnostics."""
        return self.verifier.execute(
            Periodic2DOptimizerRegressionCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
