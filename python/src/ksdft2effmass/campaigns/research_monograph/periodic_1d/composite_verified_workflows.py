"""Integrated retained-correlation and composite verification Workflow.

This module provides the supported one-call orchestration boundary for the Appendix G
composite result.  It first deserializes and correlates immutable input/result bytes,
then passes that correlated ResultObject to the algorithmically independent composite
verifier.  Both outcomes remain available to callers.

The Workflow performs no historical calculation, filesystem discovery, external
execution, scientific validation, or uncertainty quantification.  Unavailable
verification channels remain explicit in the nested verification result and do not
silently contribute to ``passes``.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .composite_verification import (
    Periodic1DCompositeResultVerifier,
    Periodic1DCompositeVerificationRequest,
    Periodic1DCompositeVerificationResult,
)
from .wilson_workflows import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeCampaignWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeVerifiedWorkflowRequest:
    """Declare retained composite bytes and independent verification tolerance.

    Parameters
    ----------
    campaign_request
        Exact immutable Appendix G composite input and result bytes.
    absolute_tolerance
        Inclusive numerical-verification tolerance in the dimensionless recoil-energy
        convention :math:`E_G`.
    """

    campaign_request: Periodic1DCompositeCampaignWorkflowRequest
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact nested request ownership and unitless tolerance.

        Raises
        ------
        TypeError
            If either field has the wrong exact semantic type.
        ValueError
            If the tolerance is dimensional or negative.
        """
        if (
            type(self.campaign_request)
            is not Periodic1DCompositeCampaignWorkflowRequest
        ):
            raise TypeError(
                "campaign_request must be Periodic1DCompositeCampaignWorkflowRequest"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeVerifiedWorkflowResult:
    """Retain correlated campaign records and independent numerical verification.

    Parameters
    ----------
    campaign_result
        Correlated typed input definition, complete retained result, and wire
        identities.
    composite_verification
        Independent reconstruction of every channel supported by the retained source
        values, including its explicit unavailable-channel inventory.
    """

    campaign_result: Periodic1DCompositeCampaignWorkflowResult
    composite_verification: Periodic1DCompositeVerificationResult

    def __post_init__(self) -> None:
        """Validate exact result types and ordered group correlation.

        Raises
        ------
        TypeError
            If either field has the wrong exact ResultObject type.
        ValueError
            If the correlated and verified group inventories differ or are reordered.
        """
        if type(self.campaign_result) is not Periodic1DCompositeCampaignWorkflowResult:
            raise TypeError("campaign_result uses the wrong Workflow ResultObject")
        if (
            type(self.composite_verification)
            is not Periodic1DCompositeVerificationResult
        ):
            raise TypeError("composite_verification uses the wrong ResultObject")
        campaign_ids = tuple(
            group.group_id for group in self.campaign_result.campaign_result.groups
        )
        verification_ids = tuple(
            group.group_id for group in self.composite_verification.groups
        )
        if verification_ids != campaign_ids:
            raise ValueError(
                "campaign and composite verification group inventories disagree"
            )

    @property
    def passes(self) -> bool:
        """Return the independent composite-verification disposition.

        Returns
        -------
        bool
            ``True`` exactly when every reconstructable group channel passes the
            explicit tolerance and identity checks.  Unavailable channels remain
            excluded and explicitly listed in ``composite_verification``.
        """
        return self.composite_verification.passes


class Periodic1DCompositeVerifiedWorkflow:
    """Compose retained campaign correlation and independent result verification.

    Processing order is fixed:

    1. deserialize and correlate the exact input and result bytes;
    2. verify all reconstructable group channels using direct NumPy operations; and
    3. return both ResultObjects without altering either one.

    Structural wire or correlation incompatibility raises before numerical
    verification.  A reconstructable numerical mismatch remains represented as
    ``passes=False``.

    See Also
    --------
    Periodic1DCompositeCampaignWorkflow
        Lower-level retained input/result correlation Workflow.
    Periodic1DCompositeResultVerifier
        Algorithmically independent numerical verifier composed by this Workflow.
    """

    __slots__ = ()

    campaign_workflow = Periodic1DCompositeCampaignWorkflow()
    composite_verifier = Periodic1DCompositeResultVerifier()

    def execute(
        self, request: Periodic1DCompositeVerifiedWorkflowRequest
    ) -> Periodic1DCompositeVerifiedWorkflowResult:
        """Correlate retained bytes and verify every reconstructable channel.

        Parameters
        ----------
        request
            Nested retained campaign request and explicit numerical tolerance.

        Returns
        -------
        Periodic1DCompositeVerifiedWorkflowResult
            Preserved correlation result and independent verification result.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If retained wire fields, campaign correlations, or represented dimensions
            are incompatible with verification.
        """
        if type(request) is not Periodic1DCompositeVerifiedWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DCompositeVerifiedWorkflowRequest"
            )
        campaign_result = self.campaign_workflow.execute(request.campaign_request)
        verification = self.composite_verifier.execute(
            Periodic1DCompositeVerificationRequest(
                campaign_result,
                request.absolute_tolerance,
            )
        )
        return Periodic1DCompositeVerifiedWorkflowResult(
            campaign_result,
            verification,
        )
