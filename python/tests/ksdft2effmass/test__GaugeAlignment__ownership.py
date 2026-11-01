"""Software ownership contracts for :class:`GaugeAlignment`."""

from __future__ import annotations

import pytest

from ksdft2effmass.gauge_alignment import GaugeAlignment
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DRank2AlignmentStudyAnalyzer,
    Periodic1DRankNAlignmentStudyAnalyzer,
)
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
    Periodic1DRank1AlignmentApplicabilityResult,
)
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestGaugeAlignment:
    """Establish nominal ownership without structural admission."""

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

        assert not isinstance(UnrelatedResult(), GaugeAlignment)
