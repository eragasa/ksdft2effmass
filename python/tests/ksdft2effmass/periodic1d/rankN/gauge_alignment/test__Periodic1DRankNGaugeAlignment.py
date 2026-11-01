"""Tests for rank-N gauge-alignment domain identities and wire values."""

from __future__ import annotations

from enum import Enum

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.serialization import StringWireEnum

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNGaugeAlignment:
    """Establish ordinary-enum identity and strict stable wire conversion."""

    def test__enum__is_an_ordinary_string_wire_enum(self) -> None:
        assert issubclass(Periodic1DRankNGaugeAlignment, StringWireEnum)
        assert issubclass(Periodic1DRankNGaugeAlignment, Enum)
        assert not issubclass(Periodic1DRankNGaugeAlignment, str)

    def test__wire_conversion__round_trips_the_descriptive_inventory(self) -> None:
        expected = {
            Periodic1DRankNGaugeAlignment.IDENTITY: "identity",
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY: "global-unitary",
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY: "pointwise-unitary",
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                "known-inverse-oracle"
            ),
        }

        for domain_value, wire_value in expected.items():
            assert domain_value.to_wire() == wire_value
            assert Periodic1DRankNGaugeAlignment.from_wire(wire_value) is domain_value

    def test__wire_conversion__rejects_wrong_types_and_old_values(self) -> None:
        with pytest.raises(TypeError, match="built-in string"):
            Periodic1DRankNGaugeAlignment.from_wire(1)  # type: ignore[arg-type]
        for legacy_value in ("A0", "A1", "A2", "A3"):
            with pytest.raises(ValueError, match="unsupported"):
                Periodic1DRankNGaugeAlignment.from_wire(legacy_value)
