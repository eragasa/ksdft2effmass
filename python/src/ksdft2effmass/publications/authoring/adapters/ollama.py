"""Loopback-only Ollama adaptation for bounded manuscript inference."""

from __future__ import annotations

import http.client
import json
import math
from dataclasses import dataclass
from typing import ClassVar, cast

from ..inference import ManuscriptInferenceRequest, ManuscriptInferenceResponse
from .ollama_retention import OllamaResponseRetention

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


@dataclass(frozen=True, slots=True, kw_only=True)
class OllamaLoopbackManuscriptInferenceAdapter:
    """Run one bounded inference request through a fixed loopback Ollama model.

    Parameters
    ----------
    response_retention
        Atomic mode-0600 ignored-cache retention Action. Exact chat-response bytes are
        retained before parsing; accepted or rejected decoded metadata is retained
        before returning to composition or re-raising.
    port
        TCP port of an Ollama service on the literal IPv4 loopback host. The default
        is Ollama's standard local port. The host, API paths, model name, model digest,
        generation bounds, and absence of tools are fixed by the implementation.

    Notes
    -----
    The adapter uses ``http.client`` directly with ``127.0.0.1`` and therefore does
    not honor proxy settings or follow redirects. It verifies the installed model
    digest before generation, sends no tool definition, permits no remote fallback,
    and performs no manuscript or bibliography operation. Its only filesystem effect
    is the required bounded response retention supplied by ``response_retention``.
    A typed response remains a candidate for the author's independent failed-closed
    admission; it is not human acceptance or scientific validation.
    """

    MODEL_NAME: ClassVar[str] = "qwen3.5:9b"
    MODEL_SHA256: ClassVar[str] = (
        "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"
    )
    INFERENCE_IMPLEMENTATION_ID: ClassVar[str] = (
        "ollama-loopback-manuscript-inference:model:qwen3.5-9b:sha256:"
        "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"
    )
    HOST: ClassVar[str] = "127.0.0.1"
    TAGS_PATH: ClassVar[str] = "/api/tags"
    CHAT_PATH: ClassVar[str] = "/api/chat"
    TIMEOUT_SECONDS: ClassVar[int] = 300
    MAX_PROMPT_UTF8_BYTES: ClassVar[int] = 32_768
    MAX_HTTP_RESPONSE_BYTES: ClassVar[int] = 65_536
    NUM_CONTEXT_TOKENS: ClassVar[int] = 32_768
    MAX_PREDICT_TOKENS: ClassVar[int] = 4_096

    response_retention: OllamaResponseRetention
    port: int = 11_434

    def __post_init__(self) -> None:
        """Reject non-integer, privileged, or out-of-range loopback ports."""
        if type(self.response_retention) is not OllamaResponseRetention:
            raise TypeError("response_retention must be OllamaResponseRetention")
        if type(self.port) is not int:
            raise TypeError("port must be a built-in int excluding bool")
        if not 1_024 <= self.port <= 65_535:
            raise ValueError("port must be between 1024 and 65535")

    def infer(
        self, request: ManuscriptInferenceRequest, /
    ) -> ManuscriptInferenceResponse:
        """Return one bounded typed response from the fixed local model.

        Parameters
        ----------
        request
            Exact request produced by the manuscript author.

        Returns
        -------
        ManuscriptInferenceResponse
            Strictly decoded candidate text and warnings combined with citation,
            evidence, and marker lineage copied from the immutable request.

        Raises
        ------
        TypeError
            If the request or decoded wire values have incorrect semantic types.
        ValueError
            If request bounds, model identity, response structure, or response bounds
            are violated.
        RuntimeError
            If the loopback service is unavailable or returns a non-success status.
        """
        if type(request) is not ManuscriptInferenceRequest:
            raise TypeError("request must be ManuscriptInferenceRequest")
        prompt_bytes = request.prompt.encode("utf-8")
        if len(prompt_bytes) > self.MAX_PROMPT_UTF8_BYTES:
            raise ValueError("prompt exceeds the Ollama adapter UTF-8 byte bound")

        self._verify_model_identity()
        raw_response = self._exchange_bytes(
            method="POST",
            path=self.CHAT_PATH,
            payload=self._chat_payload(request),
        )
        raw_artifact = self.response_retention.retain_raw(
            request.inference_request_id, raw_response
        )
        outer = self._decode_object(raw_response, "Ollama chat response")
        if self._required_string(outer, "model", "chat response") != self.MODEL_NAME:
            raise ValueError("Ollama response model does not match the fixed model")
        if not self._required_boolean(outer, "done", "chat response"):
            raise ValueError("Ollama response is not complete")
        if self._required_string(outer, "done_reason", "chat response") != "stop":
            raise ValueError("Ollama response did not terminate normally")

        message = self._required_object(outer, "message", "chat response")
        if (
            self._required_string(message, "role", "chat response.message")
            != "assistant"
        ):
            raise ValueError("Ollama response role must be assistant")
        if "tool_calls" in message and message["tool_calls"] not in (None, []):
            raise ValueError("Ollama returned tool calls although tools are disabled")
        content = self._required_string(message, "content", "chat response.message")
        generated = self._decode_object(content.encode("utf-8"), "generated response")
        self._require_exact_keys(
            generated,
            {"replacement_text", "warning_codes"},
            "generated response",
        )

        warning_codes = self._string_tuple(
            self._required_array(generated, "warning_codes", "generated response"),
            "generated response.warning_codes",
        )
        replacement_text = self._required_string(
            generated, "replacement_text", "generated response"
        )
        try:
            response = ManuscriptInferenceResponse(
                inference_request_id=request.inference_request_id,
                inference_implementation_id=self.INFERENCE_IMPLEMENTATION_ID,
                replacement_text=replacement_text,
                citations=request.expected_citations,
                evidence_ids=request.expected_evidence_ids,
                warning_codes=warning_codes,
                evidence_marker_ids=request.required_evidence_marker_ids,
            )
        except (TypeError, ValueError) as error:
            self.response_retention.retain_decoded_rejection(
                raw_artifact,
                model_name=self.MODEL_NAME,
                model_sha256=self.MODEL_SHA256,
                generated_content=content,
                generated_keys=tuple(sorted(generated)),
                replacement_text=replacement_text,
                warning_codes=warning_codes,
                error_type=type(error).__name__,
            )
            raise
        self.response_retention.retain_parsed(
            raw_artifact,
            response,
            model_name=self.MODEL_NAME,
            model_sha256=self.MODEL_SHA256,
        )
        return response

    def _verify_model_identity(self) -> None:
        """Require one exact locally installed name-and-digest pair."""
        response_bytes = self._exchange_bytes(
            method="GET", path=self.TAGS_PATH, payload=None
        )
        payload = self._decode_object(response_bytes, "Ollama tags response")
        models = self._required_array(payload, "models", "tags response")
        matches: list[str] = []
        for index, value in enumerate(models):
            model = self._object(value, f"tags response.models[{index}]")
            name_value = model.get("name")
            if type(name_value) is str and name_value == self.MODEL_NAME:
                matches.append(
                    self._required_string(
                        model, "digest", f"tags response.models[{index}]"
                    )
                )
        if matches != [self.MODEL_SHA256]:
            raise ValueError("fixed Ollama model name and digest are not installed")

    def _exchange_bytes(
        self,
        *,
        method: str,
        path: str,
        payload: JsonObject | None,
    ) -> bytes:
        """Exchange one bounded JSON document with the literal loopback service."""
        body = (
            None
            if payload is None
            else json.dumps(
                payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
        )
        headers = (
            {}
            if body is None
            else {
                "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8",
            }
        )
        connection = http.client.HTTPConnection(
            self.HOST, self.port, timeout=self.TIMEOUT_SECONDS
        )
        try:
            connection.request(method, path, body=body, headers=headers)
            response = connection.getresponse()
            response_body = response.read(self.MAX_HTTP_RESPONSE_BYTES + 1)
        except (OSError, http.client.HTTPException, TimeoutError) as error:
            raise RuntimeError("loopback Ollama request failed") from error
        finally:
            connection.close()
        if response.status != 200:
            raise RuntimeError(
                f"loopback Ollama returned unexpected HTTP status {response.status}"
            )
        if len(response_body) > self.MAX_HTTP_RESPONSE_BYTES:
            raise ValueError("loopback Ollama response exceeds the byte bound")
        return response_body

    def _chat_payload(self, request: ManuscriptInferenceRequest) -> JsonObject:
        """Construct the bounded no-tools structured-generation request."""
        response_schema: JsonObject = {
            "type": "object",
            "additionalProperties": False,
            "required": ["replacement_text", "warning_codes"],
            "properties": {
                "replacement_text": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": request.max_output_characters,
                },
                "warning_codes": {
                    "type": "array",
                    "description": (
                        "Return [] for output compliant with declared abstract-only "
                        "scope and evidence-marker gaps. Use nonempty codes only for "
                        "inability or ambiguity beyond those represented constraints; "
                        "nonempty warnings fail closed."
                    ),
                    "items": {"type": "string", "minLength": 1, "maxLength": 128},
                    "maxItems": ManuscriptInferenceResponse.MAX_WARNINGS,
                    "uniqueItems": True,
                },
            },
        }
        return {
            "model": self.MODEL_NAME,
            "messages": [{"role": "user", "content": request.prompt}],
            "stream": False,
            "think": False,
            "format": response_schema,
            "keep_alive": "0s",
            "options": {
                "num_ctx": self.NUM_CONTEXT_TOKENS,
                "num_predict": self.MAX_PREDICT_TOKENS,
                "seed": 0,
                "temperature": 0,
            },
        }

    @classmethod
    def _decode_object(cls, payload: bytes, context: str) -> JsonObject:
        """Strictly decode one UTF-8 JSON object into the closed JSON domain."""
        try:
            text = payload.decode("utf-8", errors="strict")
            decoded: object = json.loads(
                text, object_pairs_hook=cls._decoded_object_from_pairs
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"{context} must be valid UTF-8 JSON") from error
        return cls._object(cls._json_value(decoded), context)

    @staticmethod
    def _decoded_object_from_pairs(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        """Construct one decoded object while rejecting duplicate member names."""
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"JSON object contains duplicate member {key!r}")
            result[key] = value
        return result

    @classmethod
    def _json_value(cls, value: object) -> JsonValue:
        """Convert a decoded value into the closed recursive JSON representation."""
        if value is None or type(value) in (bool, int, str):
            return cast(JsonScalar, value)
        if type(value) is float:
            if not math.isfinite(value):
                raise ValueError("JSON numbers must be finite")
            return value
        if type(value) is list:
            return [cls._json_value(item) for item in cast(list[object], value)]
        if type(value) is dict:
            result: JsonObject = {}
            for key, item in cast(dict[object, object], value).items():
                if type(key) is not str:
                    raise TypeError("JSON object keys must be built-in strings")
                result[key] = cls._json_value(item)
            return result
        raise TypeError("decoded content contains a value outside the JSON domain")

    @staticmethod
    def _object(value: JsonValue, context: str) -> JsonObject:
        """Require one JSON object."""
        if type(value) is not dict:
            raise TypeError(f"{context} must be a JSON object")
        return value

    @staticmethod
    def _require_exact_keys(
        value: JsonObject, expected: set[str], context: str
    ) -> None:
        """Require one exact closed object shape."""
        if set(value) != expected:
            raise ValueError(f"{context} must contain exactly {sorted(expected)!r}")

    @classmethod
    def _required_object(cls, value: JsonObject, key: str, context: str) -> JsonObject:
        """Require one named JSON object member."""
        if key not in value:
            raise ValueError(f"{context}.{key} is required")
        return cls._object(value[key], f"{context}.{key}")

    @staticmethod
    def _required_array(value: JsonObject, key: str, context: str) -> list[JsonValue]:
        """Require one named JSON-array member."""
        if key not in value:
            raise ValueError(f"{context}.{key} is required")
        result = value[key]
        if type(result) is not list:
            raise TypeError(f"{context}.{key} must be a JSON array")
        return result

    @staticmethod
    def _required_string(value: JsonObject, key: str, context: str) -> str:
        """Require one named nonempty built-in string member."""
        if key not in value:
            raise ValueError(f"{context}.{key} is required")
        result = value[key]
        if type(result) is not str or not result:
            raise TypeError(f"{context}.{key} must be a nonempty built-in string")
        return result

    @staticmethod
    def _required_boolean(value: JsonObject, key: str, context: str) -> bool:
        """Require one named built-in Boolean member."""
        if key not in value:
            raise ValueError(f"{context}.{key} is required")
        result = value[key]
        if type(result) is not bool:
            raise TypeError(f"{context}.{key} must be a built-in bool")
        return result

    @staticmethod
    def _string_tuple(values: list[JsonValue], context: str) -> tuple[str, ...]:
        """Require a JSON array containing only built-in strings."""
        result: list[str] = []
        for index, value in enumerate(values):
            if type(value) is not str:
                raise TypeError(f"{context}[{index}] must be a built-in string")
            result.append(value)
        return tuple(result)
