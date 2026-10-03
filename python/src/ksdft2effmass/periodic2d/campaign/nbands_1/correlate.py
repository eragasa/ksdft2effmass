"""Correlation Actionizer for retained isolated periodic-2D payloads."""

import hashlib
from dataclasses import dataclass

from .calculate import (
    Periodic2DIsolatedBandCalculationRequest,
    Periodic2DIsolatedBandCalculationWorkflow,
)
from .definition import Periodic2DIsolatedBandProvenance
from .encoded_documents import Periodic2DIsolatedBandEncodedDocuments
from .serialization.decoding import JsonValue, Periodic2DCampaignJsonDecoder


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignCorrelationRequest:
    """Request typed correlation of isolated encoded documents."""

    encoded_documents: Periodic2DIsolatedBandEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact isolated campaign document type."""
        if type(self.encoded_documents) is not Periodic2DIsolatedBandEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DIsolatedBandEncodedDocuments"
            )


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignCorrelationResult:
    """Report semantic and canonical retained identity channels."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str

    @property
    def passes(self) -> bool:
        """Return whether semantic and canonical byte identities both agree."""
        return self.semantic_identity and self.canonical_byte_identity


class Periodic2DIsolatedBandCampaignCorrelator:
    """Recalculate and correlate isolated retained encoded documents."""

    __slots__ = ()

    workflow = Periodic2DIsolatedBandCalculationWorkflow()
    decoder = Periodic2DCampaignJsonDecoder()

    def execute(
        self, request: Periodic2DIsolatedBandCampaignCorrelationRequest
    ) -> Periodic2DIsolatedBandCampaignCorrelationResult:
        """Return retained-compatible semantic and byte identity channels."""
        if type(request) is not Periodic2DIsolatedBandCampaignCorrelationRequest:
            raise TypeError(
                "request must be Periodic2DIsolatedBandCampaignCorrelationRequest"
            )
        documents = request.encoded_documents
        retained = self.decoder.document(documents.result_payload)
        provenance_value = retained.get("provenance")
        if not isinstance(provenance_value, dict):
            raise ValueError("retained provenance must be an object")
        provenance = provenance_value
        calculated = self.workflow.execute(
            Periodic2DIsolatedBandCalculationRequest(
                documents.input_payload,
                Periodic2DIsolatedBandProvenance(
                    input_path=self._string(provenance.get("input_path"), "input_path"),
                    input_sha256=self._string(
                        provenance.get("input_sha256"), "input_sha256"
                    ),
                    script_path=self._string(
                        provenance.get("script_path"), "script_path"
                    ),
                    script_sha256=self._string(
                        provenance.get("script_sha256"), "script_sha256"
                    ),
                    python_version=self._string(
                        provenance.get("python_version"), "python_version"
                    ),
                    numpy_version=self._string(
                        provenance.get("numpy_version"), "numpy_version"
                    ),
                    scipy_algorithm=self._string(
                        provenance.get("scipy_algorithm"), "scipy_algorithm"
                    ),
                    floating_point=self._string(
                        provenance.get("floating_point"), "floating_point"
                    ),
                ),
            )
        ).document
        return Periodic2DIsolatedBandCampaignCorrelationResult(
            semantic_identity=self.decoder.document(calculated.payload) == retained,
            canonical_byte_identity=calculated.payload == documents.result_payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=self._sha256(documents.result_payload),
        )

    @staticmethod
    def _string(value: JsonValue, field: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{field} must be a nonempty string")
        return value

    @staticmethod
    def _sha256(payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()
