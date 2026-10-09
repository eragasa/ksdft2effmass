"""Encapsulating DataObject for the retained composite periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from .correlation import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignCorrelator,
)
from .encoded_documents import Periodic1DCompositeEncodedDocuments
from .verification import (
    Periodic1DCompositeCampaignVerificationRequest,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaign:
    """Encapsulate one retained composite-band campaign.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and result bytes delegated to campaign operations.
    """

    encoded_documents: Periodic1DCompositeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact composite encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DCompositeEncodedDocuments"
            )

    def correlate(self) -> Periodic1DCompositeCampaignCorrelationResult:
        """Correlate the exact retained input and result wires.

        Returns
        -------
        Periodic1DCompositeCampaignCorrelationResult
            Typed definition/result correlation with separate content identities.

        Raises
        ------
        TypeError
            If a decoded wire value has the wrong exact representation.
        ValueError
            If schema, intrinsic data, or cross-document correlations are invalid.

        Notes
        -----
        Correlation authenticates content relationships only; it performs no numerical
        reconstruction or scientific validation.
        """
        return Periodic1DCompositeCampaignCorrelator().execute(
            Periodic1DCompositeCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, absolute_tolerance: ScalarQuantity
    ) -> Periodic1DCompositeCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for reconstructable numerical diagnostics.

        Returns
        -------
        Periodic1DCompositeCampaignVerificationResult
            Correlation and bounded independent verification outcomes.

        Raises
        ------
        TypeError
            If the tolerance or a decoded field has the wrong exact representation.
        ValueError
            If units, wire structure, correlations, or represented dimensions are
            invalid.
        OverflowError
            If a reconstructed scalar or matrix is not finite binary64/complex128.
        MemoryError
            If dense path, Fourier, eigensolver, or least-squares allocation fails.
        numpy.linalg.LinAlgError
            If a dense eigensolver or least-squares operation does not converge.

        Notes
        -----
        A passing result covers reconstructable retained represented channels only;
        explicitly unavailable channels do not contribute evidence.
        """
        return Periodic1DCompositeCampaignVerifier().execute(
            Periodic1DCompositeCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
            )
        )
