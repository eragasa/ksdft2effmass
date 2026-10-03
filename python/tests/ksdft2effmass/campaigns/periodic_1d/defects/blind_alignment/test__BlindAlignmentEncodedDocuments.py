"""Software verification for blind-alignment encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment import (
    BlindAlignmentEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = BlindAlignmentEncodedDocuments


class TestBlindAlignmentEncodedDocuments:
    """Verify exact blind-alignment document ownership and byte preservation."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        directory = root / (
            "calculations/research-monograph/impurity-defect-1d-blind-alignment"
        )
        input_document = (directory / "input.json").read_bytes()
        result_document = (directory / "result.json").read_bytes()

        documents = SUT(input_document, result_document)

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == (
            "3476c0b1ed45913e5386be3688528d549f7eea15840b67559763d875406d7d48"
        )
        assert hashlib.sha256(documents.retained_result_document).hexdigest() == (
            "a3b7d20c870fe5d87fd6a591fbafe9a997e7a261a5bc08163c3273b4789416fe"
        )
        assert not hasattr(documents, "repository_root")

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="retained_result_document must be"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_document must be nonempty"):
            SUT(b"", b"{}")
