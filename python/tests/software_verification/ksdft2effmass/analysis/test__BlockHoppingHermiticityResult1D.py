r"""Software verification of ``BlockHoppingHermiticityResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-1D hopping Hermiticity results.

Facet and represented meaning

The ResultObject retains pairing coverage, tolerance, defect, and disposition.

Intrinsic and cross-object scope

Pass consistency with missing opposites is included.

VVUQ and scientific exclusions

Result consistency does not establish physical locality or model validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
    BlockHoppingHermiticityResult1D,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingHermiticityResult1D


class TestBlockHoppingHermiticityResult1D:
    """Own software evidence for ``BlockHoppingHermiticityResult1D``."""

    def test_constructor__passes__rejects_disposition_ignoring_missing_pair(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-019

        Requirement: Missing opposite representatives force a failed disposition.

        Acceptance: Replacing the calculated false disposition with true raises an
        error.
        """
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-1, 0), (block, block)
        )
        valid = BlockHoppingHermiticityAnalyzer1D().execute(
            model, ScalarQuantity(0.0, Unitless()), None
        )

        with pytest.raises(ValueError, match="must match coverage"):
            BlockHoppingHermiticityResult1D(
                valid.model,
                valid.representative_modulus,
                valid.paired_representatives,
                valid.missing_opposite_representatives,
                valid.maximum_frobenius_defect,
                valid.absolute_tolerance,
                True,
            )
