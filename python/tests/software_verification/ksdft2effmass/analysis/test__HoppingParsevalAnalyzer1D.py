r"""Software verification of ``HoppingParsevalAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: complete-mesh Parseval checks for periodic-1D truncation.

Facet and represented meaning

The ActionObject compares reciprocal residual energy with omitted hopping-block energy.

Intrinsic and cross-object scope

Complete transform, symmetric truncation, and squared-unit tolerance are included.

VVUQ and scientific exclusions

Parseval agreement verifies represented arithmetic, not physical model adequacy.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import HoppingParsevalAnalyzer1D
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = HoppingParsevalAnalyzer1D


class TestHoppingParsevalAnalyzer1D:
    """Own software evidence for ``HoppingParsevalAnalyzer1D``."""

    def test_method__execute__matches_discrete_fourier_parseval_scaling(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-020

        Requirement: Training squared residual equals mesh size times omitted-block
        squared norm for the complete uniform discrete Fourier pair.

        Acceptance: Removing nearest-neighbor blocks from ``2 + cos(2 pi k)`` gives
        both squared norms equal to two.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 4)
        values = 2.0 + np.cos(2.0 * np.pi * mesh.coordinates.magnitude)
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            mesh.reciprocal_period,
            (
                ComplexMatrixQuantity(np.asarray([[values[0]]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[values[1]]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[values[2]]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[values[3]]]), Unitless()),
            ),
        )
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source, mesh, 0.0, 1.0e-14
        )
        truncation = BlockHoppingTruncator1D().execute(transform.hopping_model, 0)

        result = HoppingParsevalAnalyzer1D().execute(
            transform, truncation, ScalarQuantity(1.0e-14, Unitless())
        )

        np.testing.assert_allclose(
            result.training_squared_frobenius_residual.magnitude, 2.0
        )
        np.testing.assert_allclose(
            result.expected_squared_frobenius_residual.magnitude, 2.0
        )
        assert result.passes
