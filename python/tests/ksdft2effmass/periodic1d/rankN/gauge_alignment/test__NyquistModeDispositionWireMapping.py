"""Tests for the typed odd-mesh Nyquist-mode wire boundary."""

from enum import Enum

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment import (
    NyquistModeDispositionEnum,
    NyquistModeDispositionWireMapping,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestNyquistModeDispositionWireMapping:
    """Establish domain/wire separation and the closed wire inventory."""

    def test__enum__is_not_a_string_subclass(self) -> None:
        assert issubclass(NyquistModeDispositionEnum, Enum)
        assert not issubclass(NyquistModeDispositionEnum, str)

    def test__mapping__round_trips_the_canonical_wire_value(self) -> None:
        disposition = NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH

        wire_value = NyquistModeDispositionWireMapping.to_wire(disposition)

        assert wire_value == "absent-on-odd-mesh"
        assert NyquistModeDispositionWireMapping.from_wire(wire_value) is disposition

    def test__mapping__rejects_wrong_types_and_old_wire_value(self) -> None:
        with pytest.raises(TypeError, match="NyquistModeDispositionEnum"):
            NyquistModeDispositionWireMapping.to_wire("absent-on-odd-mesh")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="built-in string"):
            NyquistModeDispositionWireMapping.from_wire(1)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="unsupported"):
            NyquistModeDispositionWireMapping.from_wire(
                "inapplicable-odd-centered-no-nyquist"
            )
