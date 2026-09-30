"""Atomic ignored-cache retention for bounded local Ollama responses."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from ..inference import ManuscriptInferenceResponse
from ..proposal import ManuscriptAuthoringResult

type RetentionJsonValue = (
    None | bool | int | str | list[RetentionJsonValue] | dict[str, RetentionJsonValue]
)


@dataclass(frozen=True, slots=True, kw_only=True)
class OllamaRawResponseArtifact:
    """Identify one exact atomically retained raw local-model response."""

    inference_request_id: str
    path: Path
    sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        """Validate the exact retained-artifact description."""
        if type(self.inference_request_id) is not str:
            raise TypeError("inference_request_id must be a built-in str")
        if not self.inference_request_id:
            raise ValueError("inference_request_id must be nonempty")
        if not isinstance(self.path, Path):
            raise TypeError("path must be pathlib.Path")
        if (
            type(self.sha256) is not str
            or re.fullmatch(r"[0-9a-f]{64}", self.sha256) is None
        ):
            raise ValueError("sha256 must be lowercase SHA-256")
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in int excluding bool")
        if self.byte_count < 1:
            raise ValueError("byte_count must be positive")


@dataclass(frozen=True, slots=True, kw_only=True)
class OllamaResponseRetention:
    """Atomically retain raw, parsed, and terminal local-run records without replace.

    Parameters
    ----------
    root
        Existing or creatable ignored-cache directory. Runtime composition supplies
        ``.pi/cache/evidence-authoring/runtime``; tests may supply an isolated temporary
        directory. Every retained file is mode ``0600`` and every directory mode
        ``0700``.
    """

    MAX_RAW_RESPONSE_BYTES: ClassVar[int] = 65_536
    REQUEST_ID_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"manuscript-inference-request:sha256:[0-9a-f]{64}\Z"
    )

    root: Path

    def __post_init__(self) -> None:
        """Validate the configured local retention directory value."""
        if not isinstance(self.root, Path):
            raise TypeError("root must be pathlib.Path")
        if not self.root.name:
            raise ValueError("root must identify a directory")

    def retain_raw(
        self, inference_request_id: str, response_bytes: bytes, /
    ) -> OllamaRawResponseArtifact:
        """Atomically retain exact bounded response bytes before parsing."""
        self._validate_request_id(inference_request_id)
        if type(response_bytes) is not bytes:
            raise TypeError("response_bytes must be built-in bytes")
        if not 1 <= len(response_bytes) <= self.MAX_RAW_RESPONSE_BYTES:
            raise ValueError("raw response byte count is outside the retention bound")
        digest = hashlib.sha256(response_bytes).hexdigest()
        path = self._atomic_write_new(
            f"raw-{inference_request_id}.json",
            response_bytes,
        )
        return OllamaRawResponseArtifact(
            inference_request_id=inference_request_id,
            path=path,
            sha256=digest,
            byte_count=len(response_bytes),
        )

    def retain_parsed(
        self,
        raw: OllamaRawResponseArtifact,
        response: ManuscriptInferenceResponse,
        /,
        *,
        model_name: str,
        model_sha256: str,
    ) -> Path:
        """Atomically retain bounded parsed-response metadata without response text."""
        if type(raw) is not OllamaRawResponseArtifact:
            raise TypeError("raw must be OllamaRawResponseArtifact")
        if type(response) is not ManuscriptInferenceResponse:
            raise TypeError("response must be ManuscriptInferenceResponse")
        if response.inference_request_id != raw.inference_request_id:
            raise ValueError("parsed response and raw artifact request IDs differ")
        for name, value in (("model_name", model_name), ("model_sha256", model_sha256)):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty built-in str")
        payload: dict[str, RetentionJsonValue] = {
            "schema_version": 1,
            "record_type": "OLLAMA_PARSED_RESPONSE_METADATA",
            "inference_request_id": response.inference_request_id,
            "inference_response_id": response.response_id,
            "inference_implementation_id": response.inference_implementation_id,
            "model_name": model_name,
            "model_sha256": model_sha256,
            "raw_response": {
                "path_name": raw.path.name,
                "sha256": raw.sha256,
                "byte_count": raw.byte_count,
            },
            "replacement_text_sha256": hashlib.sha256(
                response.replacement_text.encode("utf-8")
            ).hexdigest(),
            "replacement_text_characters": len(response.replacement_text),
            "citations": [
                {
                    "citation_id": citation.citation_id,
                    "citation_key": citation.citation_key,
                    "evidence_ids": list(citation.evidence_ids),
                }
                for citation in response.citations
            ],
            "evidence_ids": list(response.evidence_ids),
            "evidence_marker_ids": list(response.evidence_marker_ids),
            "warning_codes": list(response.warning_codes),
        }
        return self._atomic_write_new(
            f"parsed-{response.inference_request_id}.json",
            self._json_bytes(payload),
        )

    def retain_terminal(
        self,
        inference_request_id: str,
        result: ManuscriptAuthoringResult,
        /,
    ) -> Path:
        """Atomically retain the terminal authoring outcome as separate metadata."""
        self._validate_request_id(inference_request_id)
        if type(result) is not ManuscriptAuthoringResult:
            raise TypeError("result must be ManuscriptAuthoringResult")
        payload: dict[str, RetentionJsonValue] = {
            "schema_version": 1,
            "record_type": "OLLAMA_TERMINAL_AUTHORING_OUTCOME",
            "inference_request_id": inference_request_id,
            "inference_response_id": result.inference_response_id,
            "authoring_request_id": result.request.request_id,
            "result_id": result.result_id,
            "outcome": result.outcome.value,
            "issues": [issue.value for issue in result.issues],
            "proposal_id": (
                None if result.proposal is None else result.proposal.proposal_id
            ),
            "human_acceptance_status": result.human_acceptance_status.value,
        }
        return self._atomic_write_new(
            f"terminal-{inference_request_id}.json",
            self._json_bytes(payload),
        )

    @staticmethod
    def _json_bytes(payload: dict[str, RetentionJsonValue]) -> bytes:
        """Encode one compact canonical metadata document."""
        return (
            json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

    def _atomic_write_new(self, filename: str, payload: bytes) -> Path:
        """Publish complete mode-0600 bytes atomically without replacement."""
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.root.is_symlink() or not self.root.is_dir():
            raise ValueError("retention root must be a non-symlink directory")
        os.chmod(self.root, 0o700)
        final = self.root / filename
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{filename}.", suffix=".tmp", dir=self.root
        )
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.link(temporary, final)
            os.chmod(final, 0o600)
            directory_descriptor = os.open(self.root, os.O_RDONLY)
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        finally:
            temporary.unlink(missing_ok=True)
        return final

    @classmethod
    def _validate_request_id(cls, inference_request_id: str) -> None:
        """Require the exact inference-request identity grammar used in filenames."""
        if type(inference_request_id) is not str:
            raise TypeError("inference_request_id must be a built-in str")
        if cls.REQUEST_ID_PATTERN.fullmatch(inference_request_id) is None:
            raise ValueError("inference_request_id has invalid grammar")
