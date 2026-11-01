"""Software ownership contracts for :class:`GaugeAlignment`."""

from __future__ import annotations

import pytest

from ksdft2effmass.gauge_alignment import (
    GaugeAlignment,
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysis,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalyzer,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.gauge_alignment import (
    Periodic1DGaugeAlignment,
    Periodic1DGaugeAlignmentAnalysis,
    Periodic1DGaugeAlignmentAnalysisRequest,
    Periodic1DGaugeAlignmentAnalyzer,
)
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
            "analysis_identity"
        }
        assert GaugeAlignmentAnalysis.__abstractmethods__ == {"analysis_identity"}
        assert GaugeAlignmentAnalyzer.__abstractmethods__ == {"_execute", "request"}

    def test__analysis_identity__validates_exact_common_values(self) -> None:
        identity = GaugeAlignmentAnalysisIdentity(
            retained_rank=2,
            gauge_group="U(2)",
            alignment_sample_count=8,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=(
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL
            ),
        )

        assert identity.retained_rank == 2
        assert identity.gauge_group == "U(2)"
        assert identity.alignment_sample_count == 8
        assert identity.action_convention.to_wire() == "right"
        assert identity.inner_product_convention.to_wire() == "euclidean-orthonormal"
        with pytest.raises(TypeError, match="retained_rank"):
            GaugeAlignmentAnalysisIdentity(
                True,  # type: ignore[arg-type]
                "U(2)",
                8,
                GaugeAlignmentActionConvention.RIGHT,
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
            )
        with pytest.raises(ValueError, match="retained_rank"):
            GaugeAlignmentAnalysisIdentity(
                0,
                "U(0)",
                8,
                GaugeAlignmentActionConvention.RIGHT,
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
            )
        with pytest.raises(ValueError, match="gauge_group"):
            GaugeAlignmentAnalysisIdentity(
                2,
                "",
                8,
                GaugeAlignmentActionConvention.RIGHT,
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
            )
        with pytest.raises(TypeError, match="alignment_sample_count"):
            GaugeAlignmentAnalysisIdentity(
                2,
                "U(2)",
                True,  # type: ignore[arg-type]
                GaugeAlignmentActionConvention.RIGHT,
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
            )

    def test__analyzer__rejects_analysis_identity_drift(self) -> None:
        request_identity = GaugeAlignmentAnalysisIdentity(
            2,
            "U(2)",
            8,
            GaugeAlignmentActionConvention.RIGHT,
            GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
        )
        result_identity = GaugeAlignmentAnalysisIdentity(
            2,
            "U(2)",
            16,
            GaugeAlignmentActionConvention.RIGHT,
            GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL,
        )

        class Request(GaugeAlignmentAnalysisRequest):
            __slots__ = ()

            @property
            def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
                return request_identity

        class Analysis(GaugeAlignmentAnalysis):
            __slots__ = ()

            @property
            def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
                return result_identity

        class Analyzer(GaugeAlignmentAnalyzer[Request, Analysis]):
            __slots__ = ("_request",)

            def __init__(self, request: Request) -> None:
                self._request = request

            @property
            def request(self) -> Request:
                return self._request

            def _execute(self) -> Analysis:
                return Analysis()

        with pytest.raises(ValueError, match="identity must match"):
            Analyzer(Request()).execute()

    def test__periodic_role_bases__specialize_every_shared_role(self) -> None:
        assert issubclass(
            Periodic1DGaugeAlignmentAnalysisRequest,
            GaugeAlignmentAnalysisRequest,
        )
        assert issubclass(
            Periodic1DGaugeAlignmentAnalysis,
            GaugeAlignmentAnalysis,
        )
        assert issubclass(
            Periodic1DGaugeAlignmentAnalyzer,
            GaugeAlignmentAnalyzer,
        )
        for value in (
            Periodic1DGaugeAlignmentAnalysisRequest,
            Periodic1DGaugeAlignmentAnalysis,
            Periodic1DGaugeAlignmentAnalyzer,
        ):
            assert issubclass(value, Periodic1DGaugeAlignment)

    def test__rank2_and_rankN_classes__implement_every_analysis_role(self) -> None:
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalysisRequest,
            Periodic1DGaugeAlignmentAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRankNGaugeAlignmentAnalysisRequest,
            Periodic1DGaugeAlignmentAnalysisRequest,
        )
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalysis,
            Periodic1DGaugeAlignmentAnalysis,
        )
        assert issubclass(
            Periodic1DRankNGaugeAlignmentMeshResult,
            Periodic1DGaugeAlignmentAnalysis,
        )
        assert issubclass(
            Periodic1DRank2GaugeAlignmentAnalyzer,
            Periodic1DGaugeAlignmentAnalyzer,
        )
        assert issubclass(
            rankN_gauge_alignment_analysis.Periodic1DRankNGaugeAlignmentAnalyzer,
            Periodic1DGaugeAlignmentAnalyzer,
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
