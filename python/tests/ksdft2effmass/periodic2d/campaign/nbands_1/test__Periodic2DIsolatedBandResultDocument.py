"""Software verification for the periodic-2D isolated result document."""

from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandResultDocument,
)


class TestPeriodic2DIsolatedBandResultDocument:
    """Verify encoded result-document ownership and identity."""

    def test_construction__preserves_exact_retained_result(self) -> None:
        """Preserve exact result bytes and their SHA-256 identity."""
        root = Path(__file__).resolve().parents[6]
        payload = (
            root / "calculations/research-monograph/periodic-2d/result.json"
        ).read_bytes()

        document = Periodic2DIsolatedBandResultDocument(payload)

        assert document.payload is payload
        assert document.sha256 == (
            "4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte and empty payloads."""
        with pytest.raises(TypeError, match="payload must be exact bytes"):
            Periodic2DIsolatedBandResultDocument("{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="payload must be nonempty"):
            Periodic2DIsolatedBandResultDocument(b"")
