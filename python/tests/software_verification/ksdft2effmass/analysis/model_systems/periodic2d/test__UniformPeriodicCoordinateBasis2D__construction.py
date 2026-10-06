"""Software verification of uniform periodic coordinate-basis construction.

The synthetic inputs establish strict public scalar boundaries, grid ordering, and
binary64 spacing failure behavior. They do not establish continuum completeness,
quadrature accuracy, scientific validation, uncertainty quantification, or acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import UniformPeriodicCoordinateBasis2D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestUniformPeriodicCoordinateBasis2DConstruction:
    """Own coordinate-period, extent, identity, and ordering invariant evidence."""

    def test_construction_exposes_half_open_euclidean_site_basis(self) -> None:
        """A valid basis has exact dimension, spacing, order, and normalization."""
        basis = UniformPeriodicCoordinateBasis2D(2.0 * np.pi, 5, "test.basis")

        assert basis.spacing == 2.0 * np.pi / 5
        assert basis.represented_dimension == 25
        assert basis.site_indices[0] == (0, 0)
        assert basis.site_indices[-1] == (4, 4)
        assert basis.ordering == "x_outer_y_inner"
        assert basis.normalization == "euclidean_site_basis"

    def test_construction_rejects_non_float_coordinate_periods(self) -> None:
        """Booleans, integers, and numeric strings are not coordinate-period floats."""
        for invalid in (True, 1, "1.0"):
            with pytest.raises(TypeError, match="coordinate_period"):
                UniformPeriodicCoordinateBasis2D(
                    invalid,  # type: ignore[arg-type]
                    5,
                    "test.basis",
                )

    @pytest.mark.parametrize("period", (0.0, -1.0, float("inf"), float("nan")))
    def test_construction_rejects_nonpositive_or_nonfinite_coordinate_periods(
        self,
        period: float,
    ) -> None:
        """The coordinate period must be finite and strictly positive."""
        with pytest.raises(ValueError, match="finite and positive"):
            UniformPeriodicCoordinateBasis2D(period, 5, "test.basis")

    def test_construction_rejects_non_integer_or_invalid_grid_extents(self) -> None:
        """The supported grid extent is an odd built-in integer of at least five."""
        for invalid in (True, 5.0, "5"):
            with pytest.raises(TypeError, match="points_per_direction"):
                UniformPeriodicCoordinateBasis2D(
                    2.0 * np.pi,
                    invalid,  # type: ignore[arg-type]
                    "test.basis",
                )
        for invalid in (3, 6):
            with pytest.raises(ValueError, match="odd and at least five"):
                UniformPeriodicCoordinateBasis2D(
                    2.0 * np.pi,
                    invalid,
                    "test.basis",
                )

    def test_construction_rejects_missing_or_mistyped_basis_identity(self) -> None:
        """Basis identity is explicit and cannot be inferred from grid dimensions."""
        with pytest.raises(TypeError, match="basis_identifier"):
            UniformPeriodicCoordinateBasis2D(
                2.0 * np.pi,
                5,
                1,  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="nonempty"):
            UniformPeriodicCoordinateBasis2D(2.0 * np.pi, 5, "")

    def test_construction_rejects_binary64_spacing_underflow(self) -> None:
        """Reject a positive period whose division cannot retain positive spacing."""
        minimum_positive = float(np.nextafter(0.0, 1.0))

        with pytest.raises(OverflowError, match="spacing underflows"):
            UniformPeriodicCoordinateBasis2D(minimum_positive, 5, "test.basis")
