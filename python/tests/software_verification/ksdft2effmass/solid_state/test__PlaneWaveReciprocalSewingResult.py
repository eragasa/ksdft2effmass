r"""Software verification of ``PlaneWaveReciprocalSewingResult``.

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

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingResult,
    ReciprocalSewingDirection1D,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveReciprocalSewingResult


class TestPlaneWaveReciprocalSewingResult:
    """Verify correlations retained by one sewing result."""

    def test_constructor__coefficient_map__rejects_incompatible_shift(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-014

        Requirement: The public contract enforces rejects a map that does not
        match the declared basis shift.

        Acceptance: The asserted values and failures match the declared contract.
        """
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)

        with pytest.raises(ValueError, match="declared basis shift"):
            PlaneWaveReciprocalSewingResult(
                basis,
                ReciprocalSewingDirection1D.PLUS_RECIPROCAL_VECTOR,
                ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless()),
            )
