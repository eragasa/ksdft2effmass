"""Encoded result documents for the route-reconciliation campaign."""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteReconciliationCampaignResultDocument:
    """Retain one canonical version-one campaign result document."""

    payload: bytes

    def __post_init__(self) -> None:
        """Require a nonempty exact immutable byte document."""
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if not self.payload:
            raise ValueError("payload must be nonempty")

    @property
    def sha256(self) -> str:
        """Return the SHA-256 identity of the canonical result bytes."""
        return hashlib.sha256(self.payload).hexdigest()
