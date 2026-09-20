r"""Software verification of ``ReciprocalOperatorFourierTransformResult1D``.

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
    BlockHoppingModel1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = ReciprocalOperatorFourierTransformResult1D


class TestReciprocalOperatorFourierTransformResult1D:
    """Verify disposition consistency in retained Fourier-transform results."""

    def test_constructor__reconstruction__rejects_pass_not_matching_error_and_tolerance(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-021

        Requirement: The public contract enforces rejects pass not matching
        error and tolerance.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        samples = ReciprocalOperatorSamples1D(
            mesh.coordinates, mesh.reciprocal_period, (block, block)
        )
        model = BlockHoppingModel1D(mesh.reciprocal_period, (-1, 0), (block, block))

        with pytest.raises(ValueError, match="must match error"):
            ReciprocalOperatorFourierTransformResult1D(
                samples, mesh, model, samples, 0.0, 1.0e-3, 1.0e-4, True
            )
