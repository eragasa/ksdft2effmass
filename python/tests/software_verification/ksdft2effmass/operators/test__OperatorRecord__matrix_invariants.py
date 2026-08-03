r"""Software verification of ``OperatorRecord`` matrix invariants.

Represented contract
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
"""

import warnings
from typing import Any, cast

import numpy as np
import pytest
from operator_record_fixtures import make_basis, make_record, make_state_space

pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param(1.0, id="SV-OR-008-scalar"),
        pytest.param([1.0, 2.0], id="SV-OR-008-one-dimensional-list"),
        pytest.param(np.array([1.0, 2.0]), id="SV-OR-008-one-dimensional-array"),
        pytest.param(np.ones((1, 1, 1)), id="SV-OR-008-three-dimensional-array"),
        pytest.param([[[1.0]]], id="SV-OR-008-three-dimensional-list"),
    ],
)
def test_invalid_matrix_rank_is_rejected(matrix: object) -> None:
    """SV-OR-008: reject scalar, vector, and rank-three matrix inputs.

    Evidence ID
        ``SV-OR-008``; stable IDs identify rank/container cases.
    Requirement
        A matrix representation is exactly two-dimensional.
    Method
        Pass approved numerical containers with invalid rank at the deliberate
        invalid public boundary using ``Any`` only there.
    Oracle
        The public rank invariant fixes ``ValueError`` and the two-dimensional
        semantic diagnostic.
    Acceptance
        Every case raises ``ValueError`` identifying two-dimensional form.
    Interpretation
        Passing establishes stable rank rejection before matrix analysis.
    Limitations
        It does not test squareness, physical dimensions, scientific validation,
        UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="two-dimensional"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param([[1, 2, 3], [4, 5, 6]], id="SV-OR-009-two-by-three"),
        pytest.param([[1, 2], [3, 4], [5, 6]], id="SV-OR-009-three-by-two"),
    ],
)
def test_nonsquare_two_dimensional_matrices_are_rejected(
    matrix: list[list[int]],
) -> None:
    """SV-OR-009: reject rectangular matrices in both orientations.

    Evidence ID
        ``SV-OR-009``; IDs identify 2x3 and 3x2 shapes.
    Requirement
        Represented operator matrices are square.
    Method
        Construct from regular nested lists with unequal axis lengths.
    Oracle
        Literal row/column counts independently determine nonsquareness.
    Acceptance
        Each case raises ``ValueError`` identifying the square invariant.
    Interpretation
        Passing establishes shape rejection independently of metadata dimensions.
    Limitations
        No norm, Hermiticity, scientific validation, UQ, or Rust conformance is
        established.
    """

    with pytest.raises(ValueError, match="square"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "matrix",
    [
        pytest.param([[1], [2, 3]], id="SV-OR-010-short-first-row"),
        pytest.param([[1, 2], [3]], id="SV-OR-010-short-second-row"),
    ],
)
def test_ragged_nested_sequences_have_stable_public_rejection(
    matrix: list[list[int]],
) -> None:
    """SV-OR-010: reject ragged nested sequences with owned diagnostics.

    Evidence ID
        ``SV-OR-010``; stable IDs identify both ragged orientations.
    Requirement
        Nested rows form a rectangular two-dimensional array before conversion.
    Method
        Pass ragged lists directly without NumPy preprocessing.
    Oracle
        Literal row lengths independently establish raggedness.
    Acceptance
        ``ValueError`` identifies non-ragged rectangular form; backend coercion
        wording is not exposed.
    Interpretation
        Passing establishes deterministic public taxonomy for malformed shape.
    Limitations
        It does not duplicate serializer malformed-payload evidence, scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="non-ragged rectangular"):
        make_record(cast(Any, matrix))


@pytest.mark.parametrize(
    "invalid_entry",
    [
        pytest.param(True, id="SV-OR-011-boolean-true"),
        pytest.param(False, id="SV-OR-011-boolean-false"),
        pytest.param(np.bool_(True), id="SV-OR-011-numpy-boolean"),
        pytest.param("1.0", id="SV-OR-011-real-numeric-string"),
        pytest.param("1+2j", id="SV-OR-011-complex-numeric-string"),
        pytest.param(b"1.0", id="SV-OR-011-bytes"),
        pytest.param(None, id="SV-OR-011-none"),
        pytest.param(object(), id="SV-OR-011-arbitrary-object"),
    ],
)
def test_invalid_matrix_scalar_semantic_types_are_rejected(
    invalid_entry: object,
) -> None:
    """SV-OR-011: reject nonnumeric scalar semantics without coercion.

    Evidence ID
        ``SV-OR-011``; IDs distinguish every rejected semantic family.
    Requirement
        Entries are approved real/complex numeric scalars; Boolean, textual,
        null, and arbitrary values are not numbers for this contract.
    Method
        Place each invalid value in one entry of an otherwise valid nested list
        and use ``Any`` only at the invalid constructor boundary.
    Oracle
        The approved scalar taxonomy requires ``TypeError`` and numeric-scalar
        wording.
    Acceptance
        Every case raises ``TypeError`` identifying matrix entries and numeric
        scalar semantics.
    Interpretation
        Passing establishes rejection before NumPy can silently coerce values.
    Limitations
        Finiteness is separate; no scientific validation, UQ, or Rust conformance
        is established.
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
        pytest.param(float("nan"), id="SV-OR-012-real-nan"),
        pytest.param(float("inf"), id="SV-OR-012-real-positive-infinity"),
        pytest.param(float("-inf"), id="SV-OR-012-real-negative-infinity"),
        pytest.param(
            complex(float("nan"), 1.0),
            id="SV-OR-012-nonfinite-real-finite-imaginary",
        ),
    ],
)
def test_nonfinite_real_components_are_rejected(
    nonfinite_real: float | complex,
) -> None:
    """SV-OR-012: reject nonfinite real components independently.

    Evidence ID
        ``SV-OR-012``; IDs identify NaN and signed infinities.
    Requirement
        Every stored real component is finite.
    Method
        Place each semantically numerical value in a valid 2x2 matrix.
    Oracle
        IEEE finiteness of the explicitly selected real component is independent
        of production conversion.
    Acceptance
        Construction raises ``ValueError`` with finite-component semantics.
    Interpretation
        Passing establishes finite real-component storage policy.
    Limitations
        It computes no norm or physical metric and establishes no scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="components must be finite"):
        make_record([[nonfinite_real, 0], [0, 1]])


@pytest.mark.parametrize(
    "nonfinite_imaginary",
    [
        pytest.param(complex(1.0, float("nan")), id="SV-OR-013-imaginary-nan"),
        pytest.param(
            complex(1.0, float("inf")),
            id="SV-OR-013-imaginary-positive-infinity",
        ),
        pytest.param(
            complex(1.0, float("-inf")),
            id="SV-OR-013-imaginary-negative-infinity",
        ),
    ],
)
def test_nonfinite_imaginary_components_are_rejected(
    nonfinite_imaginary: complex,
) -> None:
    """SV-OR-013: reject nonfinite imaginary components independently.

    Evidence ID
        ``SV-OR-013``; IDs identify NaN and signed infinities.
    Requirement
        Every stored imaginary component is finite even when its real component
        is finite.
    Method
        Place each explicit complex scalar in a valid 2x2 matrix.
    Oracle
        IEEE finiteness of the independently selected imaginary component is the
        approved storage oracle.
    Acceptance
        Construction raises ``ValueError`` with finite-component semantics.
    Interpretation
        Passing establishes finite imaginary-component storage policy.
    Limitations
        It computes no norm or physical metric and establishes no scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="components must be finite"):
        make_record([[nonfinite_imaginary, 0], [0, 1]])


def test_conversion_overflow_is_translated_and_finite_extremes_are_admitted() -> None:
    """SV-OR-014: enforce complex128 conversion-range taxonomy.

    Evidence ID
        ``SV-OR-014``.
    Requirement
        Huge Python integers map conversion overflow to finite-number
        ``ValueError``; largest finite binary64 entries remain admissible.
    Method
        Construct with huge signed integers, then with signed maximum finite
        floats while promoting RuntimeWarning to an error.
    Oracle
        Python arbitrary-precision magnitude and ``np.finfo(float64).max`` define
        overflow and representable boundaries independently.
    Acceptance
        Huge integers raise ``ValueError`` without leaked ``OverflowError``;
        finite extremes are stored exactly without RuntimeWarning.
    Interpretation
        Passing establishes storage-range policy without a norm calculation.
    Limitations
        It does not promise later algorithms cannot overflow or establish
        scientific validation, UQ, or Rust conformance.
    """

    for huge_integer in (10**1000, -(10**1000)):
        with pytest.raises(ValueError, match="finite complex128"):
            make_record([[huge_integer, 0], [0, 1]])

    maximum = np.finfo(np.float64).max
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        record = make_record([[maximum, 0], [0, -maximum]])

    assert record.matrix[0, 0] == complex(maximum)
    assert record.matrix[1, 1] == complex(-maximum)


def test_matrix_dimension_must_match_state_space_dimension() -> None:
    """SV-OR-015: isolate matrix/StateSpace dimension disagreement.

    Evidence ID
        ``SV-OR-015``.
    Requirement
        Matrix axis dimension equals ``state_space.dimension``.
    Method
        Supply a 3x3 matrix, dimension-two StateSpace, and length-three Basis so
        basis length does not cause the selected first failure.
    Oracle
        Literal matrix and dependency dimensions establish disagreement.
    Acceptance
        Field-specific ``ValueError`` identifies matrix/state-space dimension.
    Interpretation
        Passing establishes the cross-object invariant in its diagnostic order.
    Limitations
        It does not infer dependencies from malformed matrices or establish
        scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="matrix dimension.*state-space dimension"):
        make_record(
            np.eye(3),
            state_space=make_state_space(dimension=2),
            basis=make_basis(ordering=("a", "b", "c")),
        )


def test_basis_ordering_length_must_match_state_space_dimension() -> None:
    """SV-OR-016: isolate Basis-ordering/StateSpace disagreement.

    Evidence ID
        ``SV-OR-016``.
    Requirement
        ``len(basis.ordering) == state_space.dimension``.
    Method
        Supply an agreeing 2x2 matrix and dimension-two StateSpace with an
        independently valid one-label Basis.
    Oracle
        Literal dependency dimensions establish the single disagreement.
    Acceptance
        Field-specific ``ValueError`` identifies basis ordering and state space.
    Interpretation
        Passing establishes index-order metadata agreement.
    Limitations
        It does not mutate dependencies, test Basis intrinsic invariants, or
        establish scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="basis ordering length.*state-space"):
        make_record(
            [[1, 0], [0, 1]],
            state_space=make_state_space(dimension=2),
            basis=make_basis(ordering=("a",)),
        )


def test_operator_record_requires_independently_valid_orthonormal_basis() -> None:
    """SV-OR-017: enforce the record-level orthonormal-basis restriction.

    Evidence ID
        ``SV-OR-017``.
    Requirement
        OperatorRecord requires ``basis.orthonormal is True`` while standalone
        Basis permits ``False``.
    Method
        Construct an ordinary valid two-label Basis carrying ``False`` and pass
        it with otherwise agreeing record state.
    Oracle
        The approved ownership boundary assigns this restriction to the record.
    Acceptance
        Basis construction succeeds; record construction raises field-specific
        ``ValueError``.
    Interpretation
        Passing preserves Basis validity while enforcing record representation.
    Limitations
        It performs no numerical orthogonality proof, scientific validation, UQ,
        or Rust conformance.
    """

    basis = make_basis(orthonormal=False)
    assert basis.orthonormal is False

    with pytest.raises(ValueError, match="orthonormal basis"):
        make_record(basis=basis)
