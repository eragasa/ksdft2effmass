r"""Software verification of ``OllamaLoopbackManuscriptInferenceAdapter``.

Evidence profile: routine

Bounded artifact scope: fixed-model loopback manuscript-inference adaptation.

Facet and represented meaning

The module verifies fixed local model identity, bounded no-tools transport, strict
structured-response decoding, and exact facade identity.

Intrinsic and cross-object scope

The public adapter owns loopback transport, fixed-model preflight, no-tools request
construction, strict wire decoding, and conversion to the existing immutable response.
A synthetic in-process HTTP server supplies bounded protocol responses without invoking
Ollama or a model.

VVUQ and scientific exclusions

These tests do not establish model quality, historical or scientific correctness,
reference suitability, scientific validation, uncertainty quantification, publication
readiness, or human acceptance. They make no external call and write no artifact.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast

import pytest

import ksdft2effmass.publications as publications
from ksdft2effmass.publications.authoring import (
    OllamaLoopbackManuscriptInferenceAdapter,
)
from ksdft2effmass.publications.authoring.adapters.ollama import (
    OllamaLoopbackManuscriptInferenceAdapter as DefiningAdapter,
)
from ksdft2effmass.publications.authoring.adapters.ollama_retention import (
    OllamaResponseRetention,
)
from ksdft2effmass.publications.authoring.inference import ManuscriptInferenceRequest

pytestmark = pytest.mark.software_verification
SUT = OllamaLoopbackManuscriptInferenceAdapter


class TestOllamaLoopbackManuscriptInferenceAdapter:
    """Verify the concrete local-inference adapter without invoking a model."""

    @staticmethod
    def make_request(
        *, prompt: str = "Synthetic bounded prompt."
    ) -> ManuscriptInferenceRequest:
        """Return one bounded synthetic inference request."""
        return ManuscriptInferenceRequest(
            authoring_request_id="manuscript-authoring-request:sha256:" + "a" * 64,
            prompt=prompt,
            allowed_evidence_ids=("evidence:sha256:" + "b" * 64,),
            max_output_characters=2_000,
            max_citations=4,
        )

    @staticmethod
    def start_service(
        *,
        model_digest: str,
        generated_content: str,
        include_tool_call: bool = False,
    ) -> tuple[ThreadingHTTPServer, threading.Thread, list[tuple[str, str, bytes]]]:
        """Start one synthetic loopback HTTP service and return its request log."""
        requests: list[tuple[str, str, bytes]] = []

        class SyntheticOllamaHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                """Return the synthetic installed-model inventory."""
                requests.append(("GET", self.path, b""))
                payload = json.dumps(
                    {
                        "models": [
                            {
                                "name": DefiningAdapter.MODEL_NAME,
                                "model": DefiningAdapter.MODEL_NAME,
                                "digest": model_digest,
                            }
                        ]
                    },
                    separators=(",", ":"),
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def do_POST(self) -> None:
                """Return one bounded synthetic chat response."""
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                requests.append(("POST", self.path, body))
                message: dict[str, str | list[dict[str, str]]] = {
                    "role": "assistant",
                    "content": generated_content,
                }
                if include_tool_call:
                    message["tool_calls"] = [{"function": "forbidden"}]
                payload = json.dumps(
                    {
                        "model": DefiningAdapter.MODEL_NAME,
                        "message": message,
                        "done": True,
                        "done_reason": "stop",
                    },
                    separators=(",", ":"),
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, format: str, *args: object) -> None:
                """Suppress framework access logging for synthetic requests."""

        server = ThreadingHTTPServer((DefiningAdapter.HOST, 0), SyntheticOllamaHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread, requests

    @staticmethod
    def stop_service(server: ThreadingHTTPServer, thread: threading.Thread) -> None:
        """Stop and join one synthetic loopback service."""
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive()

    @staticmethod
    def valid_generated_content() -> str:
        """Return one exact structured synthetic model payload."""
        evidence_id = "evidence:sha256:" + "b" * 64
        return json.dumps(
            {
                "replacement_text": "Synthetic proposal text \\cite{Synthetic2026}.",
                "citations": [
                    {
                        "citation_key": "Synthetic2026",
                        "source_evidence_ids": [evidence_id],
                    }
                ],
                "evidence_ids": [evidence_id],
                "evidence_marker_ids": [],
                "warning_codes": [],
            },
            separators=(",", ":"),
        )

    def test_method__infer__returns_bounded_response_without_tools(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-017

        Requirement: The concrete adapter must verify the fixed local model and convert
        one no-tools loopback response into the existing bounded response contract.

        Acceptance: Synthetic GET and POST requests use only the two fixed API paths;
        the POST names the fixed model, disables streaming and thinking, omits tools,
        and the returned response preserves request, citation, and evidence identities.
        """
        server, thread, requests = self.start_service(
            model_digest=DefiningAdapter.MODEL_SHA256,
            generated_content=self.valid_generated_content(),
        )
        try:
            address = cast(tuple[str, int], server.server_address)
            request = self.make_request()
            response = DefiningAdapter(
                response_retention=OllamaResponseRetention(root=tmp_path),
                port=address[1],
            ).infer(request)
        finally:
            self.stop_service(server, thread)

        assert tuple((method, path) for method, path, _ in requests) == (
            ("GET", DefiningAdapter.TAGS_PATH),
            ("POST", DefiningAdapter.CHAT_PATH),
        )
        post_body = requests[1][2].decode("utf-8")
        post_payload = json.loads(post_body)
        assert f'"model":"{DefiningAdapter.MODEL_NAME}"' in post_body
        assert '"stream":false' in post_body
        assert '"think":false' in post_body
        assert '"tools"' not in post_body
        warning_schema = post_payload["format"]["properties"]["warning_codes"]
        assert warning_schema["description"] == (
            "Return [] for output compliant with declared abstract-only scope and "
            "evidence-marker gaps. Use nonempty codes only for inability or ambiguity "
            "beyond those represented constraints; nonempty warnings fail closed."
        )
        assert response.inference_request_id == request.inference_request_id
        assert response.inference_implementation_id == (
            DefiningAdapter.INFERENCE_IMPLEMENTATION_ID
        )
        assert response.citations[0].citation_key == "Synthetic2026"
        assert response.evidence_ids == request.allowed_evidence_ids
        assert response.warning_codes == ()
        raw_files = tuple(tmp_path.glob("raw-*.json"))
        parsed_files = tuple(tmp_path.glob("parsed-*.json"))
        assert len(raw_files) == len(parsed_files) == 1
        assert raw_files[0].stat().st_mode & 0o777 == 0o600
        assert parsed_files[0].stat().st_mode & 0o777 == 0o600
        parsed = json.loads(parsed_files[0].read_text())
        assert "schema_version" not in parsed
        assert parsed["inference_response_id"] == response.response_id
        assert parsed["warning_codes"] == []

    def test_method__infer__rejects_nonmatching_model_digest_before_chat(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-018

        Requirement: A model tag alone must not satisfy fixed-model identity.

        Acceptance: A mismatched digest raises ``ValueError`` after only the tags
        request, and no chat request reaches the synthetic service.
        """
        server, thread, requests = self.start_service(
            model_digest="0" * 64,
            generated_content=self.valid_generated_content(),
        )
        try:
            address = cast(tuple[str, int], server.server_address)
            with pytest.raises(ValueError, match="model name and digest"):
                DefiningAdapter(
                    response_retention=OllamaResponseRetention(root=tmp_path),
                    port=address[1],
                ).infer(self.make_request())
        finally:
            self.stop_service(server, thread)
        assert tuple((method, path) for method, path, _ in requests) == (
            ("GET", DefiningAdapter.TAGS_PATH),
        )

    def test_method__infer__rejects_oversized_utf8_prompt_before_transport(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-019

        Requirement: The concrete transport bound must be enforced before service use.

        Acceptance: A request valid under the general port contract but one byte beyond
        the adapter's UTF-8 bound raises ``ValueError`` without requiring a service.
        """
        request = self.make_request(
            prompt="x" * (DefiningAdapter.MAX_PROMPT_UTF8_BYTES + 1)
        )
        with pytest.raises(ValueError, match="UTF-8 byte bound"):
            DefiningAdapter(
                response_retention=OllamaResponseRetention(root=tmp_path)
            ).infer(request)

    def test_method__infer__rejects_returned_tool_calls(self, tmp_path: Path) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-020

        Requirement: The adapter must expose no model tool interface.

        Acceptance: Even if a synthetic service returns a tool call without being
        offered tools, the adapter raises ``ValueError`` and exposes no typed response.
        """
        server, thread, _ = self.start_service(
            model_digest=DefiningAdapter.MODEL_SHA256,
            generated_content=self.valid_generated_content(),
            include_tool_call=True,
        )
        try:
            address = cast(tuple[str, int], server.server_address)
            with pytest.raises(ValueError, match="tool calls"):
                DefiningAdapter(
                    response_retention=OllamaResponseRetention(root=tmp_path),
                    port=address[1],
                ).infer(self.make_request())
        finally:
            self.stop_service(server, thread)
        assert len(tuple(tmp_path.glob("raw-*.json"))) == 1
        assert tuple(tmp_path.glob("parsed-*.json")) == ()

    def test_public_api__adapter__preserves_defining_class_identity(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-021

        Requirement: Both curated package facades must expose the defining adapter.

        Acceptance: Defining-module, authoring-facade, and publications-facade imports
        are the exact same class object.
        """
        assert OllamaLoopbackManuscriptInferenceAdapter is DefiningAdapter
        assert publications.OllamaLoopbackManuscriptInferenceAdapter is DefiningAdapter
