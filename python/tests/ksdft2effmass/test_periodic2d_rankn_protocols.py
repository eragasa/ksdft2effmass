"""Fail-closed ownership checks for periodic-2D rank-N protocols."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic2DRankNProtocols:
    """Keep the periodic-2D calculation and software boundaries fail-closed."""

    def test_calculation_owned_decision_register_is_dimension_specific(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "periodic2d"
            / "rankN"
            / "protocol-selection.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "AGGREGATE VERIFICATION INSTALLED",
            "VISUALIZATION AND LIFECYCLE PENDING",
            "EXECUTION NOT AUTHORIZED",
            "`3`, `4`, and `8`",
            "`1`, `2`, and `4`",
            "UNSELECTED",
            "No execution is\nauthorized",
            "Rank four remains a value of rank-N",
            "2 * retained_rank",
            "complete global-unitary Procrustes",
            "`Periodic2DRank2...` operation owners then refine",
            "does not inherit rank-two calculation policy",
            "INSTALLED WITH TYPED AGGREGATE VERIFICATION",
            "Visualization projection",
            "VISUALIZATION-BOUND SCHEMAS PENDING",
            "Periodic2DRankN",
        ):
            assert phrase in record
        assert "two primitive neighbor directions" in record.lower()
        assert "one primitive-axis-pair plaquette family" in record.lower()

    def test_recommended_baseline_defines_rank_general_analytic_controls(
        self,
        repository_root: Path,
    ) -> None:
        record = (
            repository_root
            / "calculations"
            / "periodic2d"
            / "rankN"
            / "recommended-baseline.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "AUTHORIZED SOFTWARE BASELINE",
            "IMPLEMENTATION IN PROGRESS; EXECUTION NOT AUTHORIZED",
            "external-gap lower bound `1.9`",
            "global-unitary",
            "pointwise-unitary",
            "known-inverse-oracle",
            "`Periodic2DRank2...` operation owners refine them",
            "does not transfer rank-two calculation policy",
            "does not authorize execution or retained evidence",
            "construction size `16`",
            "evaluation size `33`",
            "primitive-axis-pair plaquette diagnostic",
        ):
            assert phrase in record
        assert "2 * retained_rank" not in record

    def test_package_namespace_installs_reviewed_aggregate_foundation(
        self,
        repository_root: Path,
    ) -> None:
        rank_root = (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic2d"
            / "rankN"
        )
        initializer = (rank_root / "__init__.py").read_text(encoding="utf-8")

        assert initializer.strip().startswith('"""')
        assert "import " not in initializer
        assert "class " not in initializer
        assert (rank_root / "gauge_alignment" / "procrustes" / "analysis.py").is_file()
        assert (
            rank_root / "band_alignment" / "frame_transport" / "analysis.py"
        ).is_file()
        assert (rank_root / "hopping_locality" / "analysis.py").is_file()
        assert (rank_root / "support_truncation" / "analysis.py").is_file()
        assert (rank_root / "gauge_alignment" / "attack.py").is_file()
        parent_model = (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic"
            / "periodic2d"
            / "rankN"
            / "models"
            / "analytic.py"
        )
        assert parent_model.is_file()
        aggregate_root = rank_root / "band_equivalence_hopping_locality"
        for filename in (
            "case.py",
            "request.py",
            "case_expansion.py",
            "analysis.py",
            "result.py",
            "reference.py",
            "fourier_reference.py",
            "verification.py",
        ):
            assert (aggregate_root / filename).is_file()
        assert not (aggregate_root / "lifecycle.py").exists()

    def test_calculation_root_has_no_direct_entrypoints_or_rank4_namespace(
        self,
        repository_root: Path,
    ) -> None:
        calculation_root = repository_root / "calculations" / "periodic2d" / "rankN"

        assert calculation_root.is_dir()
        assert (calculation_root / "control_basis.py").is_file()
        assert not list(calculation_root.rglob("run_01_calculation.py"))
        assert not list(calculation_root.rglob("run_02_verification.py"))
        assert not list(calculation_root.rglob("run_03_render.py"))
        assert not (repository_root / "calculations" / "periodic2d" / "rank4").exists()
        assert not (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic2d"
            / "rank4"
        ).exists()
