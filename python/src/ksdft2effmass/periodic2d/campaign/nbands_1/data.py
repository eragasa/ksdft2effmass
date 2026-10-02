"""Encapsulating DataObject for the retained isolated periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from ..base import Periodic2DCampaign
from .correlate import (
    Periodic2DIsolatedBandCampaignCorrelationRequest,
    Periodic2DIsolatedBandCampaignCorrelationResult,
    Periodic2DIsolatedBandCampaignCorrelator,
)
from .retained import Periodic2DIsolatedBandCampaignModel
from .verify import (
    Periodic2DIsolatedBandCampaignVerificationRequest,
    Periodic2DIsolatedBandCampaignVerificationResult,
    Periodic2DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaign(Periodic2DCampaign):
    """Encapsulate one retained isolated-band campaign DataObjectModel."""

    model: Periodic2DIsolatedBandCampaignModel

    correlator = Periodic2DIsolatedBandCampaignCorrelator()
    verifier = Periodic2DIsolatedBandCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact isolated campaign model type."""
        if type(self.model) is not Periodic2DIsolatedBandCampaignModel:
            raise TypeError("model must be Periodic2DIsolatedBandCampaignModel")

    def correlate(self) -> Periodic2DIsolatedBandCampaignCorrelationResult:
        """Delegate retained-wire correlation to the correlation Actionizer."""
        return self.correlator.execute(
            Periodic2DIsolatedBandCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DIsolatedBandCampaignVerificationResult:
        """Delegate independent verification through a complete typed request."""
        return self.verifier.execute(
            Periodic2DIsolatedBandCampaignVerificationRequest(
                self.model, repository_root
            )
        )
