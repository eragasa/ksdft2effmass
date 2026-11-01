"""Static dependency checks for embedded rank-two scientific features."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement as amplitude_refinement  # noqa: E501
import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement as momentum_refinement  # noqa: E501
import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family as parent_family  # noqa: E501
import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale as parent_scale  # noqa: E501
import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention as retention  # noqa: E501
import ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.visualizations as visualizations  # noqa: E501
from ksdft2effmass.periodic1d.rank2 import support_truncation

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRank2FeatureDependencyDirection:
    """Keep scientific feature packages independent of retention and rendering."""

    def test_scientific_features__do_not_import_retention_or_visualizations(
        self,
    ) -> None:
        feature_directories = (
            Path(parent_scale.__file__).parent,
            Path(parent_family.__file__).parent,
            Path(momentum_refinement.__file__).parent,
            Path(amplitude_refinement.__file__).parent,
            Path(support_truncation.__file__).parent,
        )
        prohibited: list[tuple[Path, str]] = []
        for directory in feature_directories:
            for path in directory.glob("*.py"):
                for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                    if isinstance(node, ast.Import):
                        modules = tuple(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module is not None:
                        modules = (node.module,)
                    else:
                        continue
                    for module in modules:
                        if {"retention", "visualizations"}.intersection(
                            module.split(".")
                        ):
                            prohibited.append((path, module))

        assert prohibited == []

    def test_retention__does_not_import_rank2_visualizations(self) -> None:
        prohibited: list[tuple[Path, str]] = []
        for path in Path(retention.__file__).parent.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if (
                    isinstance(node, ast.ImportFrom)
                    and node.level > 0
                    and node.module is not None
                    and node.module.split(".")[0] == "visualizations"
                ):
                    prohibited.append((path, node.module))

        assert prohibited == []

    def test_visualizations__consume_retention_owned_projection_data(self) -> None:
        visualization_directory = Path(visualizations.__file__).parent

        assert not (visualization_directory / "data.py").exists()
        for name in ("figures.py", "visualizer.py"):
            tree = ast.parse(
                (visualization_directory / name).read_text(encoding="utf-8")
            )
            assert any(
                isinstance(node, ast.ImportFrom)
                and node.module == "retention.visualization_data"
                for node in ast.walk(tree)
            )

    def test_retention_and_visualizations__import_in_either_order(self) -> None:
        modules = (
            f"{retention.__name__}.visualization_data",
            visualizations.__name__,
        )
        for order in (modules, tuple(reversed(modules))):
            source = "; ".join(f"import {module}" for module in order)
            completed = subprocess.run(
                [sys.executable, "-c", source],
                check=False,
                capture_output=True,
                text=True,
            )
            assert completed.returncode == 0, completed.stderr
