"""Software verification of generic typed scientific JSON conversion."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum, auto

import numpy as np
import pytest
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
    TypedJsonValueCodec,
)

pytestmark = pytest.mark.software_verification
SUT = TypedJsonValueCodec


class _UnregisteredEnum(Enum):
    """Provide an enum absent from the codec's closed default registry."""

    member = auto()


class _Record:
    """Provide one compositional typed mapping for the codec boundary."""

    __slots__ = ("value",)

    def __init__(self, value: MatrixQuantity) -> None:
        self.value = value

    def to_dict(self) -> Mapping[str, SerializableValue]:
        return {"matrix": self.value, "labels": ("left", "right")}


class TestTypedJsonValueCodec:
    """Own reversible conversion of the admitted scientific value inventory."""

    def test_round_trip__dense_sparse_quantities_and_records__preserves_types(
        self,
    ) -> None:
        real_csr = sparse.csr_array(np.diag([1.0, 2.0]))
        complex_csr = sparse.csr_array(
            np.array([[1.0, 2.0j], [0.0, 3.0]], dtype=np.complex128)
        )
        values: dict[str, SerializableValue] = {
            "matrix_norm": MatrixNormEnum.frobenius,
            "numpy_scalar": np.float32(1.25),
            "integer_array": np.array([[1, 2]], dtype=np.int32),
            "complex_array": np.array([1.0 + 2.0j], dtype=np.complex128),
            "csr": real_csr,
            "scalar_quantity": ScalarQuantity(2.0, PhysicalUnit("electron_volt")),
            "vector_quantity": VectorQuantity(np.array([1.0, 2.0]), Unitless()),
            "complex_vector_quantity": ComplexVectorQuantity(
                np.array([1.0 + 2.0j]), Unitless()
            ),
            "matrix_quantity": MatrixQuantity(np.eye(2), Unitless()),
            "complex_matrix_quantity": ComplexMatrixQuantity(
                np.array([[1.0j]]), Unitless()
            ),
            "sparse_matrix_quantity": SparseMatrixQuantity.from_csr(
                real_csr, Unitless()
            ),
            "complex_sparse_matrix_quantity": ComplexSparseMatrixQuantity.from_csr(
                complex_csr, Unitless()
            ),
            "record": _Record(MatrixQuantity(np.eye(2), Unitless())),
        }

        decoded = SUT().deserialize(SUT().serialize(values))

        assert isinstance(decoded, dict)
        assert decoded["matrix_norm"] is MatrixNormEnum.frobenius
        assert isinstance(decoded["numpy_scalar"], np.float32)
        np.testing.assert_array_equal(
            decoded["integer_array"], np.array([[1, 2]], dtype=np.int32)
        )
        np.testing.assert_array_equal(
            decoded["complex_array"],
            np.array([1.0 + 2.0j], dtype=np.complex128),
        )
        assert isinstance(decoded["csr"], sparse.csr_array)
        np.testing.assert_array_equal(decoded["csr"].toarray(), real_csr.toarray())
        assert isinstance(decoded["scalar_quantity"], ScalarQuantity)
        assert isinstance(decoded["vector_quantity"], VectorQuantity)
        assert isinstance(decoded["complex_vector_quantity"], ComplexVectorQuantity)
        assert isinstance(decoded["matrix_quantity"], MatrixQuantity)
        assert isinstance(decoded["complex_matrix_quantity"], ComplexMatrixQuantity)
        assert isinstance(decoded["sparse_matrix_quantity"], SparseMatrixQuantity)
        assert isinstance(
            decoded["complex_sparse_matrix_quantity"],
            ComplexSparseMatrixQuantity,
        )
        record = decoded["record"]
        assert isinstance(record, dict)
        assert isinstance(record["matrix"], MatrixQuantity)
        assert record["labels"] == ("left", "right")

    def test_serialize__unregistered_enum__rejects_dynamic_type_loading(self) -> None:
        with pytest.raises(TypeError, match="closed registry"):
            SUT().serialize(_UnregisteredEnum.member)

    def test_serialize__reserved_tag_key__rejects_ambiguous_plain_mapping(self) -> None:
        with pytest.raises(ValueError, match="reserved"):
            SUT().serialize({"__ksd_type__": "caller value"})

    def test_deserialize__unknown_tag__rejects(self) -> None:
        with pytest.raises(ValueError, match="unknown typed JSON tag"):
            SUT().deserialize({"__ksd_type__": "unknown"})

    @pytest.mark.parametrize(
        "dtype",
        (
            np.dtype(np.int8),
            np.dtype(np.int16),
            np.dtype(np.int32),
            np.dtype(np.int64),
            np.dtype(np.uint8),
            np.dtype(np.uint16),
            np.dtype(np.uint32),
            np.dtype(np.uint64),
            np.dtype(np.float16),
            np.dtype(np.float32),
            np.dtype(np.float64),
            np.dtype(np.complex64),
            np.dtype(np.complex128),
        ),
    )
    def test_round_trip__supported_numpy_dtype__preserves_dtype_and_shape(
        self,
        dtype: np.dtype[np.generic],
    ) -> None:
        if dtype.kind == "c":
            values = np.asarray([[1.0 + 2.0j], [3.0 - 4.0j]], dtype=dtype)
        else:
            values = np.asarray([[1], [2]], dtype=dtype)

        decoded = SUT().deserialize(SUT().serialize(values))

        assert isinstance(decoded, np.ndarray)
        assert decoded.dtype == dtype
        np.testing.assert_array_equal(decoded, values)

    @pytest.mark.parametrize(
        "dtype",
        (np.dtype(np.float64), np.dtype(np.complex128)),
    )
    def test_round_trip__empty_multidimensional_array__preserves_shape(
        self,
        dtype: np.dtype[np.generic],
    ) -> None:
        values = np.empty((0, 3), dtype=dtype)

        decoded = SUT().deserialize(SUT().serialize(values))

        assert isinstance(decoded, np.ndarray)
        assert decoded.dtype == dtype
        assert decoded.shape == (0, 3)

    def test_serialize__boolean_and_extended_numpy_dtypes__rejects(self) -> None:
        with pytest.raises(TypeError, match="fixed-width"):
            SUT().serialize(np.asarray([True], dtype=np.bool_))
        if np.dtype(np.longdouble).itemsize > np.dtype(np.float64).itemsize:
            with pytest.raises(TypeError, match="fixed-width"):
                SUT().serialize(np.asarray([1.0], dtype=np.longdouble))

    def test_deserialize__integer_array_overflow__rejects_without_wrapping(
        self,
    ) -> None:
        encoded = {
            "__ksd_type__": "numpy_array",
            "dtype": "|u1",
            "shape": [1],
            "data": [256],
        }

        with pytest.raises(OverflowError, match="exceeds"):
            SUT().deserialize(encoded)

    def test_deserialize__noninteger_sparse_indices__rejects(self) -> None:
        encoded = {
            "__ksd_type__": "scipy_csr_array",
            "data": SUT().serialize(np.asarray([1.0], dtype=np.float64)),
            "indices": SUT().serialize(np.asarray([0.0], dtype=np.float64)),
            "indptr": SUT().serialize(np.asarray([0, 1], dtype=np.int64)),
            "shape": SUT().serialize((1, 1)),
        }

        with pytest.raises(TypeError, match="integer NumPy dtypes"):
            SUT().deserialize(encoded)

    def test_deserialize_bytes__duplicate_keys_and_nonstandard_numbers__rejects(
        self,
    ) -> None:
        with pytest.raises(ValueError, match="duplicate JSON object key"):
            SUT().deserialize_bytes(b'{"value": 1, "value": 2}\n')
        with pytest.raises(ValueError, match="nonstandard JSON numeric constant"):
            SUT().deserialize_bytes(b'{"value": NaN}\n')

    def test_mapping_actions__typed_mapping__delegate_reversible_json_bytes(
        self,
    ) -> None:
        values: dict[str, SerializableValue] = {
            "array": np.asarray([1.0, 2.0]),
            "unit": PhysicalUnit("electron_volt"),
        }

        wire = TypedJsonMappingSerializer().serialize(values)
        decoded = TypedJsonMappingDeserializer().deserialize(wire)

        assert isinstance(decoded["array"], np.ndarray)
        np.testing.assert_array_equal(decoded["array"], values["array"])
        assert decoded["unit"] == values["unit"]

    def test_serialize_bytes__same_typed_value__is_canonical(self) -> None:
        first = {
            "vector": VectorQuantity(np.asarray([1.0, 2.0]), Unitless()),
            "labels": ("one", "two"),
        }
        second = {"labels": ("one", "two"), "vector": first["vector"]}

        assert SUT().serialize_bytes(first) == SUT().serialize_bytes(second)
