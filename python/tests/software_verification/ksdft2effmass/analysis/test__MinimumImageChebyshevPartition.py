r"""Software verification of ``MinimumImageChebyshevPartition``.

Evidence profile: routine

Bounded artifact scope: immutable shell assignment and correlated core/exterior index
sets.

Facet and represented meaning

The DataObject requires its sorted index partition to agree exactly with shell values
and the declared core radius.

Intrinsic and cross-object scope

A constructed partition and intentionally incomplete core index set are included.

VVUQ and scientific exclusions

This is software record evidence, not a physical locality claim, validation, UQ,
campaign execution, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartition,
    MinimumImageChebyshevPartitioner,
)
from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = MinimumImageChebyshevPartition


class TestMinimumImageChebyshevPartition:
    """Own software evidence for immutable locality partition consistency."""

    def test_constructor__index_partition__must_agree_with_shell_radius(self) -> None:
        """Evidence ID: SV-ANALYSIS-MINIMUM-IMAGE-PARTITION-001

        Requirement: Core and exterior indices are complete consequences of shells and
        radius rather than independently editable labels.

        Acceptance: A valid 3x3 partition has two shells; dropping one core index raises
        ``ValueError``.
        """
        partition = MinimumImageChebyshevPartitioner().execute(
            FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            core_radius=1,
        )

        assert partition.shell_count == 2
        assert partition.exterior_indices == ()
        with pytest.raises(ValueError, match="agree with site shells"):
            replace(partition, core_indices=partition.core_indices[:-1])
