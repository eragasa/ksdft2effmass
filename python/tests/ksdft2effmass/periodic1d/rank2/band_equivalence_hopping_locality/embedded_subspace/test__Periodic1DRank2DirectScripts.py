"""Static contracts for ordered rank-two calculation entrypoints."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestPeriodic1DRank2DirectScripts:
    """Keep direct and diagnostic entrypoints explicit and correctly ordered."""

    @staticmethod
    def calculation_directory() -> Path:
        repository = next(
            parent
            for parent in Path(__file__).resolve().parents
            if (parent / "calculations").is_dir()
        )
        return (
            repository
            / "calculations"
            / "periodic1d"
            / "rank2"
            / "band-equivalence-versus-hopping-locality"
        )

    def test__entrypoints__have_the_complete_numbered_inventory(self) -> None:
        calculation = self.calculation_directory()
        expected_names = (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
            "run_10_flat_control.py",
            "run_11_nonflat_control.py",
            "run_12_parent_family_control.py",
            "run_13_truncation_control.py",
            "run_14_truncation_mesh_stability.py",
            "run_15_five_scale_evidence_assessment.py",
            "run_16_diagnostic_packaging.py",
            "run_complete_01_calculation.py",
            "run_complete_02_verification.py",
            "run_complete_03_render.py",
        )

        assert tuple(path.name for path in sorted(calculation.glob("run_*.py"))) == (
            expected_names
        )
        for name in expected_names:
            path = calculation / name
            assert path.stat().st_mode & 0o111
            assert path.read_text(encoding="utf-8").startswith(
                "#!/usr/bin/env python3\n"
            )

    def test__five_scale_entrypoint__uses_the_typed_assessment_owner(self) -> None:
        path = self.calculation_directory() / "run_15_five_scale_evidence_assessment.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module == "five_scale_evidence_assessment"
            for alias in node.names
        }

        assert imported_names == {"FiveScaleConsistencyAssessor"}

    def test__typed_support_modules__are_not_runnable_entrypoints(self) -> None:
        calculation = self.calculation_directory()
        for name in (
            "rank2_control_analysis.py",
            "five_scale_evidence_assessment.py",
        ):
            path = calculation / name
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))

            assert not source.startswith("#!")
            assert not any(
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                for node in ast.walk(tree)
            )
