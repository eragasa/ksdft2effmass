"""Integrated correlation and independent reduction-challenge verification.

The Workflow first deserializes and correlates caller-supplied historical input and
result bytes, then applies the independent verifier with one explicit nonnegative
unitless tolerance. Correlation and verification remain separate Results. The Workflow
performs no file discovery, historical calculation, external execution, scientific
validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .correlation_workflow import (
    Periodic1DReductionChallengeCampaignWorkflow,
    Periodic1DReductionChallengeCampaignWorkflowRequest,
    Periodic1DReductionChallengeCampaignWorkflowResult,
)
from .numerical_verification import (
    Periodic1DReductionChallengeResultVerifier,
    Periodic1DReductionChallengeVerificationRequest,
    Periodic1DReductionChallengeVerificationResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeVerifiedWorkflowRequest:
    """Declare exact retained bytes and an independent verification tolerance.

    Parameters
    ----------
    campaign_request
        Exact historical input and result bytes.
    absolute_tolerance
        Inclusive ``Unitless`` tolerance applied separately to every independently
        reconstructed channel maximum.

    Raises
    ------
    TypeError
        If either value has the wrong exact semantic type.
    ValueError
        If the tolerance is not unitless or is negative.
    OverflowError
        If the tolerance is not finite binary64.
    """

    campaign_request: Periodic1DReductionChallengeCampaignWorkflowRequest
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact nested request ownership and numerical tolerance."""
        if (
            type(self.campaign_request)
            is not Periodic1DReductionChallengeCampaignWorkflowRequest
        ):
            raise TypeError(
                "campaign_request must be "
                "Periodic1DReductionChallengeCampaignWorkflowRequest"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if not np.isfinite(self.absolute_tolerance.magnitude):
            raise OverflowError("absolute_tolerance must be finite binary64")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeVerifiedWorkflowResult:
    """Retain correlated records and numerical verification separately.

    Parameters
    ----------
    campaign_result
        Correlated typed controls, retained result, and exact wire identities.
    verification
        Independent reconstruction defects and bounded disposition.
    """

    campaign_result: Periodic1DReductionChallengeCampaignWorkflowResult
    verification: Periodic1DReductionChallengeVerificationResult

    def __post_init__(self) -> None:
        """Validate exact nested correlation and verification Result types."""
        if (
            type(self.campaign_result)
            is not Periodic1DReductionChallengeCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_result must be "
                "Periodic1DReductionChallengeCampaignWorkflowResult"
            )
        if (
            type(self.verification)
            is not Periodic1DReductionChallengeVerificationResult
        ):
            raise TypeError(
                "verification must be Periodic1DReductionChallengeVerificationResult"
            )

    @property
    def passes(self) -> bool:
        """Return the bounded independent numerical-verification disposition.

        Returns
        -------
        bool
            Aggregate result of the five separately retained channel comparisons.
        """
        return self.verification.passes


class Periodic1DReductionChallengeVerifiedWorkflow:
    """Compose retained wire correlation and independent numerical verification.

    The stateless Workflow creates fresh operation owners for each request and retains
    no mutable execution state. Expected trends under altered mathematics remain
    observations rather than additional pass criteria.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DReductionChallengeVerifiedWorkflowRequest
    ) -> Periodic1DReductionChallengeVerifiedWorkflowResult:
        """Correlate retained bytes, then verify all reconstructable channels.

        Parameters
        ----------
        request
            Exact retained campaign request and explicit numerical tolerance.

        Returns
        -------
        Periodic1DReductionChallengeVerifiedWorkflowResult
            Preserved correlation and numerical-verification outcomes.

        Raises
        ------
        TypeError
            If ``request`` or a nested value has the wrong exact representation.
        ValueError
            If units, wires, correlations, controls, or dimensions are invalid.
        OverflowError
            If a retained or reconstructed scalar or array is not finite
            binary64/complex128.
        MemoryError
            If dense matrix, path, Fourier, or least-squares allocation fails.
        numpy.linalg.LinAlgError
            If a dense eigensolver or least-squares operation does not converge.
        """
        if type(request) is not Periodic1DReductionChallengeVerifiedWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DReductionChallengeVerifiedWorkflowRequest"
            )
        campaign_result = Periodic1DReductionChallengeCampaignWorkflow().execute(
            request.campaign_request
        )
        verification = Periodic1DReductionChallengeResultVerifier().execute(
            Periodic1DReductionChallengeVerificationRequest(
                campaign_result,
                request.absolute_tolerance,
            )
        )
        return Periodic1DReductionChallengeVerifiedWorkflowResult(
            campaign_result,
            verification,
        )
