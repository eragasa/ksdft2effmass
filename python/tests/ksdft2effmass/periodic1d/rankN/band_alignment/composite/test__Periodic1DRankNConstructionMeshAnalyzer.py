"""Direct tests for one rank-N construction-mesh analysis."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation_result import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.construction_mesh import (
    Periodic1DRankNConstructionMeshAnalysisRequest,
    Periodic1DRankNConstructionMeshAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRankNConstructionMeshAnalyzer:
    """Establish direct request correlation and exact one-mesh behavior."""

    def test__execute__matches_case_level_mesh_bytes(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
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

        result = Periodic1DRankNConstructionMeshAnalyzer(
            request=Periodic1DRankNConstructionMeshAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                sample=sample,
                global_selection=higher_rank_calculation_result.global_selection,
            ),
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert result.to_json() == higher_rank_calculation_result.meshes[0].to_json()

    def test__request__rejects_model_from_another_case(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        foreign_model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=2,
        ).execute()
        foreign_sample = Periodic1DRankNAnalyticMeshSample(
            foreign_model,
            higher_rank_calculation_request.configuration,
            513,
        )

        with pytest.raises(ValueError, match="sample must match"):
            Periodic1DRankNConstructionMeshAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                sample=foreign_sample,
                global_selection=higher_rank_calculation_result.global_selection,
            )
