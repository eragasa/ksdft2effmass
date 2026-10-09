"""Immutable composition root for the retained composite periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from .correlate import (
    Periodic2DCompositeCampaignCorrelationRequest,
    Periodic2DCompositeCampaignCorrelationResult,
    Periodic2DCompositeCampaignCorrelator,
)
from .encoded_documents import Periodic2DCompositeEncodedDocuments
from .verify import (
    Periodic2DCompositeCampaignVerificationRequest,
    Periodic2DCompositeCampaignVerificationResult,
    Periodic2DCompositeCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DCompositeCampaign:
    """Compose exact composite-band documents with request-scoped operations.

    Parameters
    ----------
    encoded_documents
        Exact retained input and result bytes.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact composite document type.

    Notes
    -----
    This owner keeps campaign evidence distinct from retained spaces, represented
    operators, and effective models. Missing authenticated frame/projector arrays are
    reported as unavailable rather than inferred from rank or spectra.
    """

    encoded_documents: Periodic2DCompositeEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact composite encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DCompositeEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DCompositeEncodedDocuments"
            )

    def correlate(self) -> Periodic2DCompositeCampaignCorrelationResult:
        """Correlate the retained composite documents.

        Returns
        -------
        Periodic2DCompositeCampaignCorrelationResult
            Exact retained-document correlation diagnostics.

        Raises
        ------
        TypeError
            If decoded fields have incompatible representations.
        ValueError
            If schema, finite-value, or digest contracts fail.
        AssertionError
            If retained input and result identities disagree.
        MemoryError
            If strict decoding cannot allocate its representation.
        """
        return Periodic2DCompositeCampaignCorrelator().execute(
            Periodic2DCompositeCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DCompositeCampaignVerificationResult:
        """Independently verify the retained composite calculation.

        Parameters
        ----------
        repository_root
            Absolute repository root for confined producer authentication.

        Returns
        -------
        Periodic2DCompositeCampaignVerificationResult
            Typed gap, projection, localization, authentication, and reconstruction
            diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed field has an incompatible representation.
        ValueError
            If schema, numeric, digest, or confinement contracts fail.
        OSError
            If a confined maintained producer cannot be read.
        AssertionError
            If source authentication or independent reconstruction disagrees.
        MemoryError
            If decoding or dense eigensystem work cannot allocate required state.

        Notes
        -----
        Passing does not establish asymptotic convergence, global gauge optimality,
        scientific validation, uncertainty quantification, or acceptance.
        """
        return Periodic2DCompositeCampaignVerifier().execute(
            Periodic2DCompositeCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
