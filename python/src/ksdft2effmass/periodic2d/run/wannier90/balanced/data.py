"""Immutable composition root for the balanced Wannier90 comparison."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DWannier90BalancedEncodedDocuments
from .verify import (
    Periodic2DWannier90BalancedCampaignVerificationRequest,
    Periodic2DWannier90BalancedCampaignVerificationResult,
    Periodic2DWannier90BalancedCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedCampaign:
    """Compose one retained repository-portable Wannier90 comparison.

    Parameters
    ----------
    encoded_documents
        Exact retained result bytes with embedded portable evidence.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact balanced document type.

    Notes
    -----
    This campaign does not read a native run tree. General native-format parsing and
    artifact ownership belong to ``ksdft2effmass.integration.wannier90``; the campaign
    reconstructs only retained portable evidence.
    """

    encoded_documents: Periodic2DWannier90BalancedEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact balanced encoded-document type."""
        if (
            type(self.encoded_documents)
            is not Periodic2DWannier90BalancedEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be Periodic2DWannier90BalancedEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DWannier90BalancedCampaignVerificationResult:
        """Verify portable evidence without accessing native external files.

        Parameters
        ----------
        repository_root
            Absolute repository root confining the maintained extractor identity.

        Returns
        -------
        Periodic2DWannier90BalancedCampaignVerificationResult
            Retained-result identity and bounded reconstruction diagnostics.

        Raises
        ------
        TypeError
            If the root or a consumed field has an incompatible representation.
        ValueError
            If strict schema, finite-value, or confinement contracts fail.
        OSError
            If the confined maintained extractor cannot be read.
        AssertionError
            If content authentication or portable reconstruction disagrees.
        MemoryError
            If decoding or dense matrix reconstruction cannot allocate state.

        Notes
        -----
        Passing does not authenticate absent native files, rerun Wannier90, prove
        localization convergence, or establish validation, UQ, or acceptance.
        """
        return Periodic2DWannier90BalancedCampaignVerifier().execute(
            Periodic2DWannier90BalancedCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
