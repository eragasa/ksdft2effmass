r"""Software verification of ``PolarBandFrameTransportResult1D``.

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
    CenteredUniformReciprocalMesh1D,
    PolarBandFrameTransportResult1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = PolarBandFrameTransportResult1D


class TestPolarBandFrameTransportResult1D:
    """Verify retained polar-transport diagnostics."""

    def test_constructor__transport__rejects_minimum_overlap_not_passing_threshold(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-017

        Requirement: The public contract enforces rejects minimum overlap not
        passing threshold.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        frame = ComplexMatrixQuantity(
            np.asarray([[1.0], [0.0]], dtype=np.complex128), Unitless()
        )
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(2), Unitless()),
            1.0e-14,
        )

        with pytest.raises(ValueError, match="does not pass"):
            PolarBandFrameTransportResult1D(path, path, 0.5, 0.5, (0.0,))
