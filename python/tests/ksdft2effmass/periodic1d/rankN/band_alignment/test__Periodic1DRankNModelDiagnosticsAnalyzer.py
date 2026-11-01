"""Tests for rank-N analytic-model diagnostics ownership and execution."""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment import (
    model_diagnostics as diagnostics_module,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model_diagnostics import (
    Periodic1DRankNModelDiagnostics,
    Periodic1DRankNModelDiagnosticsAnalyzer,
    Periodic1DRankNModelDiagnosticsRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNModelDiagnosticsAnalyzer:
    """Establish direct analysis behavior and non-composite ownership."""

    def test__execute__returns_request_bound_diagnostics(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
    ) -> None:
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=higher_rank_calculation_request.retained_rank,
            circuit_depth=higher_rank_calculation_request.circuit_depth,
        ).execute()
        sample = Periodic1DRankNAnalyticMeshSample(
            model,
            higher_rank_calculation_request.configuration,
            513,
        )

        diagnostics = Periodic1DRankNModelDiagnosticsAnalyzer(
            Periodic1DRankNModelDiagnosticsRequest(
                calculation_request=higher_rank_calculation_request,
                sample=sample,
            )
        ).execute()

        assert (
            diagnostics.case_identity == higher_rank_calculation_request.case_identity
        )
        assert diagnostics.construction_mesh_size == 513
        assert diagnostics.parent_hermiticity_defect < 1.0e-12
        assert diagnostics.reference_operator_recovery_defect < 1.0e-12
        assert (
            Periodic1DRankNModelDiagnostics.from_json(diagnostics.to_json()).to_json()
            == diagnostics.to_json()
        )

    @pytest.mark.parametrize(
        "field",
        ("retained_rank", "circuit_depth", "construction_mesh_size"),
    )
    def test__result__rejects_boolean_integer_fields(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
        field: str,
    ) -> None:
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=higher_rank_calculation_request.retained_rank,
            circuit_depth=higher_rank_calculation_request.circuit_depth,
        ).execute()
        sample = Periodic1DRankNAnalyticMeshSample(
            model,
            higher_rank_calculation_request.configuration,
            513,
        )
        diagnostics = Periodic1DRankNModelDiagnosticsAnalyzer(
            Periodic1DRankNModelDiagnosticsRequest(
                calculation_request=higher_rank_calculation_request,
                sample=sample,
            )
        ).execute()

        with pytest.raises(TypeError, match="built-in integer"):
            replace(diagnostics, **{field: True})  # type: ignore[arg-type]

    def test__module__does_not_import_composite_orchestration(self) -> None:
        module_file = diagnostics_module.__file__
        assert module_file is not None
        module_path = Path(module_file).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=module_path)
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }

        assert all(
            "band_alignment.composite" not in value for value in imported_modules
        )
