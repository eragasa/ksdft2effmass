"""Encapsulating DataObject for the retained isolated periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from ...model.retained.isolated import Periodic1DIsolatedBandCampaignModel
from .correlate import (
    Periodic1DIsolatedBandCampaignCorrelationRequest,
    Periodic1DIsolatedBandCampaignCorrelationResult,
    Periodic1DIsolatedBandCampaignCorrelator,
)
from .verify import (
    Periodic1DIsolatedBandCampaignVerificationRequest,
    Periodic1DIsolatedBandCampaignVerificationResult,
    Periodic1DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaign:
    """Encapsulate one retained isolated-band campaign DataObjectModel.

    Parameters
    ----------
    model
        Exact immutable retained-wire model delegated to campaign Actionizers.
    """

    model: Periodic1DIsolatedBandCampaignModel

    correlator = Periodic1DIsolatedBandCampaignCorrelator()
    verifier = Periodic1DIsolatedBandCampaignVerifier()

    def __post_init__(self) -> None:
        """Require the exact isolated campaign model type."""
        if type(self.model) is not Periodic1DIsolatedBandCampaignModel:
            raise TypeError("model must be Periodic1DIsolatedBandCampaignModel")

    def correlate(self) -> Periodic1DIsolatedBandCampaignCorrelationResult:
        """Delegate retained-wire correlation to the correlation Actionizer."""
        return self.correlator.execute(
            Periodic1DIsolatedBandCampaignCorrelationRequest(self.model)
        )

    def verify(
        self,
        *,
        absolute_tolerance: ScalarQuantity,
        curvature_absolute_tolerance: ScalarQuantity,
    ) -> Periodic1DIsolatedBandCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for ordinary reconstruction diagnostics.
        curvature_absolute_tolerance
            Separate inclusive unitless tolerance for zone-center curvature.

        Returns
        -------
        Periodic1DIsolatedBandCampaignVerificationResult
            Correlation and verification outcomes with an aggregate disposition.
        """
        return self.verifier.execute(
            Periodic1DIsolatedBandCampaignVerificationRequest(
                self.model,
                absolute_tolerance,
                curvature_absolute_tolerance,
            )
        )
