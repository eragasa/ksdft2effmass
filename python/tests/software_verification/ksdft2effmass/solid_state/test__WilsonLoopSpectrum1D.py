r"""Software verification of ``WilsonLoopSpectrum1D``.

Evidence profile: routine

Bounded artifact scope: canonical one-dimensional Wilson eigenphase spectra.

Facet and represented meaning

Principal-branch phase storage and the explicit center convention are included.

Intrinsic and cross-object scope

Intrinsic spectrum invariants and phase-to-center conversion are included.

VVUQ and scientific exclusions

These authored phase values do not establish topology, polarization, or validation.
"""

import numpy as np
import pytest

from ksdft2effmass.solid_state import (
    WilsonCenterConvention1D,
    WilsonLoopSpectrum1D,
)

pytestmark = pytest.mark.software_verification
SUT = WilsonLoopSpectrum1D


class TestWilsonLoopSpectrum1D:
    """Verify canonical phase storage and the explicit center convention."""

    def test_method__centers_over_period__uses_phase_over_two_pi(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-030

        Requirement: Principal Wilson phases map to centers under an explicit
        convention.

        Acceptance: The retained low-pair phases map by exact division by ``2*pi``.
        """
        spectrum = SUT((-1.9856198592310257, 1.985619859231026))

        centers = spectrum.centers_over_period(
            WilsonCenterConvention1D.PHASE_OVER_TWO_PI
        )

        np.testing.assert_allclose(
            centers,
            (-0.3160212156980512, 0.3160212156980512),
            rtol=0.0,
            atol=1.0e-16,
        )
        assert spectrum.rank == 2

    def test_method__construction__rejects_noncanonical_order(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-031

        Requirement: Storage order is deterministic even though the spectrum is a set.

        Acceptance: A decreasing phase tuple is rejected.
        """
        with pytest.raises(ValueError, match="increasing"):
            SUT((0.25, -0.25))
