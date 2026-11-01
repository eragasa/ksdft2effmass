"""Authoritative ownership checks for the rank-two hopping-locality value."""

import pytest

from ksdft2effmass.periodic1d.rank2.hopping_locality import Periodic1DRank2HoppingPower
from ksdft2effmass.periodic1d.rank2.hopping_locality.result import (
    Periodic1DRank2HoppingPower as BandEquivalenceHoppingPower,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.unit]


class TestPeriodic1DRank2HoppingPower:
    def test__band_equivalence_study__consumes_authoritative_value(self) -> None:
        assert Periodic1DRank2HoppingPower is BandEquivalenceHoppingPower
        assert Periodic1DRank2HoppingPower.__module__ == (
            "ksdft2effmass.periodic1d.rank2.hopping_locality.result"
        )
