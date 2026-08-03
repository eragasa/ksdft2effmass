r"""Strict versioned JSON text serialization for operator records.

``OperatorRecordJsonSerializer`` is the ActionObject that owns the public
schema-version-1 JSON text representation of finite operator records. The
serializer maps between :class:`~ksdft2effmass.operators.OperatorRecord` objects
and deterministic UTF-8-compatible JSON strings. It does not expose an
intermediate dictionary API as public contract. The language-neutral schema and
golden fixtures are maintained under ``specification/operator-record/v1``.
Serialization preserves represented values but performs no basis or gauge
alignment, unit conversion, physical interpretation, scientific validation,
uncertainty quantification, or Python/Rust conformance check.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, ClassVar

import numpy as np

from .records import Basis, EnergyReference, Geometry, OperatorRecord, StateSpace

type JsonObject = dict[str, Any]


class OperatorRecordJsonSerializer:
    """Serialize and deserialize schema-version-1 operator records as JSON text.

    The version-1 wire format stores a dense row-major matrix as nested JSON
    arrays. Each complex entry is encoded as ``[real, imaginary]`` with finite
    JSON numbers. The top-level object contains state-space, basis, geometry,
    energy-reference, and provenance metadata. All declared fields are required
    and unknown fields are rejected at every object level.

    The serializer is deterministic: serializing the same record produces the
    same JSON text, with sorted object keys and compact separators. Deserialization
    is strict and rejects malformed JSON, duplicate object keys, non-standard
    constants such as ``NaN`` and ``Infinity``, numeric strings, booleans where
    numbers are required, and invalid DataObject invariants. Exact deterministic
    round trips preserve all eight ``OperatorRecord`` fields. The public schema
    and fixtures are integration artifacts distinct from this runtime owner; no
    Rust implementation or cross-language conformance is implied.

    Attributes
    ----------
    SCHEMA_VERSION
        Integer schema version emitted and accepted by this serializer. The only
        supported value is ``1``.
    _TOP_LEVEL_FIELDS, _STATE_SPACE_FIELDS, _BASIS_FIELDS, _GEOMETRY_FIELDS,
    _ENERGY_REFERENCE_FIELDS
        Private class-owned frozen sets of required JSON object names. They are
        private because they are serializer implementation mechanics for the
        public schema-version-1 contract; they are immutable, deterministic,
        dimensionless, do not cache caller data, and do not affect scientific
        results except by enforcing the documented wire-format boundary.

    Examples
    --------
    >>> serializer = OperatorRecordJsonSerializer()
    >>> text = serializer.serialize(record)  # doctest: +SKIP
    >>> restored = serializer.deserialize(text)  # doctest: +SKIP
    >>> restored == record  # doctest: +SKIP
    True
    """

    SCHEMA_VERSION: ClassVar[int] = 1

    _TOP_LEVEL_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "schema_version",
            "identifier",
            "operator_kind",
            "matrix",
            "state_space",
            "basis",
            "geometry",
            "energy_reference",
            "provenance",
        }
    )
    _STATE_SPACE_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"identifier", "kind", "dimension"}
    )
    _BASIS_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"identifier", "kind", "ordering", "orthonormal"}
    )
    _GEOMETRY_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "system",
            "cell",
            "boundary_conditions",
            "coordinate_convention",
            "length_unit",
        }
    )
    _ENERGY_REFERENCE_FIELDS: ClassVar[frozenset[str]] = frozenset({"zero", "unit"})

    def serialize(self, record: OperatorRecord) -> str:
        """Return deterministic schema-version-1 JSON text for ``record``.

        Parameters
        ----------
        record
            Operator record to serialize. The record must already satisfy its
            DataObject invariants: finite square ``np.complex128`` matrix,
            dimension and basis consistency, orthonormal basis, finite geometry,
            and string-to-string provenance.

        Returns
        -------
        str
            Deterministic JSON text with sorted object keys, compact separators,
            schema version ``1``, row-major complex matrix entries, and finite
            numeric values only.

        Raises
        ------
        TypeError
            If ``record`` is not an :class:`OperatorRecord`.
        ValueError
            If a nonfinite numeric value is encountered while emitting JSON.
        """

        if not isinstance(record, OperatorRecord):
            msg = "serialize() requires an OperatorRecord"
            raise TypeError(msg)
        return json.dumps(
            self._record_to_payload(record),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )

    def deserialize(self, text: str) -> OperatorRecord:
        """Construct an :class:`OperatorRecord` from schema-version-1 JSON text.

        Parameters
        ----------
        text
            JSON text whose top-level value is an operator-record object.

        Returns
        -------
        OperatorRecord
            Reconstructed record. Intrinsic DataObject invariants are reapplied
            during construction.

        Raises
        ------
        TypeError
            If ``text`` is not a Python string, if JSON values have the wrong
            type, or if numbers are provided as strings or booleans.
        ValueError
            If JSON is malformed, contains duplicate object keys or nonstandard
            constants, has missing or unknown fields, uses an unsupported schema
            version, encodes a malformed matrix, or violates any DataObject
            invariant.
        """

        if not isinstance(text, str):
            msg = "deserialize() requires JSON text as a string"
            raise TypeError(msg)
        try:
            payload = json.loads(
                text,
                object_pairs_hook=self._reject_duplicate_object_keys,
                parse_constant=self._reject_json_constant,
                parse_int=self._parse_json_integer_token,
            )
        except json.JSONDecodeError as exc:
            msg = "malformed operator-record JSON text"
            raise ValueError(msg) from exc
        if not isinstance(payload, dict):
            msg = "operator-record JSON text must contain a top-level object"
            raise TypeError(msg)
        return self._payload_to_record(payload)

    def _record_to_payload(self, record: OperatorRecord) -> JsonObject:
        """Convert an owned record into the public schema-version-1 object.

        Parameters
        ----------
        record
            Validated ``OperatorRecord`` to encode.

        Returns
        -------
        JsonObject
            Deterministically ordered JSON-compatible object containing only
            schema-version-1 fields.

        Notes
        -----
        This private method is serializer-owned mechanical encoding.  It does
        not define new scientific state, alter units, or perform numerical
        analysis; provenance ordering is deterministic for stable JSON text.
        """

        return {
            "schema_version": self.SCHEMA_VERSION,
            "identifier": record.identifier,
            "operator_kind": record.operator_kind,
            "matrix": self._serialize_matrix(record.matrix),
            "state_space": {
                "identifier": record.state_space.identifier,
                "kind": record.state_space.kind,
                "dimension": record.state_space.dimension,
            },
            "basis": {
                "identifier": record.basis.identifier,
                "kind": record.basis.kind,
                "ordering": list(record.basis.ordering),
                "orthonormal": record.basis.orthonormal,
            },
            "geometry": {
                "system": record.geometry.system,
                "cell": [list(vector) for vector in record.geometry.cell],
                "boundary_conditions": record.geometry.boundary_conditions,
                "coordinate_convention": record.geometry.coordinate_convention,
                "length_unit": record.geometry.length_unit,
            },
            "energy_reference": {
                "zero": record.energy_reference.zero,
                "unit": record.energy_reference.unit,
            },
            "provenance": {
                key: record.provenance[key] for key in sorted(record.provenance)
            },
        }

    def _payload_to_record(self, payload: JsonObject) -> OperatorRecord:
        """Validate a decoded schema-version-1 object and construct a record.

        Parameters
        ----------
        payload
            JSON object produced by the parser boundary. Values still have
            dynamic JSON types, so this private serializer-owned method routes
            every nested field through explicit wire validators before invoking
            public DataObject constructors.

        Returns
        -------
        OperatorRecord
            Immutable operator record reconstructed from the JSON text.

        Raises
        ------
        TypeError
            If a JSON value has the wrong semantic type, such as a string where
            an integer or real number is required.
        ValueError
            If required fields are missing, unknown fields are present, the
            schema version is unsupported, or nested DataObject invariants fail.
        """

        self._require_exact_fields(payload, self._TOP_LEVEL_FIELDS, "operator-record")
        version = self._require_json_integer(
            payload["schema_version"], "schema_version"
        )
        if version != self.SCHEMA_VERSION:
            msg = f"unsupported operator-record schema_version: {version!r}"
            raise ValueError(msg)

        state_space_payload = self._require_json_object(
            payload["state_space"], "state_space"
        )
        basis_payload = self._require_json_object(payload["basis"], "basis")
        geometry_payload = self._require_json_object(payload["geometry"], "geometry")
        energy_reference_payload = self._require_json_object(
            payload["energy_reference"], "energy_reference"
        )
        provenance_payload = self._require_json_object(
            payload["provenance"], "provenance"
        )

        self._require_exact_fields(
            state_space_payload, self._STATE_SPACE_FIELDS, "state_space"
        )
        self._require_exact_fields(basis_payload, self._BASIS_FIELDS, "basis")
        self._require_exact_fields(geometry_payload, self._GEOMETRY_FIELDS, "geometry")
        self._require_exact_fields(
            energy_reference_payload,
            self._ENERGY_REFERENCE_FIELDS,
            "energy_reference",
        )

        return OperatorRecord(
            identifier=self._require_string(payload["identifier"], "identifier"),
            operator_kind=self._require_string(
                payload["operator_kind"], "operator_kind"
            ),
            matrix=self._deserialize_matrix(payload["matrix"]),
            state_space=StateSpace(
                identifier=self._require_string(
                    state_space_payload["identifier"], "state_space.identifier"
                ),
                kind=self._require_string(
                    state_space_payload["kind"], "state_space.kind"
                ),
                dimension=self._require_json_integer(
                    state_space_payload["dimension"], "state_space.dimension"
                ),
            ),
            basis=Basis(
                identifier=self._require_string(
                    basis_payload["identifier"], "basis.identifier"
                ),
                kind=self._require_string(basis_payload["kind"], "basis.kind"),
                ordering=self._deserialize_ordering(basis_payload["ordering"]),
                orthonormal=self._require_json_bool(
                    basis_payload["orthonormal"], "basis.orthonormal"
                ),
            ),
            geometry=Geometry(
                system=self._require_string(
                    geometry_payload["system"], "geometry.system"
                ),
                cell=self._deserialize_cell(geometry_payload["cell"]),
                boundary_conditions=self._require_string(
                    geometry_payload["boundary_conditions"],
                    "geometry.boundary_conditions",
                ),
                coordinate_convention=self._require_string(
                    geometry_payload["coordinate_convention"],
                    "geometry.coordinate_convention",
                ),
                length_unit=self._require_string(
                    geometry_payload["length_unit"], "geometry.length_unit"
                ),
            ),
            energy_reference=EnergyReference(
                zero=self._require_string(
                    energy_reference_payload["zero"], "energy_reference.zero"
                ),
                unit=self._require_string(
                    energy_reference_payload["unit"], "energy_reference.unit"
                ),
            ),
            provenance=self._deserialize_provenance(provenance_payload),
        )

    def _serialize_matrix(self, matrix: np.ndarray) -> list[list[list[float]]]:
        """Serialize a finite matrix into row-major complex pairs.

        Parameters
        ----------
        matrix
            Canonical finite complex matrix from ``OperatorRecord``.

        Returns
        -------
        list[list[list[float]]]
            Row-major ``[real, imaginary]`` pairs using built-in floats.

        Raises
        ------
        ValueError
            If matrix entries are nonfinite.

        Notes
        -----
        The method is private because complex-pair encoding is a mechanical
        detail of the serializer's public JSON text contract.
        """

        if not np.all(np.isfinite(matrix)):
            msg = "operator matrix entries must be finite"
            raise ValueError(msg)
        return [
            [[float(value.real), float(value.imag)] for value in row]
            for row in matrix.tolist()
        ]

    def _deserialize_matrix(self, value: Any) -> np.ndarray:
        """Decode row-major complex pairs and reject invalid matrix encodings.

        Parameters
        ----------
        value
            JSON value for the ``matrix`` field. It must be an array of rows,
            each row an array of ``[real, imaginary]`` finite JSON-number pairs.

        Returns
        -------
        numpy.ndarray
            Dense ``np.complex128`` matrix candidate for ``OperatorRecord``
            validation.

        Raises
        ------
        TypeError
            If matrix or row containers are not JSON arrays or components are
            not JSON real numbers.
        ValueError
            If entries are not length-two complex pairs, rows are ragged, the
            matrix is empty, or numeric components are nonfinite.

        Notes
        -----
        This private serializer method owns only wire decoding. Squareness,
        dimension matching, and finiteness are completed by ``OperatorRecord``.
        """

        if not isinstance(value, list):
            msg = "complex matrix encoding must be a JSON array of rows"
            raise TypeError(msg)
        rows: list[list[complex]] = []
        row_length: int | None = None
        for row in value:
            if not isinstance(row, list):
                msg = "complex matrix rows must be JSON arrays"
                raise TypeError(msg)
            decoded_row: list[complex] = []
            for entry in row:
                if not isinstance(entry, list) or len(entry) != 2:
                    msg = "complex matrix entries must be [real, imaginary] pairs"
                    raise ValueError(msg)
                real = self._require_json_real(entry[0], "complex real component")
                imaginary = self._require_json_real(
                    entry[1], "complex imaginary component"
                )
                decoded_row.append(complex(real, imaginary))
            if row_length is None:
                row_length = len(decoded_row)
            elif len(decoded_row) != row_length:
                msg = "complex matrix rows must not be ragged"
                raise ValueError(msg)
            rows.append(decoded_row)
        if not rows or row_length == 0:
            msg = "complex matrix must not be empty"
            raise ValueError(msg)
        return np.array(rows, dtype=np.complex128)

    def _deserialize_ordering(self, value: Any) -> tuple[str, ...]:
        """Decode basis-label ordering from a JSON array.

        Parameters
        ----------
        value
            JSON value for ``basis.ordering``. It must be an array of nonempty
            strings.

        Returns
        -------
        tuple[str, ...]
            Immutable label tuple preserving JSON order.

        Raises
        ------
        TypeError
            If ``value`` is not a JSON array or any label is not a string.
        ValueError
            If any label is empty. Duplicate-label validation is completed by
            ``Basis``.

        Notes
        -----
        This private mechanical decoder is owned by the serializer because it
        enforces the version-1 wire-format representation of an ordered basis.
        Numeric strings are labels, not numbers.
        """

        if not isinstance(value, list):
            msg = "basis ordering must be a JSON array of labels"
            raise TypeError(msg)
        return tuple(self._require_string(label, "basis label") for label in value)

    def _deserialize_cell(self, value: Any) -> tuple[tuple[float, float, float], ...]:
        """Decode row lattice vectors from the JSON geometry cell field.

        Parameters
        ----------
        value
            JSON value for ``geometry.cell``. It must be an array of row arrays
            with three finite JSON real-number components each.

        Returns
        -------
        tuple[tuple[float, float, float], ...]
            Immutable row-vector tuple for ``Geometry`` construction.

        Raises
        ------
        TypeError
            If the cell or any row is not a JSON array or a component is not a
            JSON real number.
        ValueError
            If a row does not have exactly three components or a component is
            nonfinite.

        Notes
        -----
        The method is private because it is serializer-owned schema mechanics.
        The full 3x3 shape and linear-independence invariants are completed by
        ``Geometry``.
        """

        if not isinstance(value, list):
            msg = "geometry cell must be a JSON array of row vectors"
            raise TypeError(msg)
        rows: list[tuple[float, float, float]] = []
        for row in value:
            if not isinstance(row, list):
                msg = "geometry cell rows must be JSON arrays"
                raise TypeError(msg)
            if len(row) != 3:
                msg = "geometry cell rows must have three components"
                raise ValueError(msg)
            rows.append(
                (
                    self._require_json_real(row[0], "geometry cell component"),
                    self._require_json_real(row[1], "geometry cell component"),
                    self._require_json_real(row[2], "geometry cell component"),
                )
            )
        return tuple(rows)

    def _deserialize_provenance(self, payload: JsonObject) -> dict[str, str]:
        """Decode the compact string-to-string provenance mapping.

        Parameters
        ----------
        payload
            JSON object used as the provenance mapping. Keys and values must be
            nonempty strings.

        Returns
        -------
        dict[str, str]
            Fresh mutable dictionary passed immediately to ``OperatorRecord``,
            which performs defensive immutable copying.

        Raises
        ------
        TypeError
            If any provenance key or value is not a string.
        ValueError
            If any provenance key or value is empty.

        Notes
        -----
        This private serializer method preserves provenance as public metadata
        while keeping serializer wire validation separate from record storage.
        """

        return {
            self._require_string(key, "provenance key"): self._require_string(
                value, "provenance value"
            )
            for key, value in payload.items()
        }

    def _require_exact_fields(
        self, payload: Mapping[str, Any], required: frozenset[str], name: str
    ) -> None:
        """Enforce required and additional-field schema object constraints.

        Parameters
        ----------
        payload
            Decoded JSON object whose keys are validated.
        required
            Exact field-name set for the schema-version-1 object level.
        name
            Diagnostic object name.

        Raises
        ------
        ValueError
            If any required field is missing or any unknown field is present.

        Notes
        -----
        This private method protects deterministic wire-format invariants; it
        does not validate scientific values stored in accepted fields.
        """

        keys = set(payload)
        missing = required.difference(keys)
        if missing:
            msg = f"{name} payload missing required fields: {sorted(missing)}"
            raise ValueError(msg)
        unknown = keys.difference(required)
        if unknown:
            msg = f"{name} payload has unknown fields: {sorted(unknown)}"
            raise ValueError(msg)

    def _require_json_object(self, value: Any, name: str) -> JsonObject:
        """Return a decoded JSON object after semantic type validation.

        Parameters
        ----------
        value
            Candidate JSON value.
        name
            Diagnostic object name.

        Returns
        -------
        JsonObject
            Dictionary representing a JSON object.

        Raises
        ------
        TypeError
            If ``value`` is not a JSON object. Arrays, strings, numbers,
            booleans, and null are rejected because version-1 nested records are
            JSON objects.

        Notes
        -----
        This private owner-local method isolates dynamic JSON parser values at
        the serializer boundary before DataObject construction.
        """

        if not isinstance(value, dict):
            msg = f"{name} payload must be a JSON object"
            raise TypeError(msg)
        return value

    def _require_json_integer(self, value: Any, name: str) -> int:
        """Return a JSON integer while rejecting booleans and numeric strings.

        Parameters
        ----------
        value
            Candidate JSON integer value. Only exact Python ``int`` produced by
            the JSON parser is accepted.
        name
            Diagnostic field name.

        Returns
        -------
        int
            Accepted JSON integer.

        Raises
        ------
        TypeError
            If ``value`` is Boolean, float, string, null, array, or object.

        Notes
        -----
        ``type(value) is int`` is intentional because ``bool`` is a Python
        subclass of ``int`` but has different JSON semantics. The method is
        private because integer admission is wire-format policy owned by the
        serializer, not a domain DataObject invariant.
        """

        if type(value) is not int:
            msg = f"{name} must be a JSON integer"
            raise TypeError(msg)
        return value

    def _require_json_real(self, value: Any, name: str) -> float:
        """Return a canonical finite real component from JSON numeric input.

        Parameters
        ----------
        value
            Candidate JSON number. Integers and floats are accepted; booleans,
            strings, null, arrays, and objects are rejected.
        name
            Diagnostic field name.

        Returns
        -------
        float
            Built-in finite float at the JSON/Python boundary.

        Raises
        ------
        TypeError
            If ``value`` is not a JSON integer or float with real semantics.
        ValueError
            If conversion overflows or is nonfinite. Nonstandard JSON constants
            are rejected earlier by ``_reject_json_constant``.

        Notes
        -----
        This private owner-local method keeps JSON numeric admission separate
        from DataObject scalar validation and documents the finite-number wire
        contract.
        """

        if type(value) not in (int, float):
            msg = f"{name} must be a JSON real number"
            raise TypeError(msg)
        try:
            real = float(value)
        except OverflowError as exc:
            msg = f"{name} must be finite"
            raise ValueError(msg) from exc
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real

    def _require_json_bool(self, value: Any, name: str) -> bool:
        """Return a JSON boolean for fields with explicit Boolean semantics.

        Parameters
        ----------
        value
            Candidate JSON Boolean value.
        name
            Diagnostic field name.

        Returns
        -------
        bool
            Accepted JSON Boolean.

        Raises
        ------
        TypeError
            If ``value`` is not exactly a Python ``bool`` from JSON parsing.

        Notes
        -----
        This private serializer check rejects integers and strings so schema
        version 1 does not silently reinterpret non-Boolean values. It is
        private because Boolean admission is wire-format policy owned by the
        serializer.
        """

        if type(value) is not bool:
            msg = f"{name} must be a JSON boolean"
            raise TypeError(msg)
        return value

    def _require_string(self, value: Any, name: str) -> str:
        """Return a nonempty string from a JSON metadata boundary.

        Parameters
        ----------
        value
            Candidate JSON string value.
        name
            Diagnostic field name.

        Returns
        -------
        str
            Nonempty string without numeric interpretation.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        The method is private serializer mechanics and does not convert numeric
        JSON values to labels. It is owner-local because JSON string admission is
        serializer wire policy, while DataObjects revalidate stored strings.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)
        return value

    def _reject_duplicate_object_keys(self, pairs: list[tuple[str, Any]]) -> JsonObject:
        """Reject duplicate JSON object names before Python dict collapsing.

        Parameters
        ----------
        pairs
            Parser-supplied key/value sequence preserving duplicate names.

        Returns
        -------
        JsonObject
            JSON object with unique keys in parser order.

        Raises
        ------
        ValueError
            If a duplicate key is encountered.

        Notes
        -----
        This private callback is owned by the serializer because duplicate-key
        rejection is a JSON wire-format invariant that must happen before Python
        dictionary construction collapses repeated names.
        """

        result: JsonObject = {}
        for key, value in pairs:
            if key in result:
                msg = f"duplicate JSON object key: {key!r}"
                raise ValueError(msg)
            result[key] = value
        return result

    def _parse_json_integer_token(self, token: str) -> int:
        """Return a JSON integer token or reject implementation-overflow tokens.

        Parameters
        ----------
        token
            Decimal integer token supplied by :func:`json.loads` before Python
            integer construction.

        Returns
        -------
        int
            Python integer for normal-size JSON integer tokens.

        Raises
        ------
        ValueError
            If Python refuses to construct the integer, for example because the
            token exceeds the interpreter digit limit for safe integer parsing.

        Notes
        -----
        JSON has no infinity literal for integers, but schema-version-1 integer
        and real fields still require implementation-finite public values. This
        parser hook maps huge integer-token conversion failure to the public
        finite-number taxonomy instead of leaking interpreter diagnostics.
        """

        try:
            return int(token)
        except ValueError as exc:
            msg = "JSON integer must be finite"
            raise ValueError(msg) from exc

    def _reject_json_constant(self, constant: str) -> None:
        """Reject nonstandard JSON numeric constants accepted by ``json``.

        Parameters
        ----------
        constant
            Parser-supplied token such as ``NaN``, ``Infinity``, or
            ``-Infinity``.

        Raises
        ------
        ValueError
            Always, because schema version 1 admits only standard finite JSON
            numbers.

        Notes
        -----
        This private method is an externally required ``json.loads`` callback
        and is therefore one of the few ownerless-callable boundaries permitted
        by the architecture policy.
        """

        msg = f"nonstandard JSON constant is not allowed: {constant}"
        raise ValueError(msg)
