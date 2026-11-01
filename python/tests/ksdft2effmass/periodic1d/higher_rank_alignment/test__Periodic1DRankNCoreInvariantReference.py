"""Tests for the bounded producer-independent core-invariant reference slice."""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.higher_rank_alignment import reference as reference_module
from ksdft2effmass.periodic1d.higher_rank_alignment.reference import (
    Periodic1DRankNCoreInvariantReferenceAnalyzer,
    Periodic1DRankNCoreInvariantReferenceRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNCoreInvariantReference:
    """Establish independence, request binding, and tamper detection."""

    def test__execute__reconstructs_every_model_core_invariant(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        request = Periodic1DRankNCoreInvariantReferenceRequest(
            result=higher_rank_calculation_result
        )
        analyzer = Periodic1DRankNCoreInvariantReferenceAnalyzer(request)

        reference = analyzer.execute()

        assert analyzer.request is request
        assert len(reference.comparisons) == 51
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )

    def test__execute__detects_a_tampered_model_diagnostic(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        tampered_diagnostics = replace(
            first_mesh.model_diagnostics,
            gauge_unitarity_defect=1.0e-4,
        )
        tampered_mesh = replace(
            first_mesh,
            model_diagnostics=tampered_diagnostics,
        )
        tampered_result = replace(
            higher_rank_calculation_result,
            meshes=(tampered_mesh, *higher_rank_calculation_result.meshes[1:]),
        )
        request = Periodic1DRankNCoreInvariantReferenceRequest(result=tampered_result)

        reference = Periodic1DRankNCoreInvariantReferenceAnalyzer(request).execute()

        comparison = reference.comparisons["mesh_513_gauge_unitarity_defect"]
        assert not comparison.result().passed

    def test__request__rejects_non_result_subject(self) -> None:
        with pytest.raises(
            TypeError,
            match="Periodic1DRankNAlignmentCalculationResult",
        ):
            Periodic1DRankNCoreInvariantReferenceRequest(result="not-a-result")  # type: ignore[arg-type]

    def test__module__does_not_directly_import_producer_scientific_actions(
        self,
    ) -> None:
        module_path = Path(reference_module.__file__).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=module_path)
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }

        assert "model" not in imported_modules
        assert "analysis" not in imported_modules
        assert "diagnostics" not in imported_modules
        assert all("gauge_alignment" not in name for name in imported_modules)
