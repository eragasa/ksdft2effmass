"""Authoritative ownership checks for the rank-two hopping-locality value."""

import pytest

from ksdft2effmass.periodic1d.rank2 import (
    hopping_locality as hopping_locality_namespace,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.result import (
    Periodic1DRank2HoppingPower,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.unit]


class TestPeriodic1DRank2HoppingPower:
    def test__band_equivalence_study__consumes_authoritative_value(self) -> None:
        assert Periodic1DRank2HoppingPower.__module__ == (
            "ksdft2effmass.periodic1d.rank2.hopping_locality.result"
        )

    def test__capability_package__is_an_inert_namespace(self) -> None:
        assert not hasattr(hopping_locality_namespace, "__all__")
        assert not hasattr(
            hopping_locality_namespace,
            "Periodic1DRank2HoppingPower",
        )
