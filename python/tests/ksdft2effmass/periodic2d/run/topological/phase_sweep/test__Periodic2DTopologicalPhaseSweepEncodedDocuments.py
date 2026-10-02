"""Software verification for periodic-2D phase-sweep encoded documents."""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.topological.phase_sweep import (
    Periodic2DTopologicalPhaseSweepEncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DTopologicalPhaseSweepEncodedDocuments


class TestPeriodic2DTopologicalPhaseSweepEncodedDocuments:
    """Verify exact periodic-2D phase-sweep document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        retained = root / "calculations/research-monograph/periodic-2d"
        input_payload = (retained / "topological-phase-sweep-input.json").read_bytes()
        result_payload = (retained / "topological-phase-sweep-result.json").read_bytes()

        documents = SUT(input_payload, result_payload)

        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "f8b535250ede7efc79b96682979b72472791172d0662d41a490f8bad2a0a553c"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "298532cba30f56518c6578feb187704ad8f031eabdeae468b7ad067d0b286b11"
        )

    def test_construction__rejects_wrong_or_empty_representations(self) -> None:
        """Reject non-byte representations and empty encoded documents."""
        with pytest.raises(TypeError, match="result_payload must be exact bytes"):
            SUT(b"{}", "{}")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="input_payload must be nonempty"):
            SUT(b"", b"{}")
