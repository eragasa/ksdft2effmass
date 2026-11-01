"""Direct tests for one construction-mesh frame-transport analysis."""

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.analysis import (
    Periodic1DRankNFailedTransportAnalysis,
    Periodic1DRankNResolvedTransportAnalysis,
    Periodic1DRankNTransportAnalysisRequest,
    Periodic1DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


def _sample(
    request: Periodic1DRankNAlignmentCalculationRequest,
) -> Periodic1DRankNAnalyticMeshSample:
    model = Periodic1DRankNAnalyticCaseConstructor(
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
    ).execute()
    return Periodic1DRankNAnalyticMeshSample(model, request.configuration, 513)


class TestPeriodic1DRankNTransportAnalyzer:
    """Establish resolved and failed typed transport outcomes directly."""

    def test__execute__returns_resolved_transport_and_closure_defects(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
    ) -> None:
        analysis = Periodic1DRankNTransportAnalyzer(
            Periodic1DRankNTransportAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                sample=_sample(higher_rank_calculation_request),
            ),
            ClosedLoopPolarFrameTransporter(),
        ).execute()

        assert type(analysis) is Periodic1DRankNResolvedTransportAnalysis
        assert analysis.transport.construction_mesh_size == 513
        assert analysis.endpoint_closure_defect < 1.0e-12
        assert analysis.primitive_closure_defect < 1.0e-12

    def test__execute__returns_typed_backend_failure(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
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
