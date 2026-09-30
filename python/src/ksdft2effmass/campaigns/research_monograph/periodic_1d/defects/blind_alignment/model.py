"""Encapsulated retained-wire state for the blind-alignment campaign."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignModel:
    """Store exact campaign documents and their repository resolution boundary.

    Parameters
    ----------
    input_document
        Exact immutable version-one input JSON bytes.
    retained_result_document
        Exact immutable version-one retained-result JSON bytes.
    repository_root
        Repository root used by the authenticated baseline-loading Actionizer. Merely
        storing this path performs no filesystem access.
    """

    input_document: bytes
    retained_result_document: bytes
    repository_root: Path

    def __post_init__(self) -> None:
        """Require exact nonempty bytes and an absolute repository path value."""
        if type(self.input_document) is not bytes or not self.input_document:
            raise ValueError("input_document must be nonempty exact bytes")
        if (
            type(self.retained_result_document) is not bytes
            or not self.retained_result_document
        ):
            raise ValueError("retained_result_document must be nonempty exact bytes")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be a pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
