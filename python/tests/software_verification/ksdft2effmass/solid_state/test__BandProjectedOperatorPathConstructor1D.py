r"""Software verification of ``BandProjectedOperatorPathConstructor1D``.

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
    BandProjectedOperatorPathConstructor1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = BandProjectedOperatorPathConstructor1D


class TestBandProjectedOperatorPathConstructor1D:
    """Verify pointwise projection into scalar and composite frames."""

    def test_method__execute__projects_parent_matrices_into_composite_frame(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-001

        Requirement: The public contract enforces projects parent matrices into
        composite frame.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        parent_matrix = ComplexMatrixQuantity(
            np.diag([1.0, 2.0, 3.0]).astype(np.complex128), Unitless()
        )
        parent = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            mesh.reciprocal_period,
            (parent_matrix, parent_matrix),
        )
        frame = ComplexMatrixQuantity(
            np.asarray([[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]]), Unitless()
        )
        frames = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(3), Unitless()),
            1.0e-14,
        )

        projected = BandProjectedOperatorPathConstructor1D().execute(
            parent, frames, 0.0
        )

        np.testing.assert_array_equal(
            projected.matrices[0].magnitude, np.diag([1.0, 3.0])
        )
        np.testing.assert_array_equal(
            projected.matrices[1].magnitude, np.diag([1.0, 3.0])
        )
