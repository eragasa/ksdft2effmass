"""Periodic-3D rank-two support-truncation action contracts."""

from __future__ import annotations

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)

from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.periodic3d.rank2.support_truncation.analysis import (
    Periodic3DRank2SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.support_truncation.request import (
    Periodic3DRank2SupportTruncationAnalysisRequest,
    Periodic3DRank2SupportTruncationChannelEnum,
)
from ksdft2effmass.periodic3d.rank2.support_truncation.result import (
    Periodic3DRank2SupportTruncationAnalysis,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellSupportInventory,
    MinimumToleranceSatisfyingSupport,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRank2SupportTruncationAnalyzer:
    """Select nested three-dimensional supports for one explicit model channel."""

    @staticmethod
    def _inventory(dimension: LatticeDimension) -> MetricShellSupportInventory:
        components: tuple[LatticeIntegerComponents, ...]
        if dimension is LatticeDimension.THREE:
            components = (
                (-1, 0, 0),
                (0, -1, 0),
                (0, 0, 0),
                (0, 1, 0),
                (1, 0, 0),
            )
        else:
            components = ((-1, 0), (0, 0), (1, 0))
        indices = (1, 2, 0, 2, 1) if len(components) == 5 else (1, 0, 1)
        return MetricShellSupportInventory(
            displacements=tuple(
                LatticeDisplacement(dimension, value) for value in components
            ),
            ordinal_shell_indices=indices,
        )

    @staticmethod
    def _errors() -> tuple[BandEquivalenceHoppingLocalityErrorChannels, ...]:
        return (
            BandEquivalenceHoppingLocalityErrorChannels(0.5, 0.3, 0.4, 0.25),
            BandEquivalenceHoppingLocalityErrorChannels(0.1, 0.08, 0.2, 0.15),
            BandEquivalenceHoppingLocalityErrorChannels(0.01, 0.008, 0.02, 0.015),
        )

    def test_selects_matrix_and_band_supports_without_merging_channels(self) -> None:
        request = Periodic3DRank2SupportTruncationAnalysisRequest(
            channel=Periodic3DRank2SupportTruncationChannelEnum.REFERENCE,
            support_inventory=self._inventory(LatticeDimension.THREE),
            total_errors=self._errors(),
            tolerance=0.15,
        )

        result = Periodic3DRank2SupportTruncationAnalyzer(request=request).execute()

        assert type(result) is Periodic3DRank2SupportTruncationAnalysis
        assert result.request is request
        matrix = result.matrix_frobenius_maximum_error
        bands = result.ordered_eigenvalue_maximum_absolute_error
        assert type(matrix) is MinimumToleranceSatisfyingSupport
        assert type(bands) is MinimumToleranceSatisfyingSupport
        assert matrix.comparison_index == 1
        assert matrix.support.retained_displacement_count == 3
        assert matrix.preceding_error == pytest.approx(0.5)
        assert bands.comparison_index == 2
        assert bands.support.retained_displacement_count == 5
        assert bands.preceding_error == pytest.approx(0.2)

    def test_rejects_a_two_dimensional_support_inventory(self) -> None:
        with pytest.raises(ValueError, match="three-dimensional"):
            Periodic3DRank2SupportTruncationAnalysisRequest(
                channel=Periodic3DRank2SupportTruncationChannelEnum.COMPARISON,
                support_inventory=self._inventory(LatticeDimension.TWO),
                total_errors=self._errors()[:2],
                tolerance=0.15,
            )
