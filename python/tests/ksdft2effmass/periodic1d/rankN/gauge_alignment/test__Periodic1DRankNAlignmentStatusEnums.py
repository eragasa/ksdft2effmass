"""Tests for rank-N gauge-alignment status wire enums."""

from enum import Enum

import pytest

from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNGlobalUnitaryDownstreamApplicability,
)
from ksdft2effmass.serialization import StringWireEnum

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentStatusEnums:
    """Establish ordinary-enum identity and strict wire conversion."""

    def test__enums__use_the_shared_string_wire_boundary(self) -> None:
        for enum_type in (
            Periodic1DRankNAlignmentStatus,
            Periodic1DRankNGlobalUnitaryDownstreamApplicability,
            Periodic1DRankNAlignmentBackendExceptionCode,
        ):
            assert issubclass(enum_type, StringWireEnum)
            assert issubclass(enum_type, Enum)
            assert not issubclass(enum_type, str)

    def test__wire_conversion__round_trips_every_declared_value(self) -> None:
        for enum_type in (
            Periodic1DRankNAlignmentStatus,
            Periodic1DRankNGlobalUnitaryDownstreamApplicability,
            Periodic1DRankNAlignmentBackendExceptionCode,
        ):
            for value in enum_type:
                assert enum_type.from_wire(value.to_wire()) is value

    def test__wire_conversion__rejects_wrong_types_and_unknown_values(self) -> None:
        for enum_type in (
            Periodic1DRankNAlignmentStatus,
            Periodic1DRankNGlobalUnitaryDownstreamApplicability,
            Periodic1DRankNAlignmentBackendExceptionCode,
        ):
            with pytest.raises(TypeError, match="built-in string"):
                enum_type.from_wire(1)  # type: ignore[arg-type]
            with pytest.raises(ValueError, match="unsupported"):
                enum_type.from_wire("not-a-declared-value")
