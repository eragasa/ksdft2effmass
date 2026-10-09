"""Encapsulating DataObject for the retained isolated periodic-1D campaign."""

from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity

from .correlation import (
    Periodic1DIsolatedBandCampaignCorrelationRequest,
    Periodic1DIsolatedBandCampaignCorrelationResult,
    Periodic1DIsolatedBandCampaignCorrelator,
)
from .encoded_documents import Periodic1DIsolatedBandEncodedDocuments
from .verification import (
    Periodic1DIsolatedBandCampaignVerificationRequest,
    Periodic1DIsolatedBandCampaignVerificationResult,
    Periodic1DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaign:
    """Encapsulate one retained isolated-band campaign.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and result bytes delegated to campaign operations.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not exactly the isolated encoded-document type.

    Notes
    -----
    This DataObject binds encoded inputs to their campaign-specific operations. It
    does not itself decode the wire, execute a calculator, authenticate historical
    execution, construct a physical model, or establish convergence, scientific
    validity, uncertainty quantification, or acceptance. ``correlate`` and ``verify``
    construct fresh Actions so no request-derived state is shared between calls.
    """

    encoded_documents: Periodic1DIsolatedBandEncodedDocuments

    def __post_init__(self) -> None:
        """Validate the intrinsic encoded-document ownership invariant."""
        self._check_args_encoded_documents()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact isolated encoded-document type."""
        if type(self.encoded_documents) is not Periodic1DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DIsolatedBandEncodedDocuments"
            )

    def correlate(self) -> Periodic1DIsolatedBandCampaignCorrelationResult:
        """Correlate exact input and result documents.

        Returns
        -------
        Periodic1DIsolatedBandCampaignCorrelationResult
            Typed decoded records and exact payload identities after all represented
            input/result relations have been checked.

        Raises
        ------
        TypeError
            If a decoded field has the wrong exact wire representation.
        ValueError
            If decoding, digest binding, or represented input/result correlation
            fails.
        OverflowError
            If a retained integer cannot be represented as binary64.
        MemoryError
            If storage for a retained dense array cannot be allocated.
        """
        return Periodic1DIsolatedBandCampaignCorrelator().execute(
            Periodic1DIsolatedBandCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self,
        *,
        absolute_tolerance: ScalarQuantity,
        curvature_absolute_tolerance: ScalarQuantity,
    ) -> Periodic1DIsolatedBandCampaignVerificationResult:
        """Delegate numerical verification through a complete typed request.

        Parameters
        ----------
        absolute_tolerance
            Inclusive unitless tolerance for ordinary reconstruction diagnostics.
        curvature_absolute_tolerance
            Separate inclusive unitless tolerance for zone-center curvature.

        Returns
        -------
        Periodic1DIsolatedBandCampaignVerificationResult
            Correlation and bounded numerical-verification outcomes retained
            separately with an aggregate software disposition.

        Raises
        ------
        TypeError
            If either tolerance has the wrong exact quantity representation.
        ValueError
            If a tolerance, decoded wire, correlation, or represented numerical
            comparison is invalid.
        OverflowError
            If a retained integer cannot be represented as binary64.
        MemoryError
            If a required dense numerical allocation cannot be completed.

        Notes
        -----
        A passing result covers only implemented reconstructable channels and the
        supplied tolerances. It does not establish physical adequacy, convergence,
        provenance, uncertainty quantification, or acceptance.
        """
        return Periodic1DIsolatedBandCampaignVerifier().execute(
            Periodic1DIsolatedBandCampaignVerificationRequest(
                self.encoded_documents,
                absolute_tolerance,
                curvature_absolute_tolerance,
            )
        )
