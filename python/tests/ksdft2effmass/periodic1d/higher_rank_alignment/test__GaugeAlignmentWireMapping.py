"""Tests for strict gauge-alignment wire conversion."""

from __future__ import annotations

from enum import Enum, auto

import pytest

from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.definition import (
    GaugeAlignmentWireMapping,
    Periodic1DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestGaugeAlignmentWireMapping:
    """Keep domain identities separate from canonical wire values."""

    def test__mapping__round_trips_the_descriptive_inventory(self) -> None:
        expected = {
            Periodic1DRankNGaugeAlignment.IDENTITY: "identity",
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY: "global-unitary",
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY: "pointwise-unitary",
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                "known-inverse-oracle"
            ),
        }

        for domain_value, wire_value in expected.items():
            assert GaugeAlignmentWireMapping.to_wire(domain_value) == wire_value
            assert GaugeAlignmentWireMapping.from_wire(wire_value) is domain_value

    def test__mapping__rejects_legacy_and_wrong_typed_values(self) -> None:
        class OtherEnum(Enum):
            IDENTITY = auto()

        with pytest.raises(TypeError, match="Periodic1DRankNGaugeAlignment"):
            GaugeAlignmentWireMapping.to_wire(OtherEnum.IDENTITY)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="built-in string"):
            GaugeAlignmentWireMapping.from_wire(1)  # type: ignore[arg-type]
        for legacy_value in ("A0", "A1", "A2", "A3"):
            with pytest.raises(ValueError, match="unsupported gauge alignment"):
                GaugeAlignmentWireMapping.from_wire(legacy_value)
