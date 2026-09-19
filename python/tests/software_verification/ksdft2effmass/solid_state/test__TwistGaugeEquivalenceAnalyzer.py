r"""Software verification of ``TwistGaugeEquivalenceAnalyzer``.

Evidence profile: routine

Bounded artifact scope: nondensifying represented comparison through an explicit twist
gauge bridge.

Facet and represented meaning

The ActionObject checks comparison-critical metadata before evaluating the maximum
absolute residual of ``H_target - U H_source U^dagger``.

Intrinsic and cross-object scope

Equivalent and perturbed matrices plus a basis-identity incompatibility are included.

VVUQ and scientific exclusions

This verifies one represented comparison contract. It does not prove physical gauge
invariance, scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarFiniteLatticeOperator,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistedSupercellOperatorConstructor,
    TwistGaugeBridgeConstructor,
    TwistGaugeEquivalenceAnalyzer,
    TwistGaugeEquivalenceIssueCode,
)

pytestmark = pytest.mark.software_verification
SUT = TwistGaugeEquivalenceAnalyzer


class TestTwistGaugeEquivalenceAnalyzer:
    """Own software evidence for ``TwistGaugeEquivalenceAnalyzer``."""

    @staticmethod
    def records() -> tuple[ScalarFiniteLatticeOperator, ScalarFiniteLatticeOperator]:
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
        source = TwistedSupercellOperatorConstructor().execute(
            "uniform",
            model,
            shape,
            BoundaryTwistLift(LatticeDimension.ONE, (0.25,)),
        )
        bridge = TwistGaugeBridgeConstructor().execute(shape, source.twist_fiber)
        seam = np.array(
            [[0.0, -1.0, 1.0j], [-1.0, 0.0, -1.0], [-1.0j, -1.0, 0.0]],
            dtype=np.complex128,
        )
        target = ScalarFiniteLatticeOperator(
            "seam",
            ComplexSparseMatrixQuantity.from_csr(
                sparse.csr_array(seam), PhysicalUnit("electron_volt")
            ),
            shape,
            bridge.target_fiber,
            source.basis_identifier,
            source.energy_reference,
            (("route", "hand_derived_seam"),),
        )
        return source, target

    def test_method__execute__accepts_equivalent_and_rejects_perturbed_matrix(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-EQUIVALENCE-001

        Requirement: Compatible matrices are compared only after applying the bridge.

        Acceptance: The hand-derived seam matrix passes at ``1e-14``; adding ``0.01``
        to one entry produces residual ``0.01`` and fails the same tolerance.
        """
        source, target = self.records()
        bridge = TwistGaugeBridgeConstructor().execute(source.shape, source.twist_fiber)
        analyzer = TwistGaugeEquivalenceAnalyzer()

        equivalent = analyzer.execute(
            source, target, bridge, absolute_tolerance=1.0e-14
        )
        changed = target.matrix.to_csr().toarray()
        changed[0, 0] = 0.01
        perturbed = replace(
            target,
            matrix=ComplexSparseMatrixQuantity.from_csr(
                sparse.csr_array(changed), PhysicalUnit("electron_volt")
            ),
        )
        rejected = analyzer.execute(
            source, perturbed, bridge, absolute_tolerance=1.0e-14
        )

        assert equivalent.compatible and equivalent.is_equivalent
        assert equivalent.maximum_absolute_residual is not None
        assert equivalent.maximum_absolute_residual <= 1.0e-15
        assert rejected.maximum_absolute_residual == pytest.approx(0.01)
        assert not rejected.is_equivalent

    def test_method__execute__reports_metadata_incompatibility_without_arithmetic(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-GAUGE-EQUIVALENCE-002

        Requirement: Comparison stops before arithmetic when represented metadata
        disagree.

        Acceptance: A changed basis identity returns the structured basis issue and no
        residual.
        """
        source, target = self.records()
        bridge = TwistGaugeBridgeConstructor().execute(source.shape, source.twist_fiber)

        result = TwistGaugeEquivalenceAnalyzer().execute(
            source,
            replace(target, basis_identifier="different_basis"),
            bridge,
            absolute_tolerance=1.0e-14,
        )

        assert result.issue_codes == (TwistGaugeEquivalenceIssueCode.BASIS,)
        assert result.maximum_absolute_residual is None
        assert not result.compatible
        assert not result.is_equivalent
