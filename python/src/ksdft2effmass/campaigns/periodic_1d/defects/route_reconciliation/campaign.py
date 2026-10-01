"""Encapsulating façade and campaign-level route-reconciliation Actionizers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import cast

from .model import RouteReconciliationCampaignModel
from .verification import (
    RouteReconciliationCampaignVerifier,
    RouteReconciliationVerificationRequest,
    RouteReconciliationVerificationResult,
)
from .workflow import (
    JsonValue,
    RouteReconciliationBaselineLoader,
    RouteReconciliationCampaignInputDeserializer,
    RouteReconciliationCampaignResultDocument,
    RouteReconciliationCampaignWorkflow,
    RouteReconciliationProvenance,
)


@dataclass(frozen=True, slots=True)
class RouteReconciliationResultCorrelation:
    """Report semantic-document and canonical-byte retained identity channels."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str

    def __post_init__(self) -> None:
        """Validate Booleans and lowercase SHA-256 identities."""
        if type(self.semantic_identity) is not bool:
            raise TypeError("semantic_identity must be Boolean")
        if type(self.canonical_byte_identity) is not bool:
            raise TypeError("canonical_byte_identity must be Boolean")
        for digest in (self.calculated_sha256, self.retained_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("correlation digests must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class RouteReconciliationCampaign:
    """Encapsulate one route-reconciliation campaign behind a small façade."""

    model: RouteReconciliationCampaignModel

    def __post_init__(self) -> None:
        """Require the exact campaign model type."""
        if type(self.model) is not RouteReconciliationCampaignModel:
            raise TypeError("model must be RouteReconciliationCampaignModel")

    def calculate(
        self,
        *,
        input_path: str,
        input_sha256: str,
        script_path: str,
        script_sha256: str,
        python_version: str,
        numpy_version: str,
    ) -> RouteReconciliationCampaignResultDocument:
        """Calculate all route records under explicit adapter provenance."""
        return self._calculate(
            RouteReconciliationProvenance(
                input_path=input_path,
                input_sha256=input_sha256,
                script_path=script_path,
                script_sha256=script_sha256,
                python_version=python_version,
                numpy_version=numpy_version,
            )
        )

    def retained_result(self) -> RouteReconciliationCampaignResultDocument:
        """Return the retained result document without calculating or verifying it."""
        return RouteReconciliationCampaignResultDocument(
            self.model.retained_result_document
        )

    def correlate_retained(self) -> RouteReconciliationResultCorrelation:
        """Reconstruct under retained provenance and report identity correlation."""
        retained = self.retained_result()
        calculated = self._calculate(self._retained_provenance())
        retained_value = self._decode(retained.payload)
        calculated_value = self._decode(calculated.payload)
        return RouteReconciliationResultCorrelation(
            semantic_identity=calculated_value == retained_value,
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(self) -> RouteReconciliationVerificationResult:
        """Independently authenticate and reconstruct the retained campaign."""
        return RouteReconciliationCampaignVerifier().execute(
            RouteReconciliationVerificationRequest(self.model)
        )

    def _calculate(
        self, provenance: RouteReconciliationProvenance
    ) -> RouteReconciliationCampaignResultDocument:
        """Decode, authenticate, and execute the typed campaign Workflow."""
        specification = RouteReconciliationCampaignInputDeserializer().execute(
            self.model.input_document
        )
        baseline = RouteReconciliationBaselineLoader().execute(
            specification, self.model.repository_root
        )
        return RouteReconciliationCampaignWorkflow().execute(
            specification, baseline, provenance
        )

    def _retained_provenance(self) -> RouteReconciliationProvenance:
        """Decode only the fixed retained provenance needed for correlation."""
        root = self._decode(self.model.retained_result_document)
        provenance_value = root.get("provenance")
        if not isinstance(provenance_value, dict):
            raise ValueError("retained provenance must be an object")
        provenance = provenance_value
        expected = {
            "input_path",
            "input_sha256",
            "script_path",
            "script_sha256",
            "python_version",
            "numpy_version",
        }
        if set(provenance) != expected:
            raise ValueError("retained provenance fields are unsupported")
        return RouteReconciliationProvenance(
            input_path=self._string(provenance["input_path"], "input_path"),
            input_sha256=self._string(provenance["input_sha256"], "input_sha256"),
            script_path=self._string(provenance["script_path"], "script_path"),
            script_sha256=self._string(provenance["script_sha256"], "script_sha256"),
            python_version=self._string(provenance["python_version"], "python_version"),
            numpy_version=self._string(provenance["numpy_version"], "numpy_version"),
        )

    @classmethod
    def _decode(cls, payload: bytes) -> dict[str, JsonValue]:
        """Decode strict JSON objects for retained correlation only."""
        try:
            value = json.loads(
                payload.decode("utf-8"),
                object_pairs_hook=cls._unique_object,
                parse_constant=cls._reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as error:
            raise ValueError("result must be valid strict UTF-8 JSON") from error
        if not isinstance(value, dict):
            raise ValueError("result root must be an object")
        return cast(dict[str, JsonValue], value)

    @staticmethod
    def _unique_object(
        pairs: list[tuple[str, JsonValue]],
    ) -> dict[str, JsonValue]:
        """Reject duplicate result-object keys."""
        result: dict[str, JsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(value: str) -> JsonValue:
        """Reject non-finite JSON constants."""
        raise ValueError(f"non-finite JSON constant is unsupported: {value}")

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        """Require one nonempty string field."""
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value
