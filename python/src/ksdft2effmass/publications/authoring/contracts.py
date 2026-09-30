"""Bounded immutable request contract for manuscript proposal composition."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import ClassVar

from .evidence import EvidenceRetrievalProjection
from .target import ManuscriptTargetContext


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptAuthoringRequest:
    """Represent immutable bounded intent to compose one manuscript proposal.

    Parameters
    ----------
    target
        Exact read-only section context and replacement span.
    retrieval
        Minimal projection of an already-completed external retrieval result.
    required_bibliographic_work_ids
        Unique work identities that must all be represented before inference.
    instruction
        Bounded authoring instruction for the selected span only.
    max_output_characters
        Inclusive caller-selected upper bound for proposed replacement text.
    max_citations
        Inclusive caller-selected upper bound for structured citations.
    request_id
        Deterministic init-false identity binding the complete request.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If text, collection, uniqueness, or numeric bounds fail.
    """

    MAX_REQUIRED_WORKS: ClassVar[int] = 32
    MAX_ID_CHARACTERS: ClassVar[int] = 512
    MAX_INSTRUCTION_CHARACTERS: ClassVar[int] = 2_000
    MAX_OUTPUT_CHARACTERS: ClassVar[int] = 8_000
    MAX_CITATIONS: ClassVar[int] = 32

    target: ManuscriptTargetContext
    retrieval: EvidenceRetrievalProjection
    required_bibliographic_work_ids: tuple[str, ...]
    instruction: str
    max_output_characters: int
    max_citations: int
    request_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate bounded authoring intent and assign its deterministic identity."""
        if type(self.target) is not ManuscriptTargetContext:
            raise TypeError("target must be ManuscriptTargetContext")
        if type(self.retrieval) is not EvidenceRetrievalProjection:
            raise TypeError("retrieval must be EvidenceRetrievalProjection")
        if type(self.required_bibliographic_work_ids) is not tuple:
            raise TypeError("required_bibliographic_work_ids must be a built-in tuple")
        if (
            not 1
            <= len(self.required_bibliographic_work_ids)
            <= self.MAX_REQUIRED_WORKS
        ):
            raise ValueError(
                "required_bibliographic_work_ids must contain 1 to 32 values"
            )
        for work_id in self.required_bibliographic_work_ids:
            if type(work_id) is not str:
                raise TypeError("required_bibliographic_work_ids must contain strings")
            if (
                not work_id
                or work_id != work_id.strip()
                or len(work_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(
                    "required work IDs must be nonempty, trimmed, and bounded"
                )
        if len(set(self.required_bibliographic_work_ids)) != len(
            self.required_bibliographic_work_ids
        ):
            raise ValueError("required_bibliographic_work_ids must be unique")

        if type(self.instruction) is not str:
            raise TypeError("instruction must be a built-in str")
        if (
            not self.instruction
            or self.instruction != self.instruction.strip()
            or len(self.instruction) > self.MAX_INSTRUCTION_CHARACTERS
        ):
            raise ValueError("instruction must be nonempty, trimmed, and bounded")
        for name, value, maximum in (
            (
                "max_output_characters",
                self.max_output_characters,
                self.MAX_OUTPUT_CHARACTERS,
            ),
            ("max_citations", self.max_citations, self.MAX_CITATIONS),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 1 <= value <= maximum:
                raise ValueError(f"{name} must be in [1, {maximum}]")

        object.__setattr__(
            self,
            "request_id",
            self.identity_for(
                target=self.target,
                retrieval=self.retrieval,
                required_bibliographic_work_ids=self.required_bibliographic_work_ids,
                instruction=self.instruction,
                max_output_characters=self.max_output_characters,
                max_citations=self.max_citations,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        target: ManuscriptTargetContext,
        retrieval: EvidenceRetrievalProjection,
        required_bibliographic_work_ids: tuple[str, ...],
        instruction: str,
        max_output_characters: int,
        max_citations: int,
    ) -> str:
        """Return the deterministic identity for exact bounded authoring intent."""
        payload: dict[str, str | int | tuple[str, ...]] = {
            "instruction": instruction,
            "max_citations": max_citations,
            "max_output_characters": max_output_characters,
            "required_bibliographic_work_ids": required_bibliographic_work_ids,
            "retrieval_projection_id": retrieval.projection_id,
            "span_id": target.span_id,
            "target_id": target.target_id,
            "type": "ksdft2effmass.publications.manuscript-authoring-request.v1",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"manuscript-authoring-request:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )
