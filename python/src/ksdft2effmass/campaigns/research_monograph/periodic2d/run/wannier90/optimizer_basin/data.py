"""Encapsulating DataObject for the portable optimizer-basin study."""

from dataclasses import dataclass
from pathlib import Path

from ....model.retained.optimizer_basin import Periodic2DOptimizerBasinCampaignModel
from .verify import (
    Periodic2DOptimizerBasinCampaignVerificationRequest,
    Periodic2DOptimizerBasinCampaignVerificationResult,
    Periodic2DOptimizerBasinCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaign:
    """Encapsulate the retained nine-configuration, eight-start study."""

    model: Periodic2DOptimizerBasinCampaignModel
    verifier = Periodic2DOptimizerBasinCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Verify retained outcomes without accessing native external files."""
        return self.verifier.execute(
            Periodic2DOptimizerBasinCampaignVerificationRequest(
                self.model, repository_root
            )
        )
