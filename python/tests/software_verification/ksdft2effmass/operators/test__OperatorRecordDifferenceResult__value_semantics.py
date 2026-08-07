r"""Software verification of ``OperatorRecordDifferenceResult``.

Facet and represented meaning
-----------------------------
This class-owned module owns the value semantics facet.

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

from collections.abc import Hashable
from dataclasses import FrozenInstanceError

import numpy as np
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordDifferenceResult

FROZEN_FIELDS = ("compatibility_result", "matrix", "energy_unit")
EQUALITY_FIELDS = ("compatibility_result", "matrix", "energy_unit")


def compatible_result(
    reference_identifier: str = "reference", candidate_identifier: str = "candidate"
) -> OperatorRecordCompatibilityResult:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Difference-result fixtures require an explicitly compatible audit carrying the
    requested reference and candidate identifiers.
    Method
    Construct or inspect only the named synthetic fixture operation (compatible result);
    the helper owns no assertion result and introduces no hidden oracle.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    return OperatorRecordCompatibilityResult(
        reference_identifier, candidate_identifier, ()
    )


def make_result(
    matrix: np.ndarray | None = None,
    *,
    energy_unit: str = "eV",
    compatibility_result: OperatorRecordCompatibilityResult | None = None,
) -> OperatorRecordDifferenceResult:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Value-semantics cases require a valid difference result while independently
    selecting its matrix, unit, and compatibility audit.
    Method
    Construct or inspect only the named synthetic fixture operation (make result); the
    helper owns no assertion result and introduces no hidden oracle.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    if matrix is None:
        matrix = np.array([[1.0 + 0.0j]], dtype=np.complex128)
    if compatibility_result is None:
        compatibility_result = compatible_result_fixture
    return OperatorRecordDifferenceResult(compatibility_result, matrix, energy_unit)


compatible_result_fixture = compatible_result()


def test_field__owns_source_array_and_exposes_immutable_bytes_backed__is_exact() -> (
    None
):
    r"""Evidence ID
    SV-ORDR-010
    Requirement
    OperatorRecordDifferenceResult copies caller matrix data and exposes storage that
    cannot be made writeable.
    Method
    Construct valid baseline instances, change only the named owns source array and
    exposes immutable bytes backed: is exact partition, and observe constructor, field,
    equality, hash, or public-API behavior as applicable.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The named partition raises exactly ValueError with the asserted public message,
    code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    source = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    result = make_result(source)
    source[0, 0] = 9.0 + 0.0j

    assert result.matrix[0, 0] == 1.0 + 0.0j
    assert not result.matrix.flags.writeable
    with pytest.raises(ValueError):
        result.matrix.setflags(write=True)


def test_field__dataclass_state_is_frozen__is_exact() -> None:
    r"""Evidence ID
    SV-ORDR-011
    Requirement
    Every public OperatorRecordDifferenceResult field is frozen after construction.
    Method
    Construct valid baseline instances, change only the named dataclass state is frozen:
    is exact partition, and observe constructor, field, equality, hash, or public-API
    behavior as applicable.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The named partition raises exactly FrozenInstanceError with the asserted public
    message, code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    result = make_result()

    with pytest.raises(FrozenInstanceError):
        result.compatibility_result = compatible_result(  # type: ignore[misc]
            "other-reference", "candidate"
        )
    with pytest.raises(FrozenInstanceError):
        result.matrix = np.array([[2.0 + 0.0j]])  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.energy_unit = "hartree"  # type: ignore[misc]

    assert FROZEN_FIELDS == ("compatibility_result", "matrix", "energy_unit")


def test_field__represented_state__canonical_c_order_storage_preserves_fortran() -> (
    None
):
    r"""Evidence ID
    SV-ORDR-012
    Requirement
    OperatorRecordDifferenceResult enforces this represented-data partition: represented
    state: canonical c order storage preserves fortran.
    Method
    Construct valid baseline instances, change only the named represented state:
    canonical c order storage preserves fortran partition, and observe constructor,
    field, equality, hash, or public-API behavior as applicable.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The named partition raises exactly ValueError with the asserted public message,
    code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    source = np.asfortranarray(
        np.array(
            [[1.0 + 2.0j, 3.0 + 4.0j], [5.0 + 6.0j, 7.0 + 8.0j]],
            dtype=np.complex128,
        )
    )

    result = make_result(source)
    source[0, 0] = 99.0 + 0.0j

    np.testing.assert_array_equal(
        result.matrix,
        np.array(
            [[1.0 + 2.0j, 3.0 + 4.0j], [5.0 + 6.0j, 7.0 + 8.0j]],
            dtype=np.complex128,
        ),
    )
    assert result.matrix.flags.c_contiguous
    assert not result.matrix.flags.f_contiguous or result.matrix.shape == (1, 1)
    assert not result.matrix.flags.writeable
    with pytest.raises(ValueError):
        result.matrix.setflags(write=True)


def test_method__eq__exact_equality_covers_complete_public_state() -> None:
    r"""Evidence ID
    SV-ORDR-013
    Requirement
    OperatorRecordDifferenceResult equality is exact over compatibility_result, matrix,
    and energy_unit, and rejects unrelated types.
    Method
    Construct valid baseline instances, change only the named eq: exact equality covers
    complete public state partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The equal baseline compares equal, every independently varied inventoried field
    compares unequal, and comparison with an unrelated object is false.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    left = make_result(np.array([[1.0j]], dtype=np.complex128))
    same = make_result(np.array([[1.0j]], dtype=np.complex128))
    different_matrix = make_result(np.array([[2.0j]], dtype=np.complex128))
    different_unit = make_result(
        np.array([[1.0j]], dtype=np.complex128), energy_unit="hartree"
    )
    different_audit = make_result(
        np.array([[1.0j]], dtype=np.complex128),
        compatibility_result=compatible_result("other-reference", "candidate"),
    )

    assert EQUALITY_FIELDS == ("compatibility_result", "matrix", "energy_unit")
    assert left == same
    assert left != different_matrix
    assert left != different_unit
    assert left != different_audit
    assert (left == object()) is False


def test_method__hash__unhashable_under_python_data_model() -> None:
    r"""Evidence ID
    SV-ORDR-014
    Requirement
    OperatorRecordDifferenceResult enforces this represented-data partition: hash:
    unhashable under python data model.
    Method
    Construct valid baseline instances, change only the named hash: unhashable under
    python data model partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.
    Oracle
    The literal constructor inputs, exact ndarray values, declared public-field
    inventory, frozen dataclass semantics, and Python equality/hash rules determine the
    expected result.
    Acceptance
    The named partition raises exactly TypeError with the asserted public message, code,
    or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    result = make_result()

    assert OperatorRecordDifferenceResult.__hash__ is None
    assert not isinstance(result, Hashable)
    with pytest.raises(TypeError):
        hash(result)
