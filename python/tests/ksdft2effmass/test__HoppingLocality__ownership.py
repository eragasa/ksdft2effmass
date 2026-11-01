"""Software ownership contracts for :class:`HoppingLocality`."""

from __future__ import annotations

import pytest

from ksdft2effmass.hopping_locality import HoppingLocality
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    Periodic1DRank2HoppingPower,
)
from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.rank1.hopping_locality import (
    Periodic1DRank1HoppingLocalityAnalysis,
    Periodic1DRank1HoppingTailResult,
)
from ksdft2effmass.periodic1d.rankN.hopping_locality import (
    Periodic1DRankNHoppingLocalityAnalysis,
    Periodic1DRankNHoppingTailResult,
)
from ksdft2effmass.support_truncation import SupportTruncation

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestHoppingLocality:
    def test__periodic_rank_slices__share_nominal_owner(self) -> None:
        """Rank-one, rank-two, and rank-N values diagnose unchanged coefficients."""
        assert issubclass(Periodic1DHoppingLocality, HoppingLocality)
        assert issubclass(
            Periodic1DRank1HoppingLocalityAnalysis,
            Periodic1DHoppingLocality,
        )
        assert issubclass(
            Periodic1DRank1HoppingTailResult,
            Periodic1DHoppingLocality,
        )
        assert issubclass(Periodic1DRank2HoppingPower, Periodic1DHoppingLocality)
        assert issubclass(
            Periodic1DRankNHoppingLocalityAnalysis,
            Periodic1DHoppingLocality,
        )
        assert issubclass(
            Periodic1DRankNHoppingTailResult,
            Periodic1DHoppingLocality,
        )

    def test__hopping_diagnostics__are_not_support_truncations(self) -> None:
        """Locality of unchanged coefficients does not imply their removal."""
        assert not issubclass(
            Periodic1DRank1HoppingLocalityAnalysis,
            SupportTruncation,
        )
        assert not issubclass(
            Periodic1DRank1HoppingTailResult,
            SupportTruncation,
        )
        assert not issubclass(Periodic1DRank2HoppingPower, SupportTruncation)
        assert not issubclass(
            Periodic1DRankNHoppingLocalityAnalysis,
            SupportTruncation,
        )
        assert not issubclass(Periodic1DRankNHoppingTailResult, SupportTruncation)

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone cannot admit an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        assert not isinstance(UnrelatedResult(), HoppingLocality)
