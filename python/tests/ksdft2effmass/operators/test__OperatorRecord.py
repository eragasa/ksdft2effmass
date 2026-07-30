"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from collections.abc import Mapping
from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_state_space(dimension: int = 2) -> StateSpace:
    return StateSpace("H_test", "finite synthetic", dimension)


def make_basis(
    ordering: tuple[str, ...] = ("a", "b"), orthonormal: bool = True
) -> Basis:
    return Basis("canonical", "test basis", ordering, orthonormal)


def make_geometry() -> Geometry:
    return Geometry(
        "synthetic",
        VALID_CELL,
        "finite synthetic",
        "cartesian row lattice vectors",
        "angstrom",
    )


def make_record(
    matrix: Any | None = None,
    *,
    state_space: StateSpace | None = None,
    basis: Basis | None = None,
    provenance: Mapping[str, str] | None = None,
) -> OperatorRecord:
    if matrix is None:
        matrix = np.array([[1.0, 0.25j], [-0.25j, 2.0]])
    return OperatorRecord(
        identifier="synthetic-two-level",
        operator_kind="finite_test_hamiltonian",
        matrix=matrix,
        state_space=state_space or make_state_space(),
        basis=basis or make_basis(),
        geometry=make_geometry(),
        energy_reference=EnergyReference("explicit zero", "eV"),
        provenance=provenance or {"source": "unit test"},
    )


def test_public_import_constructs_operator_record() -> None:
    record = make_record()

    assert record.identifier == "synthetic-two-level"
    assert record.operator_kind == "finite_test_hamiltonian"
    assert record.shape == (2, 2)
    assert record.matrix.dtype == np.complex128
    assert record.matrix.flags.c_contiguous
    assert not record.matrix.flags.writeable


def test_source_matrix_mutation_does_not_affect_record() -> None:
    matrix = np.array([[1.0, 0.0], [0.0, 2.0]])
    record = make_record(matrix)

    matrix[0, 0] = 99.0

    assert record.matrix[0, 0] == 1.0


def test_stored_matrix_is_read_only_through_public_api() -> None:
    record = make_record()

    with pytest.raises(ValueError, match="read-only"):
        record.matrix[0, 0] = 10.0


def test_source_provenance_mutation_does_not_affect_record() -> None:
    provenance = {"source": "before"}
    record = make_record(provenance=provenance)

    provenance["source"] = "after"

    assert record.provenance["source"] == "before"


def test_stored_provenance_mapping_is_read_only() -> None:
    record = make_record()
    provenance: Any = record.provenance

    with pytest.raises(TypeError):
        provenance["new"] = "not allowed"


@pytest.mark.parametrize(
    "provenance",
    [{"source": 1}, {1: "source"}],
)
def test_provenance_keys_and_values_must_be_strings(
    provenance: Mapping[str, str],
) -> None:
    with pytest.raises(TypeError, match="provenance"):
        make_record(provenance=provenance)


def test_provenance_must_be_mapping_not_iterable_pairs() -> None:
    with pytest.raises(TypeError, match="mapping"):
        make_record(provenance=[("source", "test")])  # type: ignore[arg-type]


@pytest.mark.parametrize("provenance", [{"": "source"}, {"source": ""}])
def test_provenance_keys_and_values_must_be_nonempty(
    provenance: Mapping[str, str],
) -> None:
    with pytest.raises(ValueError, match="provenance"):
        make_record(provenance=provenance)


def test_exact_structural_equality_uses_exact_matrix_and_metadata() -> None:
    first = make_record()
    second = make_record()
    different_matrix = make_record(np.array([[1.0, 0.0], [0.0, 3.0]]))
    different_metadata = OperatorRecord(
        "other",
        first.operator_kind,
        first.matrix,
        first.state_space,
        first.basis,
        first.geometry,
        first.energy_reference,
        first.provenance,
    )

    assert first == second
    assert first != different_matrix
    assert first != different_metadata
    assert first.__eq__(object()) is NotImplemented


def test_operator_record_is_unhashable() -> None:
    with pytest.raises(TypeError):
        hash(make_record())


@pytest.mark.parametrize(
    "matrix, message",
    [
        (np.array([1.0, 2.0]), "two-dimensional"),
        (np.ones((2, 3)), "square"),
        (np.array([[np.nan, 0.0], [0.0, 1.0]]), "finite"),
        (np.array([[np.inf, 0.0], [0.0, 1.0]]), "finite"),
        (np.array([[1.0 + np.nan * 1j, 0.0], [0.0, 1.0]]), "finite"),
        ([["1.0", 0.0], [0.0, 1.0]], "numeric"),
        ([[True, 0.0], [0.0, 1.0]], "numeric"),
        ([[np.bool_(True)]], "numeric"),
    ],
)
def test_matrix_intrinsic_invariants(matrix: Any, message: str) -> None:
    expected_error = TypeError if message == "numeric" else ValueError

    with pytest.raises(expected_error, match=message):
        make_record(matrix)


def test_matrix_dimension_must_match_state_space_dimension() -> None:
    with pytest.raises(ValueError, match="state-space dimension"):
        make_record(
            np.eye(3),
            state_space=make_state_space(2),
            basis=make_basis(("a", "b", "c")),
        )


def test_basis_ordering_length_must_match_state_space_dimension() -> None:
    with pytest.raises(ValueError, match="basis ordering"):
        make_record(np.eye(2), basis=make_basis(("a",)))


def test_operator_record_requires_orthonormal_basis() -> None:
    with pytest.raises(ValueError, match="orthonormal basis"):
        make_record(basis=make_basis(("a", "b"), orthonormal=False))


def test_operator_record_contains_no_analysis_or_serialization_policy() -> None:
    record = make_record()

    assert not hasattr(record, "hermiticity_tolerance")
    assert not hasattr(record, "hermiticity_residual")
    assert not hasattr(record, "is_hermitian")
    assert not hasattr(record, "require_hermitian")
    assert not hasattr(record, "to_dict")
    assert not hasattr(OperatorRecord, "from_dict")
