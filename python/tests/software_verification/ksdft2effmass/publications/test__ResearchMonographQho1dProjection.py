"""Software verification for the research-monograph direct QHO1D projection."""

import hashlib
import json
from pathlib import Path

from ksdft2effmass.model_systems.qho1d import (
    Qho1dCalculationResult,
    Qho1dCrossGridAnalysisRequest,
    Qho1dCrossGridAnalyzer,
    Qho1dCrossGridVerifier,
)


class TestResearchMonographQho1dProjection:
    """Verify Appendix E consumes only the direct typed QHO1D execution."""

    repository_root = Path(__file__).resolve().parents[5]
    execution_root = (
        repository_root
        / "calculations"
        / "qho1d"
        / "executions"
        / "direct-spatial-truncation-3x3x3"
    )
    monograph_root = repository_root / "docs" / "publications" / "research-monograph"

    def test_source__appendix_e__names_direct_execution_only(self) -> None:
        """Appendix E does not cite the absent historical calculation tree."""
        source = (
            self.monograph_root / "appendices" / "E-harmonic-oscillator-comparison.tex"
        ).read_text(encoding="utf-8")

        assert "calculations/qho1d/executions/direct-spatial-truncation-3x3x3" in source
        assert (
            "83c420ccd365bfba23401b98069566625049bd18dfac47568b006e848176993b" in source
        )
        assert (
            "c8f1fcc968a2c8e497d6bd9ea6e287506eb2f528bcaaa7ea523b937d3c86c7ac" in source
        )
        assert "calculations/research-monograph/harmonic-oscillator" not in source
        assert "convergence-summary.png" not in source
        assert "operator-difference-heatmap.png" not in source

    def test_artifacts__figure_copies__equal_authenticated_execution_bytes(
        self,
    ) -> None:
        """Every manuscript-local QHO1D figure is an exact source-byte copy."""
        figure_names = (
            "qho1d-eigenstates.png",
            "qho1d-eigenstate-distortion.png",
            "qho1d-diagnostics.png",
        )
        expected_digests = {
            "qho1d-eigenstates.png": (
                "d016e16a6ecc2eea216a8e329347f1c878febb7839c096384e2009c5cb328ca7"
            ),
            "qho1d-eigenstate-distortion.png": (
                "792b8a6b80806f62efd1b6f18562d7fa21d9b76792b15c97725e744076508a66"
            ),
            "qho1d-diagnostics.png": (
                "47fc9084f3c409506befc847fbdce752f31452cdd5df8cd58b5fcf19a4cc5441"
            ),
        }
        for name in figure_names:
            source = (self.execution_root / "figures" / name).read_bytes()
            local = (
                self.monograph_root / "figures" / "retained-calculations" / name
            ).read_bytes()
            assert local == source
            assert hashlib.sha256(local).hexdigest() == expected_digests[name]

    def test_artifacts__result_and_verification__retain_declared_identities(
        self,
    ) -> None:
        """The consumed result and verification bytes match Appendix E identities."""
        result_path = self.execution_root / "results" / "result.json"
        verification_path = self.execution_root / "verification" / "verification.json"
        result_bytes = result_path.read_bytes()
        verification_bytes = verification_path.read_bytes()
        verification = json.loads(verification_bytes)

        assert hashlib.sha256(result_bytes).hexdigest() == (
            "83c420ccd365bfba23401b98069566625049bd18dfac47568b006e848176993b"
        )
        assert hashlib.sha256(verification_bytes).hexdigest() == (
            "c8f1fcc968a2c8e497d6bd9ea6e287506eb2f528bcaaa7ea523b937d3c86c7ac"
        )
        assert verification["comparison_count"] == 468
        assert verification["verification"]["components"]

    def test_analysis__cross_grid__derives_verified_direct_diagnostics(self) -> None:
        """The selected migrated diagnostic operates on the direct typed result."""
        result_bytes = (self.execution_root / "results" / "result.json").read_bytes()
        result = Qho1dCalculationResult.from_json(result_bytes)
        assert result.to_json() == result_bytes
        analysis = Qho1dCrossGridAnalyzer(
            Qho1dCrossGridAnalysisRequest(result)
        ).execute()
        verification = Qho1dCrossGridVerifier().execute(result, analysis)

        assert len(analysis.comparisons) == 18
        assert len(verification.observations) == 90
        assert verification.passed
