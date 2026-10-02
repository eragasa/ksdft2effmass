"""Encapsulating façade for the finite-rank analytical oracle."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from .encoded_documents import FiniteRankOracleEncodedDocuments
from .result_documents import FiniteRankOracleCampaignResultDocument
from .verification import (
    FiniteRankOracleCampaignVerifier,
    FiniteRankOracleVerificationRequest,
    FiniteRankOracleVerificationResult,
)
from .workflow import (
    FiniteRankOracleCampaignInputDeserializer,
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

    encoded_documents: FiniteRankOracleEncodedDocuments

    def __post_init__(self) -> None:
        """Require the exact encoded-document type."""
        if type(self.encoded_documents) is not FiniteRankOracleEncodedDocuments:
            raise TypeError(
                "encoded_documents must be FiniteRankOracleEncodedDocuments"
            )

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
    ) -> FiniteRankOracleCampaignResultDocument:
        """Calculate the oracle campaign under explicit adapter provenance."""
        return self._calculate(
            repository_root,
            FiniteRankOracleProvenance(
                input_path,
                input_sha256,
                script_path,
                script_sha256,
                python_version,
                numpy_version,
            ),
        )

    def retained_result(self) -> FiniteRankOracleCampaignResultDocument:
        """Return retained bytes without calculating or verifying them."""
        return FiniteRankOracleCampaignResultDocument(
            self.encoded_documents.retained_result_document
        )

    def correlate_retained(
        self, repository_root: Path
    ) -> FiniteRankOracleResultCorrelation:
        """Recalculate using an explicit root and report identity correlation."""
        retained = self.retained_result()
        calculated = self._calculate(repository_root, self._retained_provenance())
        return FiniteRankOracleResultCorrelation(
            semantic_identity=(
                self._decode(calculated.payload) == self._decode(retained.payload)
            ),
            canonical_byte_identity=calculated.payload == retained.payload,
            calculated_sha256=calculated.sha256,
            retained_sha256=retained.sha256,
        )

    def verify_retained(
        self, repository_root: Path
    ) -> FiniteRankOracleVerificationResult:
        """Independently authenticate and reconstruct the retained oracle result."""
        return FiniteRankOracleCampaignVerifier().execute(
            FiniteRankOracleVerificationRequest(self.encoded_documents, repository_root)
        )

    def _calculate(
        self, repository_root: Path, provenance: FiniteRankOracleProvenance
    ) -> FiniteRankOracleCampaignResultDocument:
        """Decode, authenticate, and execute the campaign Workflow."""
        specification = FiniteRankOracleCampaignInputDeserializer().execute(
            self.encoded_documents.input_document
        )
        parent = FiniteRankOracleParentDataLoader().execute(
            specification, repository_root
        )
        return FiniteRankOracleCampaignWorkflow().execute(
            specification, parent, provenance
        )

    def _retained_provenance(self) -> FiniteRankOracleProvenance:
        """Decode the fixed retained provenance used only for correlation."""
        root = self._decode(self.encoded_documents.retained_result_document)
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
