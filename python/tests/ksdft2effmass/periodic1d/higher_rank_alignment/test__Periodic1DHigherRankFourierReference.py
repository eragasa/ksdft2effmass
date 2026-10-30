"""Tests for the bounded producer-independent Fourier reference slice."""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    fourier_reference as reference_module,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.fourier_reference import (
    Periodic1DHigherRankFourierReferenceAnalyzer,
    Periodic1DHigherRankFourierReferenceRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DHigherRankFourierReference:
    """Establish bounded coverage, request binding, and module independence."""

    def test__execute__recomputes_identity_and_oracle_fourier_controls(
        self,
        higher_rank_calculation_result: (
            Periodic1DHigherRankAlignmentCalculationResult
        ),
    ) -> None:
        request = Periodic1DHigherRankFourierReferenceRequest(
            calculation_result=higher_rank_calculation_result
        )
        analyzer = Periodic1DHigherRankFourierReferenceAnalyzer(request)

        reference = analyzer.execute()

        assert analyzer.request is request
        assert len(reference.comparisons) == 474
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )
        assert all(
            ".global-unitary." not in name and ".pointwise-unitary." not in name
            for name in reference.comparisons
        )
        assert sum(".interpolation." in name for name in reference.comparisons) == 48
        assert sum(".support[" in name for name in reference.comparisons) == 324
        assert (
            sum(".exact_coefficient[" in name for name in reference.comparisons) == 15
        )
        assert (
            sum(
                ".maximum_outside_exact_support_norm" in name
                for name in reference.comparisons
            )
            == 3
        )

    def test__execute__detects_tampered_fourier_evidence(
        self,
        higher_rank_calculation_result: (
            Periodic1DHigherRankAlignmentCalculationResult
        ),
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        identity, *remaining = first_mesh.gauge_alignment_results
        tampered_identity = replace(
            identity,
            parseval_relative_defect=1.0e-4,
            parseval_pass=False,
        )
        tampered_mesh = replace(
            first_mesh,
            gauge_alignment_results=(tampered_identity, *remaining),
        )
        tampered_result = replace(
            higher_rank_calculation_result,
            meshes=(tampered_mesh, *higher_rank_calculation_result.meshes[1:]),
        )

        reference = Periodic1DHigherRankFourierReferenceAnalyzer(
            Periodic1DHigherRankFourierReferenceRequest(
                calculation_result=tampered_result
            )
        ).execute()

        comparison = reference.comparisons[
            "mesh[513].identity.parseval_relative_defect"
        ]
        assert not comparison.result().passed

    def test__request__rejects_non_result_subject(self) -> None:
        with pytest.raises(TypeError, match="exact calculation result"):
            Periodic1DHigherRankFourierReferenceRequest(
                calculation_result="not-a-result"  # type: ignore[arg-type]
            )

    def test__module__does_not_import_producer_analysis_actions(self) -> None:
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
        assert "gauge_alignment.fourier" not in imported_modules
        assert "gauge_alignment.interpolation" not in imported_modules
        assert "gauge_alignment.locality" not in imported_modules
