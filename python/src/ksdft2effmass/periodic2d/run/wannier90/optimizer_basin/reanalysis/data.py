"""Encapsulating DataObject for portable optimizer reanalysis."""

from dataclasses import dataclass
from pathlib import Path

from .....campaign.base import Periodic2DCampaign
from .....model.retained.optimizer_reanalysis import (
    Periodic2DOptimizerReanalysisCampaignModel,
)
from .verify import (
    Periodic2DOptimizerReanalysisCampaignVerificationRequest,
    Periodic2DOptimizerReanalysisCampaignVerificationResult,
    Periodic2DOptimizerReanalysisCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaign(Periodic2DCampaign):
    """Encapsulate retained spread, symmetry, trace, and grid diagnostics."""

    model: Periodic2DOptimizerReanalysisCampaignModel
    verifier = Periodic2DOptimizerReanalysisCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerReanalysisCampaignVerificationResult:
        """Verify retained diagnostics without accessing native execution files."""
        return self.verifier.execute(
            Periodic2DOptimizerReanalysisCampaignVerificationRequest(
                self.model, repository_root
            )
        )
