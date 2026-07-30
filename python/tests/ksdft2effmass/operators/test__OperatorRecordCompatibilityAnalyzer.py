"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from collections.abc import Mapping
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_record(
    *,
    identifier: str = "reference-record",
    operator_kind: str = "finite_test_hamiltonian",
    matrix: Any | None = None,
    state_space_identifier: str = "state-space-reference",
    state_space_kind: str = "finite synthetic",
    basis_identifier: str = "basis-reference",
    basis_kind: str = "site basis",
    basis_ordering: tuple[str, ...] = ("a", "b"),
    cell: tuple[tuple[float, float, float], ...] = VALID_CELL,
    geometry_system: str = "reference system",
    boundary_conditions: str = "periodic",
    coordinate_convention: str = "cartesian row lattice vectors",
    length_unit: str = "angstrom",
    energy_zero: str = "explicit zero",
    energy_unit: str = "eV",
    provenance: Mapping[str, str] | None = None,
) -> OperatorRecord:
    if matrix is None:
        matrix = np.array([[1.0, 0.0], [0.0, 2.0]])
    dimension = len(basis_ordering)
    return OperatorRecord(
        identifier,
        operator_kind,
        matrix,
        StateSpace(state_space_identifier, state_space_kind, dimension),
        Basis(basis_identifier, basis_kind, basis_ordering, True),
        Geometry(
            geometry_system,
            cell,
            boundary_conditions,
            coordinate_convention,
            length_unit,
        ),
        EnergyReference(energy_zero, energy_unit),
        provenance or {"source": "unit test", "physical_system": "reference"},
    )


def issue_codes(
    result: OperatorRecordCompatibilityResult,
) -> tuple[OperatorRecordCompatibilityMismatchCode, ...]:
    return tuple(issue.code for issue in result.issues)


def test_public_import_constructs_analyzer() -> None:
    assert isinstance(
        OperatorRecordCompatibilityAnalyzer(), OperatorRecordCompatibilityAnalyzer
    )


def test_compatible_result_ignores_identity_provenance_and_physical_labels() -> None:
    reference = make_record()
    candidate = make_record(
        identifier="candidate-record",
        state_space_identifier="state-space-candidate",
        basis_identifier="basis-candidate",
        geometry_system="candidate physical system",
        provenance={"source": "other unit test", "physical_system": "candidate"},
    )

    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)

    assert result.is_compatible
    assert result.issues == ()
    assert result.reference_identifier == "reference-record"
    assert result.candidate_identifier == "candidate-record"


@pytest.mark.parametrize(
    "candidate_kwargs, expected_codes",
    [
        (
            {"matrix": np.eye(3), "basis_ordering": ("a", "b", "c")},
            (
                OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH,
                OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,
            ),
        ),
        (
            {"state_space_kind": "different state space"},
            (OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,),
        ),
        (
            {"operator_kind": "different_operator"},
            (OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,),
        ),
        (
            {"basis_ordering": ("b", "a")},
            (OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,),
        ),
        (
            {"basis_kind": "different basis"},
            (OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH,),
        ),
        (
            {"cell": ((1.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 3.0))},
            (OperatorRecordCompatibilityMismatchCode.LATTICE_VECTORS_MISMATCH,),
        ),
        (
            {"boundary_conditions": "open"},
            (OperatorRecordCompatibilityMismatchCode.BOUNDARY_CONDITIONS_MISMATCH,),
        ),
        (
            {"coordinate_convention": "different convention"},
            (OperatorRecordCompatibilityMismatchCode.COORDINATE_CONVENTION_MISMATCH,),
        ),
        (
            {"length_unit": "bohr"},
            (OperatorRecordCompatibilityMismatchCode.GEOMETRY_LENGTH_UNIT_MISMATCH,),
        ),
        (
            {"energy_unit": "hartree"},
            (OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,),
        ),
        (
            {"energy_zero": "valence band maximum"},
            (OperatorRecordCompatibilityMismatchCode.ENERGY_ZERO_CONVENTION_MISMATCH,),
        ),
    ],
)
def test_analyzer_reports_each_exact_compatibility_rule_mismatch(
    candidate_kwargs: dict[str, Any],
    expected_codes: tuple[OperatorRecordCompatibilityMismatchCode, ...],
) -> None:
    result = OperatorRecordCompatibilityAnalyzer().execute(
        make_record(), make_record(identifier="candidate", **candidate_kwargs)
    )

    assert issue_codes(result) == expected_codes
    assert result.rules_applied == tuple(OperatorRecordCompatibilityMismatchCode)


def test_analyzer_reports_multiple_mismatches_in_deterministic_rule_order() -> None:
    reference = make_record()
    candidate = make_record(
        identifier="candidate",
        operator_kind="different_operator",
        matrix=np.eye(3),
        state_space_kind="different state space",
        basis_ordering=("c", "b", "a"),
        basis_kind="different basis",
        cell=((2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0)),
        boundary_conditions="open",
        coordinate_convention="different convention",
        length_unit="bohr",
        energy_zero="different zero",
        energy_unit="hartree",
    )
    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)

    assert issue_codes(result) == tuple(OperatorRecordCompatibilityMismatchCode)


@pytest.mark.parametrize(
    "bad_reference, bad_candidate",
    [(object(), make_record()), (make_record(), object())],
)
def test_analyzer_requires_operator_records(
    bad_reference: object, bad_candidate: object
) -> None:
    with pytest.raises(TypeError, match="OperatorRecord"):
        OperatorRecordCompatibilityAnalyzer().execute(
            cast(Any, bad_reference), cast(Any, bad_candidate)
        )
