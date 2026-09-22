"""Typed adaptation of immutable accepted F0 records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from python_public_import_foundation_model import (
    ClosedFoundationParser,
    FoundationJsonCodec,
    PublicImportFoundation,
)


@dataclass(frozen=True, slots=True)
class AcceptedF0Adapter:
    """Read accepted F0 bytes through its existing closed parser."""

    expected_sha256: str = (
        "3da51677747741fc0088d2f31f1359e6e8280bd1555ef514409ccfb5879f9e61"
    )

    def execute(self, path: Path) -> PublicImportFoundation:
        """Return the parsed immutable accepted foundation."""
        payload = path.read_bytes()
        import hashlib

        if hashlib.sha256(payload).hexdigest() != self.expected_sha256:
            raise ValueError("accepted F0 foundation identity mismatch")
        return ClosedFoundationParser().execute(FoundationJsonCodec().decode(payload))
