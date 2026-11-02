"""Periodic-3D arbitrary-rank locality and support-truncation contracts."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.periodic3d.rankN.hopping_locality.analysis import (
    Periodic3DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.hopping_locality.request import (
    Periodic3DRankNHoppingLocalityAnalysisRequest,
    Periodic3DRankNHoppingLocalityChannelEnum,
)
from ksdft2effmass.periodic3d.rankN.hopping_locality.result import (
    Periodic3DRankNHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic3d.rankN.support_truncation.analysis import (
    Periodic3DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.support_truncation.request import (
    Periodic3DRankNSupportTruncationAnalysisRequest,
    Periodic3DRankNSupportTruncationChannelEnum,
)
from ksdft2effmass.periodic3d.rankN.support_truncation.result import (
    Periodic3DRankNSupportTruncationAnalysis,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellSupportInventory,
    MinimumToleranceSatisfyingSupport,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNLocalityCapabilities:
    """Keep unchanged hopping diagnostics separate from irreversible truncation."""

    @staticmethod
    def _series(dimension: int, retained_rank: int) -> NumpyFiniteFourierMatrixSeries:
        modes = np.zeros((3, dimension), dtype=np.int64)
        modes[0, 0] = -1
        modes[2, 0] = 1
        identity = np.eye(retained_rank, dtype=np.complex128)
        blocks = np.stack((identity, 2.0 * identity, identity))
        return NumpyFiniteFourierMatrixSeries.from_arrays(dimension, modes, blocks)

    @staticmethod
    def _inventory(dimension: LatticeDimension) -> MetricShellSupportInventory:
        components: tuple[LatticeIntegerComponents, ...]
        indices: tuple[int, ...]
        if dimension is LatticeDimension.THREE:
            components = (
                (-1, 0, 0),
                (0, -1, 0),
                (0, 0, 0),
                (0, 1, 0),
                (1, 0, 0),
            )
            indices = (1, 2, 0, 2, 1)
        else:
            components = ((-1, 0), (0, 0), (1, 0))
            indices = (1, 0, 1)
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

    def test_hopping_locality_uses_explicit_rank_normalization(self) -> None:
        request = Periodic3DRankNHoppingLocalityAnalysisRequest(
            retained_rank=3,
            channel=Periodic3DRankNHoppingLocalityChannelEnum.REFERENCE,
            energy_reference="synthetic-zero",
            basis_identifier="retained-rank-three",
            series=self._series(3, 3),
            shell_indices=(1, 0, 1),
        )

        analyzer = Periodic3DRankNHoppingLocalityAnalyzer(
            request=request,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        )
        result = analyzer.execute()

        assert request.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
        assert analyzer.band_subspace_rank == 3
        assert type(result) is Periodic3DRankNHoppingLocalityAnalysis
        assert result.retained_rank == 3
        assert result.normalized_power_at_shell(0) == pytest.approx(4.0)
        assert result.normalized_power_at_shell(1) == pytest.approx(2.0)
        assert all(
            power.displacement.dimension is LatticeDimension.THREE
            for power in result.powers
        )

    def test_support_truncation_selects_each_error_functional_separately(self) -> None:
        request = Periodic3DRankNSupportTruncationAnalysisRequest(
            retained_rank=4,
            channel=Periodic3DRankNSupportTruncationChannelEnum.COMPARISON,
            support_inventory=self._inventory(LatticeDimension.THREE),
            total_errors=self._errors(),
            tolerance=0.15,
        )

        analyzer = Periodic3DRankNSupportTruncationAnalyzer(request=request)
        result = analyzer.execute()

        assert request.band_subspace_rank == 4
        assert result.band_subspace_rank == 4
        assert analyzer.band_subspace_rank == 4
        assert type(result) is Periodic3DRankNSupportTruncationAnalysis
        matrix = result.matrix_frobenius_maximum_error
        bands = result.ordered_eigenvalue_maximum_absolute_error
        assert type(matrix) is MinimumToleranceSatisfyingSupport
        assert type(bands) is MinimumToleranceSatisfyingSupport
        assert matrix.comparison_index == 1
        assert bands.comparison_index == 2

    def test_rejects_rank_two_and_two_dimensional_inputs(self) -> None:
        with pytest.raises(ValueError, match="at least three"):
            Periodic3DRankNHoppingLocalityAnalysisRequest(
                retained_rank=2,
                channel=Periodic3DRankNHoppingLocalityChannelEnum.REFERENCE,
                energy_reference="synthetic-zero",
                basis_identifier="rank-two",
                series=self._series(3, 2),
                shell_indices=(1, 0, 1),
            )
        with pytest.raises(ValueError, match="three-dimensional"):
            Periodic3DRankNSupportTruncationAnalysisRequest(
                retained_rank=3,
                channel=Periodic3DRankNSupportTruncationChannelEnum.REFERENCE,
                support_inventory=self._inventory(LatticeDimension.TWO),
                total_errors=self._errors()[:2],
                tolerance=0.15,
            )
