"""Software verification of visualization package ownership and legacy removal."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

import ksdft2effmass.model_systems.mathieu1d.visualizations as mathieu_visualizations
import ksdft2effmass.model_systems.piab1d.visualizations as piab_visualizations
import ksdft2effmass.model_systems.qho1d.visualizations as qho_visualizations
import ksdft2effmass.visualizations as visualizations
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dVisualizer
from ksdft2effmass.model_systems.piab1d import Piab1dVisualizer
from ksdft2effmass.model_systems.qho1d import Qho1dVisualizer
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVisualizer,
)
from ksdft2effmass.periodic1d.fourier_locality import (
    visualizations as fourier_visualizations,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    visualizations as composite_visualizations,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.visualizations.visualizer import (  # noqa: E501
    Periodic1DCompositeBandAlignmentVisualizer,
)
from ksdft2effmass.visualizations import (
    BaseFigure,
    BaseFigureRenderer,
    BasePlot,
    BaseSubplot,
    BaseVisualization,
    BaseVisualizationData,
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestVisualizationOwnership:
    """Keep shared mechanics domain-neutral and remove singular compatibility paths."""

    def test_public_api__exports_only_root_visualization_contracts(self) -> None:
        expected = {
            "BaseFigure": BaseFigure,
            "BaseFigureRenderer": BaseFigureRenderer,
            "BasePlot": BasePlot,
            "BaseSubplot": BaseSubplot,
            "BaseVisualization": BaseVisualization,
            "BaseVisualizationData": BaseVisualizationData,
            "BaseVisualizer": BaseVisualizer,
            "PngFigureRenderer": PngFigureRenderer,
            "PngVisualization": PngVisualization,
        }
        assert set(visualizations.__all__) == set(expected)
        for name, owner in expected.items():
            assert getattr(visualizations, name) is owner

    def test_family_packages__export_only_supported_contracts(self) -> None:
        packages_and_prefixes = (
            (piab_visualizations, "Piab1d"),
            (qho_visualizations, "Qho1d"),
            (mathieu_visualizations, "Mathieu1d"),
            (fourier_visualizations, "Periodic1DFourierLocality"),
        )
        for package, prefix in packages_and_prefixes:
            assert set(package.__all__) == {
                f"{prefix}VisualizationData",
                f"{prefix}VisualizationPlotEnum",
                f"{prefix}Visualizer",
            }
        assert not hasattr(composite_visualizations, "__all__")
        assert not any(
            name.startswith("Periodic1DCompositeBandAlignment")
            for name in vars(composite_visualizations)
        )

    def test_family_visualizers__use_final_aggregate_action(self) -> None:
        family_visualizers = (
            Piab1dVisualizer,
            Qho1dVisualizer,
            Mathieu1dVisualizer,
            Periodic1DFourierLocalityVisualizer,
            Periodic1DCompositeBandAlignmentVisualizer,
        )
        for visualizer in family_visualizers:
            assert visualizer.visualize is BaseVisualizer.visualize

    def test_source__imports_no_scientific_family(self) -> None:
        source_directory = (
            Path(__file__).resolve().parents[3]
            / "src"
            / "ksdft2effmass"
            / "visualizations"
        )
        for source_path in sorted(source_directory.glob("*.py")):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            imported_modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            }
            imported_modules.update(
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            )
            assert not any("model_systems" in name for name in imported_modules)
            assert not any("periodic1d" in name for name in imported_modules)

    @pytest.mark.parametrize(
        "module_name",
        (
            "ksdft2effmass.model_systems.visualization",
            "ksdft2effmass.model_systems.piab1d.visualization",
            "ksdft2effmass.model_systems.qho1d.visualization",
            "ksdft2effmass.model_systems.mathieu1d.visualization",
            "ksdft2effmass.periodic1d.fourier_locality.visualization",
            "ksdft2effmass.periodic1d.rank2.band_alignment.composite.visualization",
        ),
    )
    def test_import__singular_legacy_module__is_absent(self, module_name: str) -> None:
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(module_name)
