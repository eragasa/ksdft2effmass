"""Software verification for topological periodic-2D encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.topological import (
    Periodic2DTopologicalEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DTopologicalEncodedDocuments


class TestPeriodic2DTopologicalEncodedDocuments:
    """Verify exact topological periodic-2D document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        retained = root / "calculations/research-monograph/periodic-2d"
        input_payload = (retained / "topological-input.json").read_bytes()
        result_payload = (retained / "topological-result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "b4372d84ba80e84a1bf9a12d25750618bf276baa8999d298031e3ac6e0c18436"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "bd94c40a3b12f4f7ecb41009e86c936e456d09738176256f4e0d27ab9fdd959a"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte representations and empty encoded documents."""
        with pytest.raises(TypeError, match="input_payload must be exact bytes"):
            SUT("{}", b"{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_payload must be nonempty"):
            SUT(b"{}", b"")
