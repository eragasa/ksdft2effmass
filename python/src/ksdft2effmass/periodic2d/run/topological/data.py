"""Immutable composition root for the retained topological benchmark."""

from dataclasses import dataclass
from pathlib import Path

from .correlate import (
    Periodic2DTopologicalCampaignCorrelationRequest,
    Periodic2DTopologicalCampaignCorrelationResult,
    Periodic2DTopologicalCampaignCorrelator,
)
from .encoded_documents import Periodic2DTopologicalEncodedDocuments
from .verify import (
    Periodic2DTopologicalCampaignVerificationRequest,
    Periodic2DTopologicalCampaignVerificationResult,
    Periodic2DTopologicalCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalCampaign:
    """Compose exact three-model topological benchmark documents.

    Parameters
    ----------
    encoded_documents
        Exact retained input and observation bytes.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact topological document type.

    Notes
    -----
    Retained Chern and Wilson values are observations to reconstruct, not qualified
    expected-result oracles. Model identities and parameter meanings come from the
    strict campaign schema rather than names, dimensions, or spectra.
    """

    encoded_documents: Periodic2DTopologicalEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact topological encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DTopologicalEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DTopologicalEncodedDocuments"
            )

    def correlate(self) -> Periodic2DTopologicalCampaignCorrelationResult:
        """Correlate the retained documents with the maintained route.

        Returns
        -------
        Periodic2DTopologicalCampaignCorrelationResult
            Exact retained-document identity and correlation diagnostics.

        Raises
        ------
        TypeError
            If strict decoded fields have incompatible representations.
        ValueError
            If schema or digest contracts fail.
        AssertionError
            If retained identities or declared model ordering disagree.
        MemoryError
            If strict decoding cannot allocate its representation.
        """
        return Periodic2DTopologicalCampaignCorrelator().execute(
            Periodic2DTopologicalCampaignCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalCampaignVerificationResult:
        """Independently reconstruct all retained model observations.

        Parameters
        ----------
        repository_root
            Absolute repository root for confined runner authentication.

        Returns
        -------
        Periodic2DTopologicalCampaignVerificationResult
            Bounded authentication and numerical-reconstruction diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed field has an incompatible representation.
        ValueError
            If schema, finite-value, digest, or confinement contracts fail.
        OSError
            If the confined maintained runner cannot be read.
        AssertionError
            If reconstructed spectra or topology disagree with retained observations.
        MemoryError
            If mesh operators or projectors cannot be allocated.

        Notes
        -----
        Passing establishes synthetic finite-mesh consistency, not a material claim,
        continuum convergence, scientific validation, uncertainty, or acceptance.
        """
        return Periodic2DTopologicalCampaignVerifier().execute(
            Periodic2DTopologicalCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
