"""Tests for the rank-two periodic frame-transport capability."""

import numpy as np
import pytest
from projectkoios.physkit.units import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.periodic1d.rank2.band_alignment import (
    frame_transport as namespace,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport import (
    analysis as analysis_module,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport import (
    request as request_module,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport import (
    result as result_module,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.analysis import (
    Periodic1DRank2TransportAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.request import (
    Periodic1DRank2TransportAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.result import (
    Periodic1DRank2ResolvedTransportAnalysis,
)
from ksdft2effmass.solidstate.band_frames import ReciprocalBandFramePath1D
from ksdft2effmass.solidstate.reciprocal_paths import (
    CenteredUniformReciprocalMesh1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2TransportAnalyzer:
    """Establish dedicated ownership of the rank-two transport action."""

    def test__namespace__is_inert_and_defining_modules_own_the_public_types(
        self,
    ) -> None:
        assert analysis_module.__all__ == ["Periodic1DRank2TransportAnalyzer"]
        assert request_module.__all__ == ["Periodic1DRank2TransportAnalysisRequest"]
        assert result_module.__all__ == ["Periodic1DRank2ResolvedTransportAnalysis"]

        assert not hasattr(namespace, "Periodic1DRank2TransportAnalyzer")

    def test__request__requires_the_frozen_construction_mesh(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="construction inventory"):
            Periodic1DRank2TransportAnalysisRequest(
                configuration=composite_configuration,
                source=self._path(point_count=32),
            )

    def test__execute__returns_closed_transport_evidence(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        request = Periodic1DRank2TransportAnalysisRequest(
            configuration=composite_configuration,
            source=self._path(point_count=64),
        )
        analyzer = Periodic1DRank2TransportAnalyzer(request)

        analysis = analyzer.execute()

        assert analyzer.request is request
        assert type(analysis) is Periodic1DRank2ResolvedTransportAnalysis
        assert analysis.request is request
        assert analysis.transported.rank == 2
        assert analysis.transported.ambient_dimension == 4
        assert analysis.minimum_overlap_singular_value == pytest.approx(1.0)
        assert analysis.closure_eigenphases == pytest.approx((0.0, 0.0))

    @staticmethod
    def _path(*, point_count: int) -> ReciprocalBandFramePath1D:
        unit = Unitless()
        frame = np.eye(4, 2, dtype=np.complex128)
        return ReciprocalBandFramePath1D(
            mesh=CenteredUniformReciprocalMesh1D(
                reciprocal_period=ScalarQuantity(1.0, unit),
                point_count=point_count,
            ),
            frames=tuple(
                ComplexMatrixQuantity(frame.copy(), unit) for _ in range(point_count)
            ),
            sewing_map=ComplexMatrixQuantity(np.eye(4, dtype=np.complex128), unit),
            orthonormality_absolute_tolerance=1.0e-12,
        )
