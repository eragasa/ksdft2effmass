"""Encapsulating DataObject and campaign-level Actionizers for blind alignment."""

from __future__ import annotations

from dataclasses import dataclass

from .baseline import BlindAlignmentBaselineLoader
from .model import BlindAlignmentCampaignModel
from .result_encoding import BlindAlignmentRetainedResultCorrelator
from .result_records import (
    BlindAlignmentCampaignResult,
    BlindAlignmentProvenance,
    BlindAlignmentResultCorrelation,
    BlindAlignmentResultCorrelationRequest,
)
from .result_serialization import BlindAlignmentResultDeserializer
from .serialization import BlindAlignmentInputDeserializer
from .workflow import (
    BlindAlignmentCampaignWorkflow,
    BlindAlignmentCampaignWorkflowRequest,
)


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignCalculationRequest:
    """Request campaign calculation from encapsulated state and explicit provenance.

    Parameters
    ----------
    model
        Exact retained-wire state and repository-resolution boundary.
    provenance
        Provenance supplied by the caller's execution adapter.
    """

    model: BlindAlignmentCampaignModel
    provenance: BlindAlignmentProvenance

    def __post_init__(self) -> None:
        """Require exact campaign model and provenance record types."""
        if type(self.model) is not BlindAlignmentCampaignModel:
            raise TypeError("model must be BlindAlignmentCampaignModel")
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
            request.model.input_document
        )
        baseline = BlindAlignmentBaselineLoader().execute(
            specification, request.model.repository_root
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
    model
        Exact input and retained-result documents plus repository root.
    """

    model: BlindAlignmentCampaignModel

    def __post_init__(self) -> None:
        """Require the exact encapsulated campaign model type."""
        if type(self.model) is not BlindAlignmentCampaignModel:
            raise TypeError("model must be BlindAlignmentCampaignModel")


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
            Encapsulated retained campaign model.

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
            request.model.retained_result_document
        )
        calculated = BlindAlignmentCampaignCalculator().execute(
            BlindAlignmentCampaignCalculationRequest(
                model=request.model,
                provenance=retained.provenance,
            )
        )
        return BlindAlignmentRetainedResultCorrelator().execute(
            BlindAlignmentResultCorrelationRequest(
                calculated_result=calculated,
                retained_payload=request.model.retained_result_document,
            )
        )


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaign:
    """Encapsulate one blind-alignment campaign model behind a small public façade.

    Parameters
    ----------
    model
        Exact immutable documents and repository-resolution boundary delegated to
        campaign Actionizers.
    """

    model: BlindAlignmentCampaignModel

    _calculator = BlindAlignmentCampaignCalculator()
    _retained_correlator = BlindAlignmentCampaignRetainedCorrelator()
    _result_deserializer = BlindAlignmentResultDeserializer()

    def __post_init__(self) -> None:
        """Require the exact campaign model type."""
        if type(self.model) is not BlindAlignmentCampaignModel:
            raise TypeError("model must be BlindAlignmentCampaignModel")

    def calculate(
        self,
        *,
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
            BlindAlignmentCampaignCalculationRequest(self.model, provenance)
        )

    def retained_result(self) -> BlindAlignmentCampaignResult:
        """Decode the retained result without calculating or verifying it."""
        return self._result_deserializer.deserialize(
            self.model.retained_result_document
        )

    def correlate_retained(self) -> BlindAlignmentResultCorrelation:
        """Delegate retained compatibility reconstruction and identity correlation."""
        return self._retained_correlator.execute(
            BlindAlignmentCampaignRetainedCorrelationRequest(self.model)
        )
