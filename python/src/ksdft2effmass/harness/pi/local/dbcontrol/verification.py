"""Public nonmutating verification facade for maintained harness control state."""

from __future__ import annotations

from pathlib import Path

from ..control.verification import _HarnessControlSourceVerifier
from .records import HarnessControlVerificationResult


class HarnessControlVerifier:
    """Verify maintained control state against canonical repository sources."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> HarnessControlVerificationResult:
        """Generate an isolated candidate and report deterministic disagreements."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        return _HarnessControlSourceVerifier().execute(repository_root)
