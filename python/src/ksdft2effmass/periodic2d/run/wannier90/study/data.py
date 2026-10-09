"""Immutable composition root for the portable Wannier90 study."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DWannier90StudyEncodedDocuments
from .verify import (
    Periodic2DWannier90StudyCampaignVerificationRequest,
    Periodic2DWannier90StudyCampaignVerificationResult,
    Periodic2DWannier90StudyCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaign:
    """Compose the retained six-case portable Wannier90 study.

    Parameters
    ----------
    encoded_documents
        Exact study input and result bytes.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact study document type.

    Notes
    -----
    Reciprocal-mesh, cutoff, and auxiliary-embedding cases are finite campaign
    observations, not convergence proof. Native-format parsing and artifact ownership
    remain with ``ksdft2effmass.integration.wannier90``.
    """

    encoded_documents: Periodic2DWannier90StudyEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact study encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DWannier90StudyEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DWannier90StudyEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90StudyCampaignVerificationResult:
        """Verify all portable cases without native external files.

        Parameters
        ----------
        repository_root
            Absolute repository root confining referenced retained cases and sources.

        Returns
        -------
        Periodic2DWannier90StudyCampaignVerificationResult
            Bounded source-authentication and six-case reconstruction diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed field has an incompatible representation.
        ValueError
            If strict schema, case, finite-value, digest, or confinement contracts fail.
        OSError
            If a confined retained case or maintained source cannot be read.
        AssertionError
            If case identities or reconstructed observations disagree.
        MemoryError
            If strict decoding or numerical reconstruction cannot allocate state.

        Notes
        -----
        Passing neither reruns Wannier90 nor establishes convergence, scientific
        validation, uncertainty quantification, transferability, or acceptance.
        """
        return Periodic2DWannier90StudyCampaignVerifier().execute(
            Periodic2DWannier90StudyCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
