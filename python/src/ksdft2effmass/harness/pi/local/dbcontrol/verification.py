"""Private nonmutating verification boundary for maintained projections."""

from __future__ import annotations

from pathlib import Path

from ..control.verification import _HarnessProjectionSourceVerifier
from .records import _HarnessProjectionVerificationResult


class _HarnessProjectionVerifier:
    """Verify maintained control state against canonical repository sources."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _HarnessProjectionVerificationResult:
        """Generate an isolated candidate and report deterministic disagreements."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        return _HarnessProjectionSourceVerifier().execute(repository_root)
