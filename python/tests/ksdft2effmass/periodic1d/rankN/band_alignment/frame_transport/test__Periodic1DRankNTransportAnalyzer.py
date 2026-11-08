"""Direct tests for one construction-mesh frame-transport analysis."""

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.analysis import (
    Periodic1DRankNFailedTransportAnalysis,
    Periodic1DRankNResolvedTransportAnalysis,
    Periodic1DRankNTransportAnalysisRequest,
    Periodic1DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.base import (
    Periodic1DRankNFrameTransportAnalysis,
    Periodic1DRankNFrameTransportAnalysisRequest,
    Periodic1DRankNFrameTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNConstructionMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from periodic1d_rankn_analytic_case_support import (
    SyntheticPeriodic1DRankNAnalyticCaseConstructor,
)
from periodic1d_rankn_analytic_oracle import analytic_fourier_givens_transformation
from periodic1d_rankn_control_basis_support import synthetic_basis_identity

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


def _sample(
    request: Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
) -> Periodic1DRankNConstructionMeshSample:
    model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
        basis_identity=synthetic_basis_identity(request.retained_rank),
        gauge_transformation=analytic_fourier_givens_transformation(
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
        ),
    ).execute()
    return Periodic1DRankNConstructionMeshSample(
        model.parent_model,
        model.gauge_transformation,
        request.configuration,
        513,
    )


class TestPeriodic1DRankNTransportAnalyzer:
    """Establish resolved and failed typed transport outcomes directly."""

    def test__execute__returns_resolved_transport_and_closure_defects(
        self,
        higher_rank_calculation_request: (
            Periodic1DRankNBandEquivalenceHoppingLocalityRequest
        ),
    ) -> None:
        request = Periodic1DRankNTransportAnalysisRequest(
            calculation_request=higher_rank_calculation_request,
            sample=_sample(higher_rank_calculation_request),
        )
        analyzer = Periodic1DRankNTransportAnalyzer(
            request,
            ClosedLoopPolarFrameTransporter(),
        )

        analysis = analyzer.execute()

        assert isinstance(request, Periodic1DRankNFrameTransportAnalysisRequest)
        assert isinstance(analysis, Periodic1DRankNFrameTransportAnalysis)
        assert isinstance(analyzer, Periodic1DRankNFrameTransportAnalyzer)
        assert (
            request.band_subspace_rank == higher_rank_calculation_request.retained_rank
        )
        assert analysis.band_subspace_rank == request.band_subspace_rank
        assert analyzer.band_subspace_rank == request.band_subspace_rank
        assert type(analysis) is Periodic1DRankNResolvedTransportAnalysis
        assert analysis.transport.construction_mesh_size == 513
        assert analysis.endpoint_closure_defect < 1.0e-12
        assert analysis.primitive_closure_defect < 1.0e-12

    def test__execute__returns_typed_backend_failure(
        self,
        higher_rank_calculation_request: (
            Periodic1DRankNBandEquivalenceHoppingLocalityRequest
        ),
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def fail_transport(
            transporter: ClosedLoopPolarFrameTransporter,
            source: FinitePeriodicMeshFrameInventory,
        ) -> None:
            del transporter, source
            raise ClosedLoopPolarFrameTransportBackendFailure(
                operation=ClosedLoopPolarFrameTransportBackendOperation.PROCRUSTES_SVD,
                reason=ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE,
                link_index=0,
            )

        monkeypatch.setattr(
            ClosedLoopPolarFrameTransporter,
            "transport",
            fail_transport,
        )

        analysis = Periodic1DRankNTransportAnalyzer(
            Periodic1DRankNTransportAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                sample=_sample(higher_rank_calculation_request),
            ),
            ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert type(analysis) is Periodic1DRankNFailedTransportAnalysis
        assert analysis.failure.construction_mesh_size == 513
        assert analysis.failure.link_index == 0
