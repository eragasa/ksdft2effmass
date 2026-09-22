r"""Software verification of ``ReciprocalBandFramePath1D``.

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
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = ReciprocalBandFramePath1D


class TestReciprocalBandFramePath1D:
    """Verify reciprocal frame-path invariants."""

    def test_constructor__frames__retains_orthonormal_composite_frames(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-018

        Requirement: The public contract enforces retains orthonormal composite
        frames.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        identity = ComplexMatrixQuantity(np.eye(2), Unitless())

        path = ReciprocalBandFramePath1D(mesh, (identity, identity), identity, 1.0e-14)

        assert path.ambient_dimension == 2
        assert path.rank == 2

    def test_constructor__frames__rejects_nonorthonormal_frame(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-019

        Requirement: The public contract enforces rejects nonorthonormal frame.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        invalid = ComplexMatrixQuantity(
            np.asarray([[2.0], [0.0]], dtype=np.complex128), Unitless()
        )

        with pytest.raises(ValueError, match="orthonormality tolerance"):
            ReciprocalBandFramePath1D(
                mesh,
                (invalid, invalid),
                ComplexMatrixQuantity(np.eye(2), Unitless()),
                1.0e-14,
            )
