r"""Software verification of ``ContiguousBandSelection``.

Evidence profile: routine

Bounded artifact scope: inclusive contiguous band-index selections.

Facet and represented meaning

The DataObject identifies a retained contiguous band interval.

Intrinsic and cross-object scope

Index ordering and derived rank are included.

VVUQ and scientific exclusions

This verifies index semantics, not band isolation or physical suitability.
"""

import pytest

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection

pytestmark = pytest.mark.software_verification
SUT = ContiguousBandSelection


class TestContiguousBandSelection:
    """Own software evidence for ``ContiguousBandSelection``."""

    def test_constructor__indices__retains_inclusive_band_count(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-003

        Requirement: Selection bounds are inclusive.

        Acceptance: The interval from two through four has rank three.
        """
        selection = ContiguousBandSelection(2, 4)

        assert selection.band_count == 3

    def test_constructor__indices__rejects_reversed_interval(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-004

        Requirement: The upper index is not below the lower index.

        Acceptance: Reversed bounds raise ``ValueError``.
        """
        with pytest.raises(ValueError, match="nonnegative and ordered"):
            ContiguousBandSelection(2, 1)
