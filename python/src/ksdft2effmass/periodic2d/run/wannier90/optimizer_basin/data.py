"""Immutable composition root for the portable optimizer-basin study."""

from dataclasses import dataclass
from pathlib import Path

from .encoded_documents import Periodic2DOptimizerBasinEncodedDocuments
from .verify import (
    Periodic2DOptimizerBasinCampaignVerificationRequest,
    Periodic2DOptimizerBasinCampaignVerificationResult,
    Periodic2DOptimizerBasinCampaignVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaign:
    """Encapsulate the retained nine-configuration, eight-start study.

    Parameters
    ----------
    encoded_documents
        Exact input and result wires for the bounded optimizer-basin campaign.

    Raises
    ------
    TypeError
        If ``encoded_documents`` is not the exact campaign document type.

    Notes
    -----
    This immutable campaign composes exact wires with a fresh portable verifier Action
    for each request. It owns no replaceable verifier collaborator and performs no
    calculator execution, native-artifact discovery, scientific acceptance, or global
    optimizer inference.
    """

    encoded_documents: Periodic2DOptimizerBasinEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact optimizer-basin encoded-document type."""
        if type(self.encoded_documents) is not Periodic2DOptimizerBasinEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DOptimizerBasinEncodedDocuments"
            )

    def verify(
        self, *, repository_root: Path
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Verify bounded retained structure without native external-file access.

        Parameters
        ----------
        repository_root
            Absolute root used only for confined compact-source authentication.

        Returns
        -------
        Periodic2DOptimizerBasinCampaignVerificationResult
            Immutable bounded verification diagnostics.

        Raises
        ------
        TypeError
            If ``repository_root`` or decoded retained values violate their exact type
            contracts.
        ValueError
            If the root, strict wire, finite values, digest syntax, or confined source
            declarations are invalid.
        KeyError
            If a required verifier-owned field is absent.
        OSError
            If a confined directly declared compact source cannot be read.
        AssertionError
            If verifier-owned retained identities, structure, or dispositions disagree.
        MemoryError
            If decoding cannot allocate its representation.
        RecursionError
            If a retained document exceeds decoding or validation recursion depth.

        Notes
        -----
        Passing establishes only the portable verifier contract. It does not establish
        native execution authenticity, convergence, global optimality, scientific
        validation, uncertainty quantification, or acceptance.
        """
        verifier = Periodic2DOptimizerBasinCampaignVerifier()
        return verifier.execute(
            Periodic2DOptimizerBasinCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
