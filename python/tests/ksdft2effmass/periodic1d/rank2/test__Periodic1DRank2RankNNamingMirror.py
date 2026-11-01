"""Tests for mirrored rank-two and rank-N capability naming."""

import pytest

from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.analysis import (
    Periodic1DRank2TransportAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.request import (
    Periodic1DRank2TransportAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport.result import (
    Periodic1DRank2ResolvedTransportAnalysis,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.analysis import (
    Periodic1DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.request import (
    Periodic1DRank2HoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.result import (
    Periodic1DRank2HoppingLocalityAnalysis,
    Periodic1DRank2HoppingTailResult,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.analysis import (
    Periodic1DRank2SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.request import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.band_alignment.result import (
    Periodic1DRank2SupportResult,
    Periodic1DRank2SupportTruncationAnalysis,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.analysis import (
    Periodic1DRankNResolvedTransportAnalysis,
    Periodic1DRankNTransportAnalysisRequest,
    Periodic1DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.hopping_locality.analysis import (
    Periodic1DRankNHoppingLocalityAnalysis,
    Periodic1DRankNHoppingLocalityAnalysisRequest,
    Periodic1DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.hopping_locality.result import (
    Periodic1DRankNHoppingTailResult,
)
from ksdft2effmass.periodic1d.rankN.support_truncation.analysis import (
    Periodic1DRankNSupportTruncationAnalysis,
    Periodic1DRankNSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.support_truncation.result import (
    Periodic1DRankNSupportResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2RankNNamingMirror:
    """Keep equivalent capability roles lexically aligned across ranks."""

    def test__frame_transport__mirrors_rankN_role_names(self) -> None:
        rank2_names = (
            Periodic1DRank2TransportAnalysisRequest.__name__,
            Periodic1DRank2ResolvedTransportAnalysis.__name__,
            Periodic1DRank2TransportAnalyzer.__name__,
        )
        rankn_names = (
            Periodic1DRankNTransportAnalysisRequest.__name__,
            Periodic1DRankNResolvedTransportAnalysis.__name__,
            Periodic1DRankNTransportAnalyzer.__name__,
        )
        assert rank2_names == tuple(
            name.replace("RankN", "Rank2") for name in rankn_names
        )

    def test__hopping_locality__mirrors_rankN_role_names(self) -> None:
        rank2_names = (
            Periodic1DRank2HoppingLocalityAnalysisRequest.__name__,
            Periodic1DRank2HoppingLocalityAnalysis.__name__,
            Periodic1DRank2HoppingLocalityAnalyzer.__name__,
            Periodic1DRank2HoppingTailResult.__name__,
        )
        rankn_names = (
            Periodic1DRankNHoppingLocalityAnalysisRequest.__name__,
            Periodic1DRankNHoppingLocalityAnalysis.__name__,
            Periodic1DRankNHoppingLocalityAnalyzer.__name__,
            Periodic1DRankNHoppingTailResult.__name__,
        )
        assert rank2_names == tuple(
            name.replace("RankN", "Rank2") for name in rankn_names
        )

    def test__support_truncation__mirrors_rankN_role_names(self) -> None:
        rank2_names = (
            Periodic1DRank2SupportTruncationAnalysisRequest.__name__,
            Periodic1DRank2SupportTruncationAnalysis.__name__,
            Periodic1DRank2SupportTruncationAnalyzer.__name__,
            Periodic1DRank2SupportResult.__name__,
        )
        rankn_names = (
            Periodic1DRankNSupportTruncationAnalysisRequest.__name__,
            Periodic1DRankNSupportTruncationAnalysis.__name__,
            Periodic1DRankNSupportTruncationAnalyzer.__name__,
            Periodic1DRankNSupportResult.__name__,
        )
        assert rank2_names == tuple(
            name.replace("RankN", "Rank2") for name in rankn_names
        )
