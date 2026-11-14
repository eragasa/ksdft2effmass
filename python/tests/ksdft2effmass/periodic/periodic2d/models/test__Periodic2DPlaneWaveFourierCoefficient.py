"""Software verification for ``Periodic2DPlaneWaveFourierCoefficient``."""

import pytest

from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DPlaneWaveFourierCoefficient,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveFourierCoefficient:
    """Own exact reciprocal-transfer and coefficient-value evidence."""

    def test_fields__valid_coefficient__retain_exact_values(self) -> None:
        """A built-in integer pair and finite complex value are retained exactly."""
        coefficient = Periodic2DPlaneWaveFourierCoefficient((1, -2), 0.5 - 0.25j)

        assert coefficient.reciprocal_transfer == (1, -2)
        assert coefficient.value == 0.5 - 0.25j

    def test_construction__wrong_scalar_types__raises_type_error(self) -> None:
        """Booleans, NumPy-independent real shorthand, and strings are not coerced."""
        with pytest.raises(TypeError, match="components"):
            Periodic2DPlaneWaveFourierCoefficient((True, 0), 1.0 + 0.0j)
        with pytest.raises(TypeError, match="built-in complex"):
            Periodic2DPlaneWaveFourierCoefficient((0, 0), 1.0)
