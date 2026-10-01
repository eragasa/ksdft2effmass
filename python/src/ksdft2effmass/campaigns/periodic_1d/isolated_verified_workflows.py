"""Integrated retained-correlation and isolated-band verification Workflow."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .isolated_verification import (
    Periodic1DIsolatedResultVerifier,
    Periodic1DIsolatedVerificationRequest,
    Periodic1DIsolatedVerificationResult,
)
from .workflows import (
    Periodic1DIsolatedBandCampaignWorkflow,
    Periodic1DIsolatedBandCampaignWorkflowRequest,
    Periodic1DIsolatedBandCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedVerifiedWorkflowRequest:
    """Declare retained bytes and independent isolated verification controls.

    Parameters
    ----------
    campaign_request
        Exact retained isolated-band input and result bytes.
    absolute_tolerance
        Inclusive ordinary diagnostic tolerance in normalized :math:`E_G` units.
    curvature_absolute_tolerance
        Separate tolerance for cancellation-sensitive center curvature.
    """

    campaign_request: Periodic1DIsolatedBandCampaignWorkflowRequest
    absolute_tolerance: ScalarQuantity
    curvature_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate nested request ownership and nonnegative unitless tolerances."""
        if (
            type(self.campaign_request)
            is not Periodic1DIsolatedBandCampaignWorkflowRequest
        ):
            raise TypeError(
                "campaign_request must be the isolated campaign Workflow request"
            )
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
class Periodic1DIsolatedVerifiedWorkflowResult:
    """Retain correlated isolated records and independent numerical verification.

    Parameters
    ----------
    campaign_result
        Correlated typed input, retained result, and wire identities.
    isolated_verification
        Independent numerical reconstruction with explicit unavailable channels.
    """

    campaign_result: Periodic1DIsolatedBandCampaignWorkflowResult
    isolated_verification: Periodic1DIsolatedVerificationResult

    def __post_init__(self) -> None:
        """Validate exact nested ResultObject types."""
        if (
            type(self.campaign_result)
            is not Periodic1DIsolatedBandCampaignWorkflowResult
        ):
            raise TypeError("campaign_result uses the wrong Workflow ResultObject")
        if type(self.isolated_verification) is not Periodic1DIsolatedVerificationResult:
            raise TypeError("isolated_verification uses the wrong ResultObject")

    @property
    def passes(self) -> bool:
        """Return the bounded independent isolated-band verification disposition."""
        return self.isolated_verification.passes


class Periodic1DIsolatedVerifiedWorkflow:
    """Compose retained isolated correlation and independent verification.

    The Workflow performs no filesystem discovery, historical calculation, external
    execution, material validation, or uncertainty quantification.  It preserves the
    correlation and verification ResultObjects separately.
    """

    __slots__ = ()

    campaign_workflow = Periodic1DIsolatedBandCampaignWorkflow()
    verifier = Periodic1DIsolatedResultVerifier()

    def execute(
        self, request: Periodic1DIsolatedVerifiedWorkflowRequest
    ) -> Periodic1DIsolatedVerifiedWorkflowResult:
        """Correlate retained bytes, then verify reconstructable isolated channels.

        Parameters
        ----------
        request
            Retained campaign request and two explicit numerical tolerances.

        Returns
        -------
        Periodic1DIsolatedVerifiedWorkflowResult
            Preserved correlation and numerical-verification outcomes.
        """
        if type(request) is not Periodic1DIsolatedVerifiedWorkflowRequest:
            raise TypeError("request must be Periodic1DIsolatedVerifiedWorkflowRequest")
        campaign_result = self.campaign_workflow.execute(request.campaign_request)
        verification = self.verifier.execute(
            Periodic1DIsolatedVerificationRequest(
                campaign_result,
                request.absolute_tolerance,
                request.curvature_absolute_tolerance,
            )
        )
        return Periodic1DIsolatedVerifiedWorkflowResult(
            campaign_result,
            verification,
        )
