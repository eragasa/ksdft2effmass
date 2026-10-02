"""Verification Actionizer for retained adversarial periodic-1D payloads."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from ...model.retained.stress import Periodic1DStressCampaignModel
from ...stress_verification import (
    Periodic1DStressResultVerifier,
    Periodic1DStressVerificationRequest,
    Periodic1DStressVerificationResult,
)
from ...workflows import Periodic1DStressCampaignWorkflowResult
from .correlate import (
    Periodic1DStressCampaignCorrelationRequest,
    Periodic1DStressCampaignCorrelator,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignVerificationRequest:
    """Request verification of one encapsulated stress campaign model.

    Parameters
    ----------
    model
        Exact retained stress input and result payloads.
    absolute_tolerance
        Inclusive unitless tolerance applied separately to every verification channel.
    """

    model: Periodic1DStressCampaignModel
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact model ownership and a nonnegative unitless tolerance."""
        if type(self.model) is not Periodic1DStressCampaignModel:
            raise TypeError("model must be Periodic1DStressCampaignModel")
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignVerificationResult:
    """Retain stress campaign correlation and verification separately.

    Parameters
    ----------
    campaign_correlation
        Typed stress definition, retained result, and payload identities.
    verification
        Independently reconstructed stress-channel diagnostics.
    """

    campaign_correlation: Periodic1DStressCampaignWorkflowResult
    verification: Periodic1DStressVerificationResult

    def __post_init__(self) -> None:
        """Validate exact correlated and verification ResultObject types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DStressCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")
        if type(self.verification) is not Periodic1DStressVerificationResult:
            raise TypeError("verification uses the wrong ResultObject type")

    @property
    def passes(self) -> bool:
        """Return the bounded independent stress-verification disposition."""
        return self.verification.passes


class Periodic1DStressCampaignVerifier:
    """Correlate and verify one retained adversarial stress campaign model."""

    __slots__ = ()

    correlator = Periodic1DStressCampaignCorrelator()
    numerical_verifier = Periodic1DStressResultVerifier()

    def execute(
        self, request: Periodic1DStressCampaignVerificationRequest
    ) -> Periodic1DStressCampaignVerificationResult:
        """Return independently reconstructed stress campaign diagnostics."""
        if type(request) is not Periodic1DStressCampaignVerificationRequest:
            raise TypeError(
                "request must be Periodic1DStressCampaignVerificationRequest"
            )
        correlation = self.correlator.execute(
            Periodic1DStressCampaignCorrelationRequest(request.model)
        ).campaign_correlation
        verification = self.numerical_verifier.execute(
            Periodic1DStressVerificationRequest(
                correlation,
                request.absolute_tolerance,
            )
        )
        return Periodic1DStressCampaignVerificationResult(
            correlation,
            verification,
        )
