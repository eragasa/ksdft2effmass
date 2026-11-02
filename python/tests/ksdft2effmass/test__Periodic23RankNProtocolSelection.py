"""Fail-closed ownership checks for prospective periodic-2D/3D rank-N protocols."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic23RankNProtocolSelection:
    """Keep both calculation roots documented and package namespaces inert."""

    def test_calculation_owned_decision_registers_are_dimension_specific(
        self,
        repository_root: Path,
    ) -> None:
        root = repository_root
        periodic2d = (
            root / "calculations" / "periodic2d" / "rankN" / "protocol-selection.md"
        ).read_text(encoding="utf-8")
        periodic3d = (
            root / "calculations" / "periodic3d" / "rankN" / "protocol-selection.md"
        ).read_text(encoding="utf-8")

        for record in (periodic2d, periodic3d):
            assert "AGGREGATE VERIFICATION INSTALLED" in record
            assert "VISUALIZATION AND LIFECYCLE PENDING" in record
            assert "EXECUTION NOT AUTHORIZED" in record
            assert "`3`, `4`, and `8`" in record
            assert "`1`, `2`, and `4`" in record
            assert "UNSELECTED" in record
            assert "No execution is\nauthorized" in record
            assert "Rank four remains a value of rank-N" in record
            assert "2 * retained_rank" in record
            assert "complete global-unitary Procrustes" in record
            assert "they do not inherit rank-two classes" in record
            assert "INSTALLED WITH TYPED AGGREGATE VERIFICATION" in record
            assert "Visualization projection" in record
            assert "VISUALIZATION-BOUND SCHEMAS PENDING" in record

        assert "Periodic2DRankN" in periodic2d
        assert "Periodic3DRankN" in periodic3d
        assert "two primitive neighbor directions" in periodic2d.lower()
        assert "one primitive-axis-pair plaquette family" in periodic2d.lower()
        assert "three primitive neighbor directions" in periodic3d.lower()
        assert "all three primitive-axis-pair plaquette families" in periodic3d.lower()

    def test_recommended_baselines_define_rank_general_analytic_controls(
        self,
        repository_root: Path,
    ) -> None:
        root = repository_root
        periodic2d = (
            root / "calculations" / "periodic2d" / "rankN" / "recommended-baseline.md"
        ).read_text(encoding="utf-8")
        periodic3d = (
            root / "calculations" / "periodic3d" / "rankN" / "recommended-baseline.md"
        ).read_text(encoding="utf-8")

        for record in (periodic2d, periodic3d):
            assert "AUTHORIZED SOFTWARE BASELINE" in record
            assert "IMPLEMENTATION IN PROGRESS; EXECUTION NOT AUTHORIZED" in record
            assert "external-gap lower bound `1.9`" in record
            assert "2 * retained_rank" not in record
            assert "global-unitary" in record
            assert "pointwise-unitary" in record
            assert "known-inverse-oracle" in record
            assert "no inheritance from\nrank-two classes" in record
            assert "does not authorize execution or retained evidence" in record

        assert "construction size `16`" in periodic2d
        assert "evaluation size `33`" in periodic2d
        assert "construction size `8`" in periodic3d
        assert "evaluation size `17`" in periodic3d
        assert "primitive-axis-pair plaquette diagnostic" in periodic2d
        assert "all three primitive-axis-pair plaquette" in periodic3d

    def test_package_namespaces_install_reviewed_aggregate_analysis_foundation(
        self,
        repository_root: Path,
    ) -> None:
        root = repository_root
        source_root = root / "python" / "src" / "ksdft2effmass"

        for dimension in ("periodic2d", "periodic3d"):
            rank_root = source_root / dimension / "rankN"
            initializer = (rank_root / "__init__.py").read_text(encoding="utf-8")
            assert initializer.strip().startswith('"""')
            assert "import " not in initializer
            assert "class " not in initializer
            assert (
                rank_root / "gauge_alignment" / "procrustes" / "analysis.py"
            ).is_file()
            assert (
                rank_root / "band_alignment" / "frame_transport" / "analysis.py"
            ).is_file()
            assert (rank_root / "hopping_locality" / "analysis.py").is_file()
            assert (rank_root / "support_truncation" / "analysis.py").is_file()
            aggregate_root = rank_root / "band_equivalence_hopping_locality"
            assert (aggregate_root / "model.py").is_file()
            assert (aggregate_root / "request.py").is_file()
            assert (aggregate_root / "case_expansion.py").is_file()
            assert (aggregate_root / "analysis.py").is_file()
            assert (aggregate_root / "result.py").is_file()
            assert (aggregate_root / "reference.py").is_file()
            assert (aggregate_root / "fourier_reference.py").is_file()
            assert (aggregate_root / "verification.py").is_file()
            assert not (aggregate_root / "lifecycle.py").exists()

    def test_calculation_roots_have_no_direct_entrypoints_or_rank4_namespace(
        self,
        repository_root: Path,
    ) -> None:
        root = repository_root

        for dimension in ("periodic2d", "periodic3d"):
            calculation_root = root / "calculations" / dimension / "rankN"
            assert calculation_root.is_dir()
            assert not list(calculation_root.rglob("run_01_calculation.py"))
            assert not list(calculation_root.rglob("run_02_verification.py"))
            assert not list(calculation_root.rglob("run_03_render.py"))
            assert not (root / "calculations" / dimension / "rank4").exists()
            assert not (
                root / "python" / "src" / "ksdft2effmass" / dimension / "rank4"
            ).exists()
