r"""Software verification of ``PlaneWaveReciprocalSewingConstructor``.

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

from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingConstructor,
    ReciprocalSewingDirection1D,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveReciprocalSewingConstructor


class TestPlaneWaveReciprocalSewingConstructor:
    """Verify the explicit finite-cutoff reciprocal sewing map."""

    def test_method__execute__constructs_plus_reciprocal_vector_coefficient_shift(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-013

        Requirement: The public contract enforces constructs plus reciprocal
        vector coefficient shift.

        Acceptance: The asserted values and failures match the declared contract.
        """
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)

        result = PlaneWaveReciprocalSewingConstructor().execute(basis)

        assert result.basis == basis
        assert result.direction is ReciprocalSewingDirection1D.PLUS_RECIPROCAL_VECTOR
        np.testing.assert_array_equal(
            result.coefficient_map.magnitude,
            np.asarray(
                [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
                dtype=np.complex128,
            ),
        )
        assert isinstance(result.coefficient_map.unit, Unitless)
