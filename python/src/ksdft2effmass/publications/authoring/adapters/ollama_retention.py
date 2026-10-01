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
    None
    | bool
    | int
    | float
    | str
    | list[RetentionJsonValue]
    | dict[str, RetentionJsonValue]
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
    """Retain accepted/rejected and ordinary/exceptional records without replace.

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
    SAFE_STRUCTURE_KEY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Za-z][A-Za-z0-9_]{0,127}\Z"
    )
    SAFE_WARNING_CODE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Za-z0-9_.:-]{0,128}\Z"
    )
    REJECTION_STAGES: ClassVar[tuple[str, ...]] = (
        "outer_response_validation",
        "generated_response_validation",
        "typed_response_construction",
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

    def retain_decoded_rejection(
        self,
        raw: OllamaRawResponseArtifact,
        /,
        *,
        model_name: str,
        model_sha256: str,
        stage: str,
        outer_keys: tuple[str, ...],
        message_keys: tuple[str, ...] | None,
        generated_content: str | None,
        generated_keys: tuple[str, ...] | None,
        replacement_value_present: bool,
        replacement_value: RetentionJsonValue,
        warning_value_present: bool,
        warning_value: RetentionJsonValue,
        error_type: str,
    ) -> Path:
        """Retain excerpt-free structure after any successfully decoded response."""
        if type(raw) is not OllamaRawResponseArtifact:
            raise TypeError("raw must be OllamaRawResponseArtifact")
        self._validate_metadata_text("model_name", model_name, 256)
        self._validate_metadata_text("model_sha256", model_sha256, 128)
        if type(stage) is not str:
            raise TypeError("stage must be a built-in str")
        if stage not in self.REJECTION_STAGES:
            raise ValueError("stage must be a closed decoded-rejection stage")
        self._validate_key_tuple("outer_keys", outer_keys)
        if message_keys is not None:
            self._validate_key_tuple("message_keys", message_keys)
        if generated_content is not None:
            if type(generated_content) is not str:
                raise TypeError("generated_content must be a built-in str or None")
            content_bytes = generated_content.encode("utf-8")
            if not content_bytes or len(content_bytes) > self.MAX_RAW_RESPONSE_BYTES:
                raise ValueError(
                    "generated_content UTF-8 bytes must be nonempty and bounded"
                )
        else:
            content_bytes = None
        if generated_keys is not None:
            self._validate_key_tuple("generated_keys", generated_keys)
        for name, value in (
            ("replacement_value_present", replacement_value_present),
            ("warning_value_present", warning_value_present),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        self._validate_error_type(error_type)
        error_details = {
            "outer_response_validation": (
                "OUTER_RESPONSE_VALIDATION_REJECTED",
                "decoded outer response rejected by its contract",
            ),
            "generated_response_validation": (
                "GENERATED_RESPONSE_VALIDATION_REJECTED",
                "decoded generated response rejected by its contract",
            ),
            "typed_response_construction": (
                "TYPED_RESPONSE_CONTRACT_REJECTED",
                "decoded response rejected by typed response contract",
            ),
        }
        error_code, error_message = error_details[stage]
        generated_structure: dict[str, RetentionJsonValue] | None = None
        if content_bytes is not None:
            generated_structure = {
                "content_sha256": hashlib.sha256(content_bytes).hexdigest(),
                "content_utf8_bytes": len(content_bytes),
                "keys": (
                    None
                    if generated_keys is None
                    else self._key_summary(generated_keys)
                ),
                "replacement_value": self._value_summary(
                    replacement_value_present,
                    replacement_value,
                    include_safe_warning_codes=False,
                ),
                "warning_value": self._value_summary(
                    warning_value_present,
                    warning_value,
                    include_safe_warning_codes=True,
                ),
            }
        payload: dict[str, RetentionJsonValue] = {
            "record_type": "OLLAMA_DECODED_RESPONSE_REJECTION",
            "inference_request_id": raw.inference_request_id,
            "model_name": model_name,
            "model_sha256": model_sha256,
            "raw_response": {
                "path_name": raw.path.name,
                "sha256": raw.sha256,
                "byte_count": raw.byte_count,
            },
            "outer_structure": {
                "keys": self._key_summary(outer_keys),
                "message_keys": (
                    None if message_keys is None else self._key_summary(message_keys)
                ),
            },
            "generated_structure": generated_structure,
            "rejection": {
                "stage": stage,
                "error_code": error_code,
                "error_type": error_type,
                "error_message": error_message,
            },
        }
        return self._atomic_write_new(
            f"decoded-rejection-{raw.inference_request_id}.json",
            self._json_bytes(payload),
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

    def retain_exceptional_terminal(
        self,
        inference_request_id: str,
        /,
        *,
        error_type: str,
    ) -> Path:
        """Retain an exceptional run terminal record without a product result."""
        self._validate_request_id(inference_request_id)
        self._validate_error_type(error_type)
        raw_name = f"raw-{inference_request_id}.json"
        rejection_name = f"decoded-rejection-{inference_request_id}.json"
        parsed_name = f"parsed-{inference_request_id}.json"
        payload: dict[str, RetentionJsonValue] = {
            "record_type": "OLLAMA_EXCEPTIONAL_RUN_TERMINAL",
            "inference_request_id": inference_request_id,
            "failure": {
                "stage": "inference_execution",
                "error_code": "INFERENCE_EXCEPTION",
                "error_type": error_type,
                "error_message": "local inference failed closed",
            },
            "retained_path_names": {
                "raw": raw_name if (self.root / raw_name).is_file() else None,
                "decoded_rejection": (
                    rejection_name if (self.root / rejection_name).is_file() else None
                ),
                "parsed": parsed_name if (self.root / parsed_name).is_file() else None,
            },
            "inference_response_id": None,
            "authoring_result_id": None,
            "authoring_outcome": None,
            "human_acceptance_status": "not_evaluated",
        }
        return self._atomic_write_new(
            f"exceptional-terminal-{inference_request_id}.json",
            self._json_bytes(payload),
        )

    @classmethod
    def _validate_key_tuple(cls, name: str, keys: tuple[str, ...]) -> None:
        """Validate exact decoded object keys without requiring safe serialization."""
        if type(keys) is not tuple or any(type(key) is not str for key in keys):
            raise TypeError(f"{name} must be a built-in string tuple")
        if keys != tuple(sorted(set(keys))):
            raise ValueError(f"{name} must be unique and lexically sorted")

    @classmethod
    def _key_summary(cls, keys: tuple[str, ...]) -> dict[str, RetentionJsonValue]:
        """Return bounded key structure, exposing only identifier-shaped keys."""
        encoded = cls._json_value_bytes(list(keys))
        safe_keys: list[RetentionJsonValue] | None = None
        if len(keys) <= 64 and all(
            cls.SAFE_STRUCTURE_KEY_PATTERN.fullmatch(key) for key in keys
        ):
            safe_keys = []
            for key in keys:
                safe_keys.append(key)
        return {
            "count": len(keys),
            "sha256": hashlib.sha256(encoded).hexdigest(),
            "safe_keys": safe_keys,
        }

    @classmethod
    def _value_summary(
        cls,
        present: bool,
        value: RetentionJsonValue,
        /,
        *,
        include_safe_warning_codes: bool,
    ) -> dict[str, RetentionJsonValue] | None:
        """Summarize one decoded value without retaining arbitrary generated text."""
        if not present:
            return None
        encoded = cls._json_value_bytes(value)
        value_type = cls._json_value_type(value)
        summary: dict[str, RetentionJsonValue] = {
            "type": value_type,
            "sha256": hashlib.sha256(encoded).hexdigest(),
            "utf8_bytes": len(encoded),
        }
        if type(value) is str:
            value_bytes = value.encode("utf-8")
            summary["string_sha256"] = hashlib.sha256(value_bytes).hexdigest()
            summary["string_characters"] = len(value)
            summary["string_utf8_bytes"] = len(value_bytes)
        elif type(value) is list:
            counts: dict[str, int] = {}
            for item in value:
                item_type = cls._json_value_type(item)
                counts[item_type] = counts.get(item_type, 0) + 1
            summary["item_count"] = len(value)
            summary["item_type_counts"] = {key: counts[key] for key in sorted(counts)}
            safe_warning_codes: list[RetentionJsonValue] | None = None
            if (
                include_safe_warning_codes
                and len(value) <= ManuscriptInferenceResponse.MAX_WARNINGS
                and all(
                    type(item) is str
                    and cls.SAFE_WARNING_CODE_PATTERN.fullmatch(item) is not None
                    for item in value
                )
            ):
                safe_warning_codes = []
                for item in value:
                    if type(item) is str:
                        safe_warning_codes.append(item)
            if include_safe_warning_codes:
                summary["safe_warning_codes"] = safe_warning_codes
        elif type(value) is dict:
            summary["member_count"] = len(value)
        return summary

    @staticmethod
    def _json_value_type(value: RetentionJsonValue) -> str:
        """Return one closed JSON representation type name."""
        if value is None:
            return "null"
        if type(value) is bool:
            return "boolean"
        if type(value) is int:
            return "integer"
        if type(value) is float:
            return "number"
        if type(value) is str:
            return "string"
        if type(value) is list:
            return "array"
        if type(value) is dict:
            return "object"
        raise TypeError("value must be in the closed retention JSON domain")

    @staticmethod
    def _json_value_bytes(value: RetentionJsonValue) -> bytes:
        """Encode one closed JSON value canonically for excerpt-free hashing."""
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
            allow_nan=False,
        ).encode("utf-8")

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

    @staticmethod
    def _validate_metadata_text(name: str, value: str, maximum: int) -> None:
        """Validate one bounded excerpt-free metadata string."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if not value or value != value.strip() or len(value) > maximum:
            raise ValueError(f"{name} must be nonempty, trimmed, and bounded")

    @staticmethod
    def _validate_error_type(error_type: str) -> None:
        """Require one bounded built-in-style exception type name."""
        if type(error_type) is not str:
            raise TypeError("error_type must be a built-in str")
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,127}", error_type) is None:
            raise ValueError("error_type must be a bounded Python identifier")

    @classmethod
    def _validate_request_id(cls, inference_request_id: str) -> None:
        """Require the exact inference-request identity grammar used in filenames."""
        if type(inference_request_id) is not str:
            raise TypeError("inference_request_id must be a built-in str")
        if cls.REQUEST_ID_PATTERN.fullmatch(inference_request_id) is None:
            raise ValueError("inference_request_id has invalid grammar")
