"""Encapsulating DataObject for the retained composite periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from ...campaign.base import Periodic2DCampaign
from ...model.retained.composite import Periodic2DCompositeCampaignModel
from .correlate import (
    Periodic2DCompositeCampaignCorrelationRequest,
    Periodic2DCompositeCampaignCorrelationResult,
    Periodic2DCompositeCampaignCorrelator,
)
from .verify import (
    Periodic2DCompositeCampaignVerificationRequest,
    Periodic2DCompositeCampaignVerificationResult,
    Periodic2DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DCompositeCampaign(Periodic2DCampaign):
    """Encapsulate one retained composite campaign model."""

    model: Periodic2DCompositeCampaignModel
    correlator = Periodic2DCompositeCampaignCorrelator()
    verifier = Periodic2DCompositeCampaignVerifier()

    def correlate(self) -> Periodic2DCompositeCampaignCorrelationResult:
        """Correlate the retained composite document."""
        return self.correlator.execute(
            Periodic2DCompositeCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DCompositeCampaignVerificationResult:
        """Independently verify the retained composite document."""
        return self.verifier.execute(
            Periodic2DCompositeCampaignVerificationRequest(self.model, repository_root)
        )
