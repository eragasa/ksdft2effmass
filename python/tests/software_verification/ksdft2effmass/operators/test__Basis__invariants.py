r"""Software verification of ``Basis`` intrinsic constructor invariants.

Facet and represented meaning
-----------------------------
This module owns ordering-container admission; nonempty, string, and unique label
rules; independent identifier/kind rules; and exact Python Boolean typing. For
:math:`\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)`, labels define exact
ordered coordinates and are not normalized.

Intrinsic and cross-object scope
--------------------------------
``Basis`` owns these metadata invariants and tuple canonicalization.
``OperatorRecord`` separately owns ordering-length/matrix agreement and rejection
of nonorthonormal basis metadata. No vectors or overlap matrix exist here, so no
orthogonality calculation occurs. The approved architecture and Sphinx contract
are the oracle. Failure may indicate an implementation regression, contract or
documentation mismatch, or evidence defect.

VVUQ and scientific exclusions
------------------------------
This module provides only software-verification evidence ``SV-B-007`` through
``SV-B-016``. Passing establishes strict collection, label, string-field, and
Boolean metadata invariants. It establishes no linear independence, completeness,
numerical orthogonality, StateSpace dimension agreement, matrix compatibility,
gauge alignment, physical equivalence, scientific validation, uncertainty
quantification, or Rust conformance.
"""

from collections.abc import Generator
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import Basis

pytestmark = pytest.mark.software_verification


def label_generator() -> Generator[str]:
    """Yield labels for the invalid generator boundary in ``SV-B-007``.

    Evidence ID
        Supporting helper for ``SV-B-007``; it owns no separate identifier.
    Requirement
        A generator is an iterable but not an approved ordered-sequence input.
    Method
        Yield two abstract labels without materializing a sequence.
    Oracle
        The approved container contract explicitly excludes generators.
    Acceptance
        The caller receives a generator for deliberate invalid construction.
    Interpretation
        This isolates iterable rejection from label validity.
    Limitations
        It constructs no Basis and establishes no scientific validation, UQ, or
        Rust conformance.
    """

    yield "a"
    yield "b"


@pytest.mark.parametrize(
    "invalid_ordering",
    [
        pytest.param("ab", id="SV-B-007-bare-string"),
        pytest.param(b"ab", id="SV-B-007-bytes"),
        pytest.param(None, id="SV-B-007-none"),
        pytest.param(2, id="SV-B-007-integer"),
        pytest.param({"a", "b"}, id="SV-B-007-set"),
        pytest.param(frozenset({"a", "b"}), id="SV-B-007-frozenset"),
        pytest.param(label_generator(), id="SV-B-007-generator"),
        pytest.param({"a": 0, "b": 1}, id="SV-B-007-mapping"),
        pytest.param(object(), id="SV-B-007-arbitrary-object"),
    ],
)
def test_invalid_ordering_containers_are_rejected(invalid_ordering: object) -> None:
    """SV-B-007: reject non-approved ordering containers.

    Evidence ID
        ``SV-B-007`` with stable readable container-family IDs.
    Requirement
        Ordering admits ordered sequences, not bare text, unordered collections,
        mappings, generators, scalar values, or arbitrary objects.
    Method
        Use ``Any``/``cast`` only at the deliberate invalid constructor boundary.
    Oracle
        Basis order is semantic, so the approved runtime container contract
        excludes these representative inputs.
    Acceptance
        Every case raises exactly ``TypeError`` and identifies ``basis ordering``;
        non-text cases also identify the ordered-sequence requirement.
    Interpretation
        Passing establishes that arbitrary iterable consumption cannot silently
        choose or exhaust coordinate order.
    Limitations
        This does not enumerate every third-party sequence implementation and
        establishes no numerical/scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        Basis(
            identifier="canonical",
            kind="test basis",
            ordering=cast(Any, invalid_ordering),
            orthonormal=True,
        )

    message = str(exc_info.value)
    assert "basis ordering" in message
    if not isinstance(invalid_ordering, str | bytes):
        assert "ordered sequence" in message


@pytest.mark.parametrize(
    "ordering",
    [
        pytest.param((), id="SV-B-008-empty-tuple"),
        pytest.param([], id="SV-B-008-empty-list"),
    ],
)
def test_empty_ordering_sequences_are_rejected(
    ordering: tuple[str, ...] | list[str],
) -> None:
    """SV-B-008: reject zero-label ordered sequences.

    Evidence ID
        ``SV-B-008`` with stable tuple/list IDs.
    Requirement
        No zero-label Basis convention is approved.
    Method
        Construct with correctly typed empty tuple and list sequences.
    Oracle
        The intrinsic nonempty-ordering invariant defines ``ValueError``.
    Acceptance
        Each case raises exactly ``ValueError`` with ordering/empty diagnostics.
    Interpretation
        Passing distinguishes valid container type from invalid empty value.
    Limitations
        No matrix dimension, scientific validation, UQ, or Rust conformance is
        established.
    """

    with pytest.raises(ValueError) as exc_info:
        Basis("canonical", "test basis", ordering, True)

    message = str(exc_info.value)
    assert "basis ordering" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_label",
    [
        pytest.param(None, id="SV-B-009-none-label"),
        pytest.param(True, id="SV-B-009-boolean-label"),
        pytest.param(1, id="SV-B-009-integer-label"),
        pytest.param(b"a", id="SV-B-009-bytes-label"),
        pytest.param(object(), id="SV-B-009-arbitrary-object-label"),
    ],
)
def test_invalid_label_semantic_types_are_rejected(invalid_label: object) -> None:
    """SV-B-009: reject non-string labels inside a valid sequence.

    Evidence ID
        ``SV-B-009`` with stable label-family IDs.
    Requirement
        Every coordinate label must have string semantics; values are not coerced.
    Method
        Place one deliberate invalid value after a valid label and cast only at
        that public boundary.
    Oracle
        The exact-label contract requires strings and defines ``TypeError``.
    Acceptance
        Every case raises exactly ``TypeError`` identifying ``basis label`` and
        the string requirement.
    Interpretation
        Passing establishes label typing separately from container typing.
    Limitations
        Label physical meaning, scientific validation, UQ, and Rust conformance
        are not established.
    """

    ordering = cast(tuple[str, ...], ("a", cast(Any, invalid_label)))
    with pytest.raises(TypeError) as exc_info:
        Basis("canonical", "test basis", ordering, True)

    message = str(exc_info.value)
    assert "basis label" in message
    assert "string" in message


def test_empty_label_is_rejected_without_normalization() -> None:
    """SV-B-010: reject an exact empty label.

    Evidence ID
        ``SV-B-010``.
    Requirement
        Every label is nonempty; no trimming or normalization policy is added.
    Method
        Construct with ``("a", "")`` in an otherwise valid object.
    Oracle
        The intrinsic label invariant defines field-specific ``ValueError``.
    Acceptance
        Construction raises exactly ``ValueError`` identifying the empty label.
    Interpretation
        Passing establishes the explicit empty-string boundary only.
    Limitations
        Whitespace semantics, physical labels, scientific validation, UQ, and
        Rust conformance are unspecified or untested.
    """

    with pytest.raises(ValueError) as exc_info:
        Basis("canonical", "test basis", ("a", ""), True)

    message = str(exc_info.value)
    assert "basis label" in message
    assert "must not be empty" in message


def test_duplicate_labels_are_rejected_but_case_distinct_labels_are_valid() -> None:
    """SV-B-011: enforce uniqueness by exact string equality.

    Evidence ID
        ``SV-B-011``.
    Requirement
        Exact duplicates are invalid, while case-distinct labels remain distinct
        because no normalization precedes uniqueness testing.
    Method
        Reject ``("a", "a")`` and independently admit ``("a", "A")``.
    Oracle
        The approved exact-label uniqueness rule is case-sensitive.
    Acceptance
        Duplicate construction raises exactly ``ValueError`` with uniqueness
        wording; the case-distinct ordering is preserved exactly.
    Interpretation
        Passing establishes uniqueness without case folding or sorting.
    Limitations
        It does not infer orbital identity or physical equivalence and establishes
        no scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="basis ordering labels must be unique"):
        Basis("canonical", "test basis", ("a", "a"), True)

    basis = Basis("canonical", "test basis", ("a", "A"), True)
    assert basis.ordering == ("a", "A")


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        pytest.param(None, id="SV-B-012-none"),
        pytest.param(True, id="SV-B-012-boolean"),
        pytest.param(1, id="SV-B-012-integer"),
        pytest.param(b"basis", id="SV-B-012-bytes"),
        pytest.param(object(), id="SV-B-012-arbitrary-object"),
    ],
)
def test_invalid_identifier_semantic_types_are_rejected(
    invalid_identifier: object,
) -> None:
    """SV-B-012: require identifier string semantics independently.

    Evidence ID
        ``SV-B-012`` with stable invalid-family IDs.
    Requirement
        Identifier names the metadata object and must be a string without coercion.
    Method
        Cast only the deliberate invalid identifier at the public boundary.
    Oracle
        The approved field-specific identifier contract defines ``TypeError``.
    Acceptance
        Every case raises exactly ``TypeError`` identifying basis identifier/string.
    Interpretation
        Passing establishes identifier typing independently of kind.
    Limitations
        Name suitability, scientific validation, UQ, and Rust conformance are not
        established.
    """

    with pytest.raises(TypeError) as exc_info:
        Basis(cast(Any, invalid_identifier), "test basis", ("a",), True)

    message = str(exc_info.value)
    assert "basis identifier" in message
    assert "string" in message


def test_empty_identifier_is_rejected() -> None:
    """SV-B-013: reject an empty identifier.

    Evidence ID
        ``SV-B-013``.
    Requirement
        Basis metadata identifiers are nonempty exact strings.
    Method
        Construct with an empty identifier and valid independent fields.
    Oracle
        The approved identifier invariant defines ``ValueError``.
    Acceptance
        The exception identifies the empty basis identifier.
    Interpretation
        Passing establishes only nonemptiness without normalization.
    Limitations
        Physical identity, scientific validation, UQ, and Rust conformance are
        not established.
    """

    with pytest.raises(ValueError) as exc_info:
        Basis("", "test basis", ("a",), True)

    assert "basis identifier" in str(exc_info.value)
    assert "must not be empty" in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_kind",
    [
        pytest.param(None, id="SV-B-014-none"),
        pytest.param(True, id="SV-B-014-boolean"),
        pytest.param(1, id="SV-B-014-integer"),
        pytest.param(b"kind", id="SV-B-014-bytes"),
        pytest.param(object(), id="SV-B-014-arbitrary-object"),
    ],
)
def test_invalid_kind_semantic_types_are_rejected(invalid_kind: object) -> None:
    """SV-B-014: require kind string semantics independently.

    Evidence ID
        ``SV-B-014`` with stable invalid-family IDs.
    Requirement
        Kind describes a convention and must be a string without coercion.
    Method
        Cast only the deliberate invalid kind at the public boundary.
    Oracle
        The approved field-specific kind contract defines ``TypeError``.
    Acceptance
        Every case raises exactly ``TypeError`` identifying basis kind/string.
    Interpretation
        Passing establishes kind typing independently of identifier.
    Limitations
        No closed vocabulary, physical class, scientific validation, UQ, or Rust
        conformance is established.
    """

    with pytest.raises(TypeError) as exc_info:
        Basis("canonical", cast(Any, invalid_kind), ("a",), True)

    message = str(exc_info.value)
    assert "basis kind" in message
    assert "string" in message


def test_empty_kind_is_rejected() -> None:
    """SV-B-015: reject an empty kind.

    Evidence ID
        ``SV-B-015``.
    Requirement
        Basis kind metadata is nonempty but remains an open exact string.
    Method
        Construct with an empty kind and valid independent fields.
    Oracle
        The approved kind invariant defines ``ValueError``.
    Acceptance
        The exception identifies the empty basis kind.
    Interpretation
        Passing establishes nonemptiness without vocabulary normalization.
    Limitations
        Physical convention validity, scientific validation, UQ, and Rust
        conformance are not established.
    """

    with pytest.raises(ValueError) as exc_info:
        Basis("canonical", "", ("a",), True)

    assert "basis kind" in str(exc_info.value)
    assert "must not be empty" in str(exc_info.value)


@pytest.mark.parametrize(
    "invalid_orthonormal",
    [
        pytest.param(1, id="SV-B-016-integer-one"),
        pytest.param(0, id="SV-B-016-integer-zero"),
        pytest.param(np.bool_(True), id="SV-B-016-numpy-boolean-true"),
        pytest.param(np.bool_(False), id="SV-B-016-numpy-boolean-false"),
        pytest.param("true", id="SV-B-016-raw-string"),
        pytest.param(None, id="SV-B-016-none"),
        pytest.param(object(), id="SV-B-016-arbitrary-object"),
    ],
)
def test_non_python_boolean_orthonormality_is_rejected(
    invalid_orthonormal: object,
) -> None:
    """SV-B-016: reject Boolean substitutes without truth-value coercion.

    Evidence ID
        ``SV-B-016`` with stable value-family IDs.
    Requirement
        ``orthonormal`` accepts exact built-in Python ``bool`` only.
    Method
        Pass integer, NumPy Boolean, string, ``None``, and object substitutes,
        casting only at the deliberate invalid public boundary.
    Oracle
        The approved nominal Boolean contract defines ``TypeError``.
    Acceptance
        Every case raises exactly ``TypeError`` identifying ``Python bool``.
    Interpretation
        Passing establishes no truthy/falsy or NumPy-Boolean coercion.
    Limitations
        It performs no orthogonality calculation and establishes no scientific
        validation, uncertainty quantification, or Rust conformance.
    """

    with pytest.raises(TypeError, match="basis orthonormal flag must be a Python bool"):
        Basis("canonical", "test basis", ("a",), cast(Any, invalid_orthonormal))
