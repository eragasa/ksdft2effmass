"""Software verification for constrained-Bessel tail diagnostics."""

import math

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    ConstrainedBesselGeometry,
    constrained_bessel_tail_diagnostic,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestConstrainedBesselTailDiagnostic:
    """Establish selected triangular/FCC formulas and failure boundaries."""

    def test_triangular__selected_cap__has_bounded_one_index_remainder(self) -> None:
        diagnostic = constrained_bessel_tail_diagnostic(
            ConstrainedBesselGeometry.TRIANGULAR,
            math.pi / 4.0,
            shell_cap=21,
            kernel_cap=10,
            numerical_margin=1.0e-13,
        )

        assert diagnostic.bessel_argument == pytest.approx(math.pi / 6.0)
        assert diagnostic.retained_displacements == 85
        assert diagnostic.coefficient_remainder_bound < 2.2e-14
        assert diagnostic.tail_power_upper_bound == pytest.approx(
            2.87597e-9, rel=2.0e-5
        )

    def test_fcc__selected_cap__has_bounded_three_index_remainder(self) -> None:
        diagnostic = constrained_bessel_tail_diagnostic(
            ConstrainedBesselGeometry.FCC,
            math.pi / 4.0,
            shell_cap=7,
            kernel_cap=9,
            numerical_margin=1.0e-13,
        )

        assert diagnostic.bessel_argument == pytest.approx(math.pi / 12.0)
        assert diagnostic.retained_displacements == 135
        assert diagnostic.coefficient_remainder_bound < 4.3e-15
        assert diagnostic.tail_power_upper_bound == pytest.approx(5.5358e-6, rel=2.0e-4)

    def test_inputs__invalid_types_ranges_and_resource_caps__fail_closed(self) -> None:
        with pytest.raises(TypeError, match="geometry"):
            constrained_bessel_tail_diagnostic(
                "fcc",  # type: ignore[arg-type]
                math.pi / 4.0,
                shell_cap=7,
                kernel_cap=9,
                numerical_margin=1.0e-13,
            )
        with pytest.raises(TypeError, match="built-in integers"):
            constrained_bessel_tail_diagnostic(
                ConstrainedBesselGeometry.FCC,
                math.pi / 4.0,
                shell_cap=True,
                kernel_cap=9,
                numerical_margin=1.0e-13,
            )
        with pytest.raises(ValueError, match="resource bound"):
            constrained_bessel_tail_diagnostic(
                ConstrainedBesselGeometry.FCC,
                math.pi / 4.0,
                shell_cap=7,
                kernel_cap=13,
                numerical_margin=1.0e-13,
            )
