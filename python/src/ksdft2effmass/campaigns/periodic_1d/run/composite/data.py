"""Encapsulating DataObject for the retained composite periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...model.retained.composite import Periodic1DCompositeCampaignModel
from .correlate import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignCorrelator,
)
from .verify import (
    Periodic1DCompositeCampaignVerificationRequest,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaign:
    """Encapsulate one retained composite-band campaign DataObjectModel.

    Parameters
    ----------
    model
        Exact immutable retained-wire model delegated to campaign Actionizers.
    """

    model: Periodic1DCompositeCampaignModel

    correlator = Periodic1DCompositeCampaignCorrelator()
    verifier = Periodic1DCompositeCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact composite campaign model type."""
        if type(self.model) is not Periodic1DCompositeCampaignModel:
            raise TypeError("model must be Periodic1DCompositeCampaignModel")

    def correlate(self) -> Periodic1DCompositeCampaignCorrelationResult:
        """Delegate retained-wire correlation to the correlation Actionizer."""
        return self.correlator.execute(
            Periodic1DCompositeCampaignCorrelationRequest(self.model)
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DCompositeCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for reconstructable numerical diagnostics.

        Returns
        -------
        Periodic1DCompositeCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DCompositeCampaignVerificationRequest(
                self.model,
                absolute_tolerance,
            )
        )
