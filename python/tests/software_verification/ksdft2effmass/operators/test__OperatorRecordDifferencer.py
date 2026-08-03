"""Software-verification tests for ``OperatorRecordDifferencer``.

The tested ActionObject enforces compatibility before forming the represented
operator difference with sign convention
``Delta H = H_candidate - H_reference``.  It translates numerical overflow in
that direct represented subtraction into a structured public difference error.
These tests verify the software contract for dependency validation,
compatibility enforcement, execution ordering, signed subtraction, metadata/audit
propagation, and numerical-failure translation.  They do not establish a
physical impurity interpretation or scientific validation of any model.
"""

import warnings
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    IncompatibleOperatorRecordsError,
    OperatorRecord,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
    OperatorRecordDifferencer,
    OperatorRecordDifferenceResult,
    StateSpace,
)

pytestmark = pytest.mark.software_verification

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_record(
    matrix: Any, *, identifier: str, energy_unit: str = "eV"
) -> OperatorRecord:
    """Construct a deterministic synthetic operator record fixture.

    Parameters
    ----------
    matrix
        Matrix used by the public ``OperatorRecord`` constructor. The matrix
        dimension determines the synthetic state-space dimension and basis
        ordering.
    identifier
        Record identifier used to build deterministic related metadata.
    energy_unit
        Energy unit. The default produces mutually compatible records; changing
        this value intentionally creates an exact compatibility mismatch.

    Returns
    -------
    OperatorRecord
        Valid synthetic record suitable for differencer software-verification
        tests.
    """

    dimension = int(np.asarray(matrix).shape[0])
    ordering = tuple(f"state-{index}" for index in range(dimension))
    return OperatorRecord(
        identifier,
        "finite_test_hamiltonian",
        matrix,
        StateSpace(f"space-{identifier}", "finite synthetic", dimension),
        Basis(f"basis-{identifier}", "site basis", ordering, True),
        Geometry(
            identifier,
            VALID_CELL,
            "periodic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", energy_unit),
        {"source": "unit test"},
    )


def test_differencer_retains_explicit_compatibility_analyzer_dependency() -> None:
    analyzer = OperatorRecordCompatibilityAnalyzer()

    differencer = OperatorRecordDifferencer(compatibility_analyzer=analyzer)

    assert differencer.compatibility_analyzer is analyzer


def test_differencer_rejects_non_analyzer_dependency() -> None:
    with pytest.raises(
        TypeError,
        match="compatibility_analyzer must be an OperatorRecordCompatibilityAnalyzer",
    ):
        OperatorRecordDifferencer(compatibility_analyzer=cast(Any, object()))


def test_differencer_forms_signed_candidate_minus_reference_for_real_matrix() -> None:
    reference = make_record(np.array([[3.0, 1.0], [0.0, 0.0]]), identifier="reference")
    candidate = make_record(np.array([[1.0, 4.0], [2.0, 0.0]]), identifier="candidate")

    result = OperatorRecordDifferencer().execute(reference, candidate)

    assert isinstance(result, OperatorRecordDifferenceResult)
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.energy_unit == "eV"
    assert result.compatibility_result.is_compatible
    assert result.compatibility_result.reference_identifier == "reference"
    assert result.compatibility_result.candidate_identifier == "candidate"
    np.testing.assert_array_equal(
        result.matrix, np.array([[-2.0, 3.0], [2.0, 0.0]], dtype=np.complex128)
    )
    assert not np.array_equal(
        result.matrix, np.array([[2.0, -3.0], [-2.0, 0.0]], dtype=np.complex128)
    )


def test_differencer_forms_signed_candidate_minus_reference_for_complex_matrix() -> (
    None
):
    reference = make_record(
        np.array([[1.0 + 2.0j, 3.0 - 1.0j], [0.0 + 0.0j, 2.0j]], dtype=np.complex128),
        identifier="reference",
    )
    candidate = make_record(
        np.array(
            [[4.0 - 1.0j, -1.0 + 5.0j], [1.0 - 1.0j, 3.0 + 0.0j]], dtype=np.complex128
        ),
        identifier="candidate",
    )

    result = OperatorRecordDifferencer().execute(reference, candidate)

    assert isinstance(result, OperatorRecordDifferenceResult)
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.energy_unit == "eV"
    assert result.compatibility_result.is_compatible
    assert result.compatibility_result.reference_identifier == "reference"
    assert result.compatibility_result.candidate_identifier == "candidate"
    np.testing.assert_array_equal(
        result.matrix,
        np.array(
            [[3.0 - 3.0j, -4.0 + 6.0j], [1.0 - 1.0j, 3.0 - 2.0j]], dtype=np.complex128
        ),
    )
    assert not np.array_equal(
        result.matrix,
        np.array(
            [[-3.0 + 3.0j, 4.0 - 6.0j], [-1.0 + 1.0j, -3.0 + 2.0j]], dtype=np.complex128
        ),
    )


def test_differencer_propagates_structured_incompatible_records_error() -> None:
    reference = make_record(np.zeros((1, 1)), identifier="reference", energy_unit="eV")
    candidate = make_record(
        np.zeros((1, 1)), identifier="candidate", energy_unit="hartree"
    )

    with pytest.raises(IncompatibleOperatorRecordsError) as exc_info:
        OperatorRecordDifferencer().execute(reference, candidate)

    compatibility_result = exc_info.value.compatibility_result
    assert compatibility_result.reference_identifier == "reference"
    assert compatibility_result.candidate_identifier == "candidate"
    assert tuple(issue.code for issue in compatibility_result.issues) == (
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
    )


def test_differencer_enforces_compatibility_before_subtraction_without_warning() -> (
    None
):
    reference = make_record(
        np.array([[-1.0e308]], dtype=np.complex128),
        identifier="reference",
        energy_unit="eV",
    )
    candidate = make_record(
        np.array([[1.0e308]], dtype=np.complex128),
        identifier="candidate",
        energy_unit="hartree",
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(IncompatibleOperatorRecordsError) as exc_info:
            OperatorRecordDifferencer().execute(reference, candidate)

    assert tuple(
        issue.code for issue in exc_info.value.compatibility_result.issues
    ) == (OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,)


def test_differencer_requires_operator_record_inputs() -> None:
    record = make_record(np.zeros((1, 1)), identifier="reference")

    with pytest.raises(TypeError, match="reference must be an OperatorRecord"):
        OperatorRecordDifferencer().execute(cast(Any, object()), record)
    with pytest.raises(TypeError, match="candidate must be an OperatorRecord"):
        OperatorRecordDifferencer().execute(record, cast(Any, object()))


def test_differencer_translates_nonfinite_subtraction_without_warning_escape() -> None:
    reference = make_record(np.array([[-1.0e308]]), identifier="reference")
    candidate = make_record(np.array([[1.0e308]]), identifier="candidate")

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(OperatorRecordDifferenceNumericalError) as exc_info:
            OperatorRecordDifferencer().execute(reference, candidate)

    assert (
        exc_info.value.code
        is OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    )
