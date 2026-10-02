"""Encapsulating DataObject for the portable Wannier90 study."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from ....model.retained.wannier90_study import Periodic2DWannier90StudyCampaignModel
from .verify import (
    Periodic2DWannier90StudyCampaignVerificationRequest,
    Periodic2DWannier90StudyCampaignVerificationResult,
    Periodic2DWannier90StudyCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaign(Periodic2DCampaign):
    """Encapsulate the retained six-case portable study."""

    model: Periodic2DWannier90StudyCampaignModel
    verifier = Periodic2DWannier90StudyCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90StudyCampaignVerificationResult:
        """Verify all portable cases without native external files."""
        return self.verifier.execute(
            Periodic2DWannier90StudyCampaignVerificationRequest(
                self.model, repository_root
            )
        )
