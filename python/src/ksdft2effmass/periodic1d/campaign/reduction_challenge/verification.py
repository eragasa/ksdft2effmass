"""Verification Action for retained periodic-1D reduction-challenge payloads."""

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .correlation import (
    Periodic1DReductionChallengeCampaignCorrelationRequest,
    Periodic1DReductionChallengeCampaignCorrelator,
)
from .correlation_workflow import (
    Periodic1DReductionChallengeCampaignWorkflowResult,
)
from .encoded_documents import Periodic1DReductionChallengeEncodedDocuments
from .numerical_verification import (
    Periodic1DReductionChallengeResultVerifier,
    Periodic1DReductionChallengeVerificationRequest,
    Periodic1DReductionChallengeVerificationResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignVerificationRequest:
    """Request independent verification of exact challenge documents.

    Parameters
    ----------
    encoded_documents
        Exact retained historical input and result payloads.
    absolute_tolerance
        Inclusive unitless tolerance applied separately to each reconstructed channel
        maximum.

    Raises
    ------
    TypeError
        If either value has the wrong exact semantic type.
    ValueError
        If the tolerance is not unitless or is negative.
    OverflowError
        If the tolerance is not finite binary64.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact document ownership and numerical tolerance."""
        self._check_args_encoded_documents()
        self._check_args_absolute_tolerance()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact reduction-challenge document owner."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )

    def _check_args_absolute_tolerance(self) -> None:
        """Require one finite nonnegative unitless tolerance."""
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if not np.isfinite(self.absolute_tolerance.magnitude):
            raise OverflowError("absolute_tolerance must be finite binary64")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignVerificationResult:
    """Retain campaign correlation and numerical verification separately.

    Parameters
    ----------
    campaign_correlation
        Typed definition, retained result, and exact payload identities.
    verification
        Independently reconstructed channel defects and bounded disposition.

    Notes
    -----
    Preserving both Results prevents successful reconstruction from being mistaken for
    historical provenance or scientific validation.
    """

    campaign_correlation: Periodic1DReductionChallengeCampaignWorkflowResult
    verification: Periodic1DReductionChallengeVerificationResult

    def __post_init__(self) -> None:
        """Validate exact correlation and verification Result types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DReductionChallengeCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation must be "
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
            ``True`` only when every reconstructed channel maximum is within the
            explicit tolerance.
        """
        return self.verification.passes


class Periodic1DReductionChallengeCampaignVerifier:
    """Authenticate, correlate, and independently verify challenge documents.

    The Action creates fresh request-scoped correlation and numerical-verification
    owners. It does not retain mutable state, execute the historical producer, or turn
    expected qualitative trends into verification criteria.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DReductionChallengeCampaignVerificationRequest
    ) -> Periodic1DReductionChallengeCampaignVerificationResult:
        """Return correlation and independently reconstructed diagnostics.

        Parameters
        ----------
        request
            Exact documents and explicit unitless absolute tolerance.

        Returns
        -------
        Periodic1DReductionChallengeCampaignVerificationResult
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
        if type(request) is not Periodic1DReductionChallengeCampaignVerificationRequest:
            raise TypeError(
                "request must be "
                "Periodic1DReductionChallengeCampaignVerificationRequest"
            )
        correlation = (
            Periodic1DReductionChallengeCampaignCorrelator()
            .execute(
                Periodic1DReductionChallengeCampaignCorrelationRequest(
                    request.encoded_documents
                )
            )
            .campaign_correlation
        )
        verification = Periodic1DReductionChallengeResultVerifier().execute(
            Periodic1DReductionChallengeVerificationRequest(
                correlation,
                request.absolute_tolerance,
            )
        )
        return Periodic1DReductionChallengeCampaignVerificationResult(
            correlation,
            verification,
        )
