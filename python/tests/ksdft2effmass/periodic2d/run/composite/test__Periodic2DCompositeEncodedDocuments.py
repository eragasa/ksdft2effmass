"""Software verification for composite periodic-2D encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.composite import (
    Periodic2DCompositeEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DCompositeEncodedDocuments


class TestPeriodic2DCompositeEncodedDocuments:
    """Verify exact composite periodic-2D document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        retained = root / "calculations/research-monograph/periodic-2d"
        input_payload = (retained / "composite-input.json").read_bytes()
        result_payload = (retained / "composite-result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "4abe583a5198537703f3a9e4937fd93c4c7cd6f46a3eefd302a551b1f0ae7e90"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "2bd97c1138e501e0b26f19dd43b3bb1718dc6e4655804f6bc96e853c7fd87792"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte representations and empty encoded documents."""
        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_payload must be nonempty"):
            SUT(b"", b"{}")
