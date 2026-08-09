r"""Software verification of ``OperatorRecord``.

Facet and represented meaning

-----------------------------
This class-owned module owns the construction facet. Represented DataObject and
owned contract
----------------------------------------
``OperatorRecord`` stores a finite represented matrix
:math:`\mathbf H\in\mathbb C^{N\times N}` and exactly seven interpreting
metadata fields. This facet owns public field mapping, approved matrix-input
canonicalization, canonical representation properties, non-Hermitian admission,
exact descriptive-string preservation, derived shape, and prohibited-ActionObject
API exclusions.

Ownership and evidence interpretation
-------------------------------------
Matrix index order follows ``basis.ordering``; entries use
``energy_reference.unit`` and ``energy_reference.zero``. Hermiticity,
compatibility, differencing, residual analysis, comparison Workflow behavior,
alignment, conversion, and serialization remain outside this DataObject. The
approved public/Sphinx contract is the oracle. Passing establishes Python
construction behavior; failure may indicate an implementation regression,
documentation mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-OR-001`` through
``SV-OR-007``. It performs no numerical algorithm, Hermiticity calculation, DFT,
Wannier, experimental, or impurity calculation. Numerical verification is not
applicable. Scientific validation, uncertainty quantification, and Rust
conformance have not been performed.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecord``; collaborators only construct inputs or
expose public outcomes. Accepted public contracts, literal expected values, Python
language semantics, and assigned schema or fixture artifacts provide the oracles. No
runtime warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from dataclasses import fields
from typing import Any, cast

import numpy as np
import pytest
from operator_record_fixtures import (
    MatrixInput,
    make_basis,
    make_energy_reference,
    make_geometry,
    make_record,
    make_state_space,
)

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification

SUT = OperatorRecord


def test_constructor__public_fields_are_mapped_exactly__is_enforced() -> None:
    r"""Evidence ID: SV-OR-001

    Requirement: The public DataObject stores exactly identifier, operator kind,
    canonical matrix,
    StateSpace, Basis, Geometry, EnergyReference, and provenance.

    Method: Construct through the public import with distinct typed dependencies and
    inspect
    standard dataclass fields plus public values and shape.

    Oracle: The approved eight-field representation contract fixes names and roles.

    Acceptance: Field names are exact; nested objects retain identity; provenance
    content and
    canonical matrix values match; shape is ``(2, 2)``.

    Interpretation: Passing establishes constructor-to-stored-state mapping.

    Limitations: It does not inspect private storage, execute ActionObjects, establish
    physical
    meaning, scientific validation, UQ, or Rust conformance.
    """

    state_space = make_state_space()
    basis = make_basis()
    geometry = make_geometry()
    energy_reference = make_energy_reference()
    provenance = {"origin": "synthetic fixture"}
    record = OperatorRecord(
        "record-A",
        "finite synthetic operator",
        [[1, 2j], [-2j, 3]],
        state_space,
        basis,
        geometry,
        energy_reference,
        provenance,
    )

    assert tuple(field.name for field in fields(OperatorRecord)) == (
        "identifier",
        "operator_kind",
        "matrix",
        "state_space",
        "basis",
        "geometry",
        "energy_reference",
        "provenance",
    )
    assert record.identifier == "record-A"
    assert record.operator_kind == "finite synthetic operator"
    assert record.matrix.tolist() == [[1 + 0j, 2j], [-2j, 3 + 0j]]
    assert record.state_space is state_space
    assert record.basis is basis
    assert record.geometry is geometry
    assert record.energy_reference is energy_reference
    assert dict(record.provenance) == provenance
    assert record.shape == (2, 2)


@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        pytest.param(
            ((1, 2.5), (3 + 4j, np.int32(5))),
            [[1 + 0j, 2.5 + 0j], [3 + 4j, 5 + 0j]],
            id="tuple_python_and_numpy_integer",
        ),
        pytest.param(
            [[np.float32(1.5), np.complex64(2 + 3j)], [4, 5.5]],
            [[1.5 + 0j, 2 + 3j], [4 + 0j, 5.5 + 0j]],
            id="list_numpy_float_and_complex",
        ),
        pytest.param(
            np.array([[1, 2], [3, 4]], dtype=np.int64),
            [[1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]],
            id="exact_numpy_integer_array",
        ),
        pytest.param(
            np.array([[1.25, 2.5], [3.75, 4.0]], dtype=np.float64),
            [[1.25 + 0j, 2.5 + 0j], [3.75 + 0j, 4 + 0j]],
            id="exact_numpy_floating_array",
        ),
        pytest.param(
            np.array([[1 + 2j, 3 - 4j], [5j, 6]], dtype=np.complex128),
            [[1 + 2j, 3 - 4j], [5j, 6 + 0j]],
            id="exact_numpy_complex_array",
        ),
    ],
)
def test_constructor__approved_matrix_inputs_canonicalize_without__is_enforced(
    matrix: MatrixInput,
    expected: list[list[complex]],
) -> None:
    r"""Evidence ID: SV-OR-002

    Requirement: Nested exact tuple/list and exact NumPy-array inputs admit approved
    Python and NumPy
    integer, floating, and complex scalars; incidental array-like objects, ndarray
    subclasses, and ndarray row containers are outside that boundary.

    Method: Pass each admitted matrix directly without ``np.asarray`` or dtype
    preprocessing,
    then probe representative unsupported containers through deliberate invalid
    boundaries.

    Oracle: Independently literal complex values define the canonical expected state.

    Acceptance: Admitted values match exactly with exact ndarray/complex128 storage;
    every
    unsupported container raises field-semantic ``TypeError``.

    Interpretation: Passing establishes approved runtime admission and canonical
    storage.

    Limitations: It does not approve arbitrary array-like containers, Booleans, strings,
    physical
    matrices, scientific validation, UQ, or Rust conformance.
    """

    record = make_record(matrix)

    assert record.matrix.tolist() == expected
    assert type(record.matrix) is np.ndarray
    assert record.matrix.dtype == np.dtype(np.complex128)


@pytest.mark.parametrize(
    "unsupported",
    [
        pytest.param(
            memoryview(np.array([[1.0, 0.0], [0.0, 1.0]])),
            id="memoryview_container",
        ),
        pytest.param(
            np.ma.array([[1.0, 0.0], [0.0, 1.0]]),
            id="masked_array_container",
        ),
        pytest.param(
            [np.array([1.0, 0.0]), np.array([0.0, 1.0])],
            id="ndarray_row_containers",
        ),
    ],
)
def test_constructor__unsupported_matrix_containers__raise_type_error(
    unsupported: object,
) -> None:
    r"""Evidence ID: SV-OR-043

    Requirement: Matrix containers outside exact nested sequences and exact ndarrays are
    rejected.

    Method: Pass memoryview, masked-array, and ndarray-row containers without coercion.

    Oracle: The accepted public matrix-container boundary excludes all three categories.

    Acceptance: Every case raises exactly ``TypeError``.

    Interpretation: A pass confirms container taxonomy; failure indicates
    admission-contract drift.

    Limitations: Scalar invariants, numerical matrix meaning, validation, UQ, and Rust
    are excluded.
    """
    with pytest.raises(TypeError):
        make_record(cast(Any, unsupported))


def test_field__canonical_matrix_representation__has_required_properties() -> None:
    r"""Evidence ID: SV-OR-003

    Requirement: Stored matrix state is exact complex128, rank two, square,
    C-contiguous, and
    non-writeable.

    Method: Construct from a valid nested tuple and inspect only public NumPy
    representation
    properties.

    Oracle: The approved canonical representation contract fixes these properties.

    Acceptance: Every property holds exactly for the stored 2x2 matrix.

    Interpretation: Passing establishes representation state, not its private backing.

    Limitations: It does not inspect ``.base``, calculate a norm, establish scientific
    validation,
    UQ, or Rust conformance.
    """

    record = make_record(((1, 2), (3, 4)))

    assert type(record.matrix) is np.ndarray
    assert record.matrix.dtype == np.dtype(np.complex128)
    assert record.matrix.ndim == 2
    assert record.matrix.shape == (2, 2)
    assert record.matrix.flags.c_contiguous
    assert not record.matrix.flags.writeable


def test_constructor__general_nonhermitian_finite_matrix_is__is_enforced() -> None:
    r"""Evidence ID: SV-OR-004

    Requirement: OperatorRecord stores general finite represented operators and imposes
    no
    Hermiticity policy.

    Method: Construct the literal matrix ``[[0, 1], [2, 0]]`` and inspect its exact
    stored
    entries without calculating a Hermiticity residual.

    Oracle: Unequal real off-diagonal entries independently make the matrix
    non-Hermitian while
    all representation invariants remain valid.

    Acceptance: Construction succeeds and entries are preserved exactly.

    Interpretation: Passing confirms Hermiticity remains an Analyzer responsibility.

    Limitations: It does not assess physical admissibility, run HermiticityAnalyzer,
    perform
    scientific validation, UQ, or Rust conformance.
    """

    record = make_record([[0, 1], [2, 0]])

    assert record.matrix.tolist() == [[0j, 1 + 0j], [2 + 0j, 0j]]


@pytest.mark.parametrize(
    ("identifier", "operator_kind"),
    [
        pytest.param("Record A", "Finite Operator", id="case_spaces"),
        pytest.param("record-A", "finite/operator", id="sv_or_005_punctuation"),
        pytest.param("Record--A", "finite-test-kind", id="sv_or_005_hyphenation"),
    ],
)
def test_field__represented_state__identifier_and_operator_kind_are_preserved(
    identifier: str,
    operator_kind: str,
) -> None:
    r"""Evidence ID: SV-OR-005

    Requirement: Identifier and operator kind retain case, spaces, punctuation, and
    hyphenation
    without normalization or vocabulary lookup.

    Method: Pass synthetic strings unchanged and compare exact stored content.

    Oracle: Exact Python string equality is the approved preservation oracle.

    Acceptance: Both stored strings equal their supplied inputs exactly.

    Interpretation: Passing establishes literal descriptive metadata preservation.

    Limitations: It does not validate vocabulary or physical meaning, scientific
    validation, UQ, or
    Rust conformance.
    """

    record = make_record(identifier=identifier, operator_kind=operator_kind)

    assert record.identifier == identifier
    assert record.operator_kind == operator_kind


def test_field__shape_is_the_exact_canonical_matrix_shape__is_exact() -> None:
    r"""Evidence ID: SV-OR-006

    Requirement: Public ``shape`` equals canonical matrix shape and is a two-integer
    tuple.

    Method: Construct a valid 2x2 record and compare public values exactly.

    Oracle: The approved property is defined directly by represented matrix shape.

    Acceptance: ``record.shape == record.matrix.shape == (2, 2)`` and both elements are
    exact
    built-in integers.

    Interpretation: Passing establishes the documented trivial derived property.

    Limitations: It introduces no dimension property, numerical algorithm, scientific
    validation, UQ,
    or Rust conformance.
    """

    record = make_record()

    assert record.shape == record.matrix.shape == (2, 2)
    assert type(record.shape) is tuple
    assert all(type(dimension) is int for dimension in record.shape)


def test_public_api__unowned_actions__are_absent() -> None:
    r"""Evidence ID: SV-OR-007

    Requirement: OperatorRecord exposes none of the maintained removed Hermiticity,
    serialization,
    comparison, or differencing API names.

    Method: Inspect a valid instance and public class for the exact approved/removed
    names
    without invoking private implementation details.

    Oracle: DataObject/ActionObject ownership assigns these operations elsewhere.

    Acceptance: Every listed name is absent from both instance and class.

    Interpretation: Passing establishes the narrow represented-state boundary.

    Limitations: It does not test serializer fixtures or ActionObject behavior,
    scientific
    validation, UQ, or Rust conformance.
    """

    record = make_record()

    assert all(
        (not hasattr(record, name)) and (not hasattr(OperatorRecord, name))
        for name in (
            "hermiticity_residual",
            "is_hermitian",
            "require_hermitian",
            "to_dict",
            "from_dict",
            "serialize",
            "deserialize",
            "to_json",
            "from_json",
            "compare",
            "difference",
        )
    )
