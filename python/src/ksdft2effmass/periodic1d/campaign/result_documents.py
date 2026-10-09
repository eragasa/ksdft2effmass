"""Immutable versioned documents for retained Appendix G campaign results."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.serialization.json import (
    ImmutableJsonArray,
    ImmutableJsonCodec,
    ImmutableJsonObject,
    ImmutableJsonValue,
)


class Periodic1DEncodedResultKind(StrEnum):
    """Identify each demonstrated Appendix G encoded result wire.

    Members are explicit decoder discriminators. They do not imply source-file
    presence, provenance, decoded correctness, convergence, scientific validation,
    uncertainty quantification, or acceptance. Historical wire values remain unchanged.
    """

    ISOLATED_BAND = "isolated_band"
    STRESS = "stress"
    COMPOSITE = "composite"
    WANNIER90 = "wannier90"
    WANNIER90_PRECONDITIONED = "wannier90_preconditioned"
    WANNIER90_CONVERGENCE_ATTEMPT = "wannier90_convergence_attempt"


@dataclass(frozen=True, slots=True)
class Periodic1DEncodedResultDocument:
    """Retain one decoded result tree with its exact encoded source bytes.

    Parameters
    ----------
    kind
        Explicit supported wire discriminator.
    schema_version, record_id, evidence_status, calculation_status
        Decoded top-level wire fields retained for typed routing and correlation.
    root
        Complete immutable decoded JSON tree.
    source_document
        Exact nonempty built-in source bytes supplied to the decoder.
    source_sha256
        Lowercase SHA-256 identity derived from ``source_document``.

    Raises
    ------
    TypeError
        If a field has an unsupported exact representation.
    ValueError
        If version, identity, source bytes, digest correlation, or root correlation is
        invalid.

    Notes
    -----
    This supporting document is not a physical model, represented operator, scientific
    result, provenance proof, convergence result, uncertainty statement, or acceptance
    decision. The explicit kind assigns wire routing only.
    """

    kind: Periodic1DEncodedResultKind
    schema_version: int
    record_id: str
    evidence_status: str
    calculation_status: str | None
    root: ImmutableJsonObject
    source_document: bytes
    source_sha256: str

    def __post_init__(self) -> None:
        """Validate intrinsic fields, exact source identity, and root correlation."""
        self._check_args_record()
        self._check_args_source()
        self._check_args_root()

    def _check_args_record(self) -> None:
        """Validate the explicit wire kind and retained routing fields."""
        if type(self.kind) is not Periodic1DEncodedResultKind:
            raise TypeError("kind must be Periodic1DEncodedResultKind")
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in int")
        if self.schema_version != 1:
            raise ValueError("schema_version must be one")
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
        if type(self.root) is not ImmutableJsonObject:
            raise TypeError("root must be ImmutableJsonObject")

    def _check_args_source(self) -> None:
        """Validate exact source bytes and their declared content identity."""
        if type(self.source_document) is not bytes:
            raise TypeError("source_document must be exact bytes")
        if not self.source_document:
            raise ValueError("source_document must be nonempty")
        if type(self.source_sha256) is not str:
            raise TypeError("source_sha256 must be a built-in str")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")
        if hashlib.sha256(self.source_document).hexdigest() != self.source_sha256:
            raise ValueError("source_sha256 must identify source_document")

    def _check_args_root(self) -> None:
        """Correlate the complete decoded source tree with retained routing fields."""
        source_root = ImmutableJsonCodec().deserialize(self.source_document)
        if source_root != self.root:
            raise ValueError("root must be the complete decoding of source_document")
        if self.root.field("schema_version") != self.schema_version:
            raise ValueError("root schema version must match the retained record")
        id_field = (
            "execution_id"
            if self.kind is Periodic1DEncodedResultKind.WANNIER90_CONVERGENCE_ATTEMPT
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


class Periodic1DEncodedResultJsonSerializer(
    JsonCodec[Periodic1DEncodedResultDocument, bytes]
):
    """Decode exact result bytes and emit their canonical JSON representation.

    The configured kind is an explicit wire discriminator supplied by the caller; it is
    not inferred from a filename, path, identifier, or payload shape.
    """

    __slots__ = ("_immutable_codec", "_kind")

    def __init__(self, kind: Periodic1DEncodedResultKind) -> None:
        """Bind one exact supported wire kind.

        Parameters
        ----------
        kind
            Explicit wire discriminator; it is never inferred from payload content.

        Raises
        ------
        TypeError
            If ``kind`` is not exactly :class:`Periodic1DEncodedResultKind`.
        """
        if type(kind) is not Periodic1DEncodedResultKind:
            raise TypeError("kind must be Periodic1DEncodedResultKind")
        self._kind = kind
        self._immutable_codec = ImmutableJsonCodec()

    @property
    def kind(self) -> Periodic1DEncodedResultKind:
        """Return the read-only explicit result-wire kind."""
        return self._kind

    def deserialize(self, payload: bytes) -> Periodic1DEncodedResultDocument:
        """Decode one complete result without interpreting scientific validity.

        Parameters
        ----------
        payload
            Exact nonempty UTF-8 JSON bytes for the configured wire kind.

        Returns
        -------
        Periodic1DEncodedResultDocument
            Immutable complete tree, routing fields, exact source bytes, and derived
            SHA-256 content identity.

        Raises
        ------
        TypeError
            If the byte representation or a required field has an unsupported exact
            type.
        ValueError
            If JSON is malformed, ambiguous, nonfinite, missing required content, or
            has an unsupported schema version or invalid intrinsic correlation.
        UnicodeDecodeError
            If ``payload`` is not valid UTF-8.
        OverflowError
            If a decoded integer cannot be represented by a required binary64 field.
        """
        kind = self.kind
        root = self._immutable_codec.deserialize(payload)
        schema_version = self.integer(root.field("schema_version"), "schema_version")
        if schema_version != 1:
            raise ValueError("unsupported retained result schema version")
        id_field = (
            "execution_id"
            if kind is Periodic1DEncodedResultKind.WANNIER90_CONVERGENCE_ATTEMPT
            else "experiment_id"
        )
        record_id = self.string(root.field(id_field), id_field)
        evidence_status = self.string(root.field("evidence_status"), "evidence_status")
        root_keys = tuple(field[0] for field in root.fields)
        calculation_value = (
            root.field("calculation_status")
            if "calculation_status" in root_keys
            else None
        )
        calculation_status = (
            None
            if calculation_value is None
            else self.string(calculation_value, "calculation_status")
        )
        return Periodic1DEncodedResultDocument(
            kind,
            schema_version,
            record_id,
            evidence_status,
            calculation_status,
            root,
            payload,
            hashlib.sha256(payload).hexdigest(),
        )

    def serialize(self, value: Periodic1DEncodedResultDocument) -> bytes:
        """Encode one retained document as canonical newline-terminated JSON.

        Parameters
        ----------
        value
            Exact immutable result document for this serializer's configured kind.

        Returns
        -------
        bytes
            Deterministic canonical JSON. These bytes need not equal a noncanonical
            retained source wire.

        Raises
        ------
        TypeError
            If ``value`` is not exactly :class:`Periodic1DEncodedResultDocument`.
        ValueError
            If the document's explicit kind differs from the configured kind.
        """
        if type(value) is not Periodic1DEncodedResultDocument:
            raise TypeError("value must be Periodic1DEncodedResultDocument")
        if value.kind is not self.kind:
            raise ValueError("value kind must match the serializer kind")
        return self._immutable_codec.serialize(value.root)

    def object(self, value: ImmutableJsonValue, name: str) -> ImmutableJsonObject:
        """Return one exact immutable JSON object.

        Parameters
        ----------
        value
            Candidate closed JSON value.
        name
            Field name used in diagnostics.

        Returns
        -------
        ImmutableJsonObject
            The unchanged immutable object.

        Raises
        ------
        TypeError
            If ``value`` is not exactly :class:`ImmutableJsonObject`.
        """
        if type(value) is not ImmutableJsonObject:
            raise TypeError(f"{name} must be an immutable JSON object")
        return value

    def array(self, value: ImmutableJsonValue, name: str) -> ImmutableJsonArray:
        """Return one exact immutable JSON array.

        Parameters
        ----------
        value
            Candidate closed JSON value.
        name
            Field name used in diagnostics.

        Returns
        -------
        ImmutableJsonArray
            The unchanged immutable array.

        Raises
        ------
        TypeError
            If ``value`` is not exactly :class:`ImmutableJsonArray`.
        """
        if type(value) is not ImmutableJsonArray:
            raise TypeError(f"{name} must be an immutable JSON array")
        return value

    def string(self, value: ImmutableJsonValue, name: str) -> str:
        """Return one exact JSON string value.

        Parameters
        ----------
        value
            Candidate closed JSON value.
        name
            Field name used in diagnostics.

        Returns
        -------
        str
            The unchanged built-in string.

        Raises
        ------
        TypeError
            If ``value`` is not an exact built-in string.
        """
        if type(value) is not str:
            raise TypeError(f"{name} must be a JSON string")
        return value

    def integer(self, value: ImmutableJsonValue, name: str) -> int:
        """Return one exact JSON integer value while rejecting booleans.

        Parameters
        ----------
        value
            Candidate closed JSON value.
        name
            Field name used in diagnostics.

        Returns
        -------
        int
            The unchanged built-in integer.

        Raises
        ------
        TypeError
            If ``value`` is not an exact built-in integer.
        """
        if type(value) is not int:
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def real(self, value: ImmutableJsonValue, name: str) -> float:
        """Return one finite binary64 JSON real while rejecting booleans.

        Parameters
        ----------
        value
            Exact built-in integer or finite float.
        name
            Field name used in diagnostics.

        Returns
        -------
        float
            Finite binary64-compatible value.

        Raises
        ------
        TypeError
            If ``value`` is not an exact built-in integer or float.
        ValueError
            If a supplied float is nonfinite.
        OverflowError
            If an integer is outside the representable binary64 range.
        """
        if type(value) is int:
            converted = float(value)
        elif type(value) is float:
            converted = value
        else:
            raise TypeError(f"{name} must be a JSON real")
        if not np.isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    def boolean(self, value: ImmutableJsonValue, name: str) -> bool:
        """Return one exact JSON boolean value.

        Parameters
        ----------
        value
            Candidate closed JSON value.
        name
            Field name used in diagnostics.

        Returns
        -------
        bool
            The unchanged built-in Boolean.

        Raises
        ------
        TypeError
            If ``value`` is not an exact built-in Boolean.
        """
        if type(value) is not bool:
            raise TypeError(f"{name} must be a JSON boolean")
        return value

    def object_field(
        self, value: ImmutableJsonObject, name: str
    ) -> ImmutableJsonObject:
        """Return one named immutable object field.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        ImmutableJsonObject
            The named immutable object.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an immutable object.
        """
        return self.object(value.field(name), name)

    def object_array_field(
        self, value: ImmutableJsonObject, name: str
    ) -> tuple[ImmutableJsonObject, ...]:
        """Return one named array whose values are immutable objects.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        tuple[ImmutableJsonObject, ...]
            Immutable object members in wire order.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an array or a member is not an object.
        """
        array = self.array(value.field(name), name)
        return tuple(
            self.object(item, f"{name}[{index}]")
            for index, item in enumerate(array.values)
        )

    def real_field(self, value: ImmutableJsonObject, name: str) -> float:
        """Return one named finite binary64-compatible real field.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        float
            Finite decoded real value.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an exact integer or float.
        ValueError
            If a float is nonfinite.
        OverflowError
            If an integer cannot be represented as finite binary64.
        """
        return self.real(value.field(name), name)

    def integer_field(self, value: ImmutableJsonObject, name: str) -> int:
        """Return one named exact integer field.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        int
            Exact integer value.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an exact built-in integer.
        """
        return self.integer(value.field(name), name)

    def string_field(self, value: ImmutableJsonObject, name: str) -> str:
        """Return one named exact string field.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        str
            Exact string value.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an exact built-in string.
        """
        return self.string(value.field(name), name)

    def boolean_field(self, value: ImmutableJsonObject, name: str) -> bool:
        """Return one named exact Boolean field.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        bool
            Exact Boolean value.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an exact built-in Boolean.
        """
        return self.boolean(value.field(name), name)

    def real_vector_field(
        self, value: ImmutableJsonObject, name: str
    ) -> npt.NDArray[np.float64]:
        """Return one named JSON real array as binary64 values.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        numpy.ndarray
            Dense one-dimensional binary64 array in wire order.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an array or a member is not numeric.
        ValueError
            If a floating member is nonfinite.
        OverflowError
            If an integer member cannot be represented as finite binary64.
        MemoryError
            If dense array storage cannot be allocated.
        """
        array = self.array(value.field(name), name)
        return np.asarray(
            [
                self.real(item, f"{name}[{index}]")
                for index, item in enumerate(array.values)
            ],
            dtype=np.float64,
        )

    def integer_tuple_field(
        self, value: ImmutableJsonObject, name: str
    ) -> tuple[int, ...]:
        """Return one named JSON integer array as an immutable tuple.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        tuple[int, ...]
            Exact integer members in wire order.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If the field is not an array or a member is not an exact integer.
        """
        array = self.array(value.field(name), name)
        return tuple(
            self.integer(item, f"{name}[{index}]")
            for index, item in enumerate(array.values)
        )

    def complex_vector_field(
        self, value: ImmutableJsonObject, name: str
    ) -> npt.NDArray[np.complex128]:
        """Return ``[real, imaginary]`` pairs as a complex128 vector.

        Parameters
        ----------
        value
            Immutable source object.
        name
            Exact field name.

        Returns
        -------
        numpy.ndarray
            Dense one-dimensional complex128 vector in wire order.

        Raises
        ------
        KeyError
            If the field is absent.
        TypeError
            If arrays or numeric components have unsupported exact types.
        ValueError
            If a pair has the wrong length or a floating component is nonfinite.
        OverflowError
            If an integer component cannot be represented as finite binary64.
        MemoryError
            If dense complex128 storage cannot be allocated.
        """
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
        self, value: ImmutableJsonValue, name: str
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
        self, value: ImmutableJsonObject, name: str
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
        self, value: ImmutableJsonObject, name: str
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
