"""Software contracts for admitted real-space support policies."""

from __future__ import annotations

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from ksdft2effmass.real_space_support_truncation import (
    ConjugateClosedSupport,
    MetricShellSupportInventory,
    SymmetricRangeSupport1D,
)

pytestmark = pytest.mark.software_verification


def _d2(first: int, second: int) -> LatticeDisplacement:
    return LatticeDisplacement(LatticeDimension.TWO, (first, second))


class TestSupportPolicies:
    """Keep ranges, shells, and explicit support groups exact and immutable."""

    def test_symmetric_range__retains_every_integer_through_cutoff(self) -> None:
        """A 1D range projects to the exact ordered conjugate-closed inventory."""
        policy = SymmetricRangeSupport1D(maximum_range=2)

        assert tuple(value.components for value in policy.support.displacements) == (
            (-2,),
            (-1,),
            (0,),
            (1,),
            (2,),
        )
        assert policy.support.dimension is LatticeDimension.ONE

    @pytest.mark.parametrize("value", [True, 1.0, "1"])
    def test_symmetric_range__noninteger_cutoff__is_rejected(
        self, value: bool | float | str
    ) -> None:
        """Booleans, floats, and strings never enter the integer cutoff contract."""
        with pytest.raises(TypeError, match="built-in integer"):
            SymmetricRangeSupport1D(maximum_range=value)  # type: ignore[arg-type]

    def test_explicit_support__missing_conjugate__is_rejected(self) -> None:
        """An anisotropic explicit group must retain every conjugate partner."""
        with pytest.raises(ValueError, match="closed under displacement conjugation"):
            ConjugateClosedSupport((_d2(0, 0), _d2(1, 0)))

    def test_metric_shell_inventory__selects_all_blocks_through_shell(self) -> None:
        """A cutoff includes every admitted block in every preceding shell."""
        inventory = MetricShellSupportInventory(
            displacements=(
                _d2(-1, 0),
                _d2(0, -1),
                _d2(0, 0),
                _d2(0, 1),
                _d2(1, 0),
            ),
            ordinal_shell_indices=(1, 1, 0, 1, 1),
        )

        support = inventory.support_through(1)

        assert support.displacements == inventory.displacements
        assert support.retained_displacement_count == 5

    def test_metric_shell_inventory__split_conjugate_shell__is_rejected(self) -> None:
        """A metric shell label cannot split one conjugate displacement pair."""
        with pytest.raises(ValueError, match="conjugate displacements"):
            MetricShellSupportInventory(
                displacements=(
                    _d2(-1, 0),
                    _d2(0, 0),
                    _d2(1, 0),
                ),
                ordinal_shell_indices=(1, 0, 2),
            )
