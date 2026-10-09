"""Immutable campaign composition for portable optimizer-basin reanalysis."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerReanalysisEncodedDocuments
from .verify import (
    Periodic2DOptimizerReanalysisCampaignVerificationRequest,
    Periodic2DOptimizerReanalysisCampaignVerificationResult,
    Periodic2DOptimizerReanalysisCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaign:
    """Compose exact reanalysis wires with a request-scoped verifier Action.

    Parameters
    ----------
    encoded_documents
        Exact source-result and reanalysis-result documents.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact campaign document type.

    Notes
    -----
    The campaign retains no shared or replaceable verifier collaborator. It does not
    access native external data, rerun Wannier90, establish optimizer completeness,
    validate a material, quantify uncertainty, or record scientific acceptance.
    """

    encoded_documents: Periodic2DOptimizerReanalysisEncodedDocuments

    def __post_init__(self) -> None:
        """Require exact reanalysis encoded-document ownership."""
        if (
            type(self.encoded_documents)
            is not Periodic2DOptimizerReanalysisEncodedDocuments
        ):
            raise TypeError(
                "encoded_documents must be "
                "Periodic2DOptimizerReanalysisEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerReanalysisCampaignVerificationResult:
        """Verify bounded retained diagnostics without native external-file access.

        Parameters
        ----------
        repository_root
            Absolute root used for confined compact-source and maintained estimator
            fixture authentication.

        Returns
        -------
        Periodic2DOptimizerReanalysisCampaignVerificationResult
            Immutable bounded verification diagnostics.

        Raises
        ------
        TypeError
            If request or decoded values violate exact representation contracts.
        ValueError
            If root, strict JSON, finite-real, digest, coordinate, or confinement
            contracts fail.
        OverflowError
            If an integer-to-binary64 conversion is not finite.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined compact source or estimator fixture cannot be read.
        AssertionError
            If retained identities, arithmetic, classifications, basin partitions, or
            refinements disagree.
        MemoryError
            If decoding or dense permutation comparison cannot allocate required state.
        RecursionError
            If retained JSON exceeds parser or validation recursion depth.

        Notes
        -----
        A pass establishes the frozen portable-verification contract only. It does not
        authenticate external native execution or establish scientific validation.
        """
        verifier = Periodic2DOptimizerReanalysisCampaignVerifier()
        return verifier.execute(
            Periodic2DOptimizerReanalysisCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
