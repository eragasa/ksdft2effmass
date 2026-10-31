"""Verify typed ownership of normalized physical-metric shell powers."""

from __future__ import annotations

import sys
from typing import cast

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    BlockHoppingModel,
    BlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.shell_power import (  # noqa: E501
    MetricShellHoppingPower,
    MetricShellHoppingPowerAnalyzer,
    MetricShellHoppingPowerResult,
)

pytestmark = pytest.mark.unit


def _model() -> BlockHoppingModel:
    displacements = ((-1, 0), (0, 0), (1, 0))
    blocks = (
        np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128),
        np.eye(2, dtype=np.complex128),
        np.array([[0.0, 0.0], [0.0, 2.0]], dtype=np.complex128),
    )
    return BlockHoppingModel(
        identifier="typed-shell-power-test",
        dimension=LatticeDimension.TWO,
        terms=tuple(
            BlockHoppingTerm(
                displacement=LatticeDisplacement(LatticeDimension.TWO, displacement),
                coefficient=ComplexMatrixQuantity(block, Unitless()),
            )
            for displacement, block in zip(displacements, blocks, strict=True)
        ),
        energy_unit=Unitless(),
        energy_reference="test-zero",
        basis_identifier="test-rank-two",
    )


class TestMetricShellHoppingPowerAnalyzer:
    """Check PhysKit delegation, KSD grouping, and strict public typing."""

    def test_execute_groups_and_normalizes_physkit_block_powers(self) -> None:
        result = MetricShellHoppingPowerAnalyzer(
            model=_model(),
            shell_indices=(1, 0, 1),
            retained_rank=2,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()

        assert result.retained_rank == 2
        assert tuple(power.metric_shell_value for power in result.powers) == (1, 0, 1)
        assert result.normalized_total_power == pytest.approx(3.5)
        assert result.normalized_power_at_shell(0) == pytest.approx(1.0)
        assert result.normalized_power_at_shell(1) == pytest.approx(2.5)
        assert result.normalized_power_beyond_shell(0) == pytest.approx(2.5)
        assert result.normalized_power_for(
            (
                LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
                LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
            )
        ) == pytest.approx(2.5)

    def test_init_rejects_boolean_rank_and_shell_labels(self) -> None:
        with pytest.raises(TypeError, match="retained_rank"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(1, 0, 1),
                retained_rank=cast(int, True),
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )
        with pytest.raises(TypeError, match="shell_indices"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=cast(tuple[int, ...], (1, False, 1)),
                retained_rank=2,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test_init_rejects_inventory_and_basis_rank_mismatches(self) -> None:
        with pytest.raises(ValueError, match="term count"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(0,),
                retained_rank=2,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )
        with pytest.raises(ValueError, match="basis size"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(1, 0, 1),
                retained_rank=1,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test_result_queries_reject_boolean_and_foreign_displacements(self) -> None:
        result = MetricShellHoppingPowerAnalyzer(
            model=_model(),
            shell_indices=(1, 0, 1),
            retained_rank=2,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()

        with pytest.raises(TypeError, match="shell_index"):
            result.normalized_power_at_shell(cast(int, True))
        with pytest.raises(ValueError, match="power inventory"):
            result.normalized_power_for(
                (LatticeDisplacement(LatticeDimension.TWO, (2, 0)),)
            )

    def test_result_reports_aggregate_overflow(self) -> None:
        result = MetricShellHoppingPowerResult(
            retained_rank=2,
            powers=(
                MetricShellHoppingPower(
                    displacement=LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
                    shell_index=1,
                    normalized_frobenius_power=sys.float_info.max,
                ),
                MetricShellHoppingPower(
                    displacement=LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
                    shell_index=1,
                    normalized_frobenius_power=sys.float_info.max,
                ),
            ),
        )

        with pytest.raises(FloatingPointError, match="overflowed"):
            _ = result.normalized_total_power
