"""Software verification for ``PlaneWaveFourierCoefficient2D``."""

import pytest

from ksdft2effmass.analysis.model_systems import PlaneWaveFourierCoefficient2D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveFourierCoefficient2D:
    """Own exact reciprocal-transfer and coefficient-value evidence."""

    def test_fields__valid_coefficient__retain_exact_values(self) -> None:
        """A built-in integer pair and finite complex value are retained exactly."""
        coefficient = PlaneWaveFourierCoefficient2D((1, -2), 0.5 - 0.25j)

        assert coefficient.reciprocal_transfer == (1, -2)
        assert coefficient.value == 0.5 - 0.25j

    def test_construction__wrong_scalar_types__raises_type_error(self) -> None:
        """Booleans, NumPy-independent real shorthand, and strings are not coerced."""
        with pytest.raises(TypeError, match="components"):
            PlaneWaveFourierCoefficient2D((True, 0), 1.0 + 0.0j)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="built-in complex"):
            PlaneWaveFourierCoefficient2D((0, 0), 1.0)  # type: ignore[arg-type]
