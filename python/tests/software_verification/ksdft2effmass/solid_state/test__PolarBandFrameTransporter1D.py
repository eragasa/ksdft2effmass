r"""Software verification of ``PolarBandFrameTransporter1D``.

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
    PolarBandFrameTransporter1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = PolarBandFrameTransporter1D


class TestPolarBandFrameTransporter1D:
    """Verify scalar and composite unitary polar transport."""

    def test_method__execute__removes_scalar_pointwise_phase_attack(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-015

        Requirement: The public contract enforces removes scalar pointwise phase
        attack.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 4)
        frames = (
            ComplexMatrixQuantity(
                np.asarray([[np.exp(0.2j)], [0.0]], dtype=np.complex128),
                Unitless(),
            ),
            ComplexMatrixQuantity(
                np.asarray([[np.exp(-1.1j)], [0.0]], dtype=np.complex128),
                Unitless(),
            ),
            ComplexMatrixQuantity(
                np.asarray([[np.exp(2.4j)], [0.0]], dtype=np.complex128),
                Unitless(),
            ),
            ComplexMatrixQuantity(
                np.asarray([[np.exp(-0.7j)], [0.0]], dtype=np.complex128),
                Unitless(),
            ),
        )
        path = ReciprocalBandFramePath1D(
            mesh,
            frames,
            ComplexMatrixQuantity(np.eye(2), Unitless()),
            1.0e-14,
        )

        result = PolarBandFrameTransporter1D().execute(path, 1.0e-12)

        reference = result.transported.frames[0].magnitude
        np.testing.assert_allclose(
            result.transported.frames[1].magnitude, reference, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.transported.frames[2].magnitude, reference, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.transported.frames[3].magnitude, reference, atol=1.0e-14
        )
        assert result.minimum_overlap_singular_value > 1.0 - 1.0e-14
        np.testing.assert_allclose(result.closure_eigenphases, [0.0], atol=1.0e-14)

    def test_method__execute__aligns_composite_frames_without_changing_their_projector(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-016

        Requirement: The public contract enforces aligns composite frames
        without changing their projector.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        rotation = np.asarray(
            [[0.0, np.exp(0.3j)], [np.exp(-0.2j), 0.0]], dtype=np.complex128
        )
        identity = ComplexMatrixQuantity(np.eye(2), Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (identity, ComplexMatrixQuantity(rotation, Unitless())),
            identity,
            1.0e-14,
        )

        result = PolarBandFrameTransporter1D().execute(path, 1.0e-12)

        np.testing.assert_allclose(
            result.transported.frames[1].magnitude,
            result.transported.frames[0].magnitude,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            path.frames[0].magnitude @ path.frames[0].magnitude.conj().T,
            result.transported.frames[0].magnitude
            @ result.transported.frames[0].magnitude.conj().T,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            path.frames[1].magnitude @ path.frames[1].magnitude.conj().T,
            result.transported.frames[1].magnitude
            @ result.transported.frames[1].magnitude.conj().T,
            atol=1.0e-14,
        )
