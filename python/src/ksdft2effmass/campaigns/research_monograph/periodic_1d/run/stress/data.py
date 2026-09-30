"""Encapsulating DataObject for the retained adversarial periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...model.retained.stress import Periodic1DStressCampaignModel
from .correlate import (
    Periodic1DStressCampaignCorrelationRequest,
    Periodic1DStressCampaignCorrelationResult,
    Periodic1DStressCampaignCorrelator,
)
from .verify import (
    Periodic1DStressCampaignVerificationRequest,
    Periodic1DStressCampaignVerificationResult,
    Periodic1DStressCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaign:
    """Encapsulate one retained adversarial stress-campaign DataObjectModel.

    Parameters
    ----------
    model
        Exact immutable retained-wire model delegated to campaign Actionizers.
    """

    model: Periodic1DStressCampaignModel

    correlator = Periodic1DStressCampaignCorrelator()
    verifier = Periodic1DStressCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact stress campaign model type."""
        if type(self.model) is not Periodic1DStressCampaignModel:
            raise TypeError("model must be Periodic1DStressCampaignModel")

    def correlate(self) -> Periodic1DStressCampaignCorrelationResult:
        """Delegate retained-wire correlation to the correlation Actionizer."""
        return self.correlator.execute(
            Periodic1DStressCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DStressCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance applied to each reconstructed stress channel.

        Returns
        -------
        Periodic1DStressCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DStressCampaignVerificationRequest(
                self.model,
                absolute_tolerance,
            )
        )
