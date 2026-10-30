"""Generic reversible conversion between typed scientific values and JSON values."""

from __future__ import annotations

import json
from collections.abc import Mapping
from enum import Enum
from types import MappingProxyType
from typing import Protocol, runtime_checkable

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.numerics.typing.scipy.sparse import SparseMatrix
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    ModelSystemQuantity,
    ModelSystemUnit,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from scipy import sparse  # type: ignore[import-untyped]

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


@runtime_checkable
class DictionaryRecord(Protocol):
    """Expose one record as a rich typed mapping."""

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the record's typed mapping without JSON normalization.

        Returns
        -------
        Mapping[str, SerializableValue]
            Domain-owned values retaining arrays, quantities, enums, and records.
        """
        ...


type SerializableScalar = None | bool | int | float | str | np.generic | Enum
type SerializableValue = (
    SerializableScalar
    | np.ndarray
    | SparseMatrix
    | ModelSystemUnit
    | ModelSystemQuantity
    | DictionaryRecord
    | list[SerializableValue]
    | tuple[SerializableValue, ...]
    | Mapping[str, SerializableValue]
)

_tag = "__ksd_type__"
_default_enum_registry: Mapping[str, type[Enum]] = MappingProxyType(
    {"matrix_norm": MatrixNormEnum}
)


class TypedJsonValueCodec:
    """Recursively encode and decode the closed scientific value inventory.

    NumPy support is limited to fixed-width integer, binary floating-point, and
    binary complex dtypes through 64-bit real components. Integer decoding rejects
    out-of-range JSON values rather than wrapping them. SciPy sparse inputs are
    reconstructed as canonical CSR arrays.
    """

    __slots__ = ("_enum_ids", "_enum_types")

    def __init__(
        self,
        enum_registry: Mapping[str, type[Enum]] | None = None,
    ) -> None:
        """Construct a codec with an explicit closed enum registry.

        Parameters
        ----------
        enum_registry
            Additional stable identifiers mapped to exact enum classes. The default
            registry contains the canonical PhysKit matrix-norm enum.

        Raises
        ------
        TypeError
            The registry, an identifier, or an enum class has the wrong type.
        ValueError
            An identifier or enum class is registered more than once.
        """
        registered = dict(_default_enum_registry)
        if enum_registry is not None:
            if not isinstance(enum_registry, Mapping):
                raise TypeError("enum_registry must be a mapping or None")
            for identifier, enum_type in enum_registry.items():
                if type(identifier) is not str or not identifier:
                    raise TypeError(
                        "enum registry identifiers must be nonempty strings"
                    )
                if not isinstance(enum_type, type) or not issubclass(enum_type, Enum):
                    raise TypeError("enum registry values must be Enum types")
                if identifier in registered and registered[identifier] is not enum_type:
                    raise ValueError("enum registry identifiers must be unique")
                registered[identifier] = enum_type
        if len(set(registered.values())) != len(registered):
            raise ValueError("each registered Enum type must have one identifier")
        self._enum_types = MappingProxyType(registered)
        self._enum_ids = MappingProxyType(
            {enum_type: identifier for identifier, enum_type in registered.items()}
        )

    def serialize_bytes(self, value: SerializableValue) -> bytes:
        """Serialize one supported scientific value to canonical JSON bytes.

        Parameters
        ----------
        value
            Value from the closed ``SerializableValue`` inventory.

        Returns
        -------
        bytes
            Sorted, indented UTF-8 JSON with a terminal newline.

        Raises
        ------
        TypeError
            The value type, mapping key, array dtype, or enum type is unsupported.
        ValueError
            The value is nonfinite, malformed, out of range, or uses reserved
            metadata.
        """
        json_value = self.serialize(value)
        return (
            json.dumps(
                json_value,
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

    def deserialize_bytes(self, wire: bytes) -> SerializableValue:
        """Reconstruct one typed scientific value from UTF-8 JSON bytes.

        Parameters
        ----------
        wire
            JSON bytes governed by this codec's closed type registry.

        Returns
        -------
        SerializableValue
            Reconstructed scalar, array, sparse value, quantity, enum, tuple, list,
            mapping, or nested record mapping.

        Raises
        ------
        TypeError
            ``wire`` or decoded metadata has the wrong type.
        ValueError
            JSON contains duplicate keys, nonstandard numeric constants, unknown
            tags, overflow, or malformed typed data.
        """
        if type(wire) is not bytes:
            raise TypeError("wire must be built-in bytes")

        def reject_constant(value: str) -> JsonValue:
            raise ValueError(f"nonstandard JSON numeric constant is forbidden: {value}")

        def reject_duplicate_keys(
            pairs: list[tuple[str, JsonValue]],
        ) -> dict[str, JsonValue]:
            result: dict[str, JsonValue] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON object key is forbidden: {key}")
                result[key] = value
            return result

        json_value: JsonValue = json.loads(
            wire.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
        return self.deserialize(json_value)

    def serialize(self, value: SerializableValue) -> JsonValue:
        """Normalize one typed scientific value to a reversible JSON value.

        Parameters
        ----------
        value
            Supported typed value. NumPy and sparse values retain explicit dtype,
            shape, and representation metadata.

        Returns
        -------
        JsonValue
            JSON-native scalar, list, or mapping with explicit type tags where
            reconstruction requires them.

        Raises
        ------
        TypeError
            The input lies outside the closed serializable inventory.
        ValueError
            The value violates finiteness, range, key, or structural requirements.
        """
        if value is None:
            return None
        if isinstance(value, bool) and type(value) is bool:
            return value
        if isinstance(value, int) and type(value) is int:
            return value
        if isinstance(value, str) and type(value) is str:
            return value
        if isinstance(value, float) and type(value) is float:
            if not np.isfinite(value):
                raise ValueError("floating values must be finite")
            return value
        if isinstance(value, Enum):
            identifier = self._enum_ids.get(type(value))
            if identifier is None:
                raise TypeError("enum type is not present in the closed registry")
            return {
                _tag: "enum",
                "enum_type": identifier,
                "member": value.name,
            }
        if isinstance(value, np.generic):
            return self._serialize_numpy_scalar(value)
        if isinstance(value, np.ndarray):
            return self._serialize_ndarray(value)
        if isinstance(value, sparse.spmatrix | sparse.sparray):
            return self._serialize_sparse(value)
        if isinstance(value, Unitless):
            return {_tag: "unitless"}
        if isinstance(value, PhysicalUnit):
            return {_tag: "physical_unit", "expression": value.expression}
        if isinstance(value, ScalarQuantity):
            return {
                _tag: "scalar_quantity",
                "magnitude": self.serialize(value.magnitude),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, VectorQuantity):
            return {
                _tag: "vector_quantity",
                "magnitude": self.serialize(value.magnitude),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, ComplexVectorQuantity):
            return {
                _tag: "complex_vector_quantity",
                "magnitude": self.serialize(value.magnitude),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, MatrixQuantity):
            return {
                _tag: "matrix_quantity",
                "magnitude": self.serialize(value.magnitude),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, ComplexMatrixQuantity):
            return {
                _tag: "complex_matrix_quantity",
                "magnitude": self.serialize(value.magnitude),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, SparseMatrixQuantity):
            return {
                _tag: "sparse_matrix_quantity",
                "data": self.serialize(value.data),
                "column_indices": self.serialize(value.column_indices),
                "row_offsets": self.serialize(value.row_offsets),
                "shape": self.serialize(value.shape),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, ComplexSparseMatrixQuantity):
            return {
                _tag: "complex_sparse_matrix_quantity",
                "data": self.serialize(value.data),
                "column_indices": self.serialize(value.column_indices),
                "row_offsets": self.serialize(value.row_offsets),
                "shape": self.serialize(value.shape),
                "unit": self.serialize(value.unit),
            }
        if isinstance(value, DictionaryRecord):
            return self.serialize(value.to_dict())
        if isinstance(value, tuple):
            return {
                _tag: "tuple",
                "items": [self.serialize(item) for item in value],
            }
        if isinstance(value, list):
            return [self.serialize(item) for item in value]
        if isinstance(value, Mapping):
            if not all(type(key) is str for key in value):
                raise TypeError("mapping keys must be built-in strings")
            if _tag in value:
                raise ValueError(f"mapping key {_tag!r} is reserved")
            return {key: self.serialize(item) for key, item in value.items()}
        raise TypeError(f"unsupported serializable value: {type(value).__qualname__}")

    def deserialize(self, value: JsonValue) -> SerializableValue:
        """Reconstruct a typed scientific value from normalized JSON data.

        Parameters
        ----------
        value
            JSON-native value containing codec-owned type metadata.

        Returns
        -------
        SerializableValue
            Reconstructed typed value with immutable numerical storage.

        Raises
        ------
        TypeError
            JSON metadata or reconstructed content has the wrong type.
        ValueError
            Tags, dimensions, dtypes, indices, units, enum members, or numeric ranges
            violate the closed contract.
        """
        if value is None or type(value) in (bool, int, str):
            return value
        if type(value) is float:
            if not np.isfinite(value):
                raise ValueError("floating values must be finite")
            return value
        if isinstance(value, list):
            return [self.deserialize(item) for item in value]
        if not isinstance(value, dict):
            raise TypeError("value must belong to the JsonValue inventory")
        tag = value.get(_tag)
        if tag is None:
            return {key: self.deserialize(item) for key, item in value.items()}
        if type(tag) is not str:
            raise TypeError("typed JSON tags must be built-in strings")
        if tag == "enum":
            self._require_keys(value, {_tag, "enum_type", "member"})
            enum_identifier = value["enum_type"]
            member = value["member"]
            if type(enum_identifier) is not str or type(member) is not str:
                raise TypeError("enum type and member metadata must be strings")
            enum_type = self._enum_types.get(enum_identifier)
            if enum_type is None:
                raise ValueError("enum type is not present in the closed registry")
            enum_value = enum_type.__members__.get(member)
            if enum_value is None:
                raise ValueError("enum member is not defined by its registered type")
            return enum_value
        if tag == "numpy_scalar":
            return self._deserialize_numpy_scalar(value)
        if tag == "numpy_array":
            return self._deserialize_ndarray(value)
        if tag == "scipy_csr_array":
            return self._deserialize_sparse(value)
        if tag == "unitless":
            self._require_keys(value, {_tag})
            return Unitless()
        if tag == "physical_unit":
            self._require_keys(value, {_tag, "expression"})
            expression = value["expression"]
            if type(expression) is not str:
                raise TypeError("physical-unit expression must be a string")
            return PhysicalUnit(expression)
        if tag == "tuple":
            self._require_keys(value, {_tag, "items"})
            items = value["items"]
            if not isinstance(items, list):
                raise TypeError("tuple items must be a JSON array")
            return tuple(self.deserialize(item) for item in items)
        if tag in {
            "scalar_quantity",
            "vector_quantity",
            "complex_vector_quantity",
            "matrix_quantity",
            "complex_matrix_quantity",
        }:
            self._require_keys(value, {_tag, "magnitude", "unit"})
            magnitude = self.deserialize(value["magnitude"])
            unit = self.deserialize(value["unit"])
            if not isinstance(unit, PhysicalUnit | Unitless):
                raise TypeError("quantity unit did not decode to a model-system unit")
            if tag == "scalar_quantity":
                if type(magnitude) is not float:
                    raise TypeError("scalar quantity magnitude must decode to float")
                return ScalarQuantity(magnitude, unit)
            if not isinstance(magnitude, np.ndarray):
                raise TypeError("quantity magnitude must decode to numpy.ndarray")
            if tag == "vector_quantity":
                return VectorQuantity(magnitude, unit)
            if tag == "complex_vector_quantity":
                return ComplexVectorQuantity(magnitude, unit)
            if tag == "matrix_quantity":
                return MatrixQuantity(magnitude, unit)
            return ComplexMatrixQuantity(magnitude, unit)
        if tag in {"sparse_matrix_quantity", "complex_sparse_matrix_quantity"}:
            self._require_keys(
                value,
                {
                    _tag,
                    "data",
                    "column_indices",
                    "row_offsets",
                    "shape",
                    "unit",
                },
            )
            data = self.deserialize(value["data"])
            column_indices = self.deserialize(value["column_indices"])
            row_offsets = self.deserialize(value["row_offsets"])
            shape = self.deserialize(value["shape"])
            unit = self.deserialize(value["unit"])
            if not isinstance(data, np.ndarray):
                raise TypeError("sparse quantity data must decode to numpy.ndarray")
            if not isinstance(column_indices, np.ndarray) or not isinstance(
                row_offsets, np.ndarray
            ):
                raise TypeError("sparse quantity indices must decode to arrays")
            if not (
                isinstance(shape, tuple)
                and len(shape) == 2
                and all(type(dimension) is int for dimension in shape)
            ):
                raise TypeError("sparse quantity shape must decode to integer pair")
            if not isinstance(unit, PhysicalUnit | Unitless):
                raise TypeError("sparse quantity unit must decode to a unit")
            if tag == "sparse_matrix_quantity":
                return SparseMatrixQuantity(
                    data=data,
                    column_indices=column_indices,
                    row_offsets=row_offsets,
                    shape=shape,
                    unit=unit,
                )
            return ComplexSparseMatrixQuantity(
                data=data,
                column_indices=column_indices,
                row_offsets=row_offsets,
                shape=shape,
                unit=unit,
            )
        raise ValueError(f"unknown typed JSON tag: {tag}")

    def _serialize_numpy_scalar(self, value: np.generic) -> dict[str, JsonValue]:
        self._validate_dtype(value.dtype)
        if value.dtype.kind == "c":
            represented = complex(value)
            if not np.isfinite(represented.real) or not np.isfinite(represented.imag):
                raise ValueError("complex NumPy scalar must be finite")
            data: JsonValue = {
                "real": represented.real,
                "imaginary": represented.imag,
            }
        elif value.dtype.kind == "f":
            represented_float = float(value)
            if not np.isfinite(represented_float):
                raise ValueError("floating NumPy scalar must be finite")
            data = represented_float
        else:
            data = int(value)
        return {
            _tag: "numpy_scalar",
            "dtype": value.dtype.str,
            "data": data,
        }

    def _serialize_ndarray(self, value: np.ndarray) -> dict[str, JsonValue]:
        self._validate_dtype(value.dtype)
        if value.dtype.kind == "c":
            if not np.all(np.isfinite(value.real)) or not np.all(
                np.isfinite(value.imag)
            ):
                raise ValueError("complex NumPy array must be finite")
            data: JsonValue = {
                "real": value.real.tolist(),
                "imaginary": value.imag.tolist(),
            }
        else:
            if value.dtype.kind == "f" and not np.all(np.isfinite(value)):
                raise ValueError("floating NumPy array must be finite")
            data = value.tolist()
        return {
            _tag: "numpy_array",
            "dtype": value.dtype.str,
            "shape": [int(dimension) for dimension in value.shape],
            "data": data,
        }

    def _serialize_sparse(self, value: SparseMatrix) -> dict[str, JsonValue]:
        if value.dtype.kind not in "iufc":
            raise TypeError(
                "sparse matrix must contain numeric data excluding booleans"
            )
        canonical = sparse.csr_array(value)
        canonical.sum_duplicates()
        canonical.eliminate_zeros()
        canonical.sort_indices()
        return {
            _tag: "scipy_csr_array",
            "data": self.serialize(np.asarray(canonical.data)),
            "indices": self.serialize(np.asarray(canonical.indices)),
            "indptr": self.serialize(np.asarray(canonical.indptr)),
            "shape": self.serialize((int(canonical.shape[0]), int(canonical.shape[1]))),
        }

    def _deserialize_numpy_scalar(self, value: dict[str, JsonValue]) -> np.generic:
        self._require_keys(value, {_tag, "dtype", "data"})
        dtype = self._dtype(value["dtype"])
        data = value["data"]
        if dtype.kind == "c":
            if not isinstance(data, dict) or set(data) != {"real", "imaginary"}:
                raise TypeError("complex scalar data must contain real and imaginary")
            real = data["real"]
            imaginary = data["imaginary"]
            if type(real) not in (int, float) or type(imaginary) not in (int, float):
                raise TypeError("complex scalar components must be JSON numbers")
            if isinstance(real, int) and type(real) is int:
                real_number: int | float = real
            elif isinstance(real, float) and type(real) is float:
                real_number = real
            else:
                raise TypeError("complex scalar real part must be a JSON number")
            if isinstance(imaginary, int) and type(imaginary) is int:
                imaginary_number: int | float = imaginary
            elif isinstance(imaginary, float) and type(imaginary) is float:
                imaginary_number = imaginary
            else:
                raise TypeError("complex scalar imaginary part must be a JSON number")
            represented: int | float | complex = real_number + 1.0j * imaginary_number
        else:
            if isinstance(data, int) and type(data) is int:
                represented = data
            elif isinstance(data, float) and type(data) is float:
                represented = data
            else:
                raise TypeError("real scalar data must be a JSON number")
            if dtype.kind in "iu":
                if type(represented) is not int:
                    raise TypeError("integer scalar data must be a JSON integer")
                self._validate_integer(represented, dtype)
        result = np.asarray(represented, dtype=dtype)[()]
        if not isinstance(result, np.generic):
            raise TypeError("decoded scalar did not produce a NumPy scalar")
        if dtype.kind in "fc" and not np.isfinite(result):
            raise ValueError("decoded NumPy scalar must be finite")
        return result

    def _deserialize_ndarray(self, value: dict[str, JsonValue]) -> np.ndarray:
        self._require_keys(value, {_tag, "dtype", "shape", "data"})
        dtype = self._dtype(value["dtype"])
        shape = self._shape(value["shape"])
        data = value["data"]
        if dtype.kind == "c":
            if not isinstance(data, dict) or set(data) != {"real", "imaginary"}:
                raise TypeError("complex array data must contain real and imaginary")
            self._validate_real_array_data(data["real"])
            self._validate_real_array_data(data["imaginary"])
            real = np.asarray(data["real"], dtype=np.float64)
            imaginary = np.asarray(data["imaginary"], dtype=np.float64)
            if real.size == 0 and 0 in shape:
                real = real.reshape(shape)
            if imaginary.size == 0 and 0 in shape:
                imaginary = imaginary.reshape(shape)
            if real.shape != shape or imaginary.shape != shape:
                raise ValueError("complex array component shapes must match metadata")
            result = np.asarray(real + 1.0j * imaginary, dtype=dtype)
        else:
            if dtype.kind in "iu":
                self._validate_integer_array_data(data, dtype)
            else:
                self._validate_real_array_data(data)
            result = np.asarray(data, dtype=dtype)
            if result.size == 0 and 0 in shape:
                result = result.reshape(shape)
            if result.shape != shape:
                raise ValueError("array shape must match metadata")
        if dtype.kind in "fc" and not np.all(np.isfinite(result)):
            raise ValueError("decoded NumPy array must be finite")
        return result

    def _deserialize_sparse(self, value: dict[str, JsonValue]) -> sparse.csr_array:
        self._require_keys(value, {_tag, "data", "indices", "indptr", "shape"})
        data = self.deserialize(value["data"])
        indices = self.deserialize(value["indices"])
        indptr = self.deserialize(value["indptr"])
        shape = self.deserialize(value["shape"])
        if not isinstance(data, np.ndarray):
            raise TypeError("CSR data must decode to numpy.ndarray")
        if not isinstance(indices, np.ndarray) or not isinstance(indptr, np.ndarray):
            raise TypeError("CSR indices must decode to numpy.ndarray")
        if indices.dtype.kind not in "iu" or indptr.dtype.kind not in "iu":
            raise TypeError("CSR indices must use integer NumPy dtypes")
        if data.ndim != 1 or indices.ndim != 1 or indptr.ndim != 1:
            raise ValueError("CSR data, indices, and row offsets must be vectors")
        if not (
            isinstance(shape, tuple)
            and len(shape) == 2
            and all(type(dimension) is int for dimension in shape)
        ):
            raise TypeError("CSR shape must decode to an integer pair")
        result = sparse.csr_array((data, indices, indptr), shape=shape)
        result.check_format(full_check=True)
        return result

    @staticmethod
    def _require_keys(value: dict[str, JsonValue], expected: set[str]) -> None:
        if set(value) != expected:
            raise ValueError("typed JSON object fields do not match its tag")

    @classmethod
    def _dtype(cls, value: JsonValue) -> np.dtype[np.generic]:
        if type(value) is not str:
            raise TypeError("NumPy dtype metadata must be a string")
        dtype = np.dtype(value)
        cls._validate_dtype(dtype)
        return dtype

    @staticmethod
    def _validate_dtype(dtype: np.dtype[np.generic]) -> None:
        supported_item_sizes = {
            "i": frozenset({1, 2, 4, 8}),
            "u": frozenset({1, 2, 4, 8}),
            "f": frozenset({2, 4, 8}),
            "c": frozenset({8, 16}),
        }
        item_sizes = supported_item_sizes.get(dtype.kind)
        if item_sizes is None or dtype.itemsize not in item_sizes:
            raise TypeError(
                "NumPy dtype must be a fixed-width integer, binary float, or "
                "binary complex type excluding booleans"
            )

    @staticmethod
    def _validate_integer(value: int, dtype: np.dtype[np.generic]) -> None:
        bits = 8 * dtype.itemsize
        if dtype.kind == "u":
            minimum = 0
            maximum = (1 << bits) - 1
        else:
            minimum = -(1 << (bits - 1))
            maximum = (1 << (bits - 1)) - 1
        if value < minimum or value > maximum:
            raise OverflowError("integer JSON value exceeds the declared NumPy dtype")

    @classmethod
    def _validate_integer_array_data(
        cls,
        value: JsonValue,
        dtype: np.dtype[np.generic],
    ) -> None:
        if isinstance(value, list):
            for item in value:
                cls._validate_integer_array_data(item, dtype)
            return
        if type(value) is not int:
            raise TypeError("integer NumPy array data must contain JSON integers")
        cls._validate_integer(value, dtype)

    @classmethod
    def _validate_real_array_data(cls, value: JsonValue) -> None:
        if isinstance(value, list):
            for item in value:
                cls._validate_real_array_data(item)
            return
        number: int | float
        if isinstance(value, int) and type(value) is int:
            number = value
        elif isinstance(value, float) and type(value) is float:
            number = value
        else:
            raise TypeError("floating NumPy array data must contain JSON numbers")
        if not np.isfinite(number):
            raise ValueError("floating NumPy array data must be finite")

    @staticmethod
    def _shape(value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list) or not all(
            type(dimension) is int and dimension >= 0 for dimension in value
        ):
            raise TypeError("NumPy shape metadata must be nonnegative integers")
        dimensions: list[int] = []
        for dimension in value:
            if not isinstance(dimension, int) or type(dimension) is not int:
                raise TypeError("NumPy shape dimensions must be built-in integers")
            dimensions.append(dimension)
        return tuple(dimensions)
