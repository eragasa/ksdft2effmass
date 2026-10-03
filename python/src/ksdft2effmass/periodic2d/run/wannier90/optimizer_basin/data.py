"""Encapsulating DataObject for the portable optimizer-basin study."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from .encoded_documents import Periodic2DOptimizerBasinEncodedDocuments
from .verify import (
    Periodic2DOptimizerBasinCampaignVerificationRequest,
    Periodic2DOptimizerBasinCampaignVerificationResult,
    Periodic2DOptimizerBasinCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaign(Periodic2DCampaign):
    """Encapsulate the retained nine-configuration, eight-start study."""

    encoded_documents: Periodic2DOptimizerBasinEncodedDocuments
    verifier = Periodic2DOptimizerBasinCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact optimizer-basin encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DOptimizerBasinEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DOptimizerBasinEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Verify retained outcomes without accessing native external files."""
        return self.verifier.execute(
            Periodic2DOptimizerBasinCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
