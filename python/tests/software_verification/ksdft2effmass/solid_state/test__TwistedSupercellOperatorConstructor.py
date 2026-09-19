r"""Software verification of ``TwistedSupercellOperatorConstructor``.

Evidence profile: routine

Bounded artifact scope: sparse centered-uniform-link parent construction from scalar
hopping inventories.

Facet and represented meaning

The ActionObject assembles canonical complex CSR values with last-axis-fastest finite
geometry and the unreduced twist-lift phase convention.

Intrinsic and cross-object scope

A hand-derived nonzero-twist 1D matrix, closed 2D/3D construction, retained metadata,
Hermiticity interoperability, and dimensional rejection are included.

VVUQ and scientific exclusions

This is software verification of represented construction. It is not the independent
quotient-seam verifier, a finite-domain calculation, numerical validation, scientific
validation, uncertainty quantification, or human acceptance.
"""

import math

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexSparseHermiticityAnalyzer,
    PhysicalUnit,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistedSupercellOperatorConstructor,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = TwistedSupercellOperatorConstructor


class TestTwistedSupercellOperatorConstructor:
    """Own software evidence for ``TwistedSupercellOperatorConstructor``."""

    def test_method__execute__matches_hand_derived_1d_uniform_link_matrix(self) -> None:
        """Evidence ID: SV-SOLID-STATE-TWISTED-SUPERCELL-001

        Requirement: Every displacement receives the centered uniform-link phase from
        the unreduced twist lift and finite extent.

        Acceptance: A three-site nearest-neighbor ring at quarter twist equals the
        explicit matrix with phase ``sqrt(3)/2 + i/2`` and is exactly Hermitian within
        binary64 tolerance.
        """
        model = ScalarHoppingModel(
            "nearest_neighbor",
            LatticeDimension.ONE,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.ONE, (-1,)), -1.0, 0.0
                ),
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.ONE, (1,)), -1.0, 0.0
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        represented = TwistedSupercellOperatorConstructor().execute(
            "three_site_ring",
            model,
            FiniteLatticeShape(LatticeDimension.ONE, (3,)),
            BoundaryTwistLift(LatticeDimension.ONE, (0.25,)),
        )

        phase = complex(math.sqrt(3.0) / 2.0, 0.5)
        expected = np.array(
            [
                [0.0, -phase, -phase.conjugate()],
                [-phase.conjugate(), 0.0, -phase],
                [-phase, -phase.conjugate(), 0.0],
            ],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(
            represented.matrix.to_csr().toarray(), expected, rtol=0.0, atol=1.0e-15
        )
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            represented.matrix, absolute_tolerance=1.0e-14
        )
        assert hermiticity.is_hermitian
        assert represented.twist_fiber.lift.turns == (0.25,)
        assert (
            represented.twist_fiber.gauge
            is TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        )
        assert represented.provenance == (
            ("constructor", "TwistedSupercellOperatorConstructor"),
            ("source_model", "nearest_neighbor"),
        )

    def test_method__execute__constructs_closed_2d_and_3d_shapes(self) -> None:
        """Evidence ID: SV-SOLID-STATE-TWISTED-SUPERCELL-002

        Requirement: Construction is closed over exactly 1D, 2D, and 3D rather than
        hiding a 2D-only loop.

        Acceptance: Onsite-only 2D and 3D models produce sparse ``2 I`` operators with
        dimensions equal to their exact cell counts.
        """
        constructor = TwistedSupercellOperatorConstructor()
        two_model = ScalarHoppingModel(
            "onsite_2d",
            LatticeDimension.TWO,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (0, 0)), 2.0, 0.0
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )
        three_model = ScalarHoppingModel(
            "onsite_3d",
            LatticeDimension.THREE,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.THREE, (0, 0, 0)),
                    2.0,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        two = constructor.execute(
            "two",
            two_model,
            FiniteLatticeShape(LatticeDimension.TWO, (2, 3)),
            BoundaryTwistLift(LatticeDimension.TWO, (1.25, -0.25)),
        )
        three = constructor.execute(
            "three",
            three_model,
            FiniteLatticeShape(LatticeDimension.THREE, (2, 1, 2)),
            BoundaryTwistLift(LatticeDimension.THREE, (0.1, 0.2, 0.3)),
        )

        np.testing.assert_array_equal(two.matrix.to_csr().toarray(), 2.0 * np.eye(6))
        np.testing.assert_array_equal(three.matrix.to_csr().toarray(), 2.0 * np.eye(4))
        assert two.twist_fiber.representative.turns == (0.25, 0.75)
        assert two.twist_fiber.reduction.quotient.components == (1, -1)

    def test_method__execute__rejects_cross_dimension_inputs(self) -> None:
        """Evidence ID: SV-SOLID-STATE-TWISTED-SUPERCELL-003

        Requirement: Model, shape, and twist dimensions must agree exactly.

        Acceptance: A 1D model with a 2D shape raises ``ValueError``.
        """
        model = ScalarHoppingModel(
            "onsite",
            LatticeDimension.ONE,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.ONE, (0,)), 1.0, 0.0
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        with pytest.raises(ValueError, match="model and finite-lattice"):
            TwistedSupercellOperatorConstructor().execute(
                "mismatch",
                model,
                FiniteLatticeShape(LatticeDimension.TWO, (2, 2)),
                BoundaryTwistLift(LatticeDimension.TWO, (0.0, 0.0)),
            )
