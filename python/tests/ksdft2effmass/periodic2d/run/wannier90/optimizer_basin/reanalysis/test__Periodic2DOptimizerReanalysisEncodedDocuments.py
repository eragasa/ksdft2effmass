"""Software verification for optimizer-reanalysis encoded documents."""

import hashlib
from pathlib import Path

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    Periodic2DOptimizerReanalysisEncodedDocuments,
)


class TestPeriodic2DOptimizerReanalysisEncodedDocuments:
    """Verify exact optimizer-reanalysis document ownership."""

    def test_construction__preserves_retained_identities(self) -> None:
        """Preserve exact source/result SHA-256 identities."""
        base = Path(__file__).resolve().parents[8] / (
            "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        documents = Periodic2DOptimizerReanalysisEncodedDocuments(
            (base / "result.json").read_bytes(),
            (base / "reanalysis-result.json").read_bytes(),
        )
        assert hashlib.sha256(documents.source_result_payload).hexdigest() == (
            "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85"
        )
        assert hashlib.sha256(documents.result_payload).hexdigest() == (
            "89780db50cb367f429a7947894805a89fbfc757f571a55f82936507ef397f38b"
        )
