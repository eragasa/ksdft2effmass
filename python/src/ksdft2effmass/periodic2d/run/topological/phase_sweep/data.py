"""Immutable composition root for the retained topological phase sweep."""

from dataclasses import dataclass
from pathlib import Path

from .correlate import (
    Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest,
    Periodic2DTopologicalPhaseSweepCampaignCorrelationResult,
    Periodic2DTopologicalPhaseSweepCampaignCorrelator,
)
from .encoded_documents import Periodic2DTopologicalPhaseSweepEncodedDocuments
from .verify import (
    Periodic2DTopologicalPhaseSweepCampaignVerificationRequest,
    Periodic2DTopologicalPhaseSweepCampaignVerificationResult,
    Periodic2DTopologicalPhaseSweepCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaign:
    """Compose exact three-model topological phase-sweep documents.

    Parameters
    ----------
    encoded_documents
        Exact retained sweep input and observation bytes.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact phase-sweep document type.

    Notes
    -----
    Sample outcomes are observations rather than expected-result oracles. Analytic
    outcomes at declared transition points remain explicitly unavailable (``null``)
    and are not imputed from neighboring samples.
    """

    encoded_documents: Periodic2DTopologicalPhaseSweepEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact phase-sweep encoded-document type."""
        if (
            type(self.encoded_documents)
            is not Periodic2DTopologicalPhaseSweepEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DTopologicalPhaseSweepEncodedDocuments"
            )

    def correlate(self) -> Periodic2DTopologicalPhaseSweepCampaignCorrelationResult:
        """Correlate retained and maintained sweep documents.

        Returns
        -------
        Periodic2DTopologicalPhaseSweepCampaignCorrelationResult
            Exact source/result identity and sweep-correlation diagnostics.

        Raises
        ------
        TypeError
            If strict decoded fields have incompatible representations.
        ValueError
            If schema, axis, or digest contracts fail.
        AssertionError
            If retained source/result declarations disagree.
        MemoryError
            If strict decoding cannot allocate its representation.
        """
        return Periodic2DTopologicalPhaseSweepCampaignCorrelator().execute(
            Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest(
                self.encoded_documents
            )
        )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DTopologicalPhaseSweepCampaignVerificationResult:
        """Independently reconstruct every retained sweep sample.

        Parameters
        ----------
        repository_root
            Absolute repository root for confined runner authentication.

        Returns
        -------
        Periodic2DTopologicalPhaseSweepCampaignVerificationResult
            Bounded source-authentication and reconstruction diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed field has an incompatible representation.
        ValueError
            If schema, axis, finite-value, digest, or confinement contracts fail.
        OSError
            If the confined maintained runner cannot be read.
        AssertionError
            If reconstructed sample observations or explicit unavailable outcomes
            disagree.
        MemoryError
            If finite-mesh numerical work cannot allocate required state.

        Notes
        -----
        Passing establishes synthetic finite-sweep consistency only; it is not a phase
        diagram convergence proof, scientific validation, UQ, or acceptance.
        """
        return Periodic2DTopologicalPhaseSweepCampaignVerifier().execute(
            Periodic2DTopologicalPhaseSweepCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
