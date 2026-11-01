"""Compatibility-only checks for the rank-two hopping-value facade."""

import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality import (
    Periodic1DRank2HoppingPower as LegacyEquivalenceHoppingPower,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality import Periodic1DRank2HoppingPower

pytestmark = [
    pytest.mark.legacy_equivalence,
    pytest.mark.software_verification,
    pytest.mark.unit,
]


class TestPeriodic1DRank2HoppingPower:
    def test__legacy_equivalence__reexports_identical_class(self) -> None:
        """Establish import identity only, not scientific or numerical validity."""
        assert Periodic1DRank2HoppingPower is LegacyEquivalenceHoppingPower
