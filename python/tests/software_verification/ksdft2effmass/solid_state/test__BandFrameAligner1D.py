r"""Software verification of ``BandFrameAligner1D``.

Evidence profile: routine

Bounded artifact scope: pointwise unitary alignment of periodic-1D band frames.

Facet and represented meaning

The ActionObject aligns compatible candidate frames to reference frames.

Intrinsic and cross-object scope

Composite rotations and separate projector and frame defects are included.

VVUQ and scientific exclusions

Alignment is represented gauge reconciliation, not physical model validation.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandFrameAligner1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BandFrameAligner1D


class TestBandFrameAligner1D:
    """Own software evidence for ``BandFrameAligner1D``."""

    def test_method__execute__aligns_composite_right_unitary_attack(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-026

        Requirement: Pointwise unitary Procrustes removes a composite right-unitary
        gauge while preserving a separately reported projector defect.

        Acceptance: Two authored rotations align to the reference within ``1e-14``.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        reference_matrix = np.asarray(
            [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=np.complex128
        )
        first_rotation = np.asarray(
            [[0.0, np.exp(0.3j)], [np.exp(-0.2j), 0.0]], dtype=np.complex128
        )
        second_rotation = np.diag(np.exp(1j * np.asarray([0.4, -0.7])))
        reference_frame = ComplexMatrixQuantity(reference_matrix, Unitless())
        reference = ReciprocalBandFramePath1D(
            mesh,
            (reference_frame, reference_frame),
            ComplexMatrixQuantity(np.eye(3), Unitless()),
            1.0e-14,
        )
        candidate = ReciprocalBandFramePath1D(
            mesh,
            (
                ComplexMatrixQuantity(reference_matrix @ first_rotation, Unitless()),
                ComplexMatrixQuantity(reference_matrix @ second_rotation, Unitless()),
            ),
            ComplexMatrixQuantity(np.eye(3), Unitless()),
            1.0e-14,
        )

        result = BandFrameAligner1D().execute(reference, candidate)

        np.testing.assert_allclose(
            result.aligned.frames[0].magnitude, reference_matrix, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.aligned.frames[1].magnitude, reference_matrix, atol=1.0e-14
        )
        assert result.frame_maximum_frobenius_defect <= 1.0e-14
        assert result.projector_maximum_frobenius_defect <= 1.0e-14

    def test_method__execute__rejects_different_sewing_conventions(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-027

        Requirement: Alignment does not silently bridge different sewing maps.

        Acceptance: Different explicit maps raise ``ValueError``.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        frame = ComplexMatrixQuantity(np.asarray([[1.0], [0.0]]), Unitless())
        identity = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(2), Unitless()),
            1.0e-14,
        )
        shifted = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.asarray([[0.0, 1.0], [1.0, 0.0]]), Unitless()),
            1.0e-14,
        )

        with pytest.raises(ValueError, match="sewing maps"):
            BandFrameAligner1D().execute(identity, shifted)
