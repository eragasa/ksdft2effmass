"""Immutable read-only manuscript target and source-revision identity."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptTargetContext:
    """Represent a bounded read-only target and its exact source revision.

    Parameters
    ----------
    relative_path
        Root-relative POSIX path of the manuscript source.
    section_heading
        Exact section command identifying the surrounding context.
    section_label
        Stable manuscript label associated with the selected section.
    base_git_blob_sha1
        Exact 40-character lowercase SHA-1 Git blob identity observed externally.
    document_sha256
        SHA-256 digest of the complete source-file bytes observed externally.
    section_text
        Complete selected section text used only as read-only prompt context.
    selected_text
        Exact unique text span for which replacement may be proposed.
    revision_id, target_id, span_id
        Deterministic init-false identities.  ``revision_id`` binds path and source
        content identities; ``target_id`` adds section identity and context bytes;
        ``span_id`` adds the exact selected UTF-8 bytes.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a path, digest, bound, section identity, or unique-span invariant fails.

    Notes
    -----
    Construction performs no file or Git access.  A caller must observe the complete
    file digest and Git blob identity outside this module.  Line numbers are not part
    of any identity.
    """

    MAX_PATH_CHARACTERS: ClassVar[int] = 512
    MAX_HEADING_CHARACTERS: ClassVar[int] = 512
    MAX_LABEL_CHARACTERS: ClassVar[int] = 256
    MAX_SECTION_CHARACTERS: ClassVar[int] = 50_000
    MAX_SELECTED_CHARACTERS: ClassVar[int] = 10_000
    SHA1_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{40}\Z")
    SHA256_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    relative_path: str
    section_heading: str
    section_label: str
    base_git_blob_sha1: str
    document_sha256: str
    section_text: str
    selected_text: str
    revision_id: str = field(init=False)
    target_id: str = field(init=False)
    span_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the bounded target and assign its deterministic identities."""
        if type(self.relative_path) is not str:
            raise TypeError("relative_path must be a built-in str")
        if (
            not self.relative_path
            or self.relative_path.startswith("/")
            or "\\" in self.relative_path
            or self.relative_path.endswith("/")
            or "//" in self.relative_path
            or len(self.relative_path) > self.MAX_PATH_CHARACTERS
        ):
            raise ValueError("relative_path must be a bounded root-relative POSIX path")
        if any(part in {"", ".", ".."} for part in self.relative_path.split("/")):
            raise ValueError("relative_path must not contain empty, '.' or '..' parts")

        for name, value, maximum in (
            ("section_heading", self.section_heading, self.MAX_HEADING_CHARACTERS),
            ("section_label", self.section_label, self.MAX_LABEL_CHARACTERS),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or value != value.strip() or len(value) > maximum:
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")

        if type(self.base_git_blob_sha1) is not str:
            raise TypeError("base_git_blob_sha1 must be a built-in str")
        if self.SHA1_PATTERN.fullmatch(self.base_git_blob_sha1) is None:
            raise ValueError("base_git_blob_sha1 must be a lowercase SHA-1 digest")
        if type(self.document_sha256) is not str:
            raise TypeError("document_sha256 must be a built-in str")
        if self.SHA256_PATTERN.fullmatch(self.document_sha256) is None:
            raise ValueError("document_sha256 must be a lowercase SHA-256 digest")

        if type(self.section_text) is not str:
            raise TypeError("section_text must be a built-in str")
        if (
            not self.section_text
            or len(self.section_text) > self.MAX_SECTION_CHARACTERS
        ):
            raise ValueError("section_text must be nonempty and bounded")
        if type(self.selected_text) is not str:
            raise TypeError("selected_text must be a built-in str")
        if (
            not self.selected_text
            or len(self.selected_text) > self.MAX_SELECTED_CHARACTERS
        ):
            raise ValueError("selected_text must be nonempty and bounded")
        if self.section_text.count(self.selected_text) != 1:
            raise ValueError("selected_text must occur exactly once in section_text")

        section_sha256 = hashlib.sha256(self.section_text.encode("utf-8")).hexdigest()
        selected_sha256 = hashlib.sha256(self.selected_text.encode("utf-8")).hexdigest()
        revision_id = self.identity_for_revision(
            relative_path=self.relative_path,
            base_git_blob_sha1=self.base_git_blob_sha1,
            document_sha256=self.document_sha256,
        )
        target_id = self.identity_for_target(
            relative_path=self.relative_path,
            section_heading=self.section_heading,
            section_label=self.section_label,
            revision_id=revision_id,
            section_sha256=section_sha256,
        )
        span_id = self.identity_for_span(
            target_id=target_id,
            selected_text=self.selected_text,
            selected_sha256=selected_sha256,
        )
        object.__setattr__(self, "revision_id", revision_id)
        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "span_id", span_id)

    @staticmethod
    def identity_for_revision(
        *, relative_path: str, base_git_blob_sha1: str, document_sha256: str
    ) -> str:
        """Return the deterministic identity for exact source-file revision data."""
        payload: dict[str, str] = {
            "base_git_blob_sha1": base_git_blob_sha1,
            "document_sha256": document_sha256,
            "relative_path": relative_path,
            "type": "ksdft2effmass.publications.manuscript-target-revision",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"manuscript-target-revision:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )

    @staticmethod
    def identity_for_target(
        *,
        relative_path: str,
        section_heading: str,
        section_label: str,
        revision_id: str,
        section_sha256: str,
    ) -> str:
        """Return the deterministic identity for one section at one revision."""
        payload: dict[str, str] = {
            "relative_path": relative_path,
            "revision_id": revision_id,
            "section_heading": section_heading,
            "section_label": section_label,
            "section_sha256": section_sha256,
            "type": "ksdft2effmass.publications.manuscript-target",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return f"manuscript-target:sha256:{hashlib.sha256(encoded).hexdigest()}"

    @staticmethod
    def identity_for_span(
        *, target_id: str, selected_text: str, selected_sha256: str
    ) -> str:
        """Return the deterministic identity for exact selected UTF-8 text bytes."""
        payload: dict[str, str] = {
            "selected_sha256": selected_sha256,
            "selected_text": selected_text,
            "target_id": target_id,
            "type": "ksdft2effmass.publications.manuscript-target-span",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return f"manuscript-target-span:sha256:{hashlib.sha256(encoded).hexdigest()}"
