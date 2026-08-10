r"""Software verification of ``OperatorRecordDifferenceResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the invariants facet.

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

from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordDifferenceResult


class CustomArray(np.ndarray):
    r"""Synthetic ndarray subclass for strict public-boundary tests."""


def compatible_result() -> OperatorRecordCompatibilityResult:
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
    return OperatorRecordCompatibilityResult("reference", "candidate", ())


def test_constructor__requires_exact_compatibility_result_type__is_enforced() -> None:
    r"""Evidence ID: SV-ORDR-004

    Requirement: OperatorRecordDifferenceResult equality is exact over
    compatibility_result, matrix,
    and energy_unit, and rejects unrelated types.

    Method: Construct valid baseline instances, change only the named requires exact
    compatibility result type: is enforced partition, and observe constructor, field,
    equality, hash, or public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    matrix = np.zeros((1, 1), dtype=np.complex128)

    with pytest.raises(TypeError, match="OperatorRecordCompatibilityResult"):
        OperatorRecordDifferenceResult(cast(Any, object()), matrix, "eV")


def test_constructor__requires_compatible_audit_result__is_enforced() -> None:
    r"""Evidence ID: SV-ORDR-005

    Requirement: OperatorRecordDifferenceResult equality is exact over
    compatibility_result, matrix,
    and energy_unit, and rejects unrelated types.

    Method: Construct valid baseline instances, change only the named requires
    compatible audit
    result: is enforced partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

    Acceptance: The named partition raises exactly ValueError with the asserted public
    message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    )
    incompatible = OperatorRecordCompatibilityResult("reference", "candidate", (issue,))

    with pytest.raises(ValueError, match="compatible"):
        OperatorRecordDifferenceResult(
            incompatible, np.zeros((1, 1), dtype=np.complex128), "eV"
        )


@pytest.mark.parametrize(
    "energy_unit, error",
    [
        pytest.param("", ValueError, id="documented_partition"),
        pytest.param(1, TypeError, id="scalar_rank_one"),
    ],
)
def test_constructor__requires_nonempty_builtin_energy_unit__is_enforced(
    energy_unit: Any, error: type[Exception]
) -> None:
    r"""Evidence ID: SV-ORDR-006

    Requirement: OperatorRecordDifferenceResult equality is exact over
    compatibility_result, matrix,
    and energy_unit, and rejects unrelated types.

    Method: Construct valid baseline instances, change only the named requires nonempty
    builtin
    energy unit: is enforced partition, and observe constructor, field, equality, hash,
    or public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

    Acceptance: The named partition raises exactly error with the asserted public
    message, code, or
    attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(error, match="energy_unit"):
        OperatorRecordDifferenceResult(
            compatible_result(), np.zeros((1, 1), dtype=np.complex128), energy_unit
        )


@pytest.mark.parametrize(
    "matrix, error, message",
    [
        pytest.param(
            [[1.0]], TypeError, "exact NumPy ndarray", id="exact_numpy_ndarray"
        ),
        pytest.param(
            np.array([[1.0]], dtype=np.float64),
            TypeError,
            "np.complex128",
            id="np_complex128",
        ),
        pytest.param(
            np.array([[1.0 + 0j]], dtype=np.complex128).view(CustomArray),
            TypeError,
            "exact NumPy ndarray",
            id="exact_numpy_ndarray",
        ),
        pytest.param(
            np.array([1.0 + 0j], dtype=np.complex128), ValueError, "square", id="square"
        ),
        pytest.param(
            np.ones((1, 2), dtype=np.complex128), ValueError, "square", id="square"
        ),
        pytest.param(
            np.zeros((0, 0), dtype=np.complex128), ValueError, "positive", id="positive"
        ),
        pytest.param(
            np.array([[np.inf + 0j]], dtype=np.complex128),
            ValueError,
            "finite",
            id="finite",
        ),
        pytest.param(
            np.array([[1.0 + np.nan * 1j]], dtype=np.complex128),
            ValueError,
            "finite",
            id="finite",
        ),
    ],
)
def test_constructor__requires_matrix_intrinsic_invariants__is_enforced(
    matrix: Any, error: type[Exception], message: str
) -> None:
    r"""Evidence ID: SV-ORDR-007

    Requirement: OperatorRecordDifferenceResult equality is exact over
    compatibility_result, matrix,
    and energy_unit, and rejects unrelated types.

    Method: Construct valid baseline instances, change only the named requires matrix
    intrinsic
    invariants: is enforced partition, and observe constructor, field, equality, hash,
    or public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

    Acceptance: The named partition raises exactly error with the asserted public
    message, code, or
    attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(error, match=message):
        OperatorRecordDifferenceResult(compatible_result(), cast(Any, matrix), "eV")


def test_field__rejects_numpy_matrix_subclass__is_exact() -> None:
    r"""Evidence ID: SV-ORDR-008

    Requirement: OperatorRecordDifferenceResult enforces this represented-data
    partition: rejects
    numpy matrix subclass: is exact.

    Method: Construct valid baseline instances, change only the named rejects numpy
    matrix
    subclass: is exact partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    with pytest.warns(PendingDeprecationWarning):
        matrix = np.matrix([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(TypeError, match="exact NumPy ndarray"):
        OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")


def test_constructor__input_boundary__rejects_numpy_memmap(tmp_path: Path) -> None:
    r"""Evidence ID: SV-ORDR-009

    Requirement: OperatorRecordDifferenceResult enforces this represented-data
    partition: input
    boundary: rejects numpy memmap.

    Method: Construct valid baseline instances, change only the named input boundary:
    rejects
    numpy memmap partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.

    Oracle: The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.

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
    memmap_path = tmp_path / "difference.dat"
    matrix = np.memmap(memmap_path, dtype=np.complex128, mode="w+", shape=(1, 1))
    matrix[0, 0] = 1.0 + 0.0j

    with pytest.raises(TypeError, match="exact NumPy ndarray"):
        OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")
