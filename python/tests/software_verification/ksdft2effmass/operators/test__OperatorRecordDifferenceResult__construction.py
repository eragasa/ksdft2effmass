r"""Software verification of ``OperatorRecordDifferenceResult``.

Facet and represented meaning

-----------------------------
This class-owned module owns the construction facet.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordDifferenceResult``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordDifferenceResult


def compatible_result(
    reference_identifier: str = "reference", candidate_identifier: str = "candidate"
) -> OperatorRecordCompatibilityResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Difference-result fixtures require an explicitly compatible audit
    carrying the
    requested reference and candidate identifiers.

    Method: Construct or inspect only the named synthetic fixture operation (compatible
    result);
    the helper owns no assertion result and introduces no hidden oracle.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    return OperatorRecordCompatibilityResult(
        reference_identifier, candidate_identifier, ()
    )


def test_constructor__constructs_valid_difference_result_with__is_enforced() -> None:
    r"""Evidence ID: SV-ORDR-001

    Requirement: OperatorRecordDifferenceResult enforces this represented-data
    partition: constructs
    valid difference result with: is enforced.

    Method: Construct valid baseline instances, change only the named constructs valid
    difference result with: is enforced partition, and observe constructor, field,
    equality, hash, or public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    matrix = np.array([[1.0 + 2.0j]], dtype=np.complex128)

    result = OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")

    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.energy_unit == "eV"
    assert result.shape == (1, 1)
    assert result.matrix_dimension == 1
    np.testing.assert_array_equal(result.matrix, matrix)


def test_field__accepts_arbitrary_positive_square_dimension__is_exact() -> None:
    r"""Evidence ID: SV-ORDR-002

    Requirement: OperatorRecordDifferenceResult enforces this represented-data
    partition: accepts
    arbitrary positive square dimension: is exact.

    Method: Construct valid baseline instances, change only the named accepts arbitrary
    positive
    square dimension: is exact partition, and observe constructor, field, equality,
    hash, or public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    matrix = np.eye(3, dtype=np.complex128)

    result = OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")

    assert result.shape == (3, 3)
    assert result.matrix_dimension == 3
    np.testing.assert_array_equal(result.matrix, matrix)


def test_public_api__unsupported_methods__are_absent() -> None:
    r"""Evidence ID: SV-ORDR-003

    Requirement: OperatorRecordDifferenceResult enforces this represented-data
    partition: unsupported
    methods: are absent.

    Method: Construct valid baseline instances, change only the named unsupported
    methods: are
    absent partition, and observe constructor, field, equality, hash, or public-API
    behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    result = OperatorRecordDifferenceResult(
        compatible_result(), np.zeros((1, 1), dtype=np.complex128), "eV"
    )

    assert not hasattr(result, "serialize")
    assert not hasattr(result, "deserialize")
    assert not hasattr(result, "to_impurity_operator")
