r"""Software verification of ``BandProjectorPathConstructor1D``.

Evidence profile: routine

Bounded artifact scope: gauge-invariant projectors on periodic-1D frame paths.

Facet and represented meaning

The ActionObject constructs ambient-space projectors from retained frames.

Intrinsic and cross-object scope

Composite unitary gauge covariance is included.

VVUQ and scientific exclusions

Projector equality does not establish physical band isolation or validation.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandProjectorPathConstructor1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BandProjectorPathConstructor1D


class TestBandProjectorPathConstructor1D:
    """Own software evidence for ``BandProjectorPathConstructor1D``."""

    def test_method__execute__removes_composite_unitary_gauge(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-024

        Requirement: Right-unitary frame changes leave the ambient projector fixed.

        Acceptance: A complex two-band rotation gives ``diag(1,1,0)``.
        """
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, Unitless()), 2
        )
        rotation = np.asarray(
            [[0.0, np.exp(0.3j)], [np.exp(-0.2j), 0.0]], dtype=np.complex128
        )
        embedded = np.asarray(
            [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=np.complex128
        )
        frame = ComplexMatrixQuantity(embedded @ rotation, Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.eye(3), Unitless()),
            1.0e-14,
        )

        result = BandProjectorPathConstructor1D().execute(path)

        expected = np.diag([1.0, 1.0, 0.0])
        np.testing.assert_allclose(result.projectors[0].magnitude, expected)
        np.testing.assert_allclose(result.projectors[1].magnitude, expected)
