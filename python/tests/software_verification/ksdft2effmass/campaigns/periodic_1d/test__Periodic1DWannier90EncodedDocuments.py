"""Software verification for Wannier90 encoded campaign documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    Periodic1DEncodedResultKind,
    Periodic1DWannier90EncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90EncodedDocuments


class TestPeriodic1DWannier90EncodedDocuments:
    """Verify exact Wannier90 document ownership and byte preservation."""

    def test_construction__preserves_retained_bytes_kind_and_identities(self) -> None:
        """Preserve exact input/result bytes, kind, and SHA-256 identities."""
        root = Path(__file__).resolve().parents[6]
        directory = root / "calculations/research-monograph/periodic-1d"
        input_payload = (directory / "composite-input.json").read_bytes()
        result_payload = (directory / "wannier90-result.json").read_bytes()

        documents = SUT(
            input_payload,
            result_payload,
            Periodic1DEncodedResultKind.WANNIER90,
        )

        assert documents.composite_input_payload is input_payload
        assert documents.result_payload is result_payload
        assert documents.result_kind is Periodic1DEncodedResultKind.WANNIER90
        assert hashlib.sha256(documents.composite_input_payload).hexdigest() == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535"
        )

    def test_construction__rejects_invalid_documents_and_result_kind(self) -> None:
        """Reject wrong representations, empty bytes, and unsupported result kinds."""
        with pytest.raises(TypeError, match="result_payload must be built-in bytes"):
            SUT(
                b"{}",
                "{}",  # type: ignore[arg-type]
                Periodic1DEncodedResultKind.WANNIER90,
            )
        with pytest.raises(
            ValueError, match="composite_input_payload must be nonempty"
        ):
            SUT(b"", b"{}", Periodic1DEncodedResultKind.WANNIER90)
        with pytest.raises(TypeError, match="result_kind must be"):
            SUT(b"{}", b"{}", "wannier90")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_kind must identify"):
            SUT(b"{}", b"{}", Periodic1DEncodedResultKind.ISOLATED_BAND)
