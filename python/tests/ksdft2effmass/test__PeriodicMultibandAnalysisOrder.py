"""Fail-closed documentation checks for periodic multiband analysis ordering."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodicMultibandAnalysisOrder:
    """Keep every live periodic owner bound to the shared dependency order."""

    _CALCULATION_READMES = (
        "periodic1d/rank1/fourier-locality/README.md",
        "periodic1d/rank2/band-equivalence-versus-hopping-locality/README.md",
        "periodic1d/rank2/composite-band-alignment-locality/README.md",
        "periodic1d/rankN/composite-band-alignment-locality/README.md",
        "periodic2d/rank1/hopping-shell-hierarchy/README.md",
        "periodic2d/rank2/orthogonal/band-equivalence-locality/README.md",
        "periodic2d_rank2_hexagonal/README.md",
        "periodic2d_rank2_rhombic_path/README.md",
        "periodic2d/rankN/README.md",
        "periodic2d/rankN/composite-band-alignment-locality/README.md",
        "periodic3d/rank1/anisotropic-hopping-support-hierarchy/README.md",
        "periodic3d_rank2_simple_cubic/README.md",
        "periodic3d_rank2_fcc_diamond/README.md",
        "periodic3d_rank2_bain_path/README.md",
        "periodic3d/rankN/README.md",
        "periodic3d/rankN/composite-band-alignment-locality/README.md",
        "periodic3d_rankN_bain_path/README.md",
        "band-equivalence-dimensional-comparison/README.md",
    )

    def test_program_order_separates_dependencies_operations_and_evidence(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "periodic"
            / "multiband"
            / "analysis-order.md"
        ).read_text(encoding="utf-8")

        headings = (
            "## Program-level order",
            "## Fixed-geometry family order",
            "## Continuous-path family order",
            "## Higher-rank admission order",
            "## Evidence and rendering order",
        )
        positions = tuple(record.index(heading) for heading in headings)

        assert positions == tuple(sorted(positions))
        assert "NOT EXECUTION AUTHORITY" in record
        assert "Alignment must precede subtraction" in record
        assert "Descriptive locality must precede support removal" in record
        assert "Withheld interpolation must be measured before truncation" in record
        assert "Rendering never recalculates science" in record
        assert "isotropic 2-D, isotropic 3-D, anisotropic 2-D" in record
        assert "`mathieu1d/` remains outside this multiband" in record

    def test_live_calculation_owners_record_local_analysis_order(
        self,
        repository_root: Path,
    ) -> None:
        calculation_root = repository_root / "calculations"

        for relative_path in self._CALCULATION_READMES:
            record = (calculation_root / relative_path).read_text(encoding="utf-8")
            assert "## Analysis order" in record, relative_path
            assert "analysis-order.md" in record, relative_path

    def test_continuous_paths_keep_geometry_and_response_channels_ordered(
        self,
        repository_root: Path,
    ) -> None:
        calculation_root = repository_root / "calculations"
        rank_two = (
            calculation_root / "periodic3d_rank2_bain_path" / "README.md"
        ).read_text(encoding="utf-8")
        rank_n = (
            calculation_root / "periodic3d_rankN_bain_path" / "README.md"
        ).read_text(encoding="utf-8")

        assert rank_two.index("qualify the unit-volume path") < rank_two.index(
            "analyze M0"
        )
        assert rank_two.index("analyze M0") < rank_two.index("analyze M1")
        assert rank_two.index("analyze M1") < rank_two.index("analyze M2")
        assert rank_n.index("selected path geometry") < rank_n.index("selected M0")
        assert rank_n.index("selected M0") < rank_n.index("selected M1N")
        assert rank_n.index("selected M1N") < rank_n.index("exact M2")
        assert "The current protocol stops after step 3" in rank_n

    def test_cross_family_comparison_requires_admitted_sources(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "band-equivalence-dimensional-comparison"
            / "README.md"
        ).read_text(encoding="utf-8")

        assert "authenticate each family-owned nominal result" in record
        assert "without changing any\n   family threshold or identity" in record
        assert "dependent comparison remains\nunavailable or unresolved" in record
