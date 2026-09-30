"""Bounded local-inference request, response, and structural port."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import ClassVar, Protocol

from .contracts import ManuscriptAuthoringRequest
from .proposal import ProposedCitation


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptInferenceRequest:
    """Represent the exact bounded request sent to local inference.

    Parameters
    ----------
    authoring_request_id
        Identity of the originating :class:`ManuscriptAuthoringRequest`.
    prompt
        Deterministically constructed prompt with separately labeled target and
        untrusted quoted evidence JSON sections.
    allowed_evidence_ids
        Lexically sorted evidence identities that output may cite.
    max_output_characters
        Requested proposal-text limit.
    max_citations
        Requested structured-citation limit.
    inference_request_id
        Deterministic init-false identity binding all inference inputs.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a field violates a bound or canonical ordering rule.
    """

    MAX_PROMPT_CHARACTERS: ClassVar[int] = 100_000
    MAX_ID_CHARACTERS: ClassVar[int] = 512

    authoring_request_id: str
    prompt: str
    allowed_evidence_ids: tuple[str, ...]
    max_output_characters: int
    max_citations: int
    inference_request_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate exact inference inputs and assign their deterministic identity."""
        if type(self.authoring_request_id) is not str:
            raise TypeError("authoring_request_id must be a built-in str")
        if (
            not self.authoring_request_id
            or self.authoring_request_id != self.authoring_request_id.strip()
            or len(self.authoring_request_id) > self.MAX_ID_CHARACTERS
        ):
            raise ValueError(
                "authoring_request_id must be nonempty, trimmed, and bounded"
            )
        if type(self.prompt) is not str:
            raise TypeError("prompt must be a built-in str")
        if not self.prompt or len(self.prompt) > self.MAX_PROMPT_CHARACTERS:
            raise ValueError("prompt must be nonempty and bounded")
        if type(self.allowed_evidence_ids) is not tuple:
            raise TypeError("allowed_evidence_ids must be a built-in tuple")
        if not self.allowed_evidence_ids:
            raise ValueError("allowed_evidence_ids must not be empty")
        if self.allowed_evidence_ids != tuple(sorted(set(self.allowed_evidence_ids))):
            raise ValueError("allowed_evidence_ids must be unique and lexically sorted")
        for evidence_id in self.allowed_evidence_ids:
            if type(evidence_id) is not str:
                raise TypeError("allowed_evidence_ids must contain built-in strings")
            if (
                not evidence_id
                or evidence_id != evidence_id.strip()
                or len(evidence_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(
                    "allowed evidence IDs must be nonempty, trimmed, and bounded"
                )
        for name, value, maximum in (
            (
                "max_output_characters",
                self.max_output_characters,
                ManuscriptAuthoringRequest.MAX_OUTPUT_CHARACTERS,
            ),
            (
                "max_citations",
                self.max_citations,
                ManuscriptAuthoringRequest.MAX_CITATIONS,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 1 <= value <= maximum:
                raise ValueError(f"{name} is outside the authoring bound")
        object.__setattr__(
            self,
            "inference_request_id",
            self.identity_for(
                authoring_request_id=self.authoring_request_id,
                prompt=self.prompt,
                allowed_evidence_ids=self.allowed_evidence_ids,
                max_output_characters=self.max_output_characters,
                max_citations=self.max_citations,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        authoring_request_id: str,
        prompt: str,
        allowed_evidence_ids: tuple[str, ...],
        max_output_characters: int,
        max_citations: int,
    ) -> str:
        """Return the deterministic identity of exact local-inference inputs."""
        payload: dict[str, str | int | tuple[str, ...]] = {
            "allowed_evidence_ids": allowed_evidence_ids,
            "authoring_request_id": authoring_request_id,
            "max_citations": max_citations,
            "max_output_characters": max_output_characters,
            "prompt": prompt,
            "type": "ksdft2effmass.publications.manuscript-inference-request.v1",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"manuscript-inference-request:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptInferenceResponse:
    """Represent bounded text and structured citations returned by local inference.

    Parameters
    ----------
    inference_request_id
        Exact request identity copied by the local inference adapter.
    inference_implementation_id
        Content- or version-specific identity of the injected implementation.
    replacement_text
        Candidate replacement text.  Empty text is representable so the composer can
        return a closed ``OUTPUT_REJECTED`` result.
    citations
        Ordered structured citation proposals.
    evidence_ids
        Lexically sorted evidence identities the implementation reports using.
    warning_codes
        Ordered inference warnings requiring inspection.
    response_id
        Deterministic init-false identity binding the complete response.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If hard bounds, identity grammar, uniqueness, or ordering fail.
    """

    MAX_TEXT_CHARACTERS: ClassVar[int] = 16_000
    MAX_CITATIONS: ClassVar[int] = 64
    MAX_EVIDENCE_IDS: ClassVar[int] = 64
    MAX_WARNINGS: ClassVar[int] = 32
    MAX_ID_CHARACTERS: ClassVar[int] = 512

    inference_request_id: str
    inference_implementation_id: str
    replacement_text: str
    citations: tuple[ProposedCitation, ...]
    evidence_ids: tuple[str, ...]
    warning_codes: tuple[str, ...]
    response_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the bounded response and assign its deterministic identity."""
        for name, value in (
            ("inference_request_id", self.inference_request_id),
            ("inference_implementation_id", self.inference_implementation_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if (
                not value
                or value != value.strip()
                or len(value) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.replacement_text) is not str:
            raise TypeError("replacement_text must be a built-in str")
        if len(self.replacement_text) > self.MAX_TEXT_CHARACTERS:
            raise ValueError("replacement_text exceeds the hard response bound")
        if type(self.citations) is not tuple:
            raise TypeError("citations must be a built-in tuple")
        if len(self.citations) > self.MAX_CITATIONS:
            raise ValueError("citations exceeds the hard response bound")
        if any(type(citation) is not ProposedCitation for citation in self.citations):
            raise TypeError("citations must contain ProposedCitation values")
        citation_keys = tuple(citation.citation_key for citation in self.citations)
        if len(set(citation_keys)) != len(citation_keys):
            raise ValueError("citation keys must be unique in one response")

        if type(self.evidence_ids) is not tuple:
            raise TypeError("evidence_ids must be a built-in tuple")
        if len(self.evidence_ids) > self.MAX_EVIDENCE_IDS:
            raise ValueError("evidence_ids exceeds the hard response bound")
        if self.evidence_ids != tuple(sorted(set(self.evidence_ids))):
            raise ValueError("evidence_ids must be unique and lexically sorted")
        for evidence_id in self.evidence_ids:
            if type(evidence_id) is not str:
                raise TypeError("evidence_ids must contain built-in strings")
            if (
                not evidence_id
                or evidence_id != evidence_id.strip()
                or len(evidence_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError("evidence_ids must be nonempty, trimmed, and bounded")

        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        if len(self.warning_codes) > self.MAX_WARNINGS:
            raise ValueError("warning_codes exceeds the hard response bound")
        for warning_code in self.warning_codes:
            if type(warning_code) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if (
                not warning_code
                or warning_code != warning_code.strip()
                or len(warning_code) > 128
            ):
                raise ValueError("warning_codes must be nonempty, trimmed, and bounded")
        if len(set(self.warning_codes)) != len(self.warning_codes):
            raise ValueError("warning_codes must be unique")

        object.__setattr__(
            self,
            "response_id",
            self.identity_for(
                inference_request_id=self.inference_request_id,
                inference_implementation_id=self.inference_implementation_id,
                replacement_text=self.replacement_text,
                citations=self.citations,
                evidence_ids=self.evidence_ids,
                warning_codes=self.warning_codes,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        inference_request_id: str,
        inference_implementation_id: str,
        replacement_text: str,
        citations: tuple[ProposedCitation, ...],
        evidence_ids: tuple[str, ...],
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the deterministic identity of one bounded inference response."""
        payload: dict[str, str | tuple[str, ...]] = {
            "citation_ids": tuple(citation.citation_id for citation in citations),
            "evidence_ids": evidence_ids,
            "inference_implementation_id": inference_implementation_id,
            "inference_request_id": inference_request_id,
            "replacement_text": replacement_text,
            "type": "ksdft2effmass.publications.manuscript-inference-response.v1",
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return f"manuscript-inference-response:sha256:{digest}"


class LocalManuscriptInferencePort(Protocol):
    """Structural port for one bounded local inference implementation.

    Implementations receive only :class:`ManuscriptInferenceRequest` and return
    :class:`ManuscriptInferenceResponse`.  The port exposes no filesystem, shell,
    database, browser, network, retrieval, publication, or bibliography operation.
    Runtime composition is responsible for selecting a genuinely local implementation
    and for enforcing any process-level isolation required by deployment policy.
    """

    def infer(
        self, request: ManuscriptInferenceRequest, /
    ) -> ManuscriptInferenceResponse:
        """Return bounded text and structured citations for the exact request.

        Parameters
        ----------
        request
            Deterministic bounded inference request.

        Returns
        -------
        ManuscriptInferenceResponse
            Typed candidate output.  Returning it does not imply proposal admission or
            human, scientific, or publication acceptance.
        """
        ...
