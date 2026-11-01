"""Software ownership contracts for :class:`RepresentationEquivalence`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.results import (
    BandEquivalenceLocalityRepresentationEquivalenceAnalysis,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.results import (  # noqa: E501
    Periodic1DRank2PointAnalysis,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.recovery import (  # noqa: E501
    Periodic1DRankNRecoveryAnalysis,
)
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestRepresentationEquivalence:
    def test__family_results__share_nominal_owner(self) -> None:
        """Rank-two, rank-N, and multidimensional results share ownership."""
        assert issubclass(Periodic1DRank2PointAnalysis, RepresentationEquivalence)
        assert issubclass(Periodic1DRankNRecoveryAnalysis, RepresentationEquivalence)
        assert issubclass(
            BandEquivalenceLocalityRepresentationEquivalenceAnalysis,
            RepresentationEquivalence,
        )

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone cannot admit an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        assert not isinstance(UnrelatedResult(), RepresentationEquivalence)
