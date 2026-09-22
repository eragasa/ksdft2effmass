r"""Software verification of ``QuotientSeamOperatorConstructor``.

Evidence profile: routine

Bounded artifact scope: direct sparse quotient-seam construction for scalar hopping and
localized perturbation records.

Facet and represented meaning

The ActionObject independently resolves quotient-image crossings and applies seam phases
without calling uniform-link construction or a gauge bridge.

Intrinsic and cross-object scope

Hand-derived three-site hopping and out-of-cell localized bond examples are included.

VVUQ and scientific exclusions

These are independent software oracles for small represented matrices, not physical
model validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    QuotientSeamOperatorConstructor,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = QuotientSeamOperatorConstructor


class TestQuotientSeamOperatorConstructor:
    """Own software evidence for ``QuotientSeamOperatorConstructor``."""

    def test_method__execute_hopping__matches_hand_derived_twisted_ring(self) -> None:
        """Evidence ID: SV-SOLID-STATE-QUOTIENT-SEAM-001

        Requirement: Only bonds crossing a quotient seam receive the full twist phase.

        Acceptance: A three-site quarter-twisted nearest-neighbor ring equals the
        explicitly authored seam matrix in last-axis-fastest ordering.
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

        represented = QuotientSeamOperatorConstructor().execute_hopping(
            "seam",
            model,
            FiniteLatticeShape(LatticeDimension.ONE, (3,)),
            BoundaryTwistLift(LatticeDimension.ONE, (0.25,)),
        )

        expected = np.array(
            [[0.0, -1.0, 1.0j], [-1.0, 0.0, -1.0], [-1.0j, -1.0, 0.0]],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(
            represented.matrix.to_csr().toarray(), expected, rtol=0.0, atol=1.0e-15
        )
        assert represented.twist_fiber.gauge is TwistGaugeRepresentation.QUOTIENT_SEAM

    def test_method__execute_perturbation__uses_relative_image_quotient(self) -> None:
        """Evidence ID: SV-SOLID-STATE-QUOTIENT-SEAM-002

        Requirement: A localized bond whose start is outside the canonical cell uses
        target quotient minus source quotient, not target quotient alone.

        Acceptance: Explicit reverse bonds across a three-site quarter-twist seam yield
        conjugate ``+0.04 i`` and ``-0.04 i`` entries plus the declared onsite term.
        """
        perturbation = LocalizedPerturbation(
            "edge_defect",
            LatticeDimension.ONE,
            (
                LocalizedOnsiteTerm(
                    LatticeCoordinate(LatticeDimension.ONE, (0,)), 0.2, 0.0
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.ONE, (-1,)),
                    LatticeDisplacement(LatticeDimension.ONE, (1,)),
                    0.04,
                    0.0,
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.ONE, (0,)),
                    LatticeDisplacement(LatticeDimension.ONE, (-1,)),
                    0.04,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "parent_zero",
            "scalar_cell_basis",
        )

        represented = QuotientSeamOperatorConstructor().execute_perturbation(
            "seam_defect",
            perturbation,
            FiniteLatticeShape(LatticeDimension.ONE, (3,)),
            BoundaryTwistLift(LatticeDimension.ONE, (0.25,)),
        )

        expected = np.zeros((3, 3), dtype=np.complex128)
        expected[0, 0] = 0.2
        expected[2, 0] = 0.04j
        expected[0, 2] = -0.04j
        np.testing.assert_allclose(
            represented.matrix.to_csr().toarray(), expected, rtol=0.0, atol=1.0e-15
        )
        assert represented.provenance == (
            ("constructor", "QuotientSeamOperatorConstructor"),
            ("source_perturbation", "edge_defect"),
        )
