"""Integrated retained correlation and independent stress-result verification.

The Workflow first deserializes and correlates caller-supplied Appendix G stress input
and result bytes, then applies the independent numerical verifier with one explicit
nonnegative ``Unitless`` tolerance. Correlation and verification remain separate
ResultObjects. The Workflow performs no filesystem discovery, historical calculation,
external execution, material validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .stress_verification import (
    Periodic1DStressResultVerifier,
    Periodic1DStressVerificationRequest,
    Periodic1DStressVerificationResult,
)
from .workflows import (
    Periodic1DStressCampaignWorkflow,
    Periodic1DStressCampaignWorkflowRequest,
    Periodic1DStressCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressVerifiedWorkflowRequest:
    """Declare retained stress bytes and independent verification tolerance.

    Parameters
    ----------
    campaign_request
        Exact retained stress input and result bytes.
    absolute_tolerance
        Inclusive ``Unitless`` tolerance applied numerically to every independently
        reconstructed stress channel. Energy residuals already use normalized
        :math:`E_G=1` values, while overlap, frame, and phase diagnostics remain
        dimensionless.
    """

    campaign_request: Periodic1DStressCampaignWorkflowRequest
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate nested request ownership and nonnegative unitless tolerance."""
        if type(self.campaign_request) is not Periodic1DStressCampaignWorkflowRequest:
            raise TypeError(
                "campaign_request must be the stress campaign Workflow request"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DStressVerifiedWorkflowResult:
    """Retain correlated stress records and independent numerical verification.

    Parameters
    ----------
    campaign_result
        Correlated typed input, retained result, and wire identities.
    stress_verification
        Independent reconstruction defects and bounded disposition.
    """

    campaign_result: Periodic1DStressCampaignWorkflowResult
    stress_verification: Periodic1DStressVerificationResult

    def __post_init__(self) -> None:
        """Validate exact nested ResultObject types."""
        if type(self.campaign_result) is not Periodic1DStressCampaignWorkflowResult:
            raise TypeError("campaign_result uses the wrong Workflow ResultObject")
        if type(self.stress_verification) is not Periodic1DStressVerificationResult:
            raise TypeError("stress_verification uses the wrong ResultObject")

    @property
    def passes(self) -> bool:
        """Return the bounded independent stress verification disposition."""
        return self.stress_verification.passes


class Periodic1DStressVerifiedWorkflow:
    """Compose retained stress correlation and independent verification.

    The Workflow performs no filesystem discovery, historical calculation, external
    execution, material validation, or uncertainty quantification. It preserves the
    correlation and verification ResultObjects separately.
    """

    __slots__ = ()

    campaign_workflow = Periodic1DStressCampaignWorkflow()
    verifier = Periodic1DStressResultVerifier()

    def execute(
        self, request: Periodic1DStressVerifiedWorkflowRequest
    ) -> Periodic1DStressVerifiedWorkflowResult:
        """Correlate retained bytes, then verify all typed stress channels.

        Parameters
        ----------
        request
            Retained campaign request and explicit numerical tolerance.

        Returns
        -------
        Periodic1DStressVerifiedWorkflowResult
            Preserved correlation and numerical-verification outcomes.
        """
        if type(request) is not Periodic1DStressVerifiedWorkflowRequest:
            raise TypeError("request must be Periodic1DStressVerifiedWorkflowRequest")
        campaign_result = self.campaign_workflow.execute(request.campaign_request)
        verification = self.verifier.execute(
            Periodic1DStressVerificationRequest(
                campaign_result,
                request.absolute_tolerance,
            )
        )
        return Periodic1DStressVerifiedWorkflowResult(
            campaign_result,
            verification,
        )
