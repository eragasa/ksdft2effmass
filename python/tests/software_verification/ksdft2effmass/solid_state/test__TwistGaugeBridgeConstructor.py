r"""Software verification of ``TwistGaugeBridgeConstructor``.

Evidence profile: routine

Bounded artifact scope: sparse site-diagonal bridges from centered uniform-link to
quotient-seam twist gauge.

Facet and represented meaning

The ActionObject uses the unreduced twist lift and declares
``H_target = U H_source U^dagger``.

Intrinsic and cross-object scope

Hand-derived diagonal phases and a three-site uniform-to-seam matrix relation are
included.

VVUQ and scientific exclusions

This is software verification of the production bridge. It is not the independent seam
constructor, scientific validation, uncertainty quantification, or human acceptance.
"""

import math

import numpy as np
import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistedSupercellOperatorConstructor,
    TwistGaugeBridgeConstructor,
    TwistGaugeBridgeConvention,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = TwistGaugeBridgeConstructor


class TestTwistGaugeBridgeConstructor:
    """Own software evidence for ``TwistGaugeBridgeConstructor``."""

    def test_method__execute__matches_diagonal_phases_and_seam_relation(self) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-BRIDGE-001

        Requirement: The bridge uses site phase ``exp(2*pi*i*r*phi/N)`` and its
        declared source-to-target direction.

        Acceptance: A three-site quarter-twist bridge has explicit diagonal phases and
        transforms the uniform nearest-neighbor ring into the hand-derived seam matrix.
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
        shape = FiniteLatticeShape(LatticeDimension.ONE, (3,))
        uniform = TwistedSupercellOperatorConstructor().execute(
            "uniform",
            model,
            shape,
            BoundaryTwistLift(LatticeDimension.ONE, (0.25,)),
        )

        bridge = TwistGaugeBridgeConstructor().execute(shape, uniform.twist_fiber)

        expected_diagonal = np.array(
            [
                1.0 + 0.0j,
                complex(math.sqrt(3.0) / 2.0, 0.5),
                complex(0.5, math.sqrt(3.0) / 2.0),
            ]
        )
        np.testing.assert_allclose(
            bridge.transformation.data,
            expected_diagonal,
            rtol=0.0,
            atol=1.0e-15,
        )
        unitary = bridge.transformation.to_csr()
        transformed = (
            unitary @ uniform.matrix.to_csr() @ unitary.conjugate().transpose()
        )
        expected_seam = np.array(
            [[0.0, -1.0, 1.0j], [-1.0, 0.0, -1.0], [-1.0j, -1.0, 0.0]],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(
            transformed.toarray(), expected_seam, rtol=0.0, atol=1.0e-15
        )
        assert (
            bridge.source_fiber.gauge is TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        )
        assert bridge.target_fiber.gauge is TwistGaugeRepresentation.QUOTIENT_SEAM
        assert (
            bridge.convention
            is TwistGaugeBridgeConvention.TARGET_EQUALS_U_SOURCE_U_DAGGER
        )
