"""Immutable versioned documents for retained Appendix G campaign results."""

from __future__ import annotations

import builtins
import hashlib
import json
import warnings
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from ksdft2effmass.serialization import JsonCodec

from .serialization import Periodic1DCampaignJsonDecoder


class Periodic1DRetainedResultKind(StrEnum):
    """Identify each demonstrated Appendix G retained result format."""

    ISOLATED_BAND = "isolated_band"
    STRESS = "stress"
    COMPOSITE = "composite"
    WANNIER90 = "wannier90"
    WANNIER90_PRECONDITIONED = "wannier90_preconditioned"
    WANNIER90_CONVERGENCE_ATTEMPT = "wannier90_convergence_attempt"


@dataclass(frozen=True, slots=True)
class Periodic1DJsonArray:
    """Retain one immutable ordered JSON array."""

    values: tuple[Periodic1DJsonValue, ...]

    def __post_init__(self) -> None:
        """Require an exact immutable value tuple."""
        if not isinstance(self.values, tuple):
            raise TypeError("values must be a tuple")
        if any(
            item is not None
            and type(item) not in {bool, int, float, str, Periodic1DJsonArray}
            and type(item) is not Periodic1DJsonObject
            for item in self.values
        ):
            raise TypeError("every item must be an immutable JSON value")
        if any(type(item) is float and not np.isfinite(item) for item in self.values):
            raise ValueError("JSON real values must be finite")


@dataclass(frozen=True, slots=True)
class Periodic1DJsonObject:
    """Retain one immutable canonical string-keyed JSON object."""

    fields: tuple[tuple[str, Periodic1DJsonValue], ...]

    def __post_init__(self) -> None:
        """Require unique keys in canonical lexical order."""
        if not isinstance(self.fields, tuple):
            raise TypeError("fields must be a tuple")
        if any(
            not isinstance(field, tuple) or len(field) != 2 for field in self.fields
        ):
            raise TypeError("each field must be one key-value tuple")
        keys = tuple(field[0] for field in self.fields)
        if any(type(key) is not str for key in keys):
            raise TypeError("JSON object keys must be built-in strings")
        if keys != tuple(sorted(set(keys))):
            raise ValueError("JSON object keys must be unique and lexically ordered")
        values = tuple(field[1] for field in self.fields)
        if any(
            value is not None
            and type(value) not in {bool, int, float, str, Periodic1DJsonArray}
            and type(value) is not Periodic1DJsonObject
            for value in values
        ):
            raise TypeError("every field must contain an immutable JSON value")
        if any(type(value) is float and not np.isfinite(value) for value in values):
            raise ValueError("JSON real values must be finite")

    def field(self, name: str) -> Periodic1DJsonValue:
        """Return one named value or raise ``KeyError`` when it is absent."""
        if type(name) is not str:
            raise TypeError("name must be a built-in str")
        matches = tuple(value for key, value in self.fields if key == name)
        if not matches:
            raise KeyError(name)
        return matches[0]


type Periodic1DJsonScalar = None | bool | int | float | str
type Periodic1DJsonValue = (
    Periodic1DJsonScalar | Periodic1DJsonArray | Periodic1DJsonObject
)


@dataclass(frozen=True, slots=True)
class Periodic1DRetainedResultDocument:
    """Retain one complete immutable result document and its source identity."""

    kind: Periodic1DRetainedResultKind
    schema_version: int
    record_id: str
    evidence_status: str
    calculation_status: str | None
    root: Periodic1DJsonObject
    source_sha256: str

    def __post_init__(self) -> None:
        """Validate version, identity, root correlation, and SHA-256 syntax."""
        if type(self.kind) is not Periodic1DRetainedResultKind:
            raise TypeError("kind must be Periodic1DRetainedResultKind")
        if type(self.schema_version) is not int or self.schema_version != 1:
            raise ValueError("schema_version must be the built-in integer one")
        for name, value in (
            ("record_id", self.record_id),
            ("evidence_status", self.evidence_status),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if (
            self.calculation_status is not None
            and type(self.calculation_status) is not str
        ):
            raise TypeError("calculation_status must be a built-in str or None")
        if type(self.root) is not Periodic1DJsonObject:
            raise TypeError("root must be Periodic1DJsonObject")
        if (
            type(self.source_sha256) is not str
            or len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef" for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")
        if self.root.field("schema_version") != self.schema_version:
            raise ValueError("root schema version must match the retained record")
        id_field = (
            "execution_id"
            if self.kind is Periodic1DRetainedResultKind.WANNIER90_CONVERGENCE_ATTEMPT
            else "experiment_id"
        )
        if self.root.field(id_field) != self.record_id:
            raise ValueError("root identifier must match the retained record")
        if self.root.field("evidence_status") != self.evidence_status:
            raise ValueError("root evidence status must match the retained record")
        root_keys = tuple(field[0] for field in self.root.fields)
        root_calculation_status = (
            self.root.field("calculation_status")
            if "calculation_status" in root_keys
            else None
        )
        if root_calculation_status != self.calculation_status:
            raise ValueError("root calculation status must match the retained record")


class Periodic1DRetainedResultJsonSerializer(
    JsonCodec[Periodic1DRetainedResultDocument, bytes]
):
    """Decode retained result bytes and encode their canonical JSON representation."""

    __slots__ = ("kind",)

    decoder = Periodic1DCampaignJsonDecoder()

    def __init__(self, kind: Periodic1DRetainedResultKind) -> None:
        if type(kind) is not Periodic1DRetainedResultKind:
            raise TypeError("kind must be Periodic1DRetainedResultKind")
        self.kind = kind

    def deserialize(self, payload: bytes) -> Periodic1DRetainedResultDocument:
        """Decode one complete result without interpreting it as scientific validity."""
        kind = self.kind
        decoded = self.decoder.document(payload)
        schema_version = self.decoder.integer(
            decoded.get("schema_version"), "schema_version"
        )
        if schema_version != 1:
            raise ValueError("unsupported retained result schema version")
        id_field = (
            "execution_id"
            if kind is Periodic1DRetainedResultKind.WANNIER90_CONVERGENCE_ATTEMPT
            else "experiment_id"
        )
        record_id = self.decoder.string(decoded.get(id_field), id_field)
        evidence_status = self.decoder.string(
            decoded.get("evidence_status"), "evidence_status"
        )
        calculation_value = decoded.get("calculation_status")
        calculation_status = (
            None
            if calculation_value is None
            else self.decoder.string(calculation_value, "calculation_status")
        )
        return Periodic1DRetainedResultDocument(
            kind,
            schema_version,
            record_id,
            evidence_status,
            calculation_status,
            self.object_value(decoded, "root"),
            hashlib.sha256(payload).hexdigest(),
        )

    def serialize(self, value: Periodic1DRetainedResultDocument) -> bytes:
        """Encode one retained document as canonical newline-terminated JSON."""
        if type(value) is not Periodic1DRetainedResultDocument:
            raise TypeError("value must be Periodic1DRetainedResultDocument")
        if value.kind is not self.kind:
            raise ValueError("value kind must match the serializer kind")
        document = self.builtin_value(value.root)
        return (
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

    def decode(
        self,
        payload: bytes,
        kind: Periodic1DRetainedResultKind | None = None,
    ) -> Periodic1DRetainedResultDocument:
        """Deprecated compatibility alias for :meth:`deserialize`."""
        warnings.warn(
            "decode() is deprecated; use deserialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        if kind is not None and kind is not self.kind:
            raise ValueError("kind must match the serializer kind")
        return self.deserialize(payload)

    def encode(self, value: Periodic1DRetainedResultDocument) -> bytes:
        """Deprecated compatibility alias for :meth:`serialize`."""
        warnings.warn(
            "encode() is deprecated; use serialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.serialize(value)

    def object_value(self, value: object, name: str) -> Periodic1DJsonObject:
        """Convert one decoded string-keyed mapping to its immutable representation."""
        mapping = self.decoder.mapping(value, name)
        return Periodic1DJsonObject(
            tuple(
                (key, self.json_value(item, f"{name}.{key}"))
                for key, item in sorted(mapping.items())
            )
        )

    def json_value(self, value: object, name: str) -> Periodic1DJsonValue:
        """Convert one closed decoded JSON value to an immutable representation."""
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if type(value) is int:
            return self.decoder.integer(value, name)
        if type(value) is float:
            return self.decoder.real(value, name)
        if type(value) is str:
            return self.decoder.string(value, name)
        if isinstance(value, list):
            return Periodic1DJsonArray(
                tuple(
                    self.json_value(item, f"{name}[{index}]")
                    for index, item in enumerate(value)
                )
            )
        if isinstance(value, dict):
            return self.object_value(value, name)
        raise TypeError(f"{name} contains an unsupported JSON representation")

    def object(self, value: Periodic1DJsonValue, name: str) -> Periodic1DJsonObject:
        """Return one immutable JSON object value."""
        if type(value) is not Periodic1DJsonObject:
            raise TypeError(f"{name} must be an immutable JSON object")
        return value

    def array(self, value: Periodic1DJsonValue, name: str) -> Periodic1DJsonArray:
        """Return one immutable JSON array value."""
        if type(value) is not Periodic1DJsonArray:
            raise TypeError(f"{name} must be an immutable JSON array")
        return value

    def string(self, value: Periodic1DJsonValue, name: str) -> str:
        """Return one exact JSON string value."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a JSON string")
        return value

    def integer(self, value: Periodic1DJsonValue, name: str) -> int:
        """Return one exact JSON integer value while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def real(self, value: Periodic1DJsonValue, name: str) -> float:
        """Return one finite JSON real value while rejecting booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        converted = float(value)
        if not np.isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    def boolean(self, value: Periodic1DJsonValue, name: str) -> bool:
        """Return one exact JSON boolean value."""
        if type(value) is not bool:
            raise TypeError(f"{name} must be a JSON boolean")
        return value

    def object_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> Periodic1DJsonObject:
        """Return one named immutable object field."""
        return self.object(value.field(name), name)

    def object_array_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> tuple[Periodic1DJsonObject, ...]:
        """Return one named array whose values are immutable objects."""
        array = self.array(value.field(name), name)
        return tuple(
            self.object(item, f"{name}[{index}]")
            for index, item in enumerate(array.values)
        )

    def real_field(self, value: Periodic1DJsonObject, name: str) -> float:
        """Return one named finite real field."""
        return self.real(value.field(name), name)

    def integer_field(self, value: Periodic1DJsonObject, name: str) -> int:
        """Return one named integer field."""
        return self.integer(value.field(name), name)

    def string_field(self, value: Periodic1DJsonObject, name: str) -> str:
        """Return one named string field."""
        return self.string(value.field(name), name)

    def boolean_field(self, value: Periodic1DJsonObject, name: str) -> bool:
        """Return one named boolean field."""
        return self.boolean(value.field(name), name)

    def real_vector_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> npt.NDArray[np.float64]:
        """Return one named JSON real array as binary64 values."""
        array = self.array(value.field(name), name)
        return np.asarray(
            [
                self.real(item, f"{name}[{index}]")
                for index, item in enumerate(array.values)
            ],
            dtype=np.float64,
        )

    def integer_tuple_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> tuple[int, ...]:
        """Return one named JSON integer array as an immutable tuple."""
        array = self.array(value.field(name), name)
        return tuple(
            self.integer(item, f"{name}[{index}]")
            for index, item in enumerate(array.values)
        )

    def complex_vector_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> npt.NDArray[np.complex128]:
        """Return ``[real, imaginary]`` pairs as a complex128 vector."""
        array = self.array(value.field(name), name)
        values = np.empty(len(array.values), dtype=np.complex128)
        for index, item in enumerate(array.values):
            pair = self.array(item, f"{name}[{index}]")
            if len(pair.values) != 2:
                raise ValueError(
                    f"{name}[{index}] must contain real and imaginary parts"
                )
            values[index] = complex(
                self.real(pair.values[0], f"{name}[{index}].real"),
                self.real(pair.values[1], f"{name}[{index}].imaginary"),
            )
        return values

    def complex_matrix(
        self, value: Periodic1DJsonValue, name: str
    ) -> npt.NDArray[np.complex128]:
        """Return a rectangular matrix encoded as ``[real, imaginary]`` pairs.

        Parameters
        ----------
        value
            Immutable JSON array of nonempty rows and complex pairs.
        name
            Semantic field path used in exception messages.

        Returns
        -------
        numpy.ndarray
            Finite two-dimensional ``complex128`` matrix.
        """
        rows = self.array(value, name)
        if not rows.values:
            raise ValueError(f"{name} must contain at least one matrix row")
        decoded_rows: list[npt.NDArray[np.complex128]] = []
        column_count: int | None = None
        for row_index, row_value in enumerate(rows.values):
            row = self.array(row_value, f"{name}[{row_index}]")
            if not row.values:
                raise ValueError(f"{name}[{row_index}] must be nonempty")
            if column_count is None:
                column_count = len(row.values)
            elif len(row.values) != column_count:
                raise ValueError(f"{name} matrix rows must have equal lengths")
            decoded = np.empty(len(row.values), dtype=np.complex128)
            for column_index, item in enumerate(row.values):
                pair_name = f"{name}[{row_index}][{column_index}]"
                pair = self.array(item, pair_name)
                if len(pair.values) != 2:
                    raise ValueError(
                        f"{pair_name} must contain real and imaginary parts"
                    )
                decoded[column_index] = complex(
                    self.real(pair.values[0], f"{pair_name}.real"),
                    self.real(pair.values[1], f"{pair_name}.imaginary"),
                )
            decoded_rows.append(decoded)
        return np.asarray(decoded_rows, dtype=np.complex128)

    def complex_matrix_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> npt.NDArray[np.complex128]:
        """Return one named complex-matrix field as ``complex128`` values.

        Parameters
        ----------
        value
            Immutable object that owns the named field.
        name
            Field name and semantic path used in exception messages.

        Returns
        -------
        numpy.ndarray
            Finite rectangular complex matrix.
        """
        return self.complex_matrix(value.field(name), name)

    def complex_matrix_array_field(
        self, value: Periodic1DJsonObject, name: str
    ) -> tuple[npt.NDArray[np.complex128], ...]:
        """Return one named array of finite rectangular complex matrices.

        Parameters
        ----------
        value
            Immutable object that owns the named field.
        name
            Field name and semantic path used in exception messages.

        Returns
        -------
        tuple
            Nonempty ordered tuple of ``complex128`` matrices.
        """
        array = self.array(value.field(name), name)
        if not array.values:
            raise ValueError(f"{name} must contain at least one matrix")
        return tuple(
            self.complex_matrix(item, f"{name}[{index}]")
            for index, item in enumerate(array.values)
        )

    def builtin_value(self, value: Periodic1DJsonValue) -> builtins.object:
        """Convert one immutable JSON representation to built-in JSON values."""
        if type(value) is Periodic1DJsonArray:
            return [self.builtin_value(item) for item in value.values]
        if type(value) is Periodic1DJsonObject:
            return {key: self.builtin_value(item) for key, item in value.fields}
        if value is not None and type(value) not in {bool, int, float, str}:
            raise TypeError("value is not a supported immutable JSON representation")
        if type(value) is float and not np.isfinite(value):
            raise ValueError("JSON real values must be finite")
        return value
