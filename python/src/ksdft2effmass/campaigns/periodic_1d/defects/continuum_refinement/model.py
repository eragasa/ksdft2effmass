"""Encapsulated retained-wire state for continuum-refinement campaigns."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ContinuumRefinementCampaignModel:
    """Store exact campaign documents and their repository-resolution boundary."""

    input_document: bytes
    retained_result_document: bytes
    repository_root: Path

    def __post_init__(self) -> None:
        """Require nonempty exact documents and an absolute repository path."""
        if type(self.input_document) is not bytes or not self.input_document:
            raise ValueError("input_document must be nonempty exact bytes")
        if (
            type(self.retained_result_document) is not bytes
            or not self.retained_result_document
        ):
            raise ValueError("retained_result_document must be nonempty exact bytes")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
