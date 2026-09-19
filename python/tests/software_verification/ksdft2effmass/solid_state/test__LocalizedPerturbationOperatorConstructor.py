r"""Software verification of ``LocalizedPerturbationOperatorConstructor``.

Evidence profile: routine

Bounded artifact scope: sparse centered-uniform-link construction for localized scalar
onsite and directed bond perturbations.

Facet and represented meaning

The ActionObject wraps declared support, applies the unreduced twist-lift phase to each
directed bond, and never invents reverse bonds.

Intrinsic and cross-object scope

A hand-derived Hermitian 2D perturbation and directed-only adverse control are included.

VVUQ and scientific exclusions

This is software verification of represented construction, not an independent seam
verifier, impurity-model validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexSparseHermiticityAnalyzer,
    PhysicalUnit,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    LocalizedPerturbationOperatorConstructor,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = LocalizedPerturbationOperatorConstructor


class TestLocalizedPerturbationOperatorConstructor:
    """Own evidence for ``LocalizedPerturbationOperatorConstructor``."""

    def test_method__execute__matches_hand_derived_2d_uniform_link_matrix(self) -> None:
        """Evidence ID: SV-SOLID-STATE-LOCALIZED-OPERATOR-001

        Requirement: Onsite and explicitly paired directed bonds receive their exact
        represented entries in last-axis-fastest ordering.

        Acceptance: Quarter-turn-per-link phases produce conjugate ``0.04 i`` entries
        between indices zero and two, with onsite value ``0.2`` at index zero.
        """
        perturbation = LocalizedPerturbation(
            "directional",
            LatticeDimension.TWO,
            (
                LocalizedOnsiteTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)), 0.2, 0.0
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
                    0.04,
                    0.0,
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (1, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
                    0.04,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        represented = LocalizedPerturbationOperatorConstructor().execute(
            "directional_operator",
            perturbation,
            FiniteLatticeShape(LatticeDimension.TWO, (3, 2)),
            BoundaryTwistLift(LatticeDimension.TWO, (0.75, 0.0)),
        )

        expected = np.zeros((6, 6), dtype=np.complex128)
        expected[0, 0] = 0.2
        expected[0, 2] = 0.04j
        expected[2, 0] = -0.04j
        np.testing.assert_allclose(
            represented.matrix.to_csr().toarray(), expected, rtol=0.0, atol=1.0e-17
        )
        assert (
            ComplexSparseHermiticityAnalyzer()
            .execute(represented.matrix, absolute_tolerance=1.0e-15)
            .is_hermitian
        )
        assert (
            represented.twist_fiber.gauge
            is TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        )
        assert represented.provenance == (
            ("constructor", "LocalizedPerturbationOperatorConstructor"),
            ("source_perturbation", "directional"),
        )

    def test_method__execute__does_not_invent_reverse_bonds(self) -> None:
        """Evidence ID: SV-SOLID-STATE-LOCALIZED-OPERATOR-002

        Requirement: Localized bond terms are directed and reverse entries require
        explicit input terms.

        Acceptance: One directed 1D bond produces exactly one stored matrix entry and
        a failed zero-tolerance Hermiticity result.
        """
        perturbation = LocalizedPerturbation(
            "directed",
            LatticeDimension.ONE,
            (
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.ONE, (0,)),
                    LatticeDisplacement(LatticeDimension.ONE, (1,)),
                    1.0,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        represented = LocalizedPerturbationOperatorConstructor().execute(
            "directed_operator",
            perturbation,
            FiniteLatticeShape(LatticeDimension.ONE, (3,)),
            BoundaryTwistLift(LatticeDimension.ONE, (0.0,)),
        )

        assert represented.matrix.nonzero_count == 1
        result = ComplexSparseHermiticityAnalyzer().execute(
            represented.matrix, absolute_tolerance=0.0
        )
        assert result.maximum_absolute_residual == 1.0
        assert not result.is_hermitian
