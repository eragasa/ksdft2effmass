r"""Software verification of ``BandProjectorPathResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-1D frame-projector results.

Facet and represented meaning

The ResultObject binds every projector to its exact source frame.

Intrinsic and cross-object scope

Projector shape and value correlation are included.

VVUQ and scientific exclusions

Result consistency is not evidence of physical subspace suitability.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandProjectorPathResult1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BandProjectorPathResult1D


class TestBandProjectorPathResult1D:
    """Own software evidence for ``BandProjectorPathResult1D``."""

    def test_constructor__projectors__rejects_values_unbound_to_frames(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-025

        Requirement: Every retained projector equals its source frame projector.

        Acceptance: Identity projectors for rank-one frames raise ``ValueError``.
        """
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, Unitless()), 2
        )
        frame = ComplexMatrixQuantity(np.asarray([[1.0], [0.0]]), Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(2), Unitless()),
            1.0e-14,
        )
        invalid = ComplexMatrixQuantity(np.eye(2), Unitless())

        with pytest.raises(ValueError, match="source frame projector"):
            BandProjectorPathResult1D(path, (invalid, invalid))
