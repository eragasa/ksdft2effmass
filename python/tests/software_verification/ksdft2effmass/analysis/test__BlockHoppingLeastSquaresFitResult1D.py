r"""Software verification of ``BlockHoppingLeastSquaresFitResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-1D hopping least-squares fit results.

Facet and represented meaning

The ResultObject binds design rank, identification, model, and training residuals.

Intrinsic and cross-object scope

Rank disposition and represented residual correlation are included.

VVUQ and scientific exclusions

Result consistency does not establish model adequacy or validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitResult1D,
    BlockHoppingLeastSquaresFitter1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingLeastSquaresFitResult1D


class TestBlockHoppingLeastSquaresFitResult1D:
    """Own software evidence for ``BlockHoppingLeastSquaresFitResult1D``."""

    def test_constructor__identification__rejects_rank_disposition_mismatch(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-014

        Requirement: Identification is true exactly for full column rank.

        Acceptance: Replacing a full-rank fit disposition with false raises an error.
        """
        coordinates = VectorQuantity(np.asarray([-0.25, 0.25]), Unitless())
        source = ReciprocalOperatorSamples1D(
            coordinates,
            ScalarQuantity(1.0, Unitless()),
            (
                ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[2.0]]), Unitless()),
            ),
        )
        valid = BlockHoppingLeastSquaresFitter1D().execute(
            source, (0,), VectorQuantity(np.ones(2), Unitless())
        )

        with pytest.raises(ValueError, match="must match design rank"):
            BlockHoppingLeastSquaresFitResult1D(
                valid.source,
                valid.representatives,
                valid.weights,
                valid.fitted_model,
                valid.reconstructed_training,
                valid.design_rank,
                valid.design_condition_number,
                False,
                valid.training_l2_frobenius_residual,
                valid.training_maximum_frobenius_residual,
            )
