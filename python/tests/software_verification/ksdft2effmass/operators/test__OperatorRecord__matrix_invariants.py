r"""Software verification of ``OperatorRecord``.

Facet and represented meaning

-----------------------------
This class-owned module owns the matrix invariants facet. Represented contract
--------------------
This facet owns matrix rank, shape, scalar semantics, finite-component and
conversion-range taxonomy, cross-object dimension agreement, and the
record-level orthonormal-basis requirement for
:math:`\mathbf H\in\mathbb C^{N\times N}`.

Ownership and interpretation
----------------------------
These are intrinsic software representation invariants. ``Basis`` independently
admits ``orthonormal=False`` metadata; ``OperatorRecord`` rejects that state for a
represented schema-version-1 record. No test calls private methods, computes
Hermiticity, norms, residuals, subtraction, or compatibility rules. The approved
public/Sphinx contract is the oracle. Failure may indicate implementation,
documentation, or evidence defects rather than physical-model invalidity.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-OR-008`` through
``SV-OR-017``. It performs no scientific numerical algorithm, so numerical
verification is not applicable. Scientific validation, uncertainty
quantification, and Rust conformance have not been performed.

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

import warnings
from typing import Any, cast

import numpy as np
import pytest
from operator_record_fixtures import make_basis, make_record, make_state_space

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification

SUT = OperatorRecord


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param(1.0, id="sv_or_008_scalar"),
        pytest.param([1.0, 2.0], id="dimensional_list"),
        pytest.param(np.array([1.0, 2.0]), id="dimensional_array"),
        pytest.param(np.ones((1, 1, 1)), id="dimensional_array"),
        pytest.param([[[1.0]]], id="dimensional_list"),
    ],
)
def test_constructor__invalid_matrix_rank_is_rejected__is_enforced(
    matrix: object,
) -> None:
    r"""Evidence ID: SV-OR-008

    Requirement: A matrix representation is exactly two-dimensional.

    Method: Pass approved numerical containers with invalid rank at the deliberate
    invalid
    public boundary using ``Any`` only there.

    Oracle: The public rank invariant fixes ``ValueError`` and the two-dimensional
    semantic
    diagnostic.

    Acceptance: Every case raises ``ValueError`` identifying two-dimensional form.

    Interpretation: Passing establishes stable rank rejection before matrix analysis.

    Limitations: It does not test squareness, physical dimensions, scientific
    validation, UQ, or Rust
    conformance.
    """

    with pytest.raises(ValueError, match="two-dimensional"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param([[1, 2, 3], [4, 5, 6]], id="sv_or_009_two_by_three"),
        pytest.param([[1, 2], [3, 4], [5, 6]], id="sv_or_009_three_by_two"),
    ],
)
def test_constructor__nonsquare_two_dimensional_matrices_are__is_enforced(
    matrix: list[list[int]],
) -> None:
    r"""Evidence ID: SV-OR-009

    Requirement: Represented operator matrices are square.

    Method: Construct from regular nested lists with unequal axis lengths.

    Oracle: Literal row/column counts independently determine nonsquareness.

    Acceptance: Each case raises ``ValueError`` identifying the square invariant.

    Interpretation: Passing establishes shape rejection independently of metadata
    dimensions.

    Limitations: No norm, Hermiticity, scientific validation, UQ, or Rust conformance is
    established.
    """

    with pytest.raises(ValueError, match="square"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param([[1], [2, 3]], id="sv_or_010_short_first_row"),
        pytest.param([[1, 2], [3]], id="sv_or_010_short_second_row"),
    ],
)
def test_constructor__input__ragged_nested_sequences_have_stable_public(
    matrix: list[list[int]],
) -> None:
    r"""Evidence ID: SV-OR-010

    Requirement: Nested rows form a rectangular two-dimensional array before conversion.

    Method: Pass ragged lists directly without NumPy preprocessing.

    Oracle: Literal row lengths independently establish raggedness.

    Acceptance: ``ValueError`` identifies non-ragged rectangular form; backend coercion
    wording is
    not exposed.

    Interpretation: Passing establishes deterministic public taxonomy for malformed
    shape.

    Limitations: It does not duplicate serializer malformed-payload evidence, scientific
    validation,
    UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="non-ragged rectangular"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "invalid_entry",
    [
        pytest.param(True, id="sv_or_011_boolean_true"),
        pytest.param(False, id="sv_or_011_boolean_false"),
        pytest.param(np.bool_(True), id="sv_or_011_numpy_boolean"),
        pytest.param("1.0", id="real_numeric_string"),
        pytest.param("1+2j", id="complex_numeric_string"),
        pytest.param(b"1.0", id="bytes"),
        pytest.param(None, id="none"),
        pytest.param(object(), id="sv_or_011_arbitrary_object"),
    ],
)
def test_constructor__invalid_matrix_scalar_wrong_types_are__is_enforced(
    invalid_entry: object,
) -> None:
    r"""Evidence ID: SV-OR-011

    Requirement: Entries are approved real/complex numeric scalars; Boolean, textual,
    null, and
    arbitrary values are not numbers for this contract.

    Method: Place each invalid value in one entry of an otherwise valid nested list and
    use
    ``Any`` only at the invalid constructor boundary.

    Oracle: The approved scalar taxonomy requires ``TypeError`` and numeric-scalar
    wording.

    Acceptance: Every case raises ``TypeError`` identifying matrix entries and numeric
    scalar
    semantics.

    Interpretation: Passing establishes rejection before NumPy can silently coerce
    values.

    Limitations: Finiteness is separate; no scientific validation, UQ, or Rust
    conformance is
    established.
    """

    matrix = [[cast(Any, invalid_entry), 0], [0, 1]]
    with pytest.raises(TypeError) as exc_info:
        make_record(cast(Any, matrix))

    message = str(exc_info.value)
    assert "matrix entries" in message
    assert "numeric" in message


@pytest.mark.parametrize(
    "nonfinite_real",
    [
        pytest.param(float("nan"), id="real_nan"),
        pytest.param(float("inf"), id="real_positive_infinity"),
        pytest.param(float("-inf"), id="real_negative_infinity"),
        pytest.param(complex(float("nan"), 1.0), id="real_finite_imaginary"),
    ],
)
def test_constructor__nonfinite_real_components_are_rejected__is_enforced(
    nonfinite_real: float | complex,
) -> None:
    r"""Evidence ID: SV-OR-012

    Requirement: Every stored real component is finite.

    Method: Place each semantically numerical value in a valid 2x2 matrix.

    Oracle: IEEE finiteness of the explicitly selected real component is independent of
    production conversion.

    Acceptance: Construction raises ``ValueError`` with finite-component semantics.

    Interpretation: Passing establishes finite real-component storage policy.

    Limitations: It computes no norm or physical metric and establishes no scientific
    validation, UQ,
    or Rust conformance.
    """

    with pytest.raises(ValueError, match="components must be finite"):
        make_record([[nonfinite_real, 0], [0, 1]])


@pytest.mark.parametrize(
    "nonfinite_imaginary",
    [
        pytest.param(complex(1.0, float("nan")), id="nan"),
        pytest.param(complex(1.0, float("inf")), id="positive_infinity"),
        pytest.param(complex(1.0, float("-inf")), id="negative_infinity"),
    ],
)
def test_constructor__nonfinite_imaginary_components_are_rejected__is_enforced(
    nonfinite_imaginary: complex,
) -> None:
    r"""Evidence ID: SV-OR-013

    Requirement: Every stored imaginary component is finite even when its real component
    is finite.

    Method: Place each explicit complex scalar in a valid 2x2 matrix.

    Oracle: IEEE finiteness of the independently selected imaginary component is the
    approved
    storage oracle.

    Acceptance: Construction raises ``ValueError`` with finite-component semantics.

    Interpretation: Passing establishes finite imaginary-component storage policy.

    Limitations: It computes no norm or physical metric and establishes no scientific
    validation, UQ,
    or Rust conformance.
    """

    with pytest.raises(ValueError, match="components must be finite"):
        make_record([[nonfinite_imaginary, 0], [0, 1]])


@pytest.mark.parametrize(
    "huge_integer",
    [
        pytest.param(10**1000, id="huge_positive_integer"),
        pytest.param(-(10**1000), id="huge_negative_integer"),
    ],
)
def test_constructor__complex128_conversion_overflow__raises_value_error(
    huge_integer: int,
) -> None:
    r"""Evidence ID: SV-OR-014

    Requirement: Huge Python integers map conversion overflow to finite-number
    ``ValueError``;
    largest finite binary64 entries remain admissible.

    Method: Construct with huge signed integers, then with signed maximum finite floats
    while
    promoting RuntimeWarning to an error.

    Oracle: Python arbitrary-precision magnitude and ``np.finfo(float64).max`` define
    overflow
    and representable boundaries independently.

    Acceptance: Huge integers raise ``ValueError`` without leaked ``OverflowError``;
    finite extremes
    are stored exactly without RuntimeWarning.

    Interpretation: Passing establishes storage-range policy without a norm calculation.

    Limitations: It does not promise later algorithms cannot overflow or establish
    scientific
    validation, UQ, or Rust conformance.
    """
    with pytest.raises(ValueError, match="finite complex128"):
        make_record([[huge_integer, 0], [0, 1]])


def test_constructor__finite_binary64_extremes__are_admitted_without_warning() -> None:
    r"""Evidence ID: SV-OR-044

    Requirement: Signed maximum finite binary64 matrix entries remain representable.

    Method: Construct a diagonal matrix under RuntimeWarning-as-error.

    Oracle: ``np.finfo(np.float64).max`` is the finite binary64 boundary.

    Acceptance: Construction emits no RuntimeWarning and stores both signs exactly.

    Interpretation: A pass confirms finite-boundary admission; failure indicates
    conversion drift.

    Limitations: Later algorithm overflow, physical meaning, validation, UQ, and Rust
    are excluded.
    """
    maximum = np.finfo(np.float64).max
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        record = make_record([[maximum, 0], [0, -maximum]])
    assert record.matrix[0, 0] == complex(maximum)
    assert record.matrix[1, 1] == complex(-maximum)


def test_constructor__matrix_dimension_must_match_state_space__is_enforced() -> None:
    r"""Evidence ID: SV-OR-015

    Requirement: Matrix axis dimension equals ``state_space.dimension``.

    Method: Supply a 3x3 matrix, dimension-two StateSpace, and length-three Basis so
    basis
    length does not cause the selected first failure.

    Oracle: Literal matrix and dependency dimensions establish disagreement.

    Acceptance: Field-specific ``ValueError`` identifies matrix/state-space dimension.

    Interpretation: Passing establishes the cross-object invariant in its diagnostic
    order.

    Limitations: It does not infer dependencies from malformed matrices or establish
    scientific
    validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="matrix dimension.*state-space dimension"):
        make_record(
            np.eye(3),
            state_space=make_state_space(dimension=2),
            basis=make_basis(ordering=("a", "b", "c")),
        )


def test_constructor__basis_ordering_length_must_match_state__is_enforced() -> None:
    r"""Evidence ID: SV-OR-016

    Requirement: ``len(basis.ordering) == state_space.dimension``.

    Method: Supply an agreeing 2x2 matrix and dimension-two StateSpace with an
    independently
    valid one-label Basis.

    Oracle: Literal dependency dimensions establish the single disagreement.

    Acceptance: Field-specific ``ValueError`` identifies basis ordering and state space.

    Interpretation: Passing establishes index-order metadata agreement.

    Limitations: It does not mutate dependencies, test Basis intrinsic invariants, or
    establish
    scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="basis ordering length.*state-space"):
        make_record(
            [[1, 0], [0, 1]],
            state_space=make_state_space(dimension=2),
            basis=make_basis(ordering=("a",)),
        )


def test_constructor__operator_record_requires_independently__is_enforced() -> None:
    r"""Evidence ID: SV-OR-017

    Requirement: OperatorRecord requires ``basis.orthonormal is True`` while standalone
    Basis permits
    ``False``.

    Method: Construct an ordinary valid two-label Basis carrying ``False`` and pass it
    with
    otherwise agreeing record state.

    Oracle: The approved ownership boundary assigns this restriction to the record.

    Acceptance: Basis construction succeeds; record construction raises field-specific
    ``ValueError``.

    Interpretation: Passing preserves Basis validity while enforcing record
    representation.

    Limitations: It performs no numerical orthogonality proof, scientific validation,
    UQ, or Rust
    conformance.
    """

    basis = make_basis(orthonormal=False)
    assert basis.orthonormal is False

    with pytest.raises(ValueError, match="orthonormal basis"):
        make_record(basis=basis)
