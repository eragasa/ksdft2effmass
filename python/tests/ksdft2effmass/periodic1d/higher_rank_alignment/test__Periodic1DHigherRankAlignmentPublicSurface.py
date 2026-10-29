"""Tests for the maintained higher-rank alignment public surface."""

import ast
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d as periodic1d
from ksdft2effmass.periodic1d import higher_rank_alignment

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DHigherRankAlignmentPublicSurface:
    """Establish explicit exports and isolate calculation-local donor code."""

    def test__package__exports_every_declared_public_name(self) -> None:
        for name in higher_rank_alignment.__all__:
            assert getattr(periodic1d, name) is getattr(higher_rank_alignment, name)
            assert "D1" not in name

    def test__source__does_not_import_calculation_workflow_material(self) -> None:
        package = Path(higher_rank_alignment.__file__).resolve().parent

        for path in package.glob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported_modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            } | {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            assert all("workflow" not in module for module in imported_modules)
            assert "HigherRankD1" not in source
