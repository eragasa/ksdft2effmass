import json
from collections.abc import Mapping

import numpy as np
import pytest

import ksdft2effmass.operators.records as records_module
import ksdft2effmass.operators.serialization as serialization_module
from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    HermiticityAnalyzer,
    HermiticityResult,
    OperatorRecord,
    OperatorRecordJsonCodec,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_state_space(dimension: int = 2) -> StateSpace:
    return StateSpace(
        "H_test", "finite synthetic", dimension, f"C^{dimension}", f"C^{dimension}"
    )


def make_basis(ordering: tuple[str, ...] = ("a", "b")) -> Basis:
    return Basis("canonical", "orthonormal_test_basis", ordering, True)


def make_geometry(cell: object = VALID_CELL) -> Geometry:
    return Geometry(
        "synthetic",
        cell,  # type: ignore[arg-type]
        "finite synthetic",
        "cartesian dimensionless, row lattice vectors",
    )


def make_record(
    matrix: object | None = None,
    *,
    state_space: StateSpace | None = None,
    basis: Basis | None = None,
    geometry: Geometry | None = None,
    energy_reference: EnergyReference | None = None,
    provenance: Mapping[str, str] | None = None,
) -> OperatorRecord:
    if matrix is None:
        matrix = np.array([[1.0, 0.25j], [-0.25j, 2.0]])
    return OperatorRecord(
        identifier="synthetic-two-level",
        operator_kind="finite_test_hamiltonian",
        matrix=matrix,  # type: ignore[arg-type]
        state_space=state_space or make_state_space(),
        basis=basis or make_basis(),
        geometry=geometry or make_geometry(),
        energy_reference=energy_reference or EnergyReference("explicit zero", "eV"),
        provenance=provenance or {"source": "unit test"},
    )


def test_valid_construction_and_public_imports() -> None:
    record = make_record()

    assert isinstance(record.state_space, StateSpace)
    assert isinstance(record.basis, Basis)
    assert isinstance(record.geometry, Geometry)
    assert isinstance(record.energy_reference, EnergyReference)
    assert isinstance(HermiticityAnalyzer().execute(record), HermiticityResult)
    assert isinstance(OperatorRecordJsonCodec().encode(record), dict)
    assert record.shape == (2, 2)
    assert record.matrix.dtype == np.complex128


def test_operator_record_contains_no_hermiticity_policy() -> None:
    record = make_record()

    assert not hasattr(record, "hermiticity_tolerance")
    assert not hasattr(record, "hermiticity_residual")
    assert not hasattr(record, "is_hermitian")
    assert not hasattr(record, "require_hermitian")
    assert not hasattr(record, "to_dict")
    assert not hasattr(OperatorRecord, "from_dict")


def test_square_matrix_validation() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        make_record(np.array([1.0, 2.0]))
    with pytest.raises(ValueError, match="square"):
        make_record(np.ones((2, 3)))


def test_matrix_state_space_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="state-space dimension"):
        make_record(
            np.eye(3),
            state_space=make_state_space(2),
            basis=make_basis(("a", "b", "c")),
        )


def test_basis_ordering_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="basis ordering"):
        make_record(np.eye(2), basis=make_basis(("a",)))


@pytest.mark.parametrize(
    "bad_matrix",
    [
        np.array([[np.nan, 0.0], [0.0, 1.0]]),
        np.array([[np.inf, 0.0], [0.0, 1.0]]),
        np.array([[1.0 + np.nan * 1j, 0.0], [0.0, 1.0]]),
    ],
)
def test_rejects_nonfinite_matrix_entries(bad_matrix: np.ndarray) -> None:
    with pytest.raises(ValueError, match="matrix entries must be finite"):
        make_record(bad_matrix)


@pytest.mark.parametrize("dimension", [True, False, 2.0, np.float64(2.0), "2"])
def test_rejects_invalid_state_space_dimension_types(dimension: object) -> None:
    with pytest.raises(TypeError, match="positive integer"):
        StateSpace("bad", "finite synthetic", dimension, "C^N", "C^N")  # type: ignore[arg-type]


@pytest.mark.parametrize("dimension", [0, -1, np.int64(-2)])
def test_rejects_nonpositive_state_space_dimensions(dimension: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        StateSpace("bad", "finite synthetic", dimension, "C^N", "C^N")


def test_accepts_numpy_integral_state_space_dimension() -> None:
    state_space = StateSpace("ok", "finite synthetic", np.int64(2), "C^2", "C^2")

    assert state_space.dimension == 2
    assert isinstance(state_space.dimension, int)


@pytest.mark.parametrize(
    "cell, message",
    [
        (((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)), "three three-component"),
        (((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)), "three three-component"),
        (((1.0, 0.0, 0.0), (0.0, np.nan, 0.0), (0.0, 0.0, 1.0)), "finite"),
        (((1.0, 0.0, 0.0), (0.0, np.inf, 0.0), (0.0, 0.0, 1.0)), "finite"),
        (((1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 0.0, 1.0)), "independent"),
        (((1.0, 0.0, 0.0), ("bad", 1.0, 0.0), (0.0, 0.0, 1.0)), "numeric"),
    ],
)
def test_rejects_malformed_nonfinite_and_rank_deficient_cells(
    cell: object, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        make_geometry(cell)


def test_geometry_canonicalizes_runtime_lists() -> None:
    geometry = make_geometry([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    assert geometry.cell == ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_rejects_invalid_energy_reference_values(value: float) -> None:
    with pytest.raises(ValueError, match="energy-reference value"):
        EnergyReference("zero", "eV", value)


@pytest.mark.parametrize("tolerance", [-1.0, np.nan, np.inf, -np.inf])
def test_rejects_invalid_analyzer_tolerances(tolerance: float) -> None:
    message = "finite" if not np.isfinite(tolerance) else "non-negative"
    with pytest.raises(ValueError, match=message):
        HermiticityAnalyzer(tolerance=tolerance)


def test_hermiticity_analyzer_execute_and_require() -> None:
    hermitian = make_record(np.array([[1.0, 1.0j], [-1.0j, 2.0]]))
    nonhermitian = make_record(np.array([[1.0, 2.0], [3.0, 4.0]]))
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12)

    result = analyzer.execute(hermitian)
    assert result.residual == pytest.approx(0.0)
    assert result.is_hermitian
    assert analyzer.require(hermitian) == result

    failed = analyzer.execute(nonhermitian)
    assert failed.residual == pytest.approx(1.0)
    assert not failed.is_hermitian
    with pytest.raises(ValueError, match=r"residual=1.*tolerance=1e-12"):
        analyzer.require(nonhermitian)


def test_different_analyzers_can_use_different_tolerances() -> None:
    record = make_record(np.array([[1.0, 0.0], [1.0e-8, 2.0]]))

    assert not HermiticityAnalyzer(tolerance=1.0e-12).execute(record).is_hermitian
    assert HermiticityAnalyzer(tolerance=1.0e-6).execute(record).is_hermitian


def test_hermiticity_result_is_immutable() -> None:
    result = HermiticityAnalyzer().execute(make_record())

    with pytest.raises(AttributeError):
        result.residual = 5.0  # type: ignore[misc]


def test_source_matrix_mutation_does_not_affect_record() -> None:
    matrix = np.array([[1.0, 0.0], [0.0, 2.0]])
    record = make_record(matrix)
    matrix[0, 0] = 99.0
    assert record.matrix[0, 0] == 1.0


def test_direct_assignment_into_stored_matrix_is_rejected() -> None:
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
    with pytest.raises(TypeError):
        record.provenance["new"] = "not allowed"  # type: ignore[index]


def test_exact_structural_equality_without_numpy_truth_value_errors() -> None:
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


def test_record_is_unhashable() -> None:
    with pytest.raises(TypeError):
        hash(make_record())


def test_serialization_is_performed_through_codec() -> None:
    record = make_record()
    codec = OperatorRecordJsonCodec()

    payload = codec.encode(record)
    encoded = json.dumps(payload)
    restored = codec.decode(json.loads(encoded))

    assert payload["schema_version"] == 1
    assert "hermiticity_tolerance" not in payload
    assert restored == record
    assert isinstance(restored.provenance, Mapping)
    assert not restored.matrix.flags.writeable


def test_missing_or_unsupported_schema_versions_are_codec_errors() -> None:
    codec = OperatorRecordJsonCodec()
    data = codec.encode(make_record())
    del data["schema_version"]
    with pytest.raises(ValueError, match="missing schema_version"):
        codec.decode(data)

    unsupported = codec.encode(make_record())
    unsupported["schema_version"] = 999
    with pytest.raises(ValueError, match="unsupported"):
        codec.decode(unsupported)


@pytest.mark.parametrize(
    "encoded_matrix, message",
    [
        ([[[1.0, 0.0, 2.0]]], "complex matrix entries"),
        ([[["bad", 0.0]]], "numeric"),
        ([[[np.nan, 0.0]]], "finite"),
        ([[[1.0, 0.0]], [[1.0, 0.0], [2.0, 0.0]]], "ragged"),
        ([[1.0]], "complex matrix entries"),
    ],
)
def test_malformed_complex_matrix_encodings(
    encoded_matrix: list[object], message: str
) -> None:
    codec = OperatorRecordJsonCodec()
    data = codec.encode(make_record())
    data["matrix"] = encoded_matrix

    with pytest.raises(ValueError, match=message):
        codec.decode(data)


def test_no_obsolete_module_level_encoding_helpers_remain() -> None:
    assert not hasattr(records_module, "_encode_complex_matrix")
    assert not hasattr(records_module, "_decode_complex_matrix")
    assert not hasattr(serialization_module, "_encode_complex_matrix")
    assert not hasattr(serialization_module, "_decode_complex_matrix")
