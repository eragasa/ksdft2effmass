"""Encapsulating façade for the finite-rank analytical oracle."""

import json
from dataclasses import dataclass
from typing import cast

from .model import FiniteRankOracleCampaignModel
from .verification import (
    FiniteRankOracleCampaignVerifier,
    FiniteRankOracleVerificationRequest,
    FiniteRankOracleVerificationResult,
)
from .workflow import (
    FiniteRankOracleCampaignInputDeserializer,
    FiniteRankOracleCampaignResultDocument,
    FiniteRankOracleCampaignWorkflow,
    FiniteRankOracleParentDataLoader,
    FiniteRankOracleProvenance,
    JsonValue,
)


@dataclass(frozen=True, slots=True)
class FiniteRankOracleResultCorrelation:
    """Report semantic and canonical retained-result identity channels."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str


@dataclass(frozen=True, slots=True)
class FiniteRankOracleCampaign:
    """Encapsulate one finite-rank oracle campaign behind a small façade."""

    model: FiniteRankOracleCampaignModel

    def __post_init__(self) -> None:
        """Require the exact campaign model type."""
        if type(self.model) is not FiniteRankOracleCampaignModel:
            raise TypeError("model must be FiniteRankOracleCampaignModel")

    def calculate(
        self,
        *,
        input_path: str,
        input_sha256: str,
        script_path: str,
        script_sha256: str,
        python_version: str,
        numpy_version: str,
    ) -> FiniteRankOracleCampaignResultDocument:
        """Calculate the oracle campaign under explicit adapter provenance."""
        return self._calculate(
            FiniteRankOracleProvenance(
                input_path,
                input_sha256,
                script_path,
                script_sha256,
                python_version,
                numpy_version,
            )
        )

    def retained_result(self) -> FiniteRankOracleCampaignResultDocument:
        """Return retained bytes without calculating or verifying them."""
        return FiniteRankOracleCampaignResultDocument(
            self.model.retained_result_document
        )

    def correlate_retained(self) -> FiniteRankOracleResultCorrelation:
        """Recalculate under retained provenance and report identity correlation."""
        retained = self.retained_result()
        calculated = self._calculate(self._retained_provenance())
        return FiniteRankOracleResultCorrelation(
            semantic_identity=(
                self._decode(calculated.payload) == self._decode(retained.payload)
            ),
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(self) -> FiniteRankOracleVerificationResult:
        """Independently authenticate and reconstruct the retained oracle result."""
        return FiniteRankOracleCampaignVerifier().execute(
            FiniteRankOracleVerificationRequest(self.model)
        )

    def _calculate(
        self, provenance: FiniteRankOracleProvenance
    ) -> FiniteRankOracleCampaignResultDocument:
        """Decode, authenticate, and execute the campaign Workflow."""
        specification = FiniteRankOracleCampaignInputDeserializer().execute(
            self.model.input_document
        )
        parent = FiniteRankOracleParentDataLoader().execute(
            specification, self.model.repository_root
        )
        return FiniteRankOracleCampaignWorkflow().execute(
            specification, parent, provenance
        )

    def _retained_provenance(self) -> FiniteRankOracleProvenance:
        """Decode the fixed retained provenance used only for correlation."""
        root = self._decode(self.model.retained_result_document)
        value = root.get("provenance")
        if not isinstance(value, dict):
            raise ValueError("retained provenance must be an object")
        expected = {
            "input_path",
            "input_sha256",
            "script_path",
            "script_sha256",
            "python_version",
            "numpy_version",
        }
        if set(value) != expected:
            raise ValueError("retained provenance fields are unsupported")
        return FiniteRankOracleProvenance(
            self._string(value["input_path"], "input_path"),
            self._string(value["input_sha256"], "input_sha256"),
            self._string(value["script_path"], "script_path"),
            self._string(value["script_sha256"], "script_sha256"),
            self._string(value["python_version"], "python_version"),
            self._string(value["numpy_version"], "numpy_version"),
        )

    @classmethod
    def _decode(cls, payload: bytes) -> dict[str, JsonValue]:
        """Decode strict JSON for retained correlation."""
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
