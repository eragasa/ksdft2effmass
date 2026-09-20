r"""Software verification of ``HoppingParsevalResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-1D hopping Parseval results.

Facet and represented meaning

The ResultObject retains squared norms, absolute residual, tolerance, and disposition.

Intrinsic and cross-object scope

Residual and pass correlation are included.

VVUQ and scientific exclusions

Result consistency does not establish convergence or scientific validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import (
    HoppingParsevalAnalyzer1D,
    HoppingParsevalResult1D,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = HoppingParsevalResult1D


class TestHoppingParsevalResult1D:
    """Own software evidence for ``HoppingParsevalResult1D``."""

    def test_constructor__passes__rejects_disposition_mismatch(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-021

        Requirement: Parseval disposition follows retained residual and tolerance.

        Acceptance: Replacing a passing disposition with false raises ``ValueError``.
        """
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, Unitless()), 2
        )
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates, mesh.reciprocal_period, (block, block)
        )
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source, mesh, 0.0, 1.0e-14
        )
        truncation = BlockHoppingTruncator1D().execute(
            transform.hopping_model, 1
        )
        valid = HoppingParsevalAnalyzer1D().execute(
            transform, truncation, ScalarQuantity(1.0e-14, Unitless())
        )

        with pytest.raises(ValueError, match="must match residual"):
            HoppingParsevalResult1D(
                valid.transform,
                valid.truncation,
                valid.training_squared_frobenius_residual,
                valid.expected_squared_frobenius_residual,
                valid.parseval_absolute_residual,
                valid.absolute_tolerance,
                False,
            )
