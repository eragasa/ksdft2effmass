"""Direct tests for one rank-N construction-mesh analysis."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNConstructionMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.construction_mesh import (  # noqa: E501
    Periodic1DRankNConstructionMeshAnalysisRequest,
    Periodic1DRankNConstructionMeshAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest as StudyRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis as StudyAnalysis,
)
from periodic1d_rankn_analytic_case_support import (
    SyntheticPeriodic1DRankNAnalyticCaseConstructor,
)
from periodic1d_rankn_analytic_oracle import analytic_fourier_givens_transformation
from periodic1d_rankn_control_basis_support import synthetic_basis_identity

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRankNConstructionMeshAnalyzer:
    """Establish direct request correlation and exact one-mesh behavior."""

    def test__execute__matches_case_level_mesh_bytes(
        self,
        higher_rank_calculation_request: StudyRequest,
        higher_rank_calculation_result: StudyAnalysis,
    ) -> None:
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=higher_rank_calculation_request.retained_rank,
            circuit_depth=higher_rank_calculation_request.circuit_depth,
            basis_identity=synthetic_basis_identity(
                higher_rank_calculation_request.retained_rank
            ),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=higher_rank_calculation_request.retained_rank,
                circuit_depth=higher_rank_calculation_request.circuit_depth,
            ),
        ).execute()
        sample = Periodic1DRankNConstructionMeshSample(
            model.parent_model,
            model.gauge_transformation,
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
        higher_rank_calculation_request: StudyRequest,
        higher_rank_calculation_result: StudyAnalysis,
    ) -> None:
        foreign_model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=2,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=2,
            ),
        ).execute()
        foreign_sample = Periodic1DRankNConstructionMeshSample(
            foreign_model.parent_model,
            foreign_model.gauge_transformation,
            higher_rank_calculation_request.configuration,
            513,
        )

        with pytest.raises(ValueError, match="sample must match"):
            Periodic1DRankNConstructionMeshAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                sample=foreign_sample,
                global_selection=higher_rank_calculation_result.global_selection,
            )
