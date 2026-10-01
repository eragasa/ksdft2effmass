"""Verification Actionizer for retained isolated periodic-1D payloads."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from ...isolated_verification import (
    Periodic1DIsolatedResultVerifier,
    Periodic1DIsolatedVerificationRequest,
    Periodic1DIsolatedVerificationResult,
)
from ...model.retained.isolated import Periodic1DIsolatedBandCampaignModel
from ...workflows import Periodic1DIsolatedBandCampaignWorkflowResult
from .correlate import (
    Periodic1DIsolatedBandCampaignCorrelationRequest,
    Periodic1DIsolatedBandCampaignCorrelator,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignVerificationRequest:
    """Request verification of one encapsulated isolated campaign model.

    Parameters
    ----------
    model
        Exact retained input and result payloads.
    absolute_tolerance
        Inclusive tolerance for ordinary diagnostics in normalized recoil-energy
        units :math:`E_G`.
    curvature_absolute_tolerance
        Separate tolerance for the cancellation-sensitive zone-center curvature.
    """

    model: Periodic1DIsolatedBandCampaignModel
    absolute_tolerance: ScalarQuantity
    curvature_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact model ownership and nonnegative unitless tolerances."""
        if type(self.model) is not Periodic1DIsolatedBandCampaignModel:
            raise TypeError("model must be Periodic1DIsolatedBandCampaignModel")
        for name, value in (
            ("absolute_tolerance", self.absolute_tolerance),
            ("curvature_absolute_tolerance", self.curvature_absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignVerificationResult:
    """Retain isolated campaign correlation and verification separately.

    Parameters
    ----------
    campaign_correlation
        Typed definition, retained result, and payload identities.
    verification
        Independent reconstruction diagnostics and unavailable-channel inventory.
    """

    campaign_correlation: Periodic1DIsolatedBandCampaignWorkflowResult
    verification: Periodic1DIsolatedVerificationResult

    def __post_init__(self) -> None:
        """Validate exact correlated and verification ResultObject types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DIsolatedBandCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")
        if type(self.verification) is not Periodic1DIsolatedVerificationResult:
            raise TypeError("verification uses the wrong ResultObject type")

    @property
    def passes(self) -> bool:
        """Return the bounded independent numerical-verification disposition."""
        return self.verification.passes


class Periodic1DIsolatedBandCampaignVerifier:
    """Correlate and verify one retained isolated campaign model."""

    __slots__ = ()

    correlator = Periodic1DIsolatedBandCampaignCorrelator()
    numerical_verifier = Periodic1DIsolatedResultVerifier()

    def execute(
        self, request: Periodic1DIsolatedBandCampaignVerificationRequest
    ) -> Periodic1DIsolatedBandCampaignVerificationResult:
        """Return independently reconstructed isolated campaign diagnostics."""
        if type(request) is not Periodic1DIsolatedBandCampaignVerificationRequest:
            raise TypeError(
                "request must be Periodic1DIsolatedBandCampaignVerificationRequest"
            )
        correlation = self.correlator.execute(
            Periodic1DIsolatedBandCampaignCorrelationRequest(request.model)
        ).campaign_correlation
        verification = self.numerical_verifier.execute(
            Periodic1DIsolatedVerificationRequest(
                correlation,
                request.absolute_tolerance,
                request.curvature_absolute_tolerance,
            )
        )
        return Periodic1DIsolatedBandCampaignVerificationResult(
            correlation,
            verification,
        )
