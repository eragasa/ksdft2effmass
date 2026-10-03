"""Software verification for finite-rank-oracle encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle import (
    FiniteRankOracleEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteRankOracleEncodedDocuments


class TestFiniteRankOracleEncodedDocuments:
    """Verify exact finite-rank-oracle document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        directory = root / (
            "calculations/research-monograph/impurity-defect-1d-analytical-oracle"
        )
        input_document = (directory / "input.json").read_bytes()
        result_document = (directory / "result.json").read_bytes()

        documents = SUT(input_document, result_document)

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == (
            "ab653338be4f1733c8dd39878526b3293e603f2f0b0e7b8241577db2406c5840"
        )
        assert hashlib.sha256(documents.retained_result_document).hexdigest() == (
            "64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0"
        )
        assert not hasattr(documents, "repository_root")

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="retained_result_document must be"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_document must be nonempty"):
            SUT(b"", b"{}")
