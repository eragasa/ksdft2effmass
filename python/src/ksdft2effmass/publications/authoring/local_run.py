"""Retained local-inference authoring workflow."""

from __future__ import annotations

from dataclasses import dataclass

from .adapters.ollama import OllamaLoopbackManuscriptInferenceAdapter
from .author import EvidenceGroundedManuscriptAuthor
from .contracts import ManuscriptAuthoringRequest
from .proposal import ManuscriptAuthoringResult


@dataclass(frozen=True, slots=True)
class RetainedLocalManuscriptAuthoringRun:
    """Compose once and retain separate terminal metadata for the local response."""

    def execute(
        self,
        request: ManuscriptAuthoringRequest,
        current_revision_id: str,
        inference: OllamaLoopbackManuscriptInferenceAdapter,
        /,
    ) -> ManuscriptAuthoringResult:
        """Run the canonical author and atomically retain its terminal outcome."""
        if type(request) is not ManuscriptAuthoringRequest:
            raise TypeError("request must be ManuscriptAuthoringRequest")
        if type(inference) is not OllamaLoopbackManuscriptInferenceAdapter:
            raise TypeError(
                "inference must be OllamaLoopbackManuscriptInferenceAdapter"
            )
        author = EvidenceGroundedManuscriptAuthor()
        inference_request = author.inference_request_for(request)
        result = author.execute(request, current_revision_id, inference)
        inference.response_retention.retain_terminal(
            inference_request.inference_request_id,
            result,
        )
        return result
