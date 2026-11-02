"""Periodic-3D rank-two hopping-locality action contracts."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.periodic3d.rank2.hopping_locality.analysis import (
    Periodic3DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.request import (
    Periodic3DRank2HoppingLocalityAnalysisRequest,
    Periodic3DRank2HoppingLocalityChannelEnum,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.result import (
    Periodic3DRank2HoppingLocalityAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRank2HoppingLocalityAnalyzer:
    """Bind one channel and preserve its three-dimensional metric-shell identity."""

    @staticmethod
    def _series(dimension: int) -> NumpyFiniteFourierMatrixSeries:
        modes = np.zeros((3, dimension), dtype=np.int64)
        modes[0, 0] = -1
        modes[2, 0] = 1
        blocks = np.zeros((3, 2, 2), dtype=np.complex128)
        blocks[0] = np.eye(2, dtype=np.complex128)
        blocks[1] = 2.0 * np.eye(2, dtype=np.complex128)
        blocks[2] = np.eye(2, dtype=np.complex128)
        return NumpyFiniteFourierMatrixSeries.from_arrays(dimension, modes, blocks)

    def test_executes_one_typed_three_dimensional_channel(self) -> None:
        request = Periodic3DRank2HoppingLocalityAnalysisRequest(
            channel=Periodic3DRank2HoppingLocalityChannelEnum.REFERENCE,
            energy_reference="synthetic-zero",
            basis_identifier="retained-rank-two",
            series=self._series(3),
            shell_indices=(1, 0, 1),
        )

        result = Periodic3DRank2HoppingLocalityAnalyzer(
            request=request,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()

        assert type(result) is Periodic3DRank2HoppingLocalityAnalysis
        assert result.request is request
        assert result.retained_rank == 2
        assert result.normalized_power_at_shell(0) == pytest.approx(4.0)
        assert result.normalized_power_at_shell(1) == pytest.approx(2.0)
        assert all(
            power.displacement.dimension is LatticeDimension.THREE
            for power in result.powers
        )

    def test_rejects_a_two_dimensional_series(self) -> None:
        with pytest.raises(ValueError, match="three-dimensional"):
            Periodic3DRank2HoppingLocalityAnalysisRequest(
                channel=Periodic3DRank2HoppingLocalityChannelEnum.COMPARISON,
                energy_reference="synthetic-zero",
                basis_identifier="retained-rank-two",
                series=self._series(2),
                shell_indices=(1, 0, 1),
            )
