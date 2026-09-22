r"""Software verification of ``BandFrameAlignmentResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated pointwise periodic-1D frame alignment results.

Facet and represented meaning

The ResultObject binds candidate frames, rotations, aligned frames, and defects.

Intrinsic and cross-object scope

Retained rotation application and defect correlation are included.

VVUQ and scientific exclusions

Result consistency does not establish physical equivalence of parent models.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandFrameAligner1D,
    BandFrameAlignmentResult1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BandFrameAlignmentResult1D


class TestBandFrameAlignmentResult1D:
    """Own software evidence for ``BandFrameAlignmentResult1D``."""

    def test_constructor__defects__rejects_value_not_matching_frames(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-028

        Requirement: The retained frame defect is derived from represented frames.

        Acceptance: Replacing the calculated defect raises ``ValueError``.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        frame = ComplexMatrixQuantity(np.asarray([[1.0], [0.0]]), Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(2), Unitless()),
            1.0e-14,
        )
        valid = BandFrameAligner1D().execute(path, path)

        with pytest.raises(ValueError, match="must match aligned frames"):
            BandFrameAlignmentResult1D(
                valid.reference,
                valid.candidate,
                valid.aligned,
                valid.rotations,
                1.0,
                valid.projector_maximum_frobenius_defect,
            )
