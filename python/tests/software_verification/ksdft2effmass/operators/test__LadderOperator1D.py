r"""Software verification of ``LadderOperator1D``.

Evidence profile: routine

Bounded artifact scope: public retained one-dimensional ladder-algebra contract.

Facet and represented meaning

The class under test owns a finite ordered occupation-number basis and its Unitless
creation, annihilation, number, and commutator matrices.

Intrinsic and cross-object scope

Finite basis ordering, exact number labels, matrix immutability, and the highest-state
commutator defect are included.

VVUQ and scientific exclusions

This verifies finite represented algebra only. It does not identify the retained
commutator with the infinite-dimensional canonical algebra or establish scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass import operators
from ksdft2effmass.analysis.model_systems import Unitless
from ksdft2effmass.operators import (
    LadderOperator1D,
)

pytestmark = pytest.mark.software_verification
SUT = LadderOperator1D


class TestLadderOperator1D:
    """Own software evidence for ``LadderOperator1D``."""

    def test_method__commutator__exposes_retained_highest_state_defect(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-LADDER-001

        Requirement: LadderOperator1D constructs the retained Unitless algebra and
        exposes rather than conceals its finite highest-state commutator defect.

        Acceptance: In dimension three, ``a`` has ``(1,sqrt(2))`` on its upper
        diagonal, ``N=diag(0,1,2)``, and ``[a,adag]=diag(1,1,-2)``.
        """
        assert operators.LadderOperator1D is LadderOperator1D
        ladder = LadderOperator1D(3)

        np.testing.assert_allclose(
            ladder.annihilation().to_dense().magnitude,
            np.array([[0.0, 1.0, 0.0], [0.0, 0.0, np.sqrt(2.0)], [0.0, 0.0, 0.0]]),
        )
        np.testing.assert_array_equal(
            ladder.number().to_dense().magnitude, np.diag([0.0, 1.0, 2.0])
        )
        np.testing.assert_allclose(
            ladder.commutator().to_dense().magnitude, np.diag([1.0, 1.0, -2.0])
        )
        assert isinstance(ladder.commutator().unit, Unitless)
