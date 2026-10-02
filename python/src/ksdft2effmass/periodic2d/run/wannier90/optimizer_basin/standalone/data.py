"""Encapsulating DataObject for the portable standalone optimizer study."""

from dataclasses import dataclass
from pathlib import Path

from .....campaign.base import Periodic2DCampaign
from .....model.retained.optimizer_standalone import (
    Periodic2DOptimizerStandaloneCampaignModel,
)
from .verify import (
    Periodic2DOptimizerStandaloneCampaignVerificationRequest,
    Periodic2DOptimizerStandaloneCampaignVerificationResult,
    Periodic2DOptimizerStandaloneCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaign(Periodic2DCampaign):
    """Encapsulate retained initial, continuation, and basin outcomes."""

    model: Periodic2DOptimizerStandaloneCampaignModel
    verifier = Periodic2DOptimizerStandaloneCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerStandaloneCampaignVerificationResult:
        """Verify retained outcomes without accessing native execution files."""
        return self.verifier.execute(
            Periodic2DOptimizerStandaloneCampaignVerificationRequest(
                self.model, repository_root
            )
        )
