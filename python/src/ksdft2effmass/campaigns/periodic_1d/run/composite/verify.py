"""Verification Actionizer for retained composite periodic-1D payloads."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from ...composite_verification import (
    Periodic1DCompositeResultVerifier,
    Periodic1DCompositeVerificationRequest,
    Periodic1DCompositeVerificationResult,
)
from ...model.retained.composite import Periodic1DCompositeCampaignModel
from ...wilson_workflows import Periodic1DCompositeCampaignWorkflowResult
from .correlate import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelator,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignVerificationRequest:
    """Request verification of one encapsulated composite campaign model.

    Parameters
    ----------
    model
        Exact retained input and result payloads.
    absolute_tolerance
        Inclusive numerical-verification tolerance in normalized recoil-energy units
        :math:`E_G`.
    """

    model: Periodic1DCompositeCampaignModel
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact model ownership and a nonnegative unitless tolerance."""
        if type(self.model) is not Periodic1DCompositeCampaignModel:
            raise TypeError("model must be Periodic1DCompositeCampaignModel")
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignVerificationResult:
    """Retain composite campaign correlation and verification separately.

    Parameters
    ----------
    campaign_correlation
        Typed composite definition, retained result, and payload identities.
    verification
        Independent reconstructable-channel diagnostics and explicit exclusions.
    """

    campaign_correlation: Periodic1DCompositeCampaignWorkflowResult
    verification: Periodic1DCompositeVerificationResult

    def __post_init__(self) -> None:
        """Validate exact correlated and verification ResultObject types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError("campaign_correlation uses the wrong ResultObject type")
        if type(self.verification) is not Periodic1DCompositeVerificationResult:
            raise TypeError("verification uses the wrong ResultObject type")
        campaign_ids = tuple(
            group.group_id for group in self.campaign_correlation.campaign_result.groups
        )
        verification_ids = tuple(group.group_id for group in self.verification.groups)
        if campaign_ids != verification_ids:
            raise ValueError("campaign and verification group inventories disagree")

    @property
    def passes(self) -> bool:
        """Return the bounded independent numerical-verification disposition."""
        return self.verification.passes


class Periodic1DCompositeCampaignVerifier:
    """Correlate and verify one retained composite campaign model."""

    __slots__ = ()

    correlator = Periodic1DCompositeCampaignCorrelator()
    numerical_verifier = Periodic1DCompositeResultVerifier()

    def execute(
        self, request: Periodic1DCompositeCampaignVerificationRequest
    ) -> Periodic1DCompositeCampaignVerificationResult:
        """Return independently reconstructed composite campaign diagnostics."""
        if type(request) is not Periodic1DCompositeCampaignVerificationRequest:
            raise TypeError(
                "request must be Periodic1DCompositeCampaignVerificationRequest"
            )
        correlation = self.correlator.execute(
            Periodic1DCompositeCampaignCorrelationRequest(request.model)
        ).campaign_correlation
        verification = self.numerical_verifier.execute(
            Periodic1DCompositeVerificationRequest(
                correlation,
                request.absolute_tolerance,
            )
        )
        return Periodic1DCompositeCampaignVerificationResult(
            correlation,
            verification,
        )
