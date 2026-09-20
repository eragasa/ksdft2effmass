r"""Software verification of ``BlockHoppingHermiticityAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: conjugate block pairing for periodic-1D hopping models.

Facet and represented meaning

The ActionObject checks ``T[-R] = T[R]^dagger`` with explicit modular semantics.

Intrinsic and cross-object scope

Exact finite-range and Born--von Karman representative pairing are included.

VVUQ and scientific exclusions

Represented Hermiticity does not establish physical model validity.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingHermiticityAnalyzer1D


class TestBlockHoppingHermiticityAnalyzer1D:
    """Own software evidence for ``BlockHoppingHermiticityAnalyzer1D``."""

    def test_method__execute__pairs_even_mesh_nyquist_representative(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-017

        Requirement: Under modulus four, representative ``-2`` is its own opposite.

        Acceptance: A Hermitian Nyquist block and conjugate nearest neighbors pass.
        """
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (-2, -1, 0, 1),
            (
                ComplexMatrixQuantity(np.asarray([[0.2]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[0.5 + 0.1j]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[2.0]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[0.5 - 0.1j]]), Unitless()),
            ),
        )

        result = BlockHoppingHermiticityAnalyzer1D().execute(
            model, ScalarQuantity(1.0e-14, Unitless()), 4
        )

        assert result.paired_representatives == (-2, -1, 0, 1)
        assert result.missing_opposite_representatives == ()
        assert result.maximum_frobenius_defect.magnitude == 0.0
        assert result.passes

    def test_method__execute__reports_missing_exact_opposite_without_modulus(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-018

        Requirement: Modular equivalence is never inferred when no modulus is declared.

        Acceptance: The centered even-mesh Nyquist representative remains unpaired.
        """
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-2, -1, 0, 1), (block,) * 4
        )

        result = BlockHoppingHermiticityAnalyzer1D().execute(
            model, ScalarQuantity(0.0, Unitless()), None
        )

        assert result.missing_opposite_representatives == (-2,)
        assert not result.passes
