"""Project Koios References adapter for manuscript authoring."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import ClassVar

from projectkoios.references.citation_identity import (
    CitationIdentityProjectionResult,
    CitationIdentityProjectionStatus,
)

from ..statuses import CitationKeyStatus


@dataclass(frozen=True, slots=True, kw_only=True)
class ProjectedCitationIdentity:
    """Retain one exact References projection item for authoring.

    The record deliberately has no proposed-citekey field. Candidate keys therefore
    cannot be promoted into the canonical citekey used by authoring.
    """

    MAX_ID_CHARACTERS: ClassVar[int] = 512

    projection_result_id: str
    projection_id: str
    projection_item_id: str
    bibliographic_work_id: str
    status: CitationKeyStatus
    canonical_citekey: str | None
    projected_identity_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the projected owner identities and assign local identity."""
        for name, value in (
            ("projection_result_id", self.projection_result_id),
            ("projection_id", self.projection_id),
            ("projection_item_id", self.projection_item_id),
            ("bibliographic_work_id", self.bibliographic_work_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if (
                not value
                or value != value.strip()
                or len(value) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.status) is not CitationKeyStatus:
            raise TypeError("status must be CitationKeyStatus")
        if self.status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL:
            if type(self.canonical_citekey) is not str or not self.canonical_citekey:
                raise ValueError("active accepted identity requires canonical_citekey")
        elif self.canonical_citekey is not None:
            raise ValueError(
                "only active accepted identity may carry canonical_citekey"
            )
        object.__setattr__(
            self,
            "projected_identity_id",
            self.identity_for(
                projection_result_id=self.projection_result_id,
                projection_id=self.projection_id,
                projection_item_id=self.projection_item_id,
                bibliographic_work_id=self.bibliographic_work_id,
                status=self.status,
                canonical_citekey=self.canonical_citekey,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        projection_result_id: str,
        projection_id: str,
        projection_item_id: str,
        bibliographic_work_id: str,
        status: CitationKeyStatus,
        canonical_citekey: str | None,
    ) -> str:
        """Return deterministic identity for the exact projected owner item."""
        payload: dict[str, str | None] = {
            "bibliographic_work_id": bibliographic_work_id,
            "canonical_citekey": canonical_citekey,
            "projection_id": projection_id,
            "projection_item_id": projection_item_id,
            "projection_result_id": projection_result_id,
            "status": status.value,
            "type": "ksdft2effmass.publications.projected-citation-identity",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return f"projected-citation-identity:sha256:{digest}"


@dataclass(frozen=True, slots=True)
class ProjectKoiosReferencesAdapter:
    """Project one exact References result item without promoting candidate keys."""

    def project(
        self,
        result: CitationIdentityProjectionResult,
        bibliographic_work_id: str,
        /,
    ) -> ProjectedCitationIdentity:
        """Return the exact citation identity correlated to one work identity."""
        if type(result) is not CitationIdentityProjectionResult:
            raise TypeError("result must be CitationIdentityProjectionResult")
        if type(bibliographic_work_id) is not str:
            raise TypeError("bibliographic_work_id must be a built-in str")
        matches = tuple(
            item
            for item in result.items
            if item.requested_identity_id == bibliographic_work_id
        )
        if len(matches) != 1:
            raise ValueError(
                "citation projection must contain exactly one correlated work item"
            )
        item = matches[0]
        status = self.project_status(item.status)
        canonical_citekey = (
            item.canonical_citekey
            if status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
            else None
        )
        return ProjectedCitationIdentity(
            projection_result_id=result.result_id,
            projection_id=result.projection_id,
            projection_item_id=item.item_id,
            bibliographic_work_id=bibliographic_work_id,
            status=status,
            canonical_citekey=canonical_citekey,
        )

    @staticmethod
    def project_status(status: CitationIdentityProjectionStatus) -> CitationKeyStatus:
        """Map the exact closed owner status without fallback or coercion."""
        if status is CitationIdentityProjectionStatus.ACCEPTED_ACTIVE_CANONICAL:
            return CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
        if status is CitationIdentityProjectionStatus.ACCEPTED_WITHOUT_ACTIVE_CITEKEY:
            return CitationKeyStatus.ACCEPTED_WITHOUT_ACTIVE_CITEKEY
        if status is CitationIdentityProjectionStatus.CANDIDATE_PROPOSED_NONCANONICAL:
            return CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL
        if status is CitationIdentityProjectionStatus.INACTIVE_SUPERSEDED:
            return CitationKeyStatus.INACTIVE_SUPERSEDED
        if status is CitationIdentityProjectionStatus.UNRESOLVED:
            return CitationKeyStatus.UNRESOLVED
        raise ValueError("unsupported References citation identity status")
