"""Software verification for the periodic2d uniform cell grid."""

import numpy as np
import pytest

from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DUniformCellGrid,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DUniformCellGrid:
    """Own finite coordinate-grid ordering and invariant evidence."""

    def test_properties_expose_deterministic_square_grid(self) -> None:
        """An odd side count defines one period-2-pi coordinate basis."""
        grid = Periodic2DUniformCellGrid(5)

        assert grid.period == 2.0 * np.pi
        assert grid.spacing == 2.0 * np.pi / 5
        assert grid.ordering == "x_outer_y_inner"
        assert grid.represented_dimension == 25
        assert grid.site_indices[0] == (0, 0)
        assert grid.site_indices[-1] == (4, 4)
        assert len(set(grid.site_indices)) == grid.represented_dimension

    def test_init_rejects_boolean_even_and_short_grids(self) -> None:
        """Only odd built-in integer side counts of at least five are admitted."""
        with pytest.raises(TypeError, match="points_per_direction"):
            Periodic2DUniformCellGrid(True)
        with pytest.raises(ValueError, match="odd and at least five"):
            Periodic2DUniformCellGrid(4)
        with pytest.raises(ValueError, match="odd and at least five"):
            Periodic2DUniformCellGrid(6)
