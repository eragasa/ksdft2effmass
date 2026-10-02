"""Software verification for isolated periodic-2D encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DIsolatedBandEncodedDocuments


class TestPeriodic2DIsolatedBandEncodedDocuments:
    """Verify exact isolated periodic-2D document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        retained = root / "calculations/research-monograph/periodic-2d"
        input_payload = (retained / "input.json").read_bytes()
        result_payload = (retained / "result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "82e9915101e755f7cc77cb8901478f88d878ffaa808732036631b7ae5cfd78ec"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte representations and empty encoded documents."""
        with pytest.raises(TypeError, match="input_payload must be built-in bytes"):
            SUT("{}", b"{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"{}", b"")
