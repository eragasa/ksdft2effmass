"""Tests for direct composite-alignment public ownership and donor isolation."""

import ast
import importlib.util
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d as periodic1d
from ksdft2effmass.periodic1d import composite_band_alignment

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentPublicSurface:
    """Establish explicit exports and prohibit predecessor runtime dependencies."""

    def test__package__exports_every_declared_public_class(self) -> None:
        for name in composite_band_alignment.__all__:
            assert getattr(periodic1d, name) is getattr(composite_band_alignment, name)

    def test__package__has_no_legacy_multiband_alignment_surface(self) -> None:
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
        assert former_names.isdisjoint(periodic1d.__all__)
        assert all(not hasattr(periodic1d, name) for name in former_names)
        assert (
            importlib.util.find_spec("ksdft2effmass.periodic1d.multiband_alignment")
            is None
        )
        assert importlib.util.find_spec("ksdft2effmass.periodic1d.model") is None

    def test__independent_reference__has_no_verification_values_facade(self) -> None:
        former_names = {
            "Periodic1DCompositeBandAlignmentIndependentVerification",
            "Periodic1DCompositeBandAlignmentIndependentVerificationRequest",
            "Periodic1DCompositeBandAlignmentIndependentVerifier",
        }
        assert former_names.isdisjoint(composite_band_alignment.__all__)
        assert all(not hasattr(composite_band_alignment, name) for name in former_names)
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic1d.composite_band_alignment.verification_values"
            )
            is None
        )

    def test__source__does_not_import_predecessor_or_calculation_workflows(
        self,
    ) -> None:
        package = Path(composite_band_alignment.__file__).resolve().parent
        forbidden = (
            "ksdft2effmass.periodic1d.multiband_alignment",
            "ksdft2effmass.campaigns.periodic_1d",
            "workflow",
        )

        for path in package.glob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
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
            assert all(
                not any(token in module for token in forbidden) for module in modules
            )
