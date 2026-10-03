"""Encapsulating DataObject and campaign-level Actionizers for blind alignment."""

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
        Provenance supplied by the caller's execution adapter.
    """

    encoded_documents: BlindAlignmentEncodedDocuments
    repository_root: Path
    provenance: BlindAlignmentProvenance

    def __post_init__(self) -> None:
        """Require exact documents, an absolute root, and typed provenance."""
        if type(self.encoded_documents) is not BlindAlignmentEncodedDocuments:
            raise TypeError("encoded_documents must be BlindAlignmentEncodedDocuments")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be a pathlib.Path")
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
    """

    encoded_documents: BlindAlignmentEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Require exact documents and an absolute repository root."""
        if type(self.encoded_documents) is not BlindAlignmentEncodedDocuments:
            raise TypeError("encoded_documents must be BlindAlignmentEncodedDocuments")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be a pathlib.Path")
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

    _calculator = BlindAlignmentCampaignCalculator()
    _retained_correlator = BlindAlignmentCampaignRetainedCorrelator()
    _result_deserializer = BlindAlignmentResultDeserializer()
    _verifier = BlindAlignmentCampaignVerifier()

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
        """
        provenance = BlindAlignmentProvenance(
            input_path=input_path,
            input_sha256=input_sha256,
            script_path=script_path,
            script_sha256=script_sha256,
            python_version=python_version,
            numpy_version=numpy_version,
        )
        return self._calculator.execute(
            BlindAlignmentCampaignCalculationRequest(
                self.encoded_documents, repository_root, provenance
            )
        )

    def retained_result(self) -> BlindAlignmentCampaignResult:
        """Decode the retained result without calculating or verifying it."""
        return self._result_deserializer.deserialize(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> BlindAlignmentResultCorrelation:
        """Delegate retained reconstruction using an explicit repository root."""
        return self._retained_correlator.execute(
            BlindAlignmentCampaignRetainedCorrelationRequest(
                self.encoded_documents, repository_root
            )
        )

    def verify_retained(
        self, repository_root: Path
    ) -> BlindAlignmentCampaignVerificationResult:
        """Delegate independent retained-result numerical verification.

        Returns
        -------
        BlindAlignmentCampaignVerificationResult
            Separate source-authentication, structural-contract, and independent
            numerical-reconstruction channels.
        """
        return self._verifier.execute(
            BlindAlignmentCampaignVerificationRequest(
                self.encoded_documents, repository_root
            )
        )
