"""Encapsulating DataObject for the retained topological benchmark."""

from dataclasses import dataclass
from pathlib import Path

from ...model.retained.topological import Periodic2DTopologicalCampaignModel
from .correlate import (
    Periodic2DTopologicalCampaignCorrelationRequest,
    Periodic2DTopologicalCampaignCorrelationResult,
    Periodic2DTopologicalCampaignCorrelator,
)
from .verify import (
    Periodic2DTopologicalCampaignVerificationRequest,
    Periodic2DTopologicalCampaignVerificationResult,
    Periodic2DTopologicalCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalCampaign:
    """Encapsulate one retained three-model benchmark."""

    model: Periodic2DTopologicalCampaignModel
    correlator = Periodic2DTopologicalCampaignCorrelator()
    verifier = Periodic2DTopologicalCampaignVerifier()

    def correlate(self) -> Periodic2DTopologicalCampaignCorrelationResult:
        """Correlate the retained document with the maintained route."""
        return self.correlator.execute(
            Periodic2DTopologicalCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalCampaignVerificationResult:
        """Independently verify all retained model families."""
        return self.verifier.execute(
            Periodic2DTopologicalCampaignVerificationRequest(
                self.model, repository_root
            )
        )
