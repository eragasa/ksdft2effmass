"""Tests for composite-alignment public ownership and donor isolation."""

from __future__ import annotations

import ast
import importlib.util
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
    """Establish explicit exports and prohibit predecessor runtime dependencies."""

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

    def test__Periodic1DCompositeBandAlignmentPublicSurface__predecessor_absent(
        self,
    ) -> None:
        """Keep the former dimension-level composite package non-importable."""
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic1d.composite_band_alignment"
            )
            is None
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__removes_former_exports(
        self,
    ) -> None:
        """Remove former multiband-alignment names from the periodic-1D root."""
        former_names = {
            "Periodic1DBlockHamiltonianToyModel",
            "Periodic1DMultibandAlignmentCalculationDefinition",
            "Periodic1DMultibandAlignmentCalculationResult",
            "Periodic1DMultibandAlignmentCalculator",
            "Periodic1DMultibandAlignmentDiagnostics",
            "Periodic1DMultibandAlignmentRangeResult",
            "Periodic1DMultibandAlignmentResultJsonSerializer",
            "Periodic1DMultibandAlignmentResultVerifier",
            "Periodic1DMultibandAlignmentVerificationResult",
        }

        assert all(not hasattr(periodic1d, name) for name in former_names)

    def test__Periodic1DCompositeBandAlignmentPublicSurface__removes_legacy_package(
        self,
    ) -> None:
        """Keep the former multiband-alignment package non-importable."""
        assert (
            importlib.util.find_spec("ksdft2effmass.periodic1d.multiband_alignment")
            is None
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__legacy_model_absent(
        self,
    ) -> None:
        """Keep the retired singular model namespace entirely non-importable."""
        assert importlib.util.find_spec("ksdft2effmass.periodic1d.model") is None
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic.periodic1d.models.multiband_alignment"
            )
            is None
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__removes_verifier_exports(
        self,
    ) -> None:
        """Do not expose a second verifier through the composite package."""
        former_names = {
            "Periodic1DCompositeBandAlignmentIndependentVerification",
            "Periodic1DCompositeBandAlignmentIndependentVerificationRequest",
            "Periodic1DCompositeBandAlignmentIndependentVerifier",
        }

        assert all(not hasattr(composite_band_alignment, name) for name in former_names)

    def test__Periodic1DCompositeBandAlignmentPublicSurface__removes_verifier_facade(
        self,
    ) -> None:
        """Keep the predecessor verification-values facade non-importable."""
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic1d.rank2.band_alignment.composite."
                "verification_values"
            )
            is None
        )

    def test__Periodic1DCompositeBandAlignmentPublicSurface__isolates_donor_imports(
        self,
    ) -> None:
        """Exclude predecessor and workflow imports from composite source modules."""
        package = Path(composite_band_alignment.__file__).resolve().parent
        forbidden = (
            "ksdft2effmass.periodic1d.multiband_alignment",
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
