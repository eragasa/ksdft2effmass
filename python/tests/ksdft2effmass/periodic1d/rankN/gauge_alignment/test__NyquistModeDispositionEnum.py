"""Tests for the typed odd-mesh Nyquist-mode wire boundary."""

from enum import Enum

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment.nyquist import (
    NyquistModeDispositionEnum,
)
from ksdft2effmass.serialization import StringWireEnum

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestNyquistModeDispositionEnum:
    """Establish ordinary-enum identity and the closed wire inventory."""

    def test__enum__is_an_ordinary_string_wire_enum(self) -> None:
        assert issubclass(NyquistModeDispositionEnum, StringWireEnum)
        assert issubclass(NyquistModeDispositionEnum, Enum)
        assert not issubclass(NyquistModeDispositionEnum, str)

    def test__wire_conversion__round_trips_the_canonical_value(self) -> None:
        disposition = NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH

        wire_value = disposition.to_wire()

        assert wire_value == "absent-on-odd-mesh"
        assert NyquistModeDispositionEnum.from_wire(wire_value) is disposition

    def test__wire_conversion__rejects_wrong_types_and_old_value(self) -> None:
        with pytest.raises(TypeError, match="built-in string"):
            NyquistModeDispositionEnum.from_wire(1)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="unsupported"):
            NyquistModeDispositionEnum.from_wire("inapplicable-odd-centered-no-nyquist")
