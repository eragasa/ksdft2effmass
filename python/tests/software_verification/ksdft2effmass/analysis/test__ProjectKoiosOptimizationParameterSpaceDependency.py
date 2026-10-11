"""Software verification of the pinned optimization parameter-space dependency.

This test establishes only that the resolved dependency supplies the inclusive,
ordered, named bounds needed to represent a common coefficient box and exact fixed
coordinates. It does not select HSH bounds, establish feasibility, or authorize a
calculation.
"""

from __future__ import annotations

import pytest
from projectkoios.optimization import ParameterBound, ParameterSpace

pytestmark = pytest.mark.software_verification


class TestProjectKoiosOptimizationParameterSpaceDependency:
    """Own consuming-project smoke evidence for the pinned parameter-space API."""

    def test_public_api__represents_common_box_and_exact_inactive_slice(self) -> None:
        """Inclusive bounds and fixed coordinates preserve maximal-space ordering."""
        common_box = ParameterSpace(
            (
                ParameterBound("orbit-000", -2.0, 3.0),
                ParameterBound("orbit-001", -1.0, 4.0),
            )
        )
        inactive_slice = ParameterSpace(
            (
                ParameterBound("orbit-000", -2.0, 3.0),
                ParameterBound("orbit-001", 0.0, 0.0),
            )
        )

        assert common_box.names == ("orbit-000", "orbit-001")
        assert common_box.admits((-2.0, 4.0))
        assert inactive_slice.admits((1.5, 0.0))
        assert not inactive_slice.admits((1.5, 1.0e-15))

    def test_public_api__rejects_boolean_and_nonfinite_bound_values(self) -> None:
        """Optimization boundaries fail closed for invalid numeric scalars."""
        with pytest.raises(TypeError):
            ParameterBound("orbit-000", False, 1.0)
        with pytest.raises(ValueError):
            ParameterBound("orbit-000", 0.0, float("inf"))
