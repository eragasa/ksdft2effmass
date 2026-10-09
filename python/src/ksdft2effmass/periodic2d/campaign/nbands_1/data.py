"""Immutable composition root for the retained isolated periodic-2D campaign."""

from dataclasses import dataclass
from pathlib import Path

from .correlate import (
    Periodic2DIsolatedBandCampaignCorrelationRequest,
    Periodic2DIsolatedBandCampaignCorrelationResult,
    Periodic2DIsolatedBandCampaignCorrelator,
)
from .encoded_documents import Periodic2DIsolatedBandEncodedDocuments
from .verify import (
    Periodic2DIsolatedBandCampaignVerificationRequest,
    Periodic2DIsolatedBandCampaignVerificationResult,
    Periodic2DIsolatedBandCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaign:
    """Compose exact isolated-band documents with request-scoped operations.

    Parameters
    ----------
    encoded_documents
        Exact retained input and result bytes.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact family document type.

    Notes
    -----
    The campaign is not a scientific model or retained subspace. Detailed observations
    remain campaign evidence because authenticated frame/projector coordinates are
    unavailable; rank and spectra cannot replace those coordinates.
    """

    encoded_documents: Periodic2DIsolatedBandEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact isolated campaign document type."""
        if type(self.encoded_documents) is not Periodic2DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DIsolatedBandEncodedDocuments"
            )

    def correlate(self) -> Periodic2DIsolatedBandCampaignCorrelationResult:
        """Correlate the retained wires through a fresh correlation action.

        Returns
        -------
        Periodic2DIsolatedBandCampaignCorrelationResult
            Exact input/result content identities and correlation disposition.

        Raises
        ------
        TypeError
            If strict decoded fields have incompatible representations.
        ValueError
            If schema, finite-value, or digest contracts fail.
        AssertionError
            If the retained input/result correlation disagrees.
        MemoryError
            If strict decoding cannot allocate its representation.
        """
        return Periodic2DIsolatedBandCampaignCorrelator().execute(
            Periodic2DIsolatedBandCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DIsolatedBandCampaignVerificationResult:
        """Verify independently through a fresh action and typed request.

        Parameters
        ----------
        repository_root
            Absolute repository root for confined producer authentication.

        Returns
        -------
        Periodic2DIsolatedBandCampaignVerificationResult
            Bounded source-authentication and numerical-reconstruction diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed value has an incompatible representation.
        ValueError
            If schema, finite-value, digest, or confinement contracts fail.
        OSError
            If a confined maintained producer cannot be read.
        AssertionError
            If authentication or independent reconstruction disagrees.
        MemoryError
            If decoding or dense numerical work cannot allocate required state.

        Notes
        -----
        Passing verifies retained software/numerical consistency only, not convergence,
        physical adequacy, scientific validation, uncertainty, or acceptance.
        """
        return Periodic2DIsolatedBandCampaignVerifier().execute(
            Periodic2DIsolatedBandCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
