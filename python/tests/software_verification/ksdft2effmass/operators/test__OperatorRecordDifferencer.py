r"""Software verification of ``OperatorRecordDifferencer``.

Facet and represented meaning

-----------------------------
This class-owned module owns the OperatorRecordDifferencer facet. The tested
ActionObject enforces compatibility before forming the represented
operator difference with sign convention
``Delta H = H_candidate - H_reference``.  It translates numerical overflow in
that direct represented subtraction into a structured public difference error.
These tests verify the software contract for dependency validation,
compatibility enforcement, execution ordering, signed subtraction, metadata/audit
propagation, and numerical-failure translation.  They do not establish a
physical impurity interpretation or scientific validation of any model.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordDifferencer``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
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

SUT = OperatorRecordDifferencer

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_record(
    matrix: Any, *, identifier: str, energy_unit: str = "eV"
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Differencer and comparator cases require independently valid synthetic
    records with
    controlled identifiers, matrices, and energy units.

    Method: Construct or inspect only the named synthetic fixture operation (make
    record); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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


def test_method__execute__differencer_retains_explicit_compatibility_analyzer() -> None:
    r"""Evidence ID: SV-ORD-001

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: differencer retains explicit compatibility analyzer.

    Method: Construct independently valid reference and candidate records for execute:
    differencer retains explicit compatibility analyzer, then invoke execute() and
    inspect only public results or errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    analyzer = OperatorRecordCompatibilityAnalyzer()

    differencer = OperatorRecordDifferencer(compatibility_analyzer=analyzer)

    assert differencer.compatibility_analyzer is analyzer


def test_method__execute__differencer_rejects_non_analyzer_dependency() -> None:
    r"""Evidence ID: SV-ORD-002

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: differencer rejects non analyzer dependency.

    Method: Construct independently valid reference and candidate records for execute:
    differencer rejects non analyzer dependency, then invoke execute() and inspect only
    public results or errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(
        TypeError,
        match="compatibility_analyzer must be an OperatorRecordCompatibilityAnalyzer",
    ):
        OperatorRecordDifferencer(compatibility_analyzer=cast(Any, object()))


def test_method__execute__forms_signed_real_difference() -> None:
    r"""Evidence ID: SV-ORD-003

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: forms signed real difference.

    Method: Construct independently valid reference and candidate records for execute:
    forms
    signed real difference, then invoke execute() and inspect only public results or
    errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
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


def test_method__execute__complex_candidate_minus_reference() -> None:
    r"""Evidence ID: SV-ORD-004

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: complex candidate minus reference.

    Method: Construct independently valid reference and candidate records for execute:
    complex
    candidate minus reference, then invoke execute() and inspect only public results or
    errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
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


def test_method__execute__propagates_incompatibility() -> None:
    r"""Evidence ID: SV-ORD-005

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: propagates incompatibility.

    Method: Construct independently valid reference and candidate records for execute:
    propagates incompatibility, then invoke execute() and inspect only public results or
    errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The named partition raises exactly IncompatibleOperatorRecordsError with
    the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
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


def test_method__execute__checks_compatibility_first() -> None:
    r"""Evidence ID: SV-ORD-006

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: checks compatibility first.

    Method: Construct independently valid reference and candidate records for execute:
    checks
    compatibility first, then invoke execute() and inspect only public results or
    errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The named partition raises exactly IncompatibleOperatorRecordsError with
    the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
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


def test_method__execute__differencer_requires_operator_record_inputs() -> None:
    r"""Evidence ID: SV-ORD-007

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: differencer requires operator record inputs.

    Method: Construct independently valid reference and candidate records for execute:
    differencer requires operator record inputs, then invoke execute() and inspect only
    public results or errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    record = make_record(np.zeros((1, 1)), identifier="reference")

    with pytest.raises(TypeError, match="reference must be an OperatorRecord"):
        OperatorRecordDifferencer().execute(cast(Any, object()), record)
    with pytest.raises(TypeError, match="candidate must be an OperatorRecord"):
        OperatorRecordDifferencer().execute(record, cast(Any, object()))


def test_method__execute__differencer_translates_nonfinite_subtraction_without() -> (
    None
):
    r"""Evidence ID: SV-ORD-008

    Requirement: OperatorRecordDifferencer publicly enforces the
    candidate-minus-reference operation
    partition: execute: differencer translates nonfinite subtraction without.

    Method: Construct independently valid reference and candidate records for execute:
    differencer translates nonfinite subtraction without, then invoke execute() and
    inspect only public results or errors.

    Oracle: Literal elementwise candidate-minus-reference arithmetic, exact metadata,
    compatibility rules, and the public structured-error taxonomy determine the result
    independently of the differencer implementation.

    Acceptance: The named partition raises exactly
    OperatorRecordDifferenceNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
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
