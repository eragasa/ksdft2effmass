"""Immutable campaign composition for censored regression verification."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments
from .verify import (
    Periodic2DOptimizerRegressionCampaignVerificationRequest,
    Periodic2DOptimizerRegressionCampaignVerificationResult,
    Periodic2DOptimizerRegressionCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaign:
    """Compose exact encoded documents with request-scoped verification.

    Parameters
    ----------
    encoded_documents
        Exact standalone-result, analyzer, and regression-result wires.

    Raises
    ------
    TypeError
        If ``encoded_documents`` has an incompatible exact type.
    """

    encoded_documents: Periodic2DOptimizerRegressionEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document owner."""
        document_type = Periodic2DOptimizerRegressionEncodedDocuments
        if type(self.encoded_documents) is not document_type:
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerRegressionEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerRegressionCampaignVerificationResult:
        """Independently reconstruct retained regression diagnostics.

        Parameters
        ----------
        repository_root
            Absolute repository root used for maintained-file authentication.

        Returns
        -------
        Periodic2DOptimizerRegressionCampaignVerificationResult
            Bounded authentication and numerical-reconstruction result.

        Raises
        ------
        TypeError
            If ``repository_root`` or a decoded field has an incompatible type.
        ValueError
            If the root, strict JSON, finite values, counts, or probabilities are
            invalid.
        OverflowError
            If numerical reconstruction leaves finite binary64 range.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined maintained file cannot be read.
        AssertionError
            If retained identities, declarations, counts, or numerics disagree.
        numpy.linalg.LinAlgError
            If dense pseudoinversion or condition estimation fails.
        MemoryError
            If strict decoding or dense reconstruction cannot allocate state.
        RecursionError
            If a retained document exceeds strict-parser recursion depth.
        """
        verifier = Periodic2DOptimizerRegressionCampaignVerifier()
        return verifier.execute(
            Periodic2DOptimizerRegressionCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
