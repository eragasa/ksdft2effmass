"""Encapsulating DataObject for the balanced Wannier90 comparison."""

from dataclasses import dataclass
from pathlib import Path

from ....model.retained.wannier90_balanced import (
    Periodic2DWannier90BalancedCampaignModel,
)
from .verify import (
    Periodic2DWannier90BalancedCampaignVerificationRequest,
    Periodic2DWannier90BalancedCampaignVerificationResult,
    Periodic2DWannier90BalancedCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedCampaign:
    """Encapsulate the retained repository-portable comparison."""

    model: Periodic2DWannier90BalancedCampaignModel
    verifier = Periodic2DWannier90BalancedCampaignVerifier()

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90BalancedCampaignVerificationResult:
        """Verify portable evidence without accessing native external files."""
        return self.verifier.execute(
            Periodic2DWannier90BalancedCampaignVerificationRequest(
                self.model, repository_root
            )
        )
