"""Software verification for balanced Wannier90 encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.balanced import (
    Periodic2DWannier90BalancedEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DWannier90BalancedEncodedDocuments


class TestPeriodic2DWannier90BalancedEncodedDocuments:
    """Verify exact balanced Wannier90 document ownership."""

    def test_construction__preserves_retained_bytes_and_identity(self) -> None:
        """Preserve exact result bytes and their SHA-256 identity."""
        root = Path(__file__).resolve().parents[7]
        path = root / (
            "calculations/research-monograph/periodic-2d/wannier90-balanced-result.json"
        )
        payload = path.read_bytes()

        documents = SUT(payload)

        assert documents.result_payload is payload
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "422e53b012fb824164e3f03e67eeef6f5a013ce6f17da942ddc3f2d477b06e93"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte representations and empty encoded documents."""
        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT("{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"")
