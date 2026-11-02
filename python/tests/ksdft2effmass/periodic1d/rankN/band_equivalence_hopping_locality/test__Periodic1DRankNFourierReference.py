"""Tests for the bounded producer-independent Fourier reference slice."""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality import (
    analytic_reference as analytic_reference_module,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality import (
    fourier_reference as reference_module,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic1DRankNFourierReferenceAnalyzer,
    Periodic1DRankNFourierReferenceRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis as StudyAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNFourierReference:
    """Establish bounded coverage, request binding, and module independence."""

    def test__execute__recomputes_all_fourier_controls(
        self,
        higher_rank_calculation_result: (StudyAnalysis),
    ) -> None:
        request = Periodic1DRankNFourierReferenceRequest(
            calculation_result=higher_rank_calculation_result
        )
        analyzer = Periodic1DRankNFourierReferenceAnalyzer(request)

        reference = analyzer.execute()

        assert analyzer.request is request
        assert len(reference.comparisons) == 930
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )
        assert sum(".global-unitary." in name for name in reference.comparisons) == 228
        assert (
            sum(".pointwise-unitary." in name for name in reference.comparisons) == 228
        )
        assert sum(".interpolation." in name for name in reference.comparisons) == 96
        assert sum(".support[" in name for name in reference.comparisons) == 648
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

    def test__execute__detects_tampered_fourier_evidence_across_alignments(
        self,
        higher_rank_calculation_result: StudyAnalysis,
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        alignments = list(first_mesh.gauge_alignment_results)
        tampered_wires = ("identity", "global-unitary", "pointwise-unitary")
        for alignment_index in range(len(tampered_wires)):
            alignments[alignment_index] = replace(
                alignments[alignment_index],
                parseval_relative_defect=1.0e-4,
                parseval_pass=False,
            )
        tampered_mesh = replace(
            first_mesh,
            gauge_alignment_results=tuple(alignments),
        )
        tampered_result = replace(
            higher_rank_calculation_result,
            meshes=(tampered_mesh, *higher_rank_calculation_result.meshes[1:]),
        )

        reference = Periodic1DRankNFourierReferenceAnalyzer(
            Periodic1DRankNFourierReferenceRequest(calculation_result=tampered_result)
        ).execute()

        for wire_value in tampered_wires:
            comparison = reference.comparisons[
                f"mesh[513].{wire_value}.parseval_relative_defect"
            ]
            assert not comparison.result().passed

    def test__request__rejects_non_result_subject(self) -> None:
        with pytest.raises(TypeError, match="exact calculation result"):
            Periodic1DRankNFourierReferenceRequest(
                calculation_result="not-a-result"  # type: ignore[arg-type]
            )

    def test__module__does_not_import_producer_analysis_actions(self) -> None:
        for module in (reference_module, analytic_reference_module):
            module_file = module.__file__
            assert module_file is not None
            module_path = Path(module_file).resolve()
            tree = ast.parse(
                module_path.read_text(encoding="utf-8"),
                filename=module_path,
            )
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
