r"""Software verification of ``BlockHoppingInterpolator1D``.

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

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingInterpolator1D, BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingInterpolator1D


class TestBlockHoppingInterpolator1D:
    """Verify reciprocal interpolation from matrix-valued hoppings."""

    def test_method__execute__evaluates_complex_block_fourier_series(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-002

        Requirement: The public contract enforces evaluates complex block
        fourier series.

        Acceptance: The asserted values and failures match the declared contract.
        """
        blocks = (
            ComplexMatrixQuantity(np.asarray([[0.5]]), Unitless()),
            ComplexMatrixQuantity(np.asarray([[2.0]]), Unitless()),
            ComplexMatrixQuantity(np.asarray([[0.5]]), Unitless()),
        )
        model = BlockHoppingModel1D(ScalarQuantity(1.0, Unitless()), (-1, 0, 1), blocks)
        coordinates = VectorQuantity(
            np.asarray([-0.5, 0.0, 0.5], dtype=np.float64), Unitless()
        )

        result = BlockHoppingInterpolator1D().execute(model, coordinates)

        np.testing.assert_allclose(
            [matrix.magnitude[0, 0] for matrix in result.matrices],
            [1.0, 3.0, 1.0],
            atol=1.0e-15,
        )
