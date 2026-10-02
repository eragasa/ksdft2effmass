"""Software verification for composite-band encoded campaign documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeEncodedDocuments


class TestPeriodic1DCompositeEncodedDocuments:
    """Verify exact composite-band document ownership and byte preservation."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their retained SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        directory = root / "calculations/research-monograph/periodic-1d"
        input_payload = (directory / "composite-input.json").read_bytes()
        result_payload = (directory / "composite-result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"
        )

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="result_payload must be built-in bytes"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_payload must be nonempty"):
            SUT(b"", b"{}")
