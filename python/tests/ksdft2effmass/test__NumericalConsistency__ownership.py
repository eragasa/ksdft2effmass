"""Software ownership contracts for :class:`NumericalConsistency`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementDiagnostics
from ksdft2effmass.band_equivalence_hopping_locality.geometry import (
    BandEquivalenceHoppingLocalityMetricCovarianceDefectResult,
)
from ksdft2effmass.band_equivalence_hopping_locality.refinement_records import (  # noqa: E501
    BandEquivalenceHoppingLocalityRefinementAssessment,
    BandEquivalenceHoppingLocalityRefinementPair,
)
from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis,
)
from ksdft2effmass.numerical_consistency import (
    NumericalConsistency,
    ReciprocalMeshRefinementFamily,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.momentum_refinement.analysis import (  # noqa: E501
    Periodic1DRank2MomentumRefinementAnalysis,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.embedded_subspace.momentum_refinement.family import (  # noqa: E501
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.refinement import (  # noqa: E501
    Periodic1DRankNRefinementAnalysis,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fourier import (  # noqa: E501
    Periodic1DRankNFourierAnalysis,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.interpolation import (  # noqa: E501
    Periodic1DRankNInterpolationAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestNumericalConsistency:
    def test__family_slices__share_nominal_owner(self) -> None:
        """Finite-route and refinement results retain numerical ownership."""
        assert issubclass(ScalarRefinementDiagnostics, NumericalConsistency)
        assert issubclass(ReciprocalMeshRefinementFamily, NumericalConsistency)
        assert issubclass(
            Periodic1DRank2MomentumRefinementAnalysis,
            NumericalConsistency,
        )
        assert issubclass(
            Periodic1DRank2MomentumRefinementFamilyAnalysis,
            NumericalConsistency,
        )
        assert issubclass(
            Periodic1DRank2AdaptiveAmplitudeAnalysis,
            NumericalConsistency,
        )
        assert issubclass(Periodic1DRankNFourierAnalysis, NumericalConsistency)
        assert issubclass(Periodic1DRankNInterpolationAnalysis, NumericalConsistency)
        assert issubclass(Periodic1DRankNRefinementAnalysis, NumericalConsistency)
        assert issubclass(
            BandEquivalenceHoppingLocalityMetricCovarianceDefectResult,
            NumericalConsistency,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityRefinementPair,
            NumericalConsistency,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityRefinementAssessment,
            NumericalConsistency,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis,
            NumericalConsistency,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis,
            NumericalConsistency,
        )

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone cannot admit an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        assert not isinstance(UnrelatedResult(), NumericalConsistency)
