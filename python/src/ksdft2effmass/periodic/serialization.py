"""Canonical closed schema-version-1 JSON for periodic calculation records.

The serializer emits compact UTF-8 JSON with lexicographically sorted object
keys and exactly one final line feed.  It rejects duplicate and unknown keys,
nonstandard nonfinite constants, and malformed nested order representations.
Serialization changes no units, ordering, or scientific meaning.
"""

from __future__ import annotations

import json
import math
from dataclasses import fields
from typing import Any, ClassVar

from .records import PeriodicCalculationRecord, UnavailableReason


class PeriodicCalculationRecordJsonSerializer:
    """Serialize and reconstruct the closed periodic-record schema version 1.

    Attributes
    ----------
    SCHEMA_VERSION
        The only emitted and accepted schema version.
    """

    SCHEMA_VERSION: ClassVar[int] = 1
    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        field.name for field in fields(PeriodicCalculationRecord)
    )
    _VECTOR_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "direct_lattice_vectors",
            "reciprocal_lattice_vectors",
            "k_points",
        }
    )
    _SPECTRUM_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"eigenvalues", "occupations"}
    )
    _GRID_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"fft_grid", "fft_smooth", "fft_box"}
    )
    _UNAVAILABLE_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "absolute_energy_reference",
            "fermi_alignment_convention",
            "retained_subspace",
            "gauge",
            "phase_convention",
            "basis_identity",
            "spin_convention",
        }
    )

    def serialize(self, record: PeriodicCalculationRecord) -> str:
        """Return canonical schema-version-1 JSON text with a final line feed.

        Parameters
        ----------
        record
            Valid immutable periodic calculation record.

        Returns
        -------
        str
            Deterministic canonical JSON text.

        Raises
        ------
        TypeError
            If ``record`` has the wrong public type.
        """
        if not isinstance(record, PeriodicCalculationRecord):
            raise TypeError("record must be a PeriodicCalculationRecord")
        payload: dict[str, Any] = {}
        for field in fields(record):
            value = getattr(record, field.name)
            payload[field.name] = self._wire_value(value)
        return (
            json.dumps(
                payload,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        )

    def deserialize(self, text: str) -> PeriodicCalculationRecord:
        """Strictly reconstruct one immutable schema-version-1 record.

        Parameters
        ----------
        text
            JSON text with no byte-order mark.

        Returns
        -------
        PeriodicCalculationRecord
            Reconstructed record with all intrinsic invariants reapplied.

        Raises
        ------
        TypeError
            If ``text`` or decoded field semantic types are wrong.
        ValueError
            If JSON is malformed, duplicated, unknown, unsupported, nonfinite,
            or violates record invariants.
        """
        if type(text) is not str:
            raise TypeError("text must be a built-in str")
        if text.startswith("\ufeff"):
            raise ValueError("a JSON byte-order mark is prohibited")
        try:
            payload = json.loads(
                text,
                object_pairs_hook=self._unique_object,
                parse_constant=self._reject_constant,
            )
        except json.JSONDecodeError as error:
            raise ValueError("malformed periodic-calculation-record JSON") from error
        if type(payload) is not dict:
            raise TypeError("periodic calculation record must be a JSON object")
        missing = self._FIELDS - set(payload)
        unknown = set(payload) - self._FIELDS
        if missing:
            raise ValueError(f"record is missing fields: {sorted(missing)}")
        if unknown:
            raise ValueError(f"record has unknown fields: {sorted(unknown)}")
        data = dict(payload)
        if type(data["schema_version"]) is not int:
            raise TypeError("schema_version must be a JSON integer")
        if data["schema_version"] != self.SCHEMA_VERSION:
            raise ValueError("unsupported periodic calculation record schema version")
        for name in self._VECTOR_FIELDS:
            data[name] = self._vectors(data[name], name)
        data["species"] = self._species(data["species"])
        data["atoms"] = self._atoms(data["atoms"])
        data["k_point_weights"] = self._real_row(
            data["k_point_weights"], "k_point_weights"
        )
        for name in self._SPECTRUM_FIELDS:
            if data[name] is not None:
                data[name] = self._spectrum(data[name], name)
        if data["spin_channels"] is not None:
            data["spin_channels"] = self._string_tuple(
                data["spin_channels"], "spin_channels"
            )
        for name in self._GRID_FIELDS:
            data[name] = self._integer_tuple(data[name], name)
        for name in self._UNAVAILABLE_FIELDS:
            if type(data[name]) is not str:
                raise TypeError(f"{name} must be a JSON string enum")
            try:
                data[name] = UnavailableReason(data[name])
            except ValueError as error:
                raise ValueError(
                    f"unsupported unavailable reason for {name}"
                ) from error
        return PeriodicCalculationRecord(**data)

    @classmethod
    def _wire_value(cls, value: Any) -> Any:
        """Recursively map immutable tuple and enum state to JSON values."""
        if isinstance(value, UnavailableReason):
            return value.value
        if type(value) is tuple:
            return [cls._wire_value(item) for item in value]
        return value

    @staticmethod
    def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        """Build a JSON object while rejecting duplicate keys."""
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key!r}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(value: str) -> None:
        """Reject nonstandard NaN and infinity tokens accepted by ``json``."""
        raise ValueError(f"nonfinite JSON constant is prohibited: {value}")

    @staticmethod
    def _list(value: Any, context: str) -> list[Any]:
        """Require an exact decoded JSON array."""
        if type(value) is not list:
            raise TypeError(f"{context} must be a JSON array")
        return value

    @classmethod
    def _real(cls, value: Any, context: str) -> float:
        """Return one finite built-in float from a JSON real number."""
        if type(value) not in (int, float):
            raise TypeError(f"{context} must be a JSON real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{context} must be finite")
        return result

    @classmethod
    def _real_row(cls, value: Any, context: str) -> tuple[float, ...]:
        """Decode one ordered JSON array of finite real numbers."""
        return tuple(cls._real(item, context) for item in cls._list(value, context))

    @classmethod
    def _vectors(
        cls, value: Any, context: str
    ) -> tuple[tuple[float, float, float], ...]:
        """Decode ordered three-component vectors without reordering."""
        vectors: list[tuple[float, float, float]] = []
        for item in cls._list(value, context):
            row = cls._real_row(item, context)
            if len(row) != 3:
                raise ValueError(f"{context} vectors must have three components")
            vectors.append((row[0], row[1], row[2]))
        return tuple(vectors)

    @classmethod
    def _species(cls, value: Any) -> tuple[tuple[str, float, str], ...]:
        """Decode ordered species declarations."""
        result: list[tuple[str, float, str]] = []
        for item in cls._list(value, "species"):
            row = cls._list(item, "species declaration")
            if len(row) != 3 or type(row[0]) is not str or type(row[2]) is not str:
                raise TypeError("species declarations require [string, real, string]")
            result.append((row[0], cls._real(row[1], "species mass"), row[2]))
        return tuple(result)

    @classmethod
    def _atoms(
        cls, value: Any
    ) -> tuple[tuple[int, str, tuple[float, float, float]], ...]:
        """Decode ordered atom index, species reference, and position values."""
        result: list[tuple[int, str, tuple[float, float, float]]] = []
        for item in cls._list(value, "atoms"):
            row = cls._list(item, "atom declaration")
            if len(row) != 3 or type(row[0]) is not int or type(row[1]) is not str:
                raise TypeError("atom declarations require [integer, string, vector]")
            vectors = cls._vectors([row[2]], "atom position")
            result.append((row[0], row[1], vectors[0]))
        return tuple(result)

    @classmethod
    def _spectrum(cls, value: Any, context: str) -> tuple[tuple[float, ...], ...]:
        """Decode an ordered rectangular-candidate spectral array."""
        return tuple(cls._real_row(row, context) for row in cls._list(value, context))

    @classmethod
    def _string_tuple(cls, value: Any, context: str) -> tuple[str, ...]:
        """Decode an ordered JSON string array."""
        result = cls._list(value, context)
        if not all(type(item) is str for item in result):
            raise TypeError(f"{context} must contain JSON strings")
        return tuple(result)

    @classmethod
    def _integer_tuple(cls, value: Any, context: str) -> tuple[int, int, int]:
        """Decode exactly three built-in JSON integers."""
        result = cls._list(value, context)
        if len(result) != 3 or any(type(item) is not int for item in result):
            raise TypeError(f"{context} must contain three JSON integers")
        return (result[0], result[1], result[2])
