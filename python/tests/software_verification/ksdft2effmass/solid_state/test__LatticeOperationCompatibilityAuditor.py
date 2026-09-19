r"""Software verification of ``LatticeOperationCompatibilityAuditor``.

Evidence profile: routine

Bounded artifact scope: signed-axis-permutation compatibility between finite shapes.

Facet and represented meaning

The ActionObject compares source and target axis extents under an explicit operation.

Intrinsic and cross-object scope

Compatible and extent-mismatched targets are included.

VVUQ and scientific exclusions

This verifies represented shape compatibility, not Hamiltonian equivalence.
"""

import pytest

from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    IntegralLatticeOperation,
    LatticeDimension,
    LatticeOperationCompatibilityAuditor,
)

pytestmark = pytest.mark.software_verification
SUT = LatticeOperationCompatibilityAuditor


class TestLatticeOperationCompatibilityAuditor:
    """Own software evidence for ``LatticeOperationCompatibilityAuditor``."""

    def test_method__execute__maps_axis_extents_and_reports_mismatch(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-017

        Requirement: A signed axis permutation maps source extents to target axes.

        Acceptance: ``(2,3,4)`` maps to ``(3,4,2)`` and not to itself.
        """
        operation = IntegralLatticeOperation(
            "axis_cycle",
            LatticeDimension.THREE,
            ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
        )
        source = FiniteLatticeShape(LatticeDimension.THREE, (2, 3, 4))
        auditor = LatticeOperationCompatibilityAuditor()

        assert auditor.execute(
            source,
            FiniteLatticeShape(LatticeDimension.THREE, (3, 4, 2)),
            operation,
        ).compatible
        mismatch = auditor.execute(source, source, operation)
        assert mismatch.issue_codes == (
            "SOLID_STATE.LATTICE_OPERATION.EXTENT_MISMATCH",
        )
