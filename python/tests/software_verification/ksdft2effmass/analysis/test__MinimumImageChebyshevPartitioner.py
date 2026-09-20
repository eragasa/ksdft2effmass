r"""Software verification of ``MinimumImageChebyshevPartitioner``.

Evidence profile: routine

Bounded artifact scope: periodic minimum-image Chebyshev shells in canonical finite-site
ordering.

Facet and represented meaning

The ActionObject assigns every site to one exact integer shell around a canonical
origin and derives a core/exterior partition from an explicit radius.

Intrinsic and cross-object scope

A 4x4 even-size periodic geometry exercises minimum-image ties and wraparound.

VVUQ and scientific exclusions

This is software geometry evidence, not a physical locality claim, numerical or
scientific validation, UQ, campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartitioner,
)
from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = MinimumImageChebyshevPartitioner


class TestMinimumImageChebyshevPartitioner:
    """Own software evidence for periodic Chebyshev shell construction."""

    def test_method__execute__assigns_even_size_minimum_image_shells(self) -> None:
        """Evidence ID: SV-ANALYSIS-MINIMUM-IMAGE-PARTITIONER-001

        Requirement: Periodic axis distances use the minimum image and Chebyshev shell
        radius under last-axis-fastest ordering.

        Acceptance: A 4x4 origin-centered partition has shell populations 1, 8, and 7;
        radius one retains nine core sites and assigns index ten to shell two.
        """
        partition = MinimumImageChebyshevPartitioner().execute(
            FiniteLatticeShape(LatticeDimension.TWO, (4, 4)),
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            core_radius=1,
        )

        assert len(partition.indices_for_shell(0)) == 1
        assert len(partition.indices_for_shell(1)) == 8
        assert len(partition.indices_for_shell(2)) == 7
        assert len(partition.core_indices) == 9
        assert len(partition.exterior_indices) == 7
        assert partition.site_shells[10] == 2
