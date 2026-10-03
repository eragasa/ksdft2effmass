"""Software verification for Wannier90 study encoded documents."""

import hashlib
from pathlib import Path

from ksdft2effmass.periodic2d.run.wannier90.study import (
    Periodic2DWannier90StudyEncodedDocuments,
)

SUT = Periodic2DWannier90StudyEncodedDocuments


class TestPeriodic2DWannier90StudyEncodedDocuments:
    """Verify exact Wannier90 study document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        root = Path(__file__).resolve().parents[7]
        retained = root / "calculations/research-monograph/periodic-2d"
        documents = SUT(
            (retained / "wannier90-study-input.json").read_bytes(),
            (retained / "wannier90-study-result.json").read_bytes(),
        )

        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "0092895cf1ff970ab3275b976d365e3c4df8c3c4c2a3ad33f4d0eaf9dbf5517a"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "a4a400f7610520d75f42af991b5b0eacaaaca53ac5dfd0736f072b918d092e11"
        )
