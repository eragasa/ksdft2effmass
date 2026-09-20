r"""Software verification of ``ReciprocalOperatorSamples1D``.

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
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

pytestmark = pytest.mark.software_verification
SUT = ReciprocalOperatorSamples1D


class TestReciprocalOperatorSamples1D:
    """Verify ordered reciprocal operator-sample invariants."""

    def test_constructor__samples__normalizes_coordinates(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-022

        Requirement: The public contract enforces normalizes coordinate units
        and retains matrix dimension.

        Acceptance: The asserted values and failures match the declared contract.
        """
        matrix = ComplexMatrixQuantity(np.eye(2), Unitless())
        samples = ReciprocalOperatorSamples1D(
            VectorQuantity(np.asarray([0.0, 500.0]), PhysicalUnit("1 / meter")),
            ScalarQuantity(1.0, PhysicalUnit("1 / millimeter")),
            (matrix, matrix),
        )

        np.testing.assert_allclose(samples.coordinates.magnitude, [0.0, 0.5])
        assert samples.coordinates.unit == samples.reciprocal_period.unit
        assert samples.matrix_dimension == 2

    def test_constructor__samples__rejects_matrix_count_not_matching_coordinates(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-023

        Requirement: The public contract enforces rejects matrix count not
        matching coordinates.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="matrix count"):
            ReciprocalOperatorSamples1D(
                VectorQuantity(np.asarray([0.0, 0.5]), Unitless()),
                ScalarQuantity(1.0, Unitless()),
                (ComplexMatrixQuantity(np.eye(1), Unitless()),),
            )
