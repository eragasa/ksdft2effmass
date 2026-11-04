"""Cross-rank contracts for Periodic1D calculation entrypoints."""

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRankFirstCalculationEntrypoints:
    """Keep rank-specific calculations consistent without merging their science."""

    @staticmethod
    def repository() -> Path:
        return Path(__file__).resolve().parents[5]

    @classmethod
    def calculation_source(cls, rank: str, file_name: str) -> str:
        """Read one rank-owned calculation entrypoint from its maintained location."""
        if rank == "rank1":
            calculation_root = (
                cls.repository() / "calculations/periodic1d_rank1/"
                "band_equivalence_hopping_locality"
            )
        else:
            calculation_root = (
                cls.repository()
                / "calculations"
                / "periodic1d"
                / rank
                / "composite-band-alignment-locality"
            )
        return (calculation_root / file_name).read_text(encoding="utf-8")

    def test__Periodic1DRankFirstCalculationEntrypoints__uses_exact_actions(
        self,
    ) -> None:
        """Keep each retained-rank entrypoint bound to its exact action owner."""
        rank1 = self.calculation_source("rank1", "run_01_calculation.py")
        rank2 = self.calculation_source("rank2", "run_01_calculation.py")
        rankn = self.calculation_source("rankN", "run_01_calculation.py")

        assert "Periodic1DFourierLocalityAnalyzer(configuration).execute()" in rank1
        assert "Periodic1DAlignmentStudyFactory" not in rank1
        assert "AlignmentStudySpecification" not in rank1

        assert "Periodic1DAlignmentStudyFactory(" in rank2
        assert ").create()" in rank2
        assert "Periodic1DRank2AlignmentStudySpecification" in rank2
        assert "configuration.reduced_lattice_geometry" in rank2
        assert "Periodic1DCompositeBandAlignmentAnalyzer" not in rank2

        assert "Periodic1DAlignmentStudyFactory(" in rankn
        assert ").create()" in rankn
        assert "Periodic1DRankNAlignmentStudySpecification" in rankn
        assert "configuration.reduced_lattice_geometry" in rankn
        assert (
            "return Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer(" not in rankn
        )

    def test__Periodic1DRankFirstCalculationEntrypoints__preserves_geometry_wire(
        self,
    ) -> None:
        """Bind rank-two and rank-N geometry without changing retained result wires."""
        for file_name in (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        ):
            assert '"lattice_geometry"' in self.calculation_source(
                "rank2",
                file_name,
            )

        rankn_calculation = self.calculation_source(
            "rankN",
            "run_01_calculation.py",
        )
        rankn_cache = (
            self.repository()
            / "calculations"
            / "periodic1d"
            / "rankN"
            / "composite-band-alignment-locality"
            / "analysis"
            / "development"
            / "cache.py"
        ).read_text(encoding="utf-8")
        assert '"lattice-geometry.json"' in rankn_calculation
        assert '"lattice_geometry"' in rankn_calculation
        assert "higher-rank-development-result-cache.v2" in rankn_cache
        assert "manifest.lattice_geometry" in rankn_cache
