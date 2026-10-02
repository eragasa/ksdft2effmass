"""Encapsulating DataObject for the balanced Wannier90 comparison."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from .encoded_documents import Periodic2DWannier90BalancedEncodedDocuments
from .verify import (
    Periodic2DWannier90BalancedCampaignVerificationRequest,
    Periodic2DWannier90BalancedCampaignVerificationResult,
    Periodic2DWannier90BalancedCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedCampaign(Periodic2DCampaign):
    """Encapsulate the retained repository-portable comparison."""

    encoded_documents: Periodic2DWannier90BalancedEncodedDocuments
    verifier = Periodic2DWannier90BalancedCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact balanced encoded-document type."""
        if (
            type(self.encoded_documents)
            is not Periodic2DWannier90BalancedEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic2DWannier90BalancedEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90BalancedCampaignVerificationResult:
        """Verify portable evidence without accessing native external files."""
        return self.verifier.execute(
            Periodic2DWannier90BalancedCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
