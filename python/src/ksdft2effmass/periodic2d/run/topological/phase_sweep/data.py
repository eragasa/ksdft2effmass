"""Encapsulating DataObject for the retained topological phase sweep."""

from dataclasses import dataclass
from pathlib import Path

from ....campaign.base import Periodic2DCampaign
from ....model.retained.topological_phase_sweep import (
    Periodic2DTopologicalPhaseSweepCampaignModel,
)
from .correlate import (
    Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest,
    Periodic2DTopologicalPhaseSweepCampaignCorrelationResult,
    Periodic2DTopologicalPhaseSweepCampaignCorrelator,
)
from .verify import (
    Periodic2DTopologicalPhaseSweepCampaignVerificationRequest,
    Periodic2DTopologicalPhaseSweepCampaignVerificationResult,
    Periodic2DTopologicalPhaseSweepCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaign(Periodic2DCampaign):
    """Encapsulate one retained three-model parameter sweep."""

    model: Periodic2DTopologicalPhaseSweepCampaignModel
    correlator = Periodic2DTopologicalPhaseSweepCampaignCorrelator()
    verifier = Periodic2DTopologicalPhaseSweepCampaignVerifier()

    def correlate(self) -> Periodic2DTopologicalPhaseSweepCampaignCorrelationResult:
        """Correlate retained and maintained sweep documents."""
        return self.correlator.execute(
            Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalPhaseSweepCampaignVerificationResult:
        """Independently verify every retained sweep sample."""
        return self.verifier.execute(
            Periodic2DTopologicalPhaseSweepCampaignVerificationRequest(
                self.model, repository_root
            )
        )
