"""Tests for composite-alignment public ownership and donor isolation."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d as periodic1d
from ksdft2effmass.periodic1d.rank2.band_alignment import (
    composite as composite_band_alignment,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentPublicSurface:
    """Establish explicit exports and direct runtime dependencies."""

    def test__Periodic1DCompositeBandAlignmentPublicSurface__keeps_root_non_eager(
        self,
    ) -> None:
        """Keep the periodic-1D root free of an eager export inventory."""
        assert not hasattr(periodic1d, "__all__")

    def test__Periodic1DCompositeBandAlignmentPublicSurface__keeps_package_non_eager(
        self,
    ) -> None:
        """Keep the composite package free of an eager export inventory."""
        assert not hasattr(composite_band_alignment, "__all__")

    def test__Periodic1DCompositeBandAlignmentPublicSurface__avoids_package_reexports(
        self,
    ) -> None:
        """Require callers to import composite owners from defining modules."""
        assert not any(
            name.startswith("Periodic1DCompositeBandAlignment")
            for name in vars(composite_band_alignment)
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__owns_configuration(
        self,
    ) -> None:
        """Define the configuration in the rank-two band-alignment package."""
        assert Periodic1DCompositeBandAlignmentConfiguration.__module__ == (
            "ksdft2effmass.periodic1d.rank2.band_alignment.configuration"
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__owns_analyzer(
        self,
    ) -> None:
        """Define the analyzer in the rank-two composite-analysis package."""
        assert Periodic1DCompositeBandAlignmentAnalyzer.__module__ == (
            "ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis"
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__isolates_donor_imports(
        self,
    ) -> None:
        """Exclude campaign and workflow imports from composite source modules."""
        package = Path(composite_band_alignment.__file__).resolve().parent
        forbidden = (
            "ksdft2effmass.campaigns.periodic_1d",
            "workflow",
        )
        violations: list[tuple[str, str]] = []

        for path in package.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            } | {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            violations.extend(
                (path.name, module)
                for module in modules
                if any(token in module for token in forbidden)
            )

        assert violations == []
