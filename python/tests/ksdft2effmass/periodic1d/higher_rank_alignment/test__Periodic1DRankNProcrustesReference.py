"""Tests for the bounded producer-independent Procrustes reference slice."""

import ast
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    procrustes_reference as reference_module,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.procrustes_reference import (
    Periodic1DRankNProcrustesReferenceAnalyzer,
    Periodic1DRankNProcrustesReferenceRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNProcrustesReference:
    """Establish bounded selection coverage, binding, and independence."""

    def test__execute__recomputes_global_and_pointwise_selections(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        request = Periodic1DRankNProcrustesReferenceRequest(
            calculation_result=higher_rank_calculation_result
        )
        analyzer = Periodic1DRankNProcrustesReferenceAnalyzer(request)

        reference = analyzer.execute()

        assert analyzer.request is request
        assert len(reference.comparisons) == 57
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )
        assert (
            sum(name.startswith("global-selection") for name in reference.comparisons)
            == 15
        )
        assert (
            sum(".pointwise-selection." in name for name in reference.comparisons) == 42
        )
        assert (
            sum(
                name.endswith(".cross_singular_values")
                for name in reference.comparisons
            )
            == 4
        )
        assert (
            sum(
                name.endswith(".normalized_optimal_residuals")
                for name in reference.comparisons
            )
            == 4
        )

    def test__execute__detects_tampered_selected_global_unitary(
        self,
        higher_rank_calculation_result: (Periodic1DRankNAlignmentCalculationResult),
    ) -> None:
        global_selection = higher_rank_calculation_result.global_selection
        selected = global_selection.selected_global_right_unitary
        assert selected is not None
        tampered_selection = replace(
            global_selection,
            selected_global_right_unitary=ComplexMatrixQuantity(
                -np.asarray(selected.magnitude, dtype=np.complex128),
                Unitless(),
            ),
        )
        tampered_result = replace(
            higher_rank_calculation_result,
            global_selection=tampered_selection,
        )

        reference = Periodic1DRankNProcrustesReferenceAnalyzer(
            Periodic1DRankNProcrustesReferenceRequest(
                calculation_result=tampered_result
            )
        ).execute()

        comparison = reference.comparisons["global-selection[2049].right_unitary"]
        assert not comparison.result().passed

    def test__request__rejects_non_result_subject(self) -> None:
        with pytest.raises(TypeError, match="exact calculation result"):
            Periodic1DRankNProcrustesReferenceRequest(
                calculation_result="not-a-result"  # type: ignore[arg-type]
            )

    def test__module__does_not_import_producer_selection_actions(self) -> None:
        module_path = Path(reference_module.__file__).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=module_path)
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }

        assert "calculation" not in imported_modules
        assert "model" not in imported_modules
        assert "analysis" not in imported_modules
        assert "analysis.procrustes" not in imported_modules
        assert all(
            not module.startswith("projectkoios.optimization")
            for module in imported_modules
        )
