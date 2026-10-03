"""Software verification for continuum-refinement encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d.defects.continuum_refinement import (
    ContinuumRefinementEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = ContinuumRefinementEncodedDocuments


class TestContinuumRefinementEncodedDocuments:
    """Verify exact continuum-refinement document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        directory = root / (
            "calculations/research-monograph/impurity-defect-1d-continuum-refinement"
        )
        input_document = (directory / "input.json").read_bytes()
        result_document = (directory / "result.json").read_bytes()

        documents = SUT(input_document, result_document)

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == (
            "55d647a8c259d3a1f1e5c756b496a9d1a16fee0a691c7b53d2f877da5f287fdd"
        )
        assert hashlib.sha256(documents.retained_result_document).hexdigest() == (
            "1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc"
        )
        assert not hasattr(documents, "repository_root")

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="retained_result_document must be"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_document must be nonempty"):
            SUT(b"", b"{}")
