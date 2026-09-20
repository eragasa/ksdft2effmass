"""Public abstract contracts for JSON serialization boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod


class JsonSerializer[RecordT, WireT: (str, bytes)](ABC):
    """Serialize one exact record type to one JSON wire representation type."""

    __slots__ = ()

    @abstractmethod
    def serialize(self, record: RecordT) -> WireT:
        """Return the JSON wire representation of ``record``."""


class JsonDeserializer[RecordT, WireT: (str, bytes)](ABC):
    """Deserialize one JSON wire representation to one exact record type."""

    __slots__ = ()

    @abstractmethod
    def deserialize(self, wire: WireT) -> RecordT:
        """Return the exact record represented by ``wire``."""


class JsonCodec[RecordT, WireT: (str, bytes)](
    JsonSerializer[RecordT, WireT],
    JsonDeserializer[RecordT, WireT],
    ABC,
):
    """Combine matching JSON serialization and deserialization contracts."""

    __slots__ = ()
