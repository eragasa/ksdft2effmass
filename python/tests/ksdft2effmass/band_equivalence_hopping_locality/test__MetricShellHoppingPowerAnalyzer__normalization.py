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
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (
    MetricShellHoppingPower,
    MetricShellHoppingPowerAnalyzer,
    MetricShellHoppingPowerResult,
)

pytestmark = pytest.mark.unit


def _model() -> DenseBlockHoppingModel:
    """Return one canonical dense rank-two model for shell-power tests."""
    displacements = ((-1, 0), (0, 0), (1, 0))
    blocks = (
        np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128),
        np.eye(2, dtype=np.complex128),
        np.array([[0.0, 0.0], [0.0, 2.0]], dtype=np.complex128),
    )
    return DenseBlockHoppingModel(
        identifier="typed-shell-power-test",
        dimension=LatticeDimension.TWO,
        terms=tuple(
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(LatticeDimension.TWO, displacement),
                coefficient=ComplexMatrixQuantity(block, Unitless()),
            )
            for displacement, block in zip(displacements, blocks, strict=True)
        ),
        energy_unit=Unitless(),
        energy_reference="test-zero",
        basis_identifier="test-rank-two",
    )


def _result() -> MetricShellHoppingPowerResult:
    """Execute the canonical dense shell-power analysis."""
    return MetricShellHoppingPowerAnalyzer(
        model=_model(),
        shell_indices=(1, 0, 1),
        retained_rank=2,
        power_analyzer=BlockHoppingPowerAnalyzer(),
    ).execute()


class TestMetricShellHoppingPowerAnalyzer:
    """Check PhysKit delegation, KSD grouping, and strict public typing."""

    def test__MetricShellHoppingPowerAnalyzer__retains_rank_and_shell_inventory(
        self,
    ) -> None:
        """Retain the declared rank and shell label for every canonical term."""
        result = _result()

        assert (
            result.retained_rank,
            tuple(power.metric_shell_value for power in result.powers),
        ) == (2, (1, 0, 1))

    def test__MetricShellHoppingPowerAnalyzer__normalizes_each_dense_block(
        self,
    ) -> None:
        """Divide each PhysKit Frobenius power by the retained rank."""
        result = _result()

        np.testing.assert_allclose(
            [power.normalized_frobenius_power for power in result.powers],
            [0.5, 1.0, 2.0],
            rtol=0.0,
            atol=0.0,
        )

    def test__MetricShellHoppingPowerAnalyzer__aggregates_shell_queries(self) -> None:
        """Aggregate total, exact-shell, beyond-shell, and selected powers."""
        result = _result()
        selected = (
            LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
            LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
        )

        np.testing.assert_allclose(
            (
                result.normalized_total_power,
                result.normalized_power_at_shell(0),
                result.normalized_power_at_shell(1),
                result.normalized_power_beyond_shell(0),
                result.normalized_power_for(selected),
            ),
            (3.5, 1.0, 2.5, 2.5, 2.5),
            rtol=0.0,
            atol=0.0,
        )

    def test__MetricShellHoppingPowerAnalyzer__rejects_boolean_rank(self) -> None:
        """Reject booleans at the retained-rank integer boundary."""
        with pytest.raises(TypeError, match="retained_rank"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(1, 0, 1),
                retained_rank=cast(int, True),
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test__MetricShellHoppingPowerAnalyzer__rejects_boolean_shell_label(
        self,
    ) -> None:
        """Reject booleans in the metric-shell inventory."""
        with pytest.raises(TypeError, match="shell_indices"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=cast(tuple[int, ...], (1, False, 1)),
                retained_rank=2,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test__MetricShellHoppingPowerAnalyzer__rejects_term_count_mismatch(
        self,
    ) -> None:
        """Require one shell label for every dense hopping term."""
        with pytest.raises(ValueError, match="term count"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(0,),
                retained_rank=2,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test__MetricShellHoppingPowerAnalyzer__rejects_basis_rank_mismatch(
        self,
    ) -> None:
        """Require the normalization rank to match the dense block size."""
        with pytest.raises(ValueError, match="basis size"):
            MetricShellHoppingPowerAnalyzer(
                model=_model(),
                shell_indices=(1, 0, 1),
                retained_rank=1,
                power_analyzer=BlockHoppingPowerAnalyzer(),
            )

    def test__MetricShellHoppingPowerAnalyzer__rejects_boolean_query_shell(
        self,
    ) -> None:
        """Reject booleans when querying an exact shell."""
        with pytest.raises(TypeError, match="shell_index"):
            _result().normalized_power_at_shell(cast(int, True))

    def test__MetricShellHoppingPowerAnalyzer__rejects_foreign_displacement(
        self,
    ) -> None:
        """Reject displacement queries outside the retained model inventory."""
        with pytest.raises(ValueError, match="power inventory"):
            _result().normalized_power_for(
                (LatticeDisplacement(LatticeDimension.TWO, (2, 0)),)
            )

    def test__MetricShellHoppingPowerAnalyzer__reports_aggregate_overflow(
        self,
    ) -> None:
        """Report binary64 overflow rather than returning a nonfinite sum."""
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
