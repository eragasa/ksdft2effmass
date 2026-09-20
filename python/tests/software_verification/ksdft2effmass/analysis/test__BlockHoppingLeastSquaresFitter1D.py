r"""Software verification of ``BlockHoppingLeastSquaresFitter1D``.

Evidence profile: routine

Bounded artifact scope: weighted periodic-1D block-hopping least-squares fits.

Facet and represented meaning

The ActionObject fits a declared Fourier class to reciprocal operator samples.

Intrinsic and cross-object scope

Uniform positive weights, complex coefficients, rank, and residuals are included.

VVUQ and scientific exclusions

A least-squares fit is not scientific validation or an uncertainty estimate.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_fits import BlockHoppingLeastSquaresFitter1D
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingLeastSquaresFitter1D


class TestBlockHoppingLeastSquaresFitter1D:
    """Own software evidence for ``BlockHoppingLeastSquaresFitter1D``."""

    def test_method__execute__recovers_nearest_neighbor_coefficients(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-013

        Requirement: Complete uniform least squares recovers an exactly represented
        scalar nearest-neighbor Fourier series.

        Acceptance: The fitted coefficients are ``(0.5, 2, 0.5)`` with full rank.
        """
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, Unitless()), 4
        )
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

        result = BlockHoppingLeastSquaresFitter1D().execute(
            source,
            (-1, 0, 1),
            VectorQuantity(np.ones(4), Unitless()),
        )

        np.testing.assert_allclose(
            np.asarray(
                [
                    result.fitted_model.hopping_blocks[0].magnitude[0, 0],
                    result.fitted_model.hopping_blocks[1].magnitude[0, 0],
                    result.fitted_model.hopping_blocks[2].magnitude[0, 0],
                ]
            ),
            [0.5, 2.0, 0.5],
            atol=1.0e-14,
        )
        assert result.design_rank == 3
        assert result.is_identified
        assert result.training_maximum_frobenius_residual <= 1.0e-14

    def test_method__execute__retains_rank_deficiency_without_failure(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-024

        Requirement: An underdetermined fit remains a result with explicit failed
        identification rather than inventing a finite condition number.

        Acceptance: One sample for two representatives has rank one, ``None``
        condition number, and ``is_identified`` false.
        """
        source = ReciprocalOperatorSamples1D(
            VectorQuantity(np.asarray([0.0]), Unitless()),
            ScalarQuantity(1.0, Unitless()),
            (ComplexMatrixQuantity(np.asarray([[2.0]]), Unitless()),),
        )

        result = BlockHoppingLeastSquaresFitter1D().execute(
            source, (0, 1), VectorQuantity(np.ones(1), Unitless())
        )

        assert result.design_rank == 1
        assert result.design_condition_number is None
        assert not result.is_identified
