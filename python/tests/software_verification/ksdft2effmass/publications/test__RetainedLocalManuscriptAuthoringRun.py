r"""Software verification of ``RetainedLocalManuscriptAuthoringRun``.

Evidence profile: routine

Bounded artifact scope: retained local-inference authoring terminal outcomes.

Facet and represented meaning

The Workflow composes through the canonical author and retains terminal metadata after
raw and parsed response records already exist.

Intrinsic and cross-object scope

A synthetic loopback service supplies bounded responses. Ollama adaptation owns raw
and parsed retention; the author owns inspection and mismatch outcomes; the Workflow
owns terminal outcome retention.

VVUQ and scientific exclusions

No model or external service is invoked. These tests establish observability mechanics,
not source correctness, model quality, scientific validation, or human acceptance.
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.publications import (
    AdHocEvidenceRetrievalProjection,
    AuthorSuppliedPublisherAbstractEvidence,
    CitationKeyStatus,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
    ManuscriptAuthoringRequest,
    ManuscriptTargetContext,
    OllamaLoopbackManuscriptInferenceAdapter,
    OllamaResponseRetention,
    ProjectedCitationIdentity,
    RetainedLocalManuscriptAuthoringRun,
)

pytestmark = pytest.mark.software_verification
SUT = RetainedLocalManuscriptAuthoringRun


class TestRetainedLocalManuscriptAuthoringRun:
    """Verify retention survives terminal non-proposal outcomes."""

    @staticmethod
    def make_request() -> tuple[ManuscriptAuthoringRequest, str]:
        """Return one accepted-key synthetic abstract request and evidence ID."""
        abstract = "Synthetic publisher abstract used only for retention verification."
        citation_identity = ProjectedCitationIdentity(
            projection_result_id="references-result:synthetic",
            projection_id="references-projection:synthetic",
            projection_item_id="references-item:synthetic",
            bibliographic_work_id="doi:10.1103/PhysRev.97.869",
            status=CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
            canonical_citekey="luttingerKohn1955",
        )
        evidence = AuthorSuppliedPublisherAbstractEvidence(
            bibliographic_work_id=citation_identity.bibliographic_work_id,
            source_url=("https://journals.aps.org/pr/abstract/10.1103/PhysRev.97.869"),
            doi="10.1103/PhysRev.97.869",
            title="Synthetic abstract title",
            authors=("A. Synthetic", "B. Synthetic"),
            publication_date="1955-01-01",
            abstract_text=abstract,
            source_document_sha256=hashlib.sha256(b"synthetic page").hexdigest(),
            citation_identity=citation_identity,
            proposed_citekey=None,
        )
        projection = AdHocEvidenceRetrievalProjection(evidence=(evidence,))
        selected = "Synthetic selected text."
        section = f"\\section{{Synthetic}}\n\\label{{sec:synthetic}}\n\n{selected}\n"
        target = ManuscriptTargetContext(
            relative_path="docs/synthetic/chapter.tex",
            section_heading="\\section{Synthetic}",
            section_label="sec:synthetic",
            base_git_blob_sha1="a" * 40,
            document_sha256="b" * 64,
            section_text=section,
            selected_text=selected,
        )
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=projection,
            required_bibliographic_work_ids=(evidence.bibliographic_work_id,),
            instruction="Draft only from the synthetic publisher abstract.",
            max_output_characters=1_000,
            max_citations=1,
        )
        return request, evidence.evidence_id

    @staticmethod
    def start_service(
        *, generated_content: str
    ) -> tuple[ThreadingHTTPServer, threading.Thread]:
        """Start one synthetic loopback Ollama-shaped service."""

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                """Return the exact configured model identity."""
                payload = json.dumps(
                    {
                        "models": [
                            {
                                "name": (
                                    OllamaLoopbackManuscriptInferenceAdapter.MODEL_NAME
                                ),
                                "digest": (
                                    OllamaLoopbackManuscriptInferenceAdapter.MODEL_SHA256
                                ),
                            }
                        ]
                    },
                    separators=(",", ":"),
                ).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def do_POST(self) -> None:
                """Return one configured structured chat response."""
                length = int(self.headers.get("Content-Length", "0"))
                self.rfile.read(length)
                payload = json.dumps(
                    {
                        "model": OllamaLoopbackManuscriptInferenceAdapter.MODEL_NAME,
                        "message": {
                            "role": "assistant",
                            "content": generated_content,
                        },
                        "done": True,
                        "done_reason": "stop",
                    },
                    separators=(",", ":"),
                ).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, format: str, *args: object) -> None:
                """Suppress synthetic framework request logs."""

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread

    @staticmethod
    def stop_service(server: ThreadingHTTPServer, thread: threading.Thread) -> None:
        """Stop and join one synthetic service."""
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive()

    @staticmethod
    def generated(*, citation_key: str, warnings: tuple[str, ...]) -> str:
        """Return candidate text and warnings without structural lineage echoes."""
        return json.dumps(
            {
                "replacement_text": f"Synthetic draft \\cite{{{citation_key}}}.",
                "warning_codes": list(warnings),
            },
            separators=(",", ":"),
        )

    def test_method__execute__retains_warning_response_before_inspection_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-034

        Requirement: An inference warning must not erase its exact raw or parsed
        response when composition returns inspection-required.

        Acceptance: Raw, parsed, and terminal files all exist mode 0600; parsed
        metadata preserves the exact warning tuple and terminal metadata preserves the
        inspection outcome and response identity.
        """
        request, _ = self.make_request()
        warning = "ABSTRACT_SCOPE_QUALIFICATION"
        server, thread = self.start_service(
            generated_content=self.generated(
                citation_key="luttingerKohn1955",
                warnings=(warning,),
            )
        )
        try:
            port = cast(tuple[str, int], server.server_address)[1]
            retention = OllamaResponseRetention(root=tmp_path / "runtime")
            result = SUT().execute(
                request,
                request.target.revision_id,
                OllamaLoopbackManuscriptInferenceAdapter(
                    response_retention=retention,
                    port=port,
                ),
            )
        finally:
            self.stop_service(server, thread)

        assert result.outcome is ManuscriptAuthoringOutcome.INSPECTION_REQUIRED
        assert result.issues == (ManuscriptAuthoringIssue.INFERENCE_WARNING,)
        (raw,) = tuple((tmp_path / "runtime").glob("raw-*.json"))
        (parsed,) = tuple((tmp_path / "runtime").glob("parsed-*.json"))
        (terminal,) = tuple((tmp_path / "runtime").glob("terminal-*.json"))
        assert all(
            path.stat().st_mode & 0o777 == 0o600 for path in (raw, parsed, terminal)
        )
        parsed_payload = json.loads(parsed.read_text())
        terminal_payload = json.loads(terminal.read_text())
        assert "schema_version" not in parsed_payload
        assert "schema_version" not in terminal_payload
        assert parsed_payload["warning_codes"] == [warning]
        assert parsed_payload["inference_response_id"] == result.inference_response_id
        assert terminal_payload["outcome"] == "inspection_required"
        assert terminal_payload["issues"] == ["inference_warning"]

    def test_method__execute__retains_decoded_rejection_and_exceptional_terminal(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-039

        Requirement: A decoded response rejected during typed construction must retain
        raw bytes, excerpt-free rejection metadata, and an exceptional terminal record
        before the original exception is re-raised.

        Acceptance: An empty warning code raises the typed contract error; raw,
        decoded-rejection, and exceptional-terminal files survive mode 0600 while no
        parsed response or product terminal record is fabricated.
        """
        request, _ = self.make_request()
        replacement_text = "Synthetic draft \\cite{luttingerKohn1955}."
        generated_content = self.generated(
            citation_key="luttingerKohn1955",
            warnings=("",),
        )
        server, thread = self.start_service(generated_content=generated_content)
        root = tmp_path / "runtime"
        try:
            port = cast(tuple[str, int], server.server_address)[1]
            with pytest.raises(ValueError, match="warning_codes must be nonempty"):
                SUT().execute(
                    request,
                    request.target.revision_id,
                    OllamaLoopbackManuscriptInferenceAdapter(
                        response_retention=OllamaResponseRetention(root=root),
                        port=port,
                    ),
                )
        finally:
            self.stop_service(server, thread)

        (raw,) = tuple(root.glob("raw-*.json"))
        (rejection,) = tuple(root.glob("decoded-rejection-*.json"))
        (exceptional,) = tuple(root.glob("exceptional-terminal-*.json"))
        assert tuple(root.glob("parsed-*.json")) == ()
        assert tuple(root.glob("terminal-*.json")) == ()
        assert all(
            path.stat().st_mode & 0o777 == 0o600
            for path in (raw, rejection, exceptional)
        )
        rejection_text = rejection.read_text()
        rejection_payload = json.loads(rejection_text)
        terminal_payload = json.loads(exceptional.read_text())
        assert rejection_payload["record_type"] == ("OLLAMA_DECODED_RESPONSE_REJECTION")
        raw_bytes = raw.read_bytes()
        assert rejection_payload["raw_response"] == {
            "byte_count": len(raw_bytes),
            "path_name": raw.name,
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        }
        generated_structure = rejection_payload["generated_structure"]
        assert generated_structure["warning_codes"] == [""]
        assert (
            generated_structure["content_sha256"]
            == hashlib.sha256(generated_content.encode()).hexdigest()
        )
        assert generated_structure["content_utf8_bytes"] == len(
            generated_content.encode()
        )
        assert (
            generated_structure["replacement_text_sha256"]
            == hashlib.sha256(replacement_text.encode()).hexdigest()
        )
        assert generated_structure["replacement_text_characters"] == len(
            replacement_text
        )
        assert generated_structure["replacement_text_utf8_bytes"] == len(
            replacement_text.encode()
        )
        assert rejection_payload["rejection"] == {
            "error_code": "TYPED_RESPONSE_CONTRACT_REJECTED",
            "error_message": "decoded response rejected by typed response contract",
            "error_type": "ValueError",
            "stage": "typed_response_construction",
        }
        assert "replacement_text" not in rejection_payload
        assert "Synthetic draft" not in rejection_text
        assert "Synthetic publisher abstract" not in rejection_text
        assert terminal_payload["record_type"] == ("OLLAMA_EXCEPTIONAL_RUN_TERMINAL")
        assert terminal_payload["failure"] == {
            "error_code": "INFERENCE_EXCEPTION",
            "error_message": "local inference failed closed",
            "error_type": "ValueError",
            "stage": "inference_execution",
        }
        assert terminal_payload["inference_response_id"] is None
        assert terminal_payload["authoring_result_id"] is None
        assert terminal_payload["authoring_outcome"] is None
        assert terminal_payload["retained_path_names"] == {
            "decoded_rejection": rejection.name,
            "parsed": None,
            "raw": raw.name,
        }

    def test_method__execute__retains_response_through_post_parse_key_failure(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-035

        Requirement: A response parsed successfully but rejected by citation policy
        must retain raw, parsed, and terminal evidence.

        Acceptance: Wrong-key output returns inspection-required, while all three
        separate records survive and terminal metadata names the key mismatch.
        """
        request, _ = self.make_request()
        server, thread = self.start_service(
            generated_content=self.generated(
                citation_key="Wrong1955",
                warnings=(),
            )
        )
        try:
            port = cast(tuple[str, int], server.server_address)[1]
            root = tmp_path / "runtime"
            result = SUT().execute(
                request,
                request.target.revision_id,
                OllamaLoopbackManuscriptInferenceAdapter(
                    response_retention=OllamaResponseRetention(root=root),
                    port=port,
                ),
            )
        finally:
            self.stop_service(server, thread)

        assert result.outcome is ManuscriptAuthoringOutcome.INSPECTION_REQUIRED
        assert result.issues == (ManuscriptAuthoringIssue.CITATION_KEY_MISMATCH,)
        assert len(tuple(root.glob("raw-*.json"))) == 1
        assert len(tuple(root.glob("parsed-*.json"))) == 1
        (terminal,) = tuple(root.glob("terminal-*.json"))
        terminal_payload = json.loads(terminal.read_text())
        assert terminal_payload["issues"] == ["citation_key_mismatch"]
        assert terminal_payload["proposal_id"] is None
