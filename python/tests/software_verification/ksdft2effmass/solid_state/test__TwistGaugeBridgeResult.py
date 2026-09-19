r"""Software verification of ``TwistGaugeBridgeResult``.

Evidence profile: routine

Bounded artifact scope: immutable correlated metadata for one twist-gauge bridge.

Facet and represented meaning

The ResultObject binds one shape, common twist reduction, ordered source and target
gauges, unitless sparse transformation, and direction convention.

Intrinsic and cross-object scope

Valid correlation and reversed-gauge rejection are included.

VVUQ and scientific exclusions

This verifies result-state consistency, not gauge equivalence of arbitrary operators,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, Unitless
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    FiniteLatticeShape,
    LatticeDimension,
    TwistFiber,
    TwistGaugeBridgeConstructor,
    TwistGaugeBridgeResult,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = TwistGaugeBridgeResult


class TestTwistGaugeBridgeResult:
    """Own software evidence for ``TwistGaugeBridgeResult``."""

    def test_constructor__fibers__requires_ordered_common_reduction(self) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-BRIDGE-002

        Requirement: Source and target roles are ordered and share one exact reduction.

        Acceptance: A constructor result retains its reduction; replacing the target
        with a uniform-link fiber raises ``ValueError``.
        """
        reduction = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.TWO, (1.25, -0.25))
        )
        source = TwistFiber(reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK)
        result = TwistGaugeBridgeConstructor().execute(
            FiniteLatticeShape(LatticeDimension.TWO, (2, 3)), source
        )

        assert result.source_fiber.reduction == result.target_fiber.reduction
        assert result.transformation.shape == (6, 6)
        with pytest.raises(ValueError, match="target fiber"):
            replace(result, target_fiber=source)

    def test_constructor__transformation__requires_site_diagonal_phases(self) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-BRIDGE-004

        Requirement: A retained gauge transformation has one unit-magnitude diagonal
        entry per represented site.

        Acceptance: Replacing a valid one-site bridge by a diagonal scaling of two
        raises ``ValueError``.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (1,))
        reduction = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
        )
        source = TwistFiber(reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK)
        result = TwistGaugeBridgeConstructor().execute(shape, source)
        scaling = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[2.0 + 0.0j]])), Unitless()
        )

        with pytest.raises(ValueError, match="unit magnitude"):
            replace(result, transformation=scaling)
