"""Encapsulating DataObject for the portable Wannier90 study."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from .encoded_documents import Periodic2DWannier90StudyEncodedDocuments
from .verify import (
    Periodic2DWannier90StudyCampaignVerificationRequest,
    Periodic2DWannier90StudyCampaignVerificationResult,
    Periodic2DWannier90StudyCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaign(Periodic2DCampaign):
    """Encapsulate the retained six-case portable study."""

    encoded_documents: Periodic2DWannier90StudyEncodedDocuments
    verifier = Periodic2DWannier90StudyCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact study encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DWannier90StudyEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DWannier90StudyEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90StudyCampaignVerificationResult:
        """Verify all portable cases without native external files."""
        return self.verifier.execute(
            Periodic2DWannier90StudyCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
