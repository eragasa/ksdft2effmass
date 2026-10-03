"""Encoded result documents for the continuum-refinement campaign."""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContinuumRefinementCampaignResultDocument:
    """Retain one canonical version-one refinement result document."""

    payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact immutable bytes."""
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if not self.payload:
            raise ValueError("payload must be nonempty")

    @property
    def sha256(self) -> str:
        """Return the canonical result SHA-256 identity."""
        return hashlib.sha256(self.payload).hexdigest()
