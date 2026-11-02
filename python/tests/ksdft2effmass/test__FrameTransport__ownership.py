"""Scientific ownership contracts for frame transport."""

from __future__ import annotations

import pytest

from ksdft2effmass.frame_transport.base import (
    FrameTransport,
    FrameTransportAnalysis,
    FrameTransportAnalysisRequest,
    FrameTransportAnalyzer,
    PeriodicFrameTransport,
    PeriodicFrameTransportAnalysis,
    PeriodicFrameTransportAnalysisRequest,
    PeriodicFrameTransportAnalyzer,
)
from ksdft2effmass.gauge_alignment.base import GaugeAlignment
from ksdft2effmass.periodic1d.frame_transport.base import (
    Periodic1DFrameTransport,
    Periodic1DFrameTransportAnalysis,
    Periodic1DFrameTransportAnalysisRequest,
    Periodic1DFrameTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.base import (
    Periodic1DRank2FrameTransport,
    Periodic1DRank2FrameTransportAnalysis,
    Periodic1DRank2FrameTransportAnalysisRequest,
    Periodic1DRank2FrameTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.base import (
    Periodic1DRankNFrameTransportAnalysis,
    Periodic1DRankNFrameTransportAnalysisRequest,
    Periodic1DRankNFrameTransportAnalyzer,
    Periodic1DRankNFrameTransportCapability,
)
from ksdft2effmass.periodic2d.frame_transport.base import Periodic2DFrameTransport
from ksdft2effmass.periodic3d.frame_transport.base import Periodic3DFrameTransport

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestFrameTransportOwnership:
    """Keep transport distinct while enforcing domain-to-rank ownership."""

    def test_domain_and_periodic_roles_are_abstract_and_distinct_from_alignment(
        self,
    ) -> None:
        assert FrameTransportAnalysisRequest.__abstractmethods__ == frozenset()
        assert FrameTransportAnalysis.__abstractmethods__ == frozenset()
        assert FrameTransportAnalyzer.__abstractmethods__ == {"execute", "request"}
        assert issubclass(PeriodicFrameTransport, FrameTransport)
        assert issubclass(
            PeriodicFrameTransportAnalysisRequest,
            FrameTransportAnalysisRequest,
        )
        assert issubclass(PeriodicFrameTransportAnalysis, FrameTransportAnalysis)
        assert issubclass(PeriodicFrameTransportAnalyzer, FrameTransportAnalyzer)
        assert not issubclass(FrameTransport, GaugeAlignment)
        assert not issubclass(GaugeAlignment, FrameTransport)

    def test_dimension_roles_preserve_periodic_transport_ownership(self) -> None:
        for capability in (
            Periodic1DFrameTransport,
            Periodic2DFrameTransport,
            Periodic3DFrameTransport,
        ):
            assert issubclass(capability, PeriodicFrameTransport)
        assert issubclass(
            Periodic1DFrameTransportAnalysisRequest,
            PeriodicFrameTransportAnalysisRequest,
        )
        assert issubclass(
            Periodic1DFrameTransportAnalysis,
            PeriodicFrameTransportAnalysis,
        )
        assert issubclass(
            Periodic1DFrameTransportAnalyzer,
            PeriodicFrameTransportAnalyzer,
        )

    def test_rank_two_and_rank_n_are_sibling_specializations(self) -> None:
        assert Periodic1DRank2FrameTransport.__abstractmethods__ == {
            "band_subspace_rank"
        }
        assert Periodic1DRankNFrameTransportCapability.__abstractmethods__ == {
            "band_subspace_rank"
        }
        assert issubclass(Periodic1DRank2FrameTransport, Periodic1DFrameTransport)
        assert issubclass(
            Periodic1DRank2FrameTransportAnalysisRequest,
            Periodic1DFrameTransportAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRank2FrameTransportAnalysis,
            Periodic1DFrameTransportAnalysis,
        )
        assert issubclass(
            Periodic1DRank2FrameTransportAnalyzer,
            Periodic1DFrameTransportAnalyzer,
        )
        assert issubclass(
            Periodic1DRankNFrameTransportCapability,
            Periodic1DFrameTransport,
        )
        assert issubclass(
            Periodic1DRankNFrameTransportAnalysisRequest,
            Periodic1DFrameTransportAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRankNFrameTransportAnalysis,
            Periodic1DFrameTransportAnalysis,
        )
        assert issubclass(
            Periodic1DRankNFrameTransportAnalyzer,
            Periodic1DFrameTransportAnalyzer,
        )
        assert not issubclass(
            Periodic1DRank2FrameTransport,
            Periodic1DRankNFrameTransportCapability,
        )
        assert not issubclass(
            Periodic1DRankNFrameTransportCapability,
            Periodic1DRank2FrameTransport,
        )
