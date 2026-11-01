"""Software ownership contracts for :class:`GaugeAlignment`."""

from __future__ import annotations

import pytest

from ksdft2effmass.gauge_alignment import (
    GaugeAlignment,
    GaugeAlignmentAnalysis,
    GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DRank2AlignmentStudyAnalyzer,
    Periodic1DRankNAlignmentStudyAnalyzer,
)
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
    Periodic1DRank1AlignmentApplicabilityResult,
)
from ksdft2effmass.periodic1d.rank2.gauge_alignment.analysis import (
    Periodic1DRank2GaugeAlignmentAnalysisRequest,
    Periodic1DRank2GaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.gauge_alignment.result import (
    Periodic1DRank2GaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    Periodic1DRankNGaugeAlignmentMeshResult,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.analysis import (
    gauge_alignment as rankN_gauge_alignment_analysis,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestGaugeAlignment:
    """Establish nominal ownership and explicit analysis-role contracts."""

    def test__analysis_role_bases__require_scientific_identity_and_execution(
        self,
    ) -> None:
        assert GaugeAlignmentAnalysisRequest.__abstractmethods__ == {
            "alignment_sample_count",
            "gauge_group",
            "retained_rank",
        }
        assert GaugeAlignmentAnalysis.__abstractmethods__ == {
            "alignment_sample_count",
            "gauge_group",
            "retained_rank",
        }
        assert GaugeAlignmentAnalyzer.__abstractmethods__ == {"execute", "request"}

    def test__rank2_and_rankN_classes__implement_every_analysis_role(self) -> None:
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalysisRequest,
            GaugeAlignmentAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRankNGaugeAlignmentAnalysisRequest,
            GaugeAlignmentAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalysis,
            GaugeAlignmentAnalysis,
        )
        assert issubclass(
            Periodic1DRankNGaugeAlignmentMeshResult,
            GaugeAlignmentAnalysis,
        )
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalyzer,
            GaugeAlignmentAnalyzer,
        )
        assert issubclass(
            rankN_gauge_alignment_analysis.Periodic1DRankNGaugeAlignmentAnalyzer,
            GaugeAlignmentAnalyzer,
        )

    def test__periodic_rank_actions__share_nominal_owner(self) -> None:
        assert issubclass(Periodic1DGaugeAlignment, GaugeAlignment)
        assert issubclass(
            Periodic1DRank1AlignmentApplicabilityAnalyzer,
            Periodic1DGaugeAlignment,
        )
        assert issubclass(
            Periodic1DRank1AlignmentApplicabilityResult,
            Periodic1DGaugeAlignment,
        )
        assert issubclass(
            Periodic1DRank2AlignmentStudyAnalyzer,
            Periodic1DGaugeAlignment,
        )
        assert issubclass(
            Periodic1DRankNAlignmentStudyAnalyzer,
            Periodic1DGaugeAlignment,
        )

    def test__gauge_alignment__is_not_representation_equivalence(self) -> None:
        assert not issubclass(
            Periodic1DRank1AlignmentApplicabilityResult,
            RepresentationEquivalence,
        )
        assert not issubclass(
            Periodic1DRank2AlignmentStudyAnalyzer,
            RepresentationEquivalence,
        )
        assert not issubclass(
            Periodic1DRankNAlignmentStudyAnalyzer,
            RepresentationEquivalence,
        )

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        class UnrelatedResult:
            __slots__ = ()

            @property
            def retained_rank(self) -> int:
                return 2

            @property
            def gauge_group(self) -> str:
                return "U(2)"

            @property
            def alignment_sample_count(self) -> int:
                return 8

        unrelated = UnrelatedResult()
        assert not isinstance(unrelated, GaugeAlignment)
        assert not isinstance(unrelated, GaugeAlignmentAnalysis)
