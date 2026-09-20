r"""Software verification of ``PlaneWaveBasis1D``.

Evidence profile: routine

Bounded artifact scope: extracted Appendix G periodic-1D public contract.

Facet and represented meaning

The public class retains or transforms the explicitly represented periodic-1D values.

Intrinsic and cross-object scope

Construction invariants and the demonstrated public operation are included.

VVUQ and scientific exclusions

This is software verification, not a rerun or scientific validation of Appendix G.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity
from ksdft2effmass.solid_state import PlaneWaveBasis1D

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveBasis1D


class TestPlaneWaveBasis1D:
    """Verify ordered finite reciprocal-index bases."""

    def test_constructor__basis__retains_ordered_indices_and_wave_vectors(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-010

        Requirement: The public contract enforces retains ordered indices and
        wave vectors.

        Acceptance: The asserted values and failures match the declared contract.
        """
        basis = PlaneWaveBasis1D(ScalarQuantity(2.0, PhysicalUnit("1 / nanometer")), 2)

        assert basis.reciprocal_indices == (-2, -1, 0, 1, 2)
        assert basis.dimension == 5
        np.testing.assert_array_equal(
            basis.wave_vectors.magnitude,
            np.asarray([-4.0, -2.0, 0.0, 2.0, 4.0], dtype=np.float64),
        )
        assert basis.wave_vectors.unit == basis.reciprocal_vector.unit

    def test_constructor__basis__allows_the_single_constant_plane_wave(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-011

        Requirement: The public contract enforces allows the single constant
        plane wave.

        Acceptance: The asserted values and failures match the declared contract.
        """
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, PhysicalUnit("1 / meter")), 0)

        assert basis.reciprocal_indices == (0,)
        assert basis.dimension == 1

    def test_constructor__basis__rejects_negative_cutoff(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-012

        Requirement: The public contract enforces rejects negative cutoff.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="nonnegative"):
            PlaneWaveBasis1D(ScalarQuantity(1.0, PhysicalUnit("1 / meter")), -1)
