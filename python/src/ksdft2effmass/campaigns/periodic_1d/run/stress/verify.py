"""Verification action for periodic-1D reduction-challenge payloads."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from ...encoded_documents import Periodic1DReductionChallengeEncodedDocuments
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
    """Request verification of reduction-challenge encoded documents.

    Parameters
    ----------
    encoded_documents
        Exact retained reduction-challenge input and result payloads.
    absolute_tolerance
        Inclusive unitless tolerance applied separately to every verification channel.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact document ownership and a nonnegative unitless tolerance."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )
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
        """Validate exact correlated and verification AbstractResultObject types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DStressCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation uses the wrong AbstractResultObject type"
            )
        if type(self.verification) is not Periodic1DStressVerificationResult:
            raise TypeError("verification uses the wrong AbstractResultObject type")

    @property
    def passes(self) -> bool:
        """Return the bounded independent stress-verification disposition."""
        return self.verification.passes


class Periodic1DStressCampaignVerifier:
    """Bind, validate, and verify reduction-challenge encoded documents."""

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
            Periodic1DStressCampaignCorrelationRequest(request.encoded_documents)
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
