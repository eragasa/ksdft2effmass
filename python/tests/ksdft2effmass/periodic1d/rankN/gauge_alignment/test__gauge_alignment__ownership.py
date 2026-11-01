"""Ownership checks for rank-N gauge-alignment capabilities."""

import ast
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fields import (
    Periodic1DRankNGaugeAlignedFields,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.result import (
    Periodic1DRankNProcrustesDiagnostics,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
    Periodic1DRankNGaugeAlignmentConstructionRequest,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentStatusResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestGaugeAlignmentOwnership:
    """Keep gauge values and actions independent of composite orchestration."""

    def test__types__belong_to_gauge_alignment_modules(self) -> None:
        for value in (
            Periodic1DRankNGaugeAlignment,
            Periodic1DRankNGaugeAlignedFields,
            Periodic1DRankNGaugeAlignmentAnalysisRequest,
            Periodic1DRankNGaugeAlignmentConstructionRequest,
            Periodic1DRankNProcrustesDiagnostics,
            Periodic1DRankNAlignmentStatusResult,
        ):
            assert ".rankN.gauge_alignment" in value.__module__

    def test__source__does_not_import_composite_orchestration(self) -> None:
        package = Path(__file__).parents[5] / "src" / "ksdft2effmass" / "periodic1d"
        package = package / "rankN" / "gauge_alignment"

        for path in package.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
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
            assert all(
                "band_alignment.composite" not in value
                for value in imported_modules
            )
