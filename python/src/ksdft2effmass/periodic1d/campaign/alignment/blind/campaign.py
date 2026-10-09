"""Encapsulating DataObject and campaign-level Actions for blind alignment."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .baseline import BlindAlignmentBaselineLoader
from .encoded_documents import BlindAlignmentEncodedDocuments
from .result_encoding import BlindAlignmentRetainedResultCorrelator
from .result_records import (
    BlindAlignmentCampaignResult,
    BlindAlignmentProvenance,
    BlindAlignmentResultCorrelation,
    BlindAlignmentResultCorrelationRequest,
)
from .result_serialization import BlindAlignmentResultDeserializer
from .serialization import BlindAlignmentInputDeserializer
from .verification import (
    BlindAlignmentCampaignVerificationRequest,
    BlindAlignmentCampaignVerificationResult,
    BlindAlignmentCampaignVerifier,
)
from .workflow import (
    BlindAlignmentCampaignWorkflow,
    BlindAlignmentCampaignWorkflowRequest,
)


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignCalculationRequest:
    """Request campaign calculation from encapsulated state and explicit provenance.

    Parameters
    ----------
    encoded_documents
        Exact input and retained-result document bytes.
    repository_root
        Absolute filesystem base for repository-relative authenticated sources.
    provenance
        Provenance supplied by the caller's execution adapter. The request does not
        derive historical provenance from encoded documents or repository location.

    Raises
    ------
    TypeError
        If documents, repository root, or provenance use unsupported public types.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction validates location syntax only and performs no filesystem access.
    The caller retains responsibility for selecting the repository root; the downstream
    baseline loader authenticates repository-relative sources before calculation.
    """

    encoded_documents: BlindAlignmentEncodedDocuments
    repository_root: Path
    provenance: BlindAlignmentProvenance

    def __post_init__(self) -> None:
        """Require exact documents, an absolute root, and typed provenance.

        Raises
        ------
        TypeError
            If any composed value has an unsupported public type.
        ValueError
            If the repository root is relative.
        """
        if type(self.encoded_documents) is not BlindAlignmentEncodedDocuments:
            raise TypeError("encoded_documents must be BlindAlignmentEncodedDocuments")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be a pathlib.Path")
        # Keep the caller-owned path unresolved: construction checks only that source
        # resolution has an explicit absolute base and does not touch the filesystem.
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        if not isinstance(self.provenance, BlindAlignmentProvenance):
            raise TypeError("provenance must be BlindAlignmentProvenance")


class BlindAlignmentCampaignCalculator:
    """Decode, authenticate, and calculate one complete blind-alignment campaign."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentCampaignCalculationRequest
    ) -> BlindAlignmentCampaignResult:
        """Calculate one campaign through explicit typed boundaries.

        Parameters
        ----------
        request
            Encapsulated documents, repository path, and execution provenance.

        Returns
        -------
        BlindAlignmentCampaignResult
            Complete typed synthetic campaign result.

        Raises
        ------
        TypeError
            If the request has the wrong public type.
        ValueError
            If decoding, source authentication, or campaign construction fails.
        """
        if not isinstance(request, BlindAlignmentCampaignCalculationRequest):
            raise TypeError("request must be BlindAlignmentCampaignCalculationRequest")
        specification = BlindAlignmentInputDeserializer().execute(
            request.encoded_documents.input_document
        )
        baseline = BlindAlignmentBaselineLoader().execute(
            specification, request.repository_root
        )
        return BlindAlignmentCampaignWorkflow().execute(
            BlindAlignmentCampaignWorkflowRequest(
                specification=specification,
                baseline=baseline,
                provenance=request.provenance,
            )
        )


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignRetainedCorrelationRequest:
    """Request retained compatibility reconstruction from encapsulated state.

    Parameters
    ----------
    encoded_documents
        Exact input and retained-result document bytes.
    repository_root
        Absolute filesystem base for repository-relative authenticated sources.

    Raises
    ------
    TypeError
        If documents or repository root use unsupported public types.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction performs no filesystem access. The later correlator uses the explicit
    root to authenticate sources while reusing retained provenance solely for historical
    result reconstruction; it does not claim current execution under that provenance.
    """

    encoded_documents: BlindAlignmentEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Require exact documents and an absolute repository root.

        Raises
        ------
        TypeError
            If documents or repository root have unsupported public types.
        ValueError
            If the repository root is relative.
        """
        if type(self.encoded_documents) is not BlindAlignmentEncodedDocuments:
            raise TypeError("encoded_documents must be BlindAlignmentEncodedDocuments")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be a pathlib.Path")
        # Retain the explicit caller boundary without cwd-dependent normalization or
        # ambient repository discovery during request construction.
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


class BlindAlignmentCampaignRetainedCorrelator:
    """Reconstruct under retained provenance and report identity-only correlation."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentCampaignRetainedCorrelationRequest
    ) -> BlindAlignmentResultCorrelation:
        """Correlate a compatibility reconstruction with retained bytes.

        The retained provenance is reused only to reconstruct the historical document
        identity. This operation does not claim that the current process ran under the
        historical adapter and does not numerically verify the result.

        Parameters
        ----------
        request
            Encoded documents and explicit repository-resolution request.

        Returns
        -------
        BlindAlignmentResultCorrelation
            Semantic, canonical-byte, and digest identity channels.

        Raises
        ------
        TypeError
            If the request has the wrong public type.
        ValueError
            If decoding, authentication, calculation, or correlation fails.
        """
        if not isinstance(request, BlindAlignmentCampaignRetainedCorrelationRequest):
            raise TypeError(
                "request must be BlindAlignmentCampaignRetainedCorrelationRequest"
            )
        retained = BlindAlignmentResultDeserializer().deserialize(
            request.encoded_documents.retained_result_document
        )
        calculated = BlindAlignmentCampaignCalculator().execute(
            BlindAlignmentCampaignCalculationRequest(
                encoded_documents=request.encoded_documents,
                repository_root=request.repository_root,
                provenance=retained.provenance,
            )
        )
        return BlindAlignmentRetainedResultCorrelator().execute(
            BlindAlignmentResultCorrelationRequest(
                calculated_result=calculated,
                retained_payload=request.encoded_documents.retained_result_document,
            )
        )


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaign:
    """Encapsulate blind-alignment documents behind a small public façade.

    Parameters
    ----------
    encoded_documents
        Exact immutable input and retained-result documents.
    """

    encoded_documents: BlindAlignmentEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not BlindAlignmentEncodedDocuments:
            raise TypeError("encoded_documents must be BlindAlignmentEncodedDocuments")

    def calculate(
        self,
        *,
        repository_root: Path,
        input_path: str,
        input_sha256: str,
        script_path: str,
        script_sha256: str,
        python_version: str,
        numpy_version: str,
    ) -> BlindAlignmentCampaignResult:
        """Delegate calculation with explicit execution-provenance fields.

        Parameters
        ----------
        repository_root
            Absolute filesystem base for authenticated repository-relative sources.
        input_path
            Repository-relative input path used by the execution adapter.
        input_sha256
            SHA-256 identity of that input.
        script_path
            Repository-relative execution-adapter path.
        script_sha256
            SHA-256 identity of that adapter.
        python_version
            Python version reported by the adapter.
        numpy_version
            NumPy version reported by the adapter.

        Returns
        -------
        BlindAlignmentCampaignResult
            Complete typed campaign result.

        Raises
        ------
        TypeError
            If a request, provenance field, or decoded source field has an invalid
            semantic type.
        ValueError
            If the root is relative, source authentication fails, or a campaign
            invariant is invalid.
        OverflowError
            If a decoded real value cannot be represented as finite binary64.
        MemoryError
            If the dense synthetic campaign matrices cannot be allocated.
        """
        provenance = BlindAlignmentProvenance(
            input_path=input_path,
            input_sha256=input_sha256,
            script_path=script_path,
            script_sha256=script_sha256,
            python_version=python_version,
            numpy_version=numpy_version,
        )
        # Action collaborators are operation-scoped so the immutable facade retains
        # documents only and cannot acquire hidden execution state between calls.
        return BlindAlignmentCampaignCalculator().execute(
            BlindAlignmentCampaignCalculationRequest(
                self.encoded_documents, repository_root, provenance
            )
        )

    def retained_result(self) -> BlindAlignmentCampaignResult:
        """Decode the retained result without calculating or verifying it.

        Returns
        -------
        BlindAlignmentCampaignResult
            Typed retained result decoded from the encapsulated exact bytes.

        Raises
        ------
        TypeError
            If a retained JSON field has an invalid semantic primitive type.
        ValueError
            If the result schema or an intrinsic result invariant is invalid.
        OverflowError
            If a JSON number cannot be represented as finite binary64.
        """
        return BlindAlignmentResultDeserializer().deserialize(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> BlindAlignmentResultCorrelation:
        """Recalculate and correlate the retained result.

        Parameters
        ----------
        repository_root
            Absolute filesystem root used to resolve authenticated source paths.

        Returns
        -------
        BlindAlignmentResultCorrelation
            Exact-byte and typed-result correlation outcome.

        Raises
        ------
        TypeError
            If ``repository_root`` or decoded source fields have invalid types.
        ValueError
            If the root is relative, source authentication fails, or reconstructed
            campaign data disagree with the retained result.
        OverflowError
            If a decoded real value cannot be represented as finite binary64.
        MemoryError
            If dense campaign matrices cannot be allocated.
        """
        return BlindAlignmentCampaignRetainedCorrelator().execute(
            BlindAlignmentCampaignRetainedCorrelationRequest(
                self.encoded_documents, repository_root
            )
        )

    def verify_retained(
        self, repository_root: Path
    ) -> BlindAlignmentCampaignVerificationResult:
        """Independently verify the retained synthetic result.

        Parameters
        ----------
        repository_root
            Absolute filesystem root used to resolve authenticated source paths.

        Returns
        -------
        BlindAlignmentCampaignVerificationResult
            Separate source-authentication, structural-contract, and independent
            numerical-reconstruction channels.

        Raises
        ------
        TypeError
            If ``repository_root`` or a decoded source field has an invalid type.
        ValueError
            If source authentication, a closed schema, or an independently
            reconstructed numerical channel fails.
        OverflowError
            If a decoded real value cannot be represented as finite binary64.
        MemoryError
            If dense independent-verification matrices cannot be allocated.
        """
        return BlindAlignmentCampaignVerifier().execute(
            BlindAlignmentCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
