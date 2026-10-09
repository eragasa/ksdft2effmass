"""Immutable campaign composition for the portable standalone optimizer study."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerStandaloneEncodedDocuments
from .verify import (
    Periodic2DOptimizerStandaloneCampaignVerificationRequest,
    Periodic2DOptimizerStandaloneCampaignVerificationResult,
    Periodic2DOptimizerStandaloneCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaign:
    """Encapsulate exact standalone optimizer-study documents.

    Parameters
    ----------
    encoded_documents
        Exact proposal, deterministic initial-gauge, and retained-result bytes.

    Notes
    -----
    This campaign owns no external native run tree and creates a fresh verifier for each
    request. Passing verification is not scientific validation or acceptance.
    """

    encoded_documents: Periodic2DOptimizerStandaloneEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact standalone encoded-document owner."""
        if (
            type(self.encoded_documents)
            is not Periodic2DOptimizerStandaloneEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerStandaloneEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerStandaloneCampaignVerificationResult:
        """Verify retained compact evidence without accessing native run files.

        Parameters
        ----------
        repository_root
            Absolute repository root for confined maintained-file authentication.

        Returns
        -------
        Periodic2DOptimizerStandaloneCampaignVerificationResult
            Bounded authentication and reconstruction result.

        Raises
        ------
        TypeError
            If the root, wire, or consumed field has an incompatible exact type.
        ValueError
            If the root, JSON, digest, or consumed numeric value is invalid.
        OverflowError
            If a consumed integer cannot be represented in binary64.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined compact source cannot be read.
        AssertionError
            If authentication or reconstruction disagrees with retained evidence.
        MemoryError
            If decoding or record construction cannot allocate state.
        RecursionError
            If a retained document exceeds parser or validation recursion depth.
        """
        request = Periodic2DOptimizerStandaloneCampaignVerificationRequest(
            self.encoded_documents, repository_root
        )
        return Periodic2DOptimizerStandaloneCampaignVerifier().execute(request)
