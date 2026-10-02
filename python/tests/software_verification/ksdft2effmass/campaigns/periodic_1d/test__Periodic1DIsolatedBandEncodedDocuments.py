"""Software verification for isolated-band encoded campaign documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandEncodedDocuments


class TestPeriodic1DIsolatedBandEncodedDocuments:
    """Verify exact isolated-band document ownership and byte preservation."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their retained SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        directory = root / "calculations/research-monograph/periodic-1d"
        input_payload = (directory / "input.json").read_bytes()
        result_payload = (directory / "result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"
        )

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="input_payload must be built-in bytes"):
            SUT("{}", b"{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"{}", b"")
