"""Software contracts for ordinary string-mapped Enum vocabularies."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Self, cast

import pytest

from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)

pytestmark = pytest.mark.software_verification


class ExampleStringWireEnum(StringWireEnum):
    """Provide a local closed vocabulary for base-class verification."""

    FIRST = "first"
    SECOND = "second"


@dataclass(frozen=True, slots=True)
class ExampleProbeRecord(BaseTypedRecord):
    """Exercise explicit enum conversion inside the common record pipeline."""

    probe: ExampleStringWireEnum

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"probe": self.probe.to_wire()}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"probe"}:
            raise ValueError("probe-record fields do not match")
        wire = values["probe"]
        if type(wire) is not str:
            raise TypeError("probe must decode to a built-in string")
        return cls(probe=ExampleStringWireEnum.from_wire(wire))


class TestStringWireEnum:
    """Establish ordinary-Enum inheritance and exact mapping conversion."""

    def test_subclass__remains_an_ordinary_enum_not_a_string(self) -> None:
        assert issubclass(ExampleStringWireEnum, Enum)
        assert not issubclass(ExampleStringWireEnum, str)
        assert not isinstance(ExampleStringWireEnum.FIRST, str)

    def test_mapping__round_trips_exact_built_in_strings(self) -> None:
        for member in ExampleStringWireEnum:
            wire = member.to_wire()
            assert type(wire) is str
            assert ExampleStringWireEnum.from_wire(wire) is member

    def test_base_typed_record__uses_explicit_enum_mapping_conversion(self) -> None:
        record = ExampleProbeRecord(probe=ExampleStringWireEnum.SECOND)

        assert record.to_dict() == {"probe": "second"}
        assert ExampleProbeRecord.from_dict(record.to_dict()) == record
        assert ExampleProbeRecord.from_json(record.to_json()) == record

    def test_from_wire__rejects_wrong_or_unknown_strings(self) -> None:
        with pytest.raises(TypeError, match="built-in string"):
            ExampleStringWireEnum.from_wire(cast(str, True))
        with pytest.raises(ValueError, match="ExampleStringWireEnum"):
            ExampleStringWireEnum.from_wire("unknown")

    def test_subclass__rejects_non_string_member_values_at_definition(self) -> None:
        with pytest.raises(TypeError, match="member values"):

            class InvalidIntegerWireEnum(StringWireEnum):
                """Attempt to define an invalid non-string vocabulary."""

                VALUE = 1
