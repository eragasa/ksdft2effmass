"""Software verification for optimizer-basin encoded documents."""

import hashlib
from pathlib import Path

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    Periodic2DOptimizerBasinEncodedDocuments,
)

SUT = Periodic2DOptimizerBasinEncodedDocuments


class TestPeriodic2DOptimizerBasinEncodedDocuments:
    """Verify exact optimizer-basin document ownership."""

    def test_construction__preserves_retained_bytes_and_identities(self) -> None:
        """Preserve exact input/result bytes and their SHA-256 identities."""
        base = Path(__file__).resolve().parents[7] / (
            "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        documents = SUT(
            (base / "study-input.json").read_bytes(),
            (base / "result.json").read_bytes(),
        )
        assert hashlib.sha256(documents.input_payload).hexdigest() == (
            "c2e0f601198be51d56da1ccacd03251491480e6602eb5a32633b7be6efd3fa6f"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85"
        )
