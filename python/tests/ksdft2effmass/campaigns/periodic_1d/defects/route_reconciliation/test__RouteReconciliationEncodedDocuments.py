"""Software verification for route-reconciliation encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d.defects.route_reconciliation import (
    RouteReconciliationEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = RouteReconciliationEncodedDocuments


class TestRouteReconciliationEncodedDocuments:
    """Verify exact route-reconciliation document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        directory = root / (
            "calculations/research-monograph/impurity-defect-1d-independent-route"
        )
        input_document = (directory / "input.json").read_bytes()
        result_document = (directory / "result.json").read_bytes()

        documents = SUT(input_document, result_document)

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == (
            "aa7bd0750556bca3199678877f9ca2cd340f6c6b02885d6019c56173e912953f"
        )
        assert hashlib.sha256(documents.retained_result_document).hexdigest() == (
            "861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc"
        )
        assert not hasattr(documents, "repository_root")

    def test_construction__rejects_non_bytes_and_empty_documents(self) -> None:
        """Reject wrong representations and empty encoded documents."""
        with pytest.raises(TypeError, match="retained_result_document must be"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_document must be nonempty"):
            SUT(b"", b"{}")
