"""Encapsulating façade for separated continuum refinement."""

import json
from dataclasses import dataclass
from typing import cast

from .model import ContinuumRefinementCampaignModel
from .verification import (
    ContinuumRefinementCampaignVerifier,
    ContinuumRefinementVerificationRequest,
    ContinuumRefinementVerificationResult,
)
from .workflow import (
    ContinuumParentLoader,
    ContinuumRefinementCampaignCalculator,
    ContinuumRefinementCampaignResultDocument,
    ContinuumRefinementInputDeserializer,
    ContinuumRefinementProvenance,
    ContinuumResultSerializer,
    JsonValue,
)


@dataclass(frozen=True, slots=True)
class ContinuumRefinementResultCorrelation:
    """Report semantic and canonical retained identity channels."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str


@dataclass(frozen=True, slots=True)
class ContinuumRefinementCampaign:
    """Encapsulate one separated continuum-refinement campaign."""

    model: ContinuumRefinementCampaignModel

    def __post_init__(self) -> None:
        """Require the exact campaign model type."""
        if type(self.model) is not ContinuumRefinementCampaignModel:
            raise TypeError("model must be ContinuumRefinementCampaignModel")

    def retained_result(self) -> ContinuumRefinementCampaignResultDocument:
        """Return retained bytes without calculating or verifying them."""
        return ContinuumRefinementCampaignResultDocument(
            self.model.retained_result_document
        )

    def correlate_retained(self) -> ContinuumRefinementResultCorrelation:
        """Recalculate under retained provenance and report identity correlation."""
        retained = self.retained_result()
        calculated = self._calculate(self._retained_provenance())
        return ContinuumRefinementResultCorrelation(
            semantic_identity=self._decode(calculated.payload)
            == self._decode(retained.payload),
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(self) -> ContinuumRefinementVerificationResult:
        """Independently authenticate and reconstruct every refinement axis."""
        return ContinuumRefinementCampaignVerifier().execute(
            ContinuumRefinementVerificationRequest(self.model)
        )

    def _calculate(
        self, provenance: ContinuumRefinementProvenance
    ) -> ContinuumRefinementCampaignResultDocument:
        """Decode, authenticate, calculate, and serialize one campaign."""
        specification = ContinuumRefinementInputDeserializer().execute(
            self.model.input_document
        )
        parent = ContinuumParentLoader().execute(
            self.model.repository_root, specification
        )
        result = ContinuumRefinementCampaignCalculator(specification, parent).execute(
            provenance
        )
        return ContinuumRefinementCampaignResultDocument(
            ContinuumResultSerializer().execute(result)
        )

    def _retained_provenance(self) -> ContinuumRefinementProvenance:
        """Decode retained provenance used only for identity correlation."""
        root = self._decode(self.model.retained_result_document)
        value = root.get("provenance")
        if not isinstance(value, dict):
            raise ValueError("retained provenance must be an object")
        implementations = value.get("implementation_identities")
        implementation_path: str | None = None
        implementation_sha256: str | None = None
        if implementations is not None:
            if not isinstance(implementations, list) or len(implementations) != 1:
                raise ValueError("one retained implementation identity is required")
            identity = implementations[0]
            if not isinstance(identity, dict):
                raise ValueError("implementation identity must be an object")
            implementation_path = self._string(identity.get("path"), "path")
            implementation_sha256 = self._string(identity.get("sha256"), "sha256")
        return ContinuumRefinementProvenance(
            input_sha256=self._string(value.get("input_sha256"), "input_sha256"),
            implementation_path=implementation_path,
            implementation_sha256=implementation_sha256,
            python_version=self._string(value.get("python"), "python"),
            numpy_version=self._string(value.get("numpy"), "numpy"),
        )

    @classmethod
    def _decode(cls, payload: bytes) -> dict[str, JsonValue]:
        """Decode strict UTF-8 JSON for retained correlation."""
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
        """Reject duplicate result keys."""
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
        """Require one nonempty string."""
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name} must be a nonempty string")
        return value
