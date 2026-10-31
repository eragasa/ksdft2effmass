"""Static software contracts for the unexecuted complete-five-scale lifecycle."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestPeriodic1DRank2CompleteFiveScaleDirectScripts:
    """Check stage ownership without executing scientific-scale parameters."""

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

    def test__scripts__declare_distinct_ordered_stage_contracts(self) -> None:
        directory = self.calculation_directory()
        contracts = {
            "run_complete_01_calculation.py": (
                "direct-embedded-rank2-five-scale-complete-v1",
                "Periodic1DRank2CompleteFiveScaleCalculationRecord",
                "calculation.json",
            ),
            "run_complete_02_verification.py": (
                "calculation.json",
                "Periodic1DRank2CompleteFiveScaleVerifier",
                "verification.json",
            ),
            "run_complete_03_render.py": (
                "verification.json",
                "Periodic1DRank2CompleteFiveScaleSummaryRenderer",
                "complete-five-scale-summary.md",
            ),
        }

        for name, required_fragments in contracts.items():
            path = directory / name
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))

            assert source.startswith("#!/usr/bin/env python3\n")
            assert path.stat().st_mode & 0o111
            assert all(fragment in source for fragment in required_fragments)
            assert "workflow" not in source
        calculation_source = (directory / "run_complete_01_calculation.py").read_text(
            encoding="utf-8"
        )
        assert '"source_revision": source_revision' in calculation_source
        assert '"source_worktree_clean": True' in calculation_source

    def test__scripts__use_generic_typed_records_without_private_codecs(self) -> None:
        directory = self.calculation_directory()
        forbidden = (
            "CalculationWireEnum",
            "_mapping(",
            "_from_mapping(",
            "mapping_json",
            "schema.json",
        )

        for path in sorted(directory.glob("run_complete_*.py")):
            source = path.read_text(encoding="utf-8")

            assert not any(fragment in source for fragment in forbidden)
            assert ".to_json()" in source or ".from_json(" in source
