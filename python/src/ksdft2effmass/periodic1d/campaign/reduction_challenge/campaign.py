"""Encapsulating DataObject for one retained reduction challenge."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from .correlation import (
    Periodic1DReductionChallengeCampaignCorrelationRequest,
    Periodic1DReductionChallengeCampaignCorrelationResult,
    Periodic1DReductionChallengeCampaignCorrelator,
)
from .encoded_documents import Periodic1DReductionChallengeEncodedDocuments
from .verification import (
    Periodic1DReductionChallengeCampaignVerificationRequest,
    Periodic1DReductionChallengeCampaignVerificationResult,
    Periodic1DReductionChallengeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaign:
    """Encapsulate one retained adversarial reduction challenge.

    Parameters
    ----------
    encoded_documents
        Exact immutable historical input and result bytes delegated to explicit
        correlation or verification Actions.

    Raises
    ------
    TypeError
        If ``encoded_documents`` has the wrong exact semantic type.

    Notes
    -----
    ``ReductionChallenge`` refers to adversarial tests of isolation,
    discretization, sampling, gauge, truncation, and fitting-route assumptions. It
    does not denote mechanical stress, strain, elasticity, or a stress tensor. The
    campaign record is evidence infrastructure rather than a physical model, retained
    space, represented operator, effective model, or scientific conclusion.
    """

    encoded_documents: Periodic1DReductionChallengeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact reduction-challenge document type."""
        if (
            type(self.encoded_documents)
            is not Periodic1DReductionChallengeEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic1DReductionChallengeEncodedDocuments"
            )

    def correlate(self) -> Periodic1DReductionChallengeCampaignCorrelationResult:
        """Correlate exact retained input and result wires.

        Returns
        -------
        Periodic1DReductionChallengeCampaignCorrelationResult
            Typed records and separate exact wire-content identities.

        Raises
        ------
        TypeError
            If a decoded value has the wrong exact representation.
        ValueError
            If strict schemas, intrinsic values, or cross-document correlations are
            invalid.
        OverflowError
            If a retained diagnostic is not finite binary64.

        Notes
        -----
        Correlation authenticates available content relationships only; it performs no
        numerical reconstruction or scientific validation.
        """
        return Periodic1DReductionChallengeCampaignCorrelator().execute(
            Periodic1DReductionChallengeCampaignCorrelationRequest(
                self.encoded_documents
            )
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DReductionChallengeCampaignVerificationResult:
        """Correlate and independently reconstruct retained challenge channels.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance applied separately to every reconstructed
            channel maximum.

        Returns
        -------
        Periodic1DReductionChallengeCampaignVerificationResult
            Preserved correlation and bounded numerical-verification outcomes.

        Raises
        ------
        TypeError
            If the tolerance or a decoded field has the wrong exact representation.
        ValueError
            If units, wire structure, correlations, controls, or dimensions are
            invalid.
        OverflowError
            If a retained or reconstructed scalar or array is not finite
            binary64/complex128.
        MemoryError
            If dense matrix, path, Fourier, or least-squares allocation fails.
        numpy.linalg.LinAlgError
            If a dense eigensolver or least-squares operation does not converge.

        Notes
        -----
        Passing establishes only retained-versus-reconstructed agreement for the
        frozen represented challenge. It does not establish convergence, parent-model
        adequacy, material validation, UQ, transferability, or human acceptance.
        """
        return Periodic1DReductionChallengeCampaignVerifier().execute(
            Periodic1DReductionChallengeCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
            )
        )
