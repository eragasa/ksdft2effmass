"""Software verification of ``SpectralDispersionContrast``.

Evidence profile: routine

The tests establish exact runtime typing, explicit bound ownership, and deterministic
contrast properties. They do not establish convergence or scientific validity.
"""

import pytest

from ksdft2effmass.analysis import SpectralDispersionContrast

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSpectralDispersionContrast:
    """Own software evidence for the public spectral-contrast DataObject."""

    def test_properties__report_observed_contrast(self) -> None:
        """A low error below 2% and high error above 50% satisfy those bounds."""
        contrast = SpectralDispersionContrast(0.01, 0.60, 0.02, 0.50)

        assert contrast.low_mode_condition_satisfied
        assert contrast.high_mode_condition_satisfied
        assert contrast.is_observed
        assert contrast.error_difference == pytest.approx(0.59)

    def test_properties__retain_unsatisfied_high_mode_condition(self) -> None:
        """The result remains descriptive when one supplied condition is false."""
        contrast = SpectralDispersionContrast(0.01, 0.40, 0.02, 0.50)

        assert contrast.low_mode_condition_satisfied
        assert not contrast.high_mode_condition_satisfied
        assert not contrast.is_observed

    @pytest.mark.parametrize(
        "value",
        (True, 1),
        ids=("boolean", "integer"),
    )
    def test_constructor__rejects_nonfloat_errors(self, value: bool | int) -> None:
        """Boolean and integer values are not coerced to binary64 relative errors."""
        with pytest.raises(TypeError, match="built-in float"):
            SpectralDispersionContrast(
                value,
                0.60,
                0.02,
                0.50,
            )

    def test_constructor__rejects_overlapping_reference_bounds(self) -> None:
        """The declared low and high regimes must be distinct."""
        with pytest.raises(ValueError, match="must exceed"):
            SpectralDispersionContrast(0.01, 0.60, 0.50, 0.50)
