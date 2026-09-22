r"""Software verification of ``ScalarFiniteLatticeOperator``.

Evidence profile: routine

Bounded artifact scope: complete metadata for one sparse scalar finite-lattice operator
representation.

Facet and represented meaning

The DataObject correlates canonical complex CSR values with finite shape, twist, gauge,
basis, unit, energy reference, and provenance identities.

Intrinsic and cross-object scope

Valid 2D construction, matrix-size agreement, twist-dimension agreement, and canonical
provenance ordering are included.

VVUQ and scientific exclusions

This verifies represented metadata consistency, not Hermiticity, gauge equivalence,
operator construction, numerical verification, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    FiniteLatticeShape,
    LatticeDimension,
    ScalarFiniteLatticeOperator,
    TwistFiber,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeOperator


class TestScalarFiniteLatticeOperator:
    """Own software evidence for ``ScalarFiniteLatticeOperator``."""

    def test_constructor__metadata__retains_complete_scalar_representation(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-SCALAR-OPERATOR-001

        Requirement: The record correlates one matrix state with all interpreting
        scalar finite-lattice metadata.

        Acceptance: A six-state 2D representation retains exact geometry, twist,
        gauge, basis, unit, reference, and provenance values.
        """
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.identity(6, dtype=np.complex128, format="csr"),
            PhysicalUnit("electron_volt"),
        )
        shape = FiniteLatticeShape(LatticeDimension.TWO, (2, 3))
        twist_fiber = TwistFiber(
            BoundaryTwistReducer().execute(
                BoundaryTwistLift(LatticeDimension.TWO, (0.25, 0.5))
            ),
            TwistGaugeRepresentation.CENTERED_UNIFORM_LINK,
        )

        represented = ScalarFiniteLatticeOperator(
            "twisted_parent",
            matrix,
            shape,
            twist_fiber,
            "scalar_cell_basis",
            "parent_zero",
            (("model", "parent"), ("route", "uniform_link")),
        )

        assert represented.dimension is LatticeDimension.TWO
        assert represented.matrix.shape == (6, 6)
        assert represented.matrix.unit == PhysicalUnit("electron_volt")
        assert represented.twist_fiber == twist_fiber
        assert represented.provenance == (
            ("model", "parent"),
            ("route", "uniform_link"),
        )

    def test_constructor__correlation__rejects_shape_twist_and_provenance_drift(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-SCALAR-OPERATOR-002

        Requirement: Matrix dimension, geometry dimension, and provenance order are
        exact constructor invariants.

        Acceptance: Wrong matrix size, wrong twist dimension, and unsorted provenance
        each raise ``ValueError``.
        """
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.identity(4, dtype=np.complex128, format="csr"),
            PhysicalUnit("electron_volt"),
        )
        shape = FiniteLatticeShape(LatticeDimension.TWO, (2, 3))
        twist_fiber = TwistFiber(
            BoundaryTwistReducer().execute(
                BoundaryTwistLift(LatticeDimension.TWO, (0.0, 0.0))
            ),
            TwistGaugeRepresentation.QUOTIENT_SEAM,
        )

        with pytest.raises(ValueError, match="matrix shape"):
            ScalarFiniteLatticeOperator(
                "operator",
                matrix,
                shape,
                twist_fiber,
                "scalar_cell_basis",
                "parent_zero",
                (),
            )
        valid_matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.identity(6, dtype=np.complex128, format="csr"),
            PhysicalUnit("electron_volt"),
        )
        with pytest.raises(ValueError, match="dimensions must agree"):
            ScalarFiniteLatticeOperator(
                "operator",
                valid_matrix,
                shape,
                TwistFiber(
                    BoundaryTwistReducer().execute(
                        BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
                    ),
                    TwistGaugeRepresentation.QUOTIENT_SEAM,
                ),
                "scalar_cell_basis",
                "parent_zero",
                (),
            )
        with pytest.raises(ValueError, match="sorted and unique"):
            ScalarFiniteLatticeOperator(
                "operator",
                valid_matrix,
                shape,
                twist_fiber,
                "scalar_cell_basis",
                "parent_zero",
                (("route", "seam"), ("model", "parent")),
            )
