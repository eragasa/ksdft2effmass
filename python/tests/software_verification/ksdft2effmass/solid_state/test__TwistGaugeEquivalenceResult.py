r"""Software verification of ``TwistGaugeEquivalenceResult``.

Evidence profile: routine

Bounded artifact scope: immutable compatibility and residual outcomes for represented
twist-gauge comparison.

Facet and represented meaning

The ResultObject distinguishes compatibility, residual availability, caller tolerance,
and inclusive equivalence status.

Intrinsic and cross-object scope

A compatible zero-residual result and contradictory residual state are included.

VVUQ and scientific exclusions

This verifies result-state consistency, not analyzer correctness, scientific validation,
uncertainty quantification, or human acceptance.
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
    ScalarFiniteLatticeOperator,
    TwistFiber,
    TwistGaugeBridgeConstructor,
    TwistGaugeEquivalenceAnalyzer,
    TwistGaugeEquivalenceResult,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = TwistGaugeEquivalenceResult


class TestTwistGaugeEquivalenceResult:
    """Own software evidence for ``TwistGaugeEquivalenceResult``."""

    def test_constructor__residual_presence__agrees_with_compatibility(self) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-EQUIVALENCE-003

        Requirement: A compatible result retains a residual and incompatible state does
        not masquerade as evaluated arithmetic.

        Acceptance: Equal one-site representations yield zero and removing that
        residual through dataclass replacement raises ``ValueError``.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (1,))
        reduction = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
        )
        source_fiber = TwistFiber(
            reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        )
        bridge = TwistGaugeBridgeConstructor().execute(shape, source_fiber)
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[2.0 + 0.0j]])), Unitless()
        )
        source = ScalarFiniteLatticeOperator(
            "source", matrix, shape, source_fiber, "basis", "zero", ()
        )
        target = ScalarFiniteLatticeOperator(
            "target", matrix, shape, bridge.target_fiber, "basis", "zero", ()
        )

        result = TwistGaugeEquivalenceAnalyzer().execute(
            source, target, bridge, absolute_tolerance=0.0
        )

        assert result.compatible and result.is_equivalent
        assert result.maximum_absolute_residual == 0.0
        with pytest.raises(ValueError, match="residual presence"):
            replace(result, maximum_absolute_residual=None)
