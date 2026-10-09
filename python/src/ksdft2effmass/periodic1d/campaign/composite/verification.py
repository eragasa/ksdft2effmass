"""Verification action for retained composite periodic-1D payloads."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .correlation import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelator,
)
from .correlation_workflow import Periodic1DCompositeCampaignWorkflowResult
from .encoded_documents import Periodic1DCompositeEncodedDocuments
from .numerical_verification import (
    Periodic1DCompositeResultVerifier,
    Periodic1DCompositeVerificationRequest,
    Periodic1DCompositeVerificationResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignVerificationRequest:
    """Request verification of composite encoded campaign documents.

    Parameters
    ----------
    encoded_documents
        Exact retained input and result payloads.
    absolute_tolerance
        Inclusive numerical-verification tolerance in normalized recoil-energy units
        :math:`E_G`.
    """

    encoded_documents: Periodic1DCompositeEncodedDocuments
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact document ownership and a nonnegative unitless tolerance."""
        if type(self.encoded_documents) is not Periodic1DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DCompositeEncodedDocuments"
            )
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
        """Validate exact correlated and verification AbstractResultObject types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation uses the wrong AbstractResultObject type"
            )
        if type(self.verification) is not Periodic1DCompositeVerificationResult:
            raise TypeError("verification uses the wrong AbstractResultObject type")
        campaign_ids = tuple(
            group.group_id for group in self.campaign_correlation.campaign_result.groups
        )
        verification_ids = tuple(group.group_id for group in self.verification.groups)
        if campaign_ids != verification_ids:
            raise ValueError("campaign and verification group inventories disagree")

    @property
    def passes(self) -> bool:
        """Return the bounded independent numerical-verification disposition.

        Returns
        -------
        bool
            ``True`` only when every reconstructable numerical check passes.

        Notes
        -----
        Explicitly unavailable source channels are excluded and cannot contribute
        positive evidence.
        """
        return self.verification.passes


class Periodic1DCompositeCampaignVerifier:
    """Bind, validate, and verify composite encoded campaign documents.

    The Action constructs request-scoped correlation and numerical-verification
    operations. It owns orchestration order, not retained bytes, numerical algorithms,
    provenance, or scientific acceptance.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeCampaignVerificationRequest
    ) -> Periodic1DCompositeCampaignVerificationResult:
        """Return independently reconstructed composite campaign diagnostics.

        Parameters
        ----------
        request
            Exact retained documents and an explicit unitless absolute tolerance.

        Returns
        -------
        Periodic1DCompositeCampaignVerificationResult
            Preserved correlation and independent reconstructable-channel diagnostics.

        Raises
        ------
        TypeError
            If ``request`` or a nested value has the wrong exact representation.
        ValueError
            If units, wires, correlations, or represented dimensions are invalid.
        OverflowError
            If a reconstructed scalar or matrix is not finite binary64/complex128.
        MemoryError
            If dense path, Fourier, eigensolver, or least-squares allocation fails.
        numpy.linalg.LinAlgError
            If a dense eigensolver or least-squares operation does not converge.
        """
        if type(request) is not Periodic1DCompositeCampaignVerificationRequest:
            raise TypeError(
                "request must be Periodic1DCompositeCampaignVerificationRequest"
            )
        correlation = (
            Periodic1DCompositeCampaignCorrelator()
            .execute(
                Periodic1DCompositeCampaignCorrelationRequest(request.encoded_documents)
            )
            .campaign_correlation
        )
        verification = Periodic1DCompositeResultVerifier().execute(
            Periodic1DCompositeVerificationRequest(
                correlation,
                request.absolute_tolerance,
            )
        )
        return Periodic1DCompositeCampaignVerificationResult(
            correlation,
            verification,
        )
