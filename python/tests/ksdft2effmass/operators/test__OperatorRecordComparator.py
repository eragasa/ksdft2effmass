"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    IncompatibleOperatorRecordsError,
    OperatorRecord,
    OperatorRecordComparator,
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityMismatchCode,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_record(
    matrix: Any,
    *,
    identifier: str = "record",
    operator_kind: str = "finite_test_hamiltonian",
    energy_unit: str = "eV",
) -> OperatorRecord:
    return OperatorRecord(
        identifier,
        operator_kind,
        matrix,
        StateSpace(f"state-space-{identifier}", "finite synthetic", 2),
        Basis(f"basis-{identifier}", "site basis", ("a", "b"), True),
        Geometry(
            f"system-{identifier}",
            VALID_CELL,
            "periodic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", energy_unit),
        {"source": "unit test", "record": identifier},
    )


def test_public_import_constructs_comparator() -> None:
    comparator = OperatorRecordComparator()

    assert isinstance(
        comparator.compatibility_analyzer, OperatorRecordCompatibilityAnalyzer
    )


def test_comparator_rejects_non_analyzer_dependency() -> None:
    with pytest.raises(TypeError, match="compatibility_analyzer"):
        OperatorRecordComparator(compatibility_analyzer=cast(Any, object()))


def test_comparator_returns_zero_residual_for_identical_matrices() -> None:
    reference = make_record(np.array([[1.0, 0.0], [0.0, 2.0]]), identifier="reference")
    candidate = make_record(np.array([[1.0, 0.0], [0.0, 2.0]]), identifier="candidate")

    result = OperatorRecordComparator().execute(reference, candidate)

    assert isinstance(result, OperatorRecordComparisonResult)
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.matrix_dimension == 2
    assert result.energy_unit == "eV"
    assert result.maximum_absolute_residual == 0.0
    assert result.frobenius_residual == 0.0
    assert result.spectral_residual == 0.0


def test_comparator_reports_roles_and_symmetric_absolute_metrics() -> None:
    reference = make_record(np.array([[3.0, 0.0], [0.0, 0.0]]), identifier="reference")
    candidate = make_record(np.array([[1.0, 0.0], [0.0, 4.0]]), identifier="candidate")

    forward = OperatorRecordComparator().execute(reference, candidate)
    swapped = OperatorRecordComparator().execute(candidate, reference)

    assert forward.reference_identifier == "reference"
    assert forward.candidate_identifier == "candidate"
    assert swapped.reference_identifier == "candidate"
    assert swapped.candidate_identifier == "reference"
    assert forward.maximum_absolute_residual == 4.0
    assert forward.frobenius_residual == pytest.approx((20.0) ** 0.5)
    assert forward.spectral_residual == 4.0
    assert swapped.maximum_absolute_residual == forward.maximum_absolute_residual
    assert swapped.frobenius_residual == forward.frobenius_residual
    assert swapped.spectral_residual == forward.spectral_residual


def test_comparator_metrics_are_analytically_checkable_for_real_matrix() -> None:
    reference = make_record(np.zeros((2, 2)), identifier="reference")
    candidate = make_record(np.array([[3.0, 0.0], [0.0, 4.0]]), identifier="candidate")

    result = OperatorRecordComparator().execute(reference, candidate)

    assert result.maximum_absolute_residual == 4.0
    assert result.frobenius_residual == 5.0
    assert result.spectral_residual == 4.0
    assert (
        0.0
        <= result.maximum_absolute_residual
        <= result.spectral_residual
        <= result.frobenius_residual
    )


def test_comparator_handles_scale_safe_large_diagonal_residual() -> None:
    reference = make_record(np.zeros((2, 2)), identifier="reference")
    candidate = make_record(
        np.array([[1.0e200, 0.0], [0.0, 0.0]]), identifier="candidate"
    )

    result = OperatorRecordComparator().execute(reference, candidate)

    assert result.maximum_absolute_residual == pytest.approx(1.0e200)
    assert result.frobenius_residual == pytest.approx(1.0e200)
    assert result.spectral_residual == pytest.approx(1.0e200)


def test_comparator_handles_scale_safe_small_diagonal_residual() -> None:
    reference = make_record(np.zeros((2, 2)), identifier="reference")
    candidate = make_record(
        np.array([[1.0e-200, 0.0], [0.0, 0.0]]), identifier="candidate"
    )

    result = OperatorRecordComparator().execute(reference, candidate)

    assert result.maximum_absolute_residual == pytest.approx(1.0e-200)
    assert result.frobenius_residual == pytest.approx(1.0e-200)
    assert result.spectral_residual == pytest.approx(1.0e-200)


def test_comparator_raises_structured_error_for_subtraction_overflow() -> None:
    reference = make_record(
        np.array([[-1.0e308, 0.0], [0.0, 0.0]]), identifier="reference"
    )
    candidate = make_record(
        np.array([[1.0e308, 0.0], [0.0, 0.0]]), identifier="candidate"
    )

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordComparator().execute(reference, candidate)

    assert exc_info.value.reason == "nonfinite_residual"


def test_comparator_metrics_are_analytically_checkable_for_complex_matrix() -> None:
    reference = make_record(np.zeros((2, 2)), identifier="reference")
    candidate = make_record(
        np.array([[0.0, 3.0 + 4.0j], [0.0, 0.0]]), identifier="candidate"
    )

    result = OperatorRecordComparator().execute(reference, candidate)

    assert result.maximum_absolute_residual == 5.0
    assert result.frobenius_residual == 5.0
    assert result.spectral_residual == 5.0
    assert (
        0.0
        <= result.maximum_absolute_residual
        <= result.spectral_residual
        <= result.frobenius_residual
    )


def test_comparator_rejects_incompatible_records_before_metrics() -> None:
    reference = make_record(np.eye(2), identifier="reference")
    candidate = make_record(
        np.eye(2), identifier="candidate", operator_kind="different_operator"
    )

    with pytest.raises(IncompatibleOperatorRecordsError) as exc_info:
        OperatorRecordComparator().execute(reference, candidate)

    result = exc_info.value.compatibility_result
    assert not result.is_compatible
    assert tuple(issue.code for issue in result.issues) == (
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
    )


def test_comparator_requires_operator_records_through_compatibility_analyzer() -> None:
    with pytest.raises(TypeError, match="OperatorRecord"):
        OperatorRecordComparator().execute(cast(Any, object()), make_record(np.eye(2)))
