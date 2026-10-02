"""Software verification for reduction-challenge encoded campaign documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DReductionChallengeEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DReductionChallengeEncodedDocuments


class TestPeriodic1DReductionChallengeEncodedDocuments:
    """Verify reduction-challenge document ownership and byte preservation."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their retained SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        directory = root / "calculations/research-monograph/periodic-1d"
        input_payload = (directory / "stress-input.json").read_bytes()
        result_payload = (directory / "stress-result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"
        )

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="input_payload must be built-in bytes"):
            SUT(bytearray(b"{}"), b"{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"{}", b"")
