r"""Software verification of intrinsic ``Geometry`` constructor invariants.

Object and evidence class
-------------------------
This facet owns the public ordered-container, 3x3 shape, component scalar,
finiteness, conversion-overflow, and four independent metadata-string boundaries
of ``Geometry``. The approved public architecture and Sphinx contract are the
oracle; linear-independence numerics are intentionally owned by the separate
numerical-verification facet.

Interpretation and exclusions
-----------------------------
Passing ``SV-G-007`` through ``SV-G-019`` establishes exact public error taxonomy
for synthetic inputs. Failure may indicate implementation regression,
contract/documentation mismatch, or evidence defect. No DFT, Wannier,
experimental, crystallographic, impurity, unit-conversion, scientific-validation,
or UQ calculation is performed. Rust conformance is not established.
"""

from collections.abc import Generator
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import Geometry

pytestmark = pytest.mark.software_verification

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def component_generator() -> Generator[tuple[int, int, int]]:
    """Yield synthetic rows for the invalid outer-generator boundary.

    Evidence ID
        Supporting helper for ``SV-G-007``; it owns no separate identifier.
    Requirement
        Inputs are yielded unchanged and are not coerced or materialized.
    Method
        Yield three synthetic integer rows.
    Oracle
        Generators are iterable but not approved ordered-sequence containers.
    Acceptance
        The caller receives an invalid generator fixture.
    Interpretation
        This isolates container semantics from otherwise valid row values.
    Limitations
        Metadata would use synthetic ``test-L`` and ``row Cartesian`` labels. No
        DFT, Wannier, experimental, crystallographic, or impurity calculation
        produced the data; it establishes no scientific validity, validation,
        UQ, or Rust conformance.
    """

    yield (1, 0, 0)
    yield (0, 1, 0)
    yield (0, 0, 1)


def construct_with(**overrides: object) -> Geometry:
    """Pass one or more deliberate boundary values unchanged to Geometry.

    Evidence ID
        Supporting helper for ``SV-G-007`` through ``SV-G-019``; it owns no
        separate identifier.
    Requirement
        No ``np.asarray``, ``float``, ``tuple``, string normalization, or other
        coercion occurs before the public constructor.
    Method
        Replace explicit valid synthetic defaults and cast only at the deliberate
        dynamic constructor boundary.
    Oracle
        The public constructor owns all tested canonicalization and rejection.
    Acceptance
        Construction returns or raises directly from ``Geometry``.
    Interpretation
        The helper keeps invalid admission tests independent of preprocessing.
    Limitations
        Defaults use synthetic ``test-L`` units and ``row Cartesian`` metadata.
        No DFT, Wannier, experimental, crystallographic, or impurity calculation
        produced them; no scientific validity, scientific validation, UQ, or
        Rust conformance is established.
    """

    kwargs: dict[str, object] = {
        "system": "synthetic",
        "cell": VALID_CELL,
        "boundary_conditions": "open",
        "coordinate_convention": "row Cartesian",
        "length_unit": "test-L",
    }
    kwargs.update(overrides)
    return Geometry(**cast(Any, kwargs))


@pytest.mark.parametrize(
    "invalid_cell",
    [
        pytest.param("rows", id="SV-G-007-bare-string"),
        pytest.param(b"rows", id="SV-G-007-bytes"),
        pytest.param({"r0": (1, 0, 0)}, id="SV-G-007-mapping"),
        pytest.param({(1, 0, 0), (0, 1, 0), (0, 0, 1)}, id="SV-G-007-set"),
        pytest.param(
            frozenset({(1, 0, 0), (0, 1, 0), (0, 0, 1)}),
            id="SV-G-007-frozenset",
        ),
        pytest.param(component_generator(), id="SV-G-007-generator"),
        pytest.param(None, id="SV-G-007-none"),
        pytest.param(object(), id="SV-G-007-arbitrary-object"),
    ],
)
def test_invalid_outer_cell_structure_is_rejected(invalid_cell: object) -> None:
    """SV-G-007: reject non-approved outer cell containers with TypeError.

    Evidence ID
        ``SV-G-007`` with stable readable container-family IDs.
    Requirement
        The outer cell must be an approved ordered sequence, not every iterable.
    Method
        Pass bare text, bytes, mappings, unordered collections, a generator,
        ``None``, and an arbitrary object without preprocessing.
    Oracle
        Row order has represented meaning, so the approved container contract
        excludes these families.
    Acceptance
        Every case raises exactly ``TypeError`` naming the cell and ordered
        sequence reason.
    Interpretation
        Passing prevents arbitrary iteration from selecting represented row order.
    Limitations
        It does not enumerate all third-party sequence types or establish
        numerical/scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        construct_with(cell=invalid_cell)

    message = str(exc_info.value)
    assert "cell" in message
    assert "ordered sequence" in message


@pytest.mark.parametrize(
    "invalid_cell, expected_error, reason",
    [
        pytest.param(
            (), ValueError, "three three-component", id="SV-G-008-empty-outer"
        ),
        pytest.param(
            ((1, 0, 0), (0, 1, 0)),
            ValueError,
            "three three-component",
            id="SV-G-008-two-rows",
        ),
        pytest.param(
            ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)),
            ValueError,
            "three three-component",
            id="SV-G-008-four-rows",
        ),
        pytest.param(
            ((), (0, 1, 0), (0, 0, 1)),
            ValueError,
            "three three-component",
            id="SV-G-008-empty-row",
        ),
        pytest.param(
            ((1, 0), (0, 1, 0), (0, 0, 1)),
            ValueError,
            "three three-component",
            id="SV-G-008-short-row",
        ),
        pytest.param(
            ((1, 0, 0, 0), (0, 1, 0), (0, 0, 1)),
            ValueError,
            "three three-component",
            id="SV-G-008-long-row",
        ),
        pytest.param(
            ("100", (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-bare-string",
        ),
        pytest.param(
            (b"100", (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-bytes",
        ),
        pytest.param(
            ({0: 1, 1: 0, 2: 0}, (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-mapping",
        ),
        pytest.param(
            ({0, 1, 2}, (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-set",
        ),
        pytest.param(
            (frozenset({0, 1, 2}), (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-frozenset",
        ),
        pytest.param(
            ((value for value in (1, 0, 0)), (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-generator",
        ),
        pytest.param(
            (object(), (0, 1, 0), (0, 0, 1)),
            TypeError,
            "cell rows",
            id="SV-G-008-row-arbitrary-object",
        ),
    ],
)
def test_invalid_row_structure_is_rejected(
    invalid_cell: object,
    expected_error: type[TypeError] | type[ValueError],
    reason: str,
) -> None:
    r"""SV-G-008: reject malformed row shapes and container semantics.

    Evidence ID
        ``SV-G-008`` with stable shape and row-container IDs.
    Requirement
        Cell shape is exactly :math:`3\times3`, and every row is an approved
        ordered sequence rather than an arbitrary iterable or unordered object.
    Method
        Collect empty/short/long approved sequences and invalid row-container
        families in one cohesive parameterized evidence owner.
    Oracle
        The approved nested ordered-sequence and exact-shape contract.
    Acceptance
        Wrong approved lengths raise exactly ``ValueError`` with the shape
        reason; wrong semantic row containers raise exactly ``TypeError`` naming
        cell rows.
    Interpretation
        Passing distinguishes wrong semantic type from wrong value/shape while
        preventing unordered or one-shot component traversal.
    Limitations
        No numerical independence, scientific validation, UQ, or Rust
        conformance is established.
    """

    with pytest.raises(expected_error) as exc_info:
        construct_with(cell=invalid_cell)

    message = str(exc_info.value)
    assert reason in message
    if expected_error is TypeError:
        assert "ordered sequences" in message


@pytest.mark.parametrize(
    "invalid_component",
    [
        pytest.param(True, id="SV-G-009-python-bool-true"),
        pytest.param(False, id="SV-G-009-python-bool-false"),
        pytest.param(np.bool_(True), id="SV-G-009-numpy-bool"),
        pytest.param("1.0", id="SV-G-009-numeric-string"),
        pytest.param(b"1.0", id="SV-G-009-bytes"),
        pytest.param(1.0 + 0.0j, id="SV-G-009-complex"),
        pytest.param(None, id="SV-G-009-none"),
        pytest.param(object(), id="SV-G-009-arbitrary-object"),
    ],
)
def test_invalid_component_semantic_types_are_rejected(
    invalid_component: object,
) -> None:
    """SV-G-009: reject wrong scalar semantics without coercion.

    Evidence ID
        ``SV-G-009`` with stable scalar-family IDs.
    Requirement
        Cell components are real numeric values; Booleans, numeric text, bytes,
        complex values, ``None``, and arbitrary objects are not real components.
    Method
        Replace one component in an otherwise valid cell and cast only at the
        deliberate invalid constructor boundary.
    Oracle
        The approved scalar-family contract defines ``TypeError``.
    Acceptance
        Every case raises exactly ``TypeError`` naming a cell component and real
        numeric requirement.
    Interpretation
        Passing shows the public constructor, not test preprocessing, owns typing.
    Limitations
        It does not exhaust third-party scalar classes or establish scientific
        validation, UQ, or Rust conformance.
    """

    cell = ((invalid_component, 0, 0), (0, 1, 0), (0, 0, 1))
    with pytest.raises(TypeError) as exc_info:
        construct_with(cell=cell)

    message = str(exc_info.value)
    assert "cell component" in message
    assert "real numeric" in message


@pytest.mark.parametrize(
    "value, position",
    [
        pytest.param(float("nan"), (0, 0), id="SV-G-010-nan-first-row"),
        pytest.param(float("inf"), (1, 1), id="SV-G-010-positive-inf-second-row"),
        pytest.param(float("-inf"), (2, 2), id="SV-G-010-negative-inf-third-row"),
        pytest.param(float("nan"), (0, 2), id="SV-G-010-nan-off-diagonal"),
    ],
)
def test_nonfinite_components_are_rejected(
    value: float, position: tuple[int, int]
) -> None:
    """SV-G-010: reject NaN and signed infinity at multiple positions.

    Evidence ID
        ``SV-G-010`` with stable value/position IDs.
    Requirement
        Every admitted real cell component must be finite.
    Method
        Insert one nonfinite float into independently selected cell positions.
    Oracle
        IEEE nonfiniteness violates the approved intrinsic value invariant.
    Acceptance
        Every case raises exactly ``ValueError`` naming component finiteness.
    Interpretation
        Passing distinguishes valid real scalar type from invalid finite value.
    Limitations
        No independence decision or scientific validation, UQ, or Rust
        conformance is established.
    """

    cell = [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]]
    row, column = position
    cell[row][column] = value

    with pytest.raises(ValueError) as exc_info:
        construct_with(cell=cell)

    message = str(exc_info.value)
    assert "cell component" in message
    assert "finite" in message


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(10**10000, id="SV-G-011-huge-positive-integer"),
        pytest.param(-(10**10000), id="SV-G-011-huge-negative-integer"),
    ],
)
def test_huge_integer_conversion_overflow_uses_finite_value_taxonomy(
    value: int,
) -> None:
    """SV-G-011: translate binary64 integer-conversion overflow to ValueError.

    Evidence ID
        ``SV-G-011`` with positive/negative stable IDs.
    Requirement
        Accepted integer semantics that cannot become finite binary64 values use
        the documented finite-number ``ValueError``; raw ``OverflowError`` does
        not leak.
    Method
        Place huge signed Python integers in one otherwise valid row.
    Oracle
        Their magnitudes exceed the finite binary64 range analytically.
    Acceptance
        Each case raises exactly ``ValueError`` naming component finiteness.
    Interpretation
        Passing verifies the public conversion-overflow taxonomy.
    Limitations
        It does not approve arbitrary-precision cell storage, scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        construct_with(cell=((value, 0, 0), (0, 1, 0), (0, 0, 1)))

    message = str(exc_info.value)
    assert "cell component" in message
    assert "finite" in message


INVALID_METADATA = [
    pytest.param(None, id="none"),
    pytest.param(True, id="boolean-true"),
    pytest.param(False, id="boolean-false"),
    pytest.param(b"text", id="bytes"),
    pytest.param(object(), id="arbitrary-object"),
]


def assert_metadata_type_error(field: str, value: object, diagnostic: str) -> None:
    """Assert unchanged invalid metadata reaches its field-specific boundary.

    Evidence ID
        Supporting helper for ``SV-G-012``, ``SV-G-014``, ``SV-G-016``, and
        ``SV-G-018``; it owns no separate identifier.
    Requirement
        The value is passed unchanged; no string conversion or normalization is
        performed.
    Method
        Delegate to ``construct_with`` and inspect semantic diagnostic fragments.
    Oracle
        Each public metadata role requires a Python string.
    Acceptance
        Exactly ``TypeError`` names the role and string reason.
    Interpretation
        This supports independent role evidence without freezing full messages.
    Limitations
        Synthetic ``test-L``/``row Cartesian`` defaults establish no DFT,
        Wannier, experimental, crystallographic, impurity, scientific-validation,
        UQ, or Rust-conformance result.
    """

    with pytest.raises(TypeError) as exc_info:
        construct_with(**{field: value})
    message = str(exc_info.value)
    assert diagnostic in message
    assert "string" in message


@pytest.mark.parametrize("value", INVALID_METADATA)
def test_invalid_system_semantic_types_are_rejected(value: object) -> None:
    """SV-G-012: require string semantics independently for ``system``.

    Evidence ID
        ``SV-G-012`` with stable invalid-family IDs.
    Requirement
        ``system`` must be a Python string and is not coerced.
    Method
        Exercise representative non-string values through the public constructor.
    Oracle
        The approved field-specific semantic boundary.
    Acceptance
        Exactly ``TypeError`` identifies ``geometry system`` and ``string``.
    Interpretation
        Passing verifies system-role typing independently.
    Limitations
        No label vocabulary, scientific validation, UQ, or Rust conformance is
        established.
    """

    assert_metadata_type_error("system", value, "geometry system")


def test_empty_system_is_rejected() -> None:
    """SV-G-013: reject the empty ``system`` string with ValueError.

    Evidence ID
        ``SV-G-013``.
    Requirement
        A correctly typed system string is nonempty.
    Method
        Pass exactly ``""`` without normalization.
    Oracle
        The approved nonempty-string invariant.
    Acceptance
        Exactly ``ValueError`` identifies ``geometry system`` and emptiness.
    Interpretation
        Passing separates semantic type from invalid empty value.
    Limitations
        Whitespace-only strings remain preserved metadata; no scientific
        validation, UQ, or Rust conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        construct_with(system="")
    assert "geometry system" in str(exc_info.value)
    assert "empty" in str(exc_info.value)


@pytest.mark.parametrize("value", INVALID_METADATA)
def test_invalid_boundary_condition_types_are_rejected(value: object) -> None:
    """SV-G-014: require string semantics for ``boundary_conditions``.

    Evidence ID
        ``SV-G-014`` with stable invalid-family IDs.
    Requirement
        Boundary-condition metadata must be a Python string and is not coerced.
    Method
        Exercise representative non-string values independently.
    Oracle
        The approved role-specific string boundary.
    Acceptance
        Exactly ``TypeError`` names geometry boundary conditions and string.
    Interpretation
        Passing verifies role-specific typing only.
    Limitations
        No boundary physics, scientific validation, UQ, or Rust conformance is
        established.
    """

    assert_metadata_type_error(
        "boundary_conditions", value, "geometry boundary conditions"
    )


def test_empty_boundary_conditions_are_rejected() -> None:
    """SV-G-015: reject empty boundary-condition metadata.

    Evidence ID
        ``SV-G-015``.
    Requirement
        The correctly typed field is nonempty.
    Method
        Pass exactly ``""``.
    Oracle
        The approved nonempty-string invariant.
    Acceptance
        Exactly ``ValueError`` identifies boundary conditions and emptiness.
    Interpretation
        Passing verifies the field-specific value boundary.
    Limitations
        No boundary-condition interpretation, scientific validation, UQ, or Rust
        conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        construct_with(boundary_conditions="")
    assert "geometry boundary conditions" in str(exc_info.value)
    assert "empty" in str(exc_info.value)


@pytest.mark.parametrize("value", INVALID_METADATA)
def test_invalid_coordinate_convention_types_are_rejected(value: object) -> None:
    """SV-G-016: require string semantics for ``coordinate_convention``.

    Evidence ID
        ``SV-G-016`` with stable invalid-family IDs.
    Requirement
        Coordinate-convention metadata must be a Python string, without coercion.
    Method
        Exercise representative non-string values independently.
    Oracle
        The approved role-specific string boundary.
    Acceptance
        Exactly ``TypeError`` names geometry coordinate convention and string.
    Interpretation
        Passing verifies role-specific typing only.
    Limitations
        No coordinate transform, scientific validation, UQ, or Rust conformance
        is established.
    """

    assert_metadata_type_error(
        "coordinate_convention", value, "geometry coordinate convention"
    )


def test_empty_coordinate_convention_is_rejected() -> None:
    """SV-G-017: reject empty coordinate-convention metadata.

    Evidence ID
        ``SV-G-017``.
    Requirement
        The correctly typed field is nonempty.
    Method
        Pass exactly ``""``.
    Oracle
        The approved nonempty-string invariant.
    Acceptance
        Exactly ``ValueError`` identifies coordinate convention and emptiness.
    Interpretation
        Passing verifies the field-specific value boundary.
    Limitations
        No coordinate interpretation, scientific validation, UQ, or Rust
        conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        construct_with(coordinate_convention="")
    assert "geometry coordinate convention" in str(exc_info.value)
    assert "empty" in str(exc_info.value)


@pytest.mark.parametrize("value", INVALID_METADATA)
def test_invalid_length_unit_types_are_rejected(value: object) -> None:
    """SV-G-018: require string semantics for ``length_unit``.

    Evidence ID
        ``SV-G-018`` with stable invalid-family IDs.
    Requirement
        Length-unit metadata must be a Python string and is not coerced.
    Method
        Exercise representative non-string values independently.
    Oracle
        The approved role-specific string boundary.
    Acceptance
        Exactly ``TypeError`` names geometry length unit and string.
    Interpretation
        Passing verifies role-specific typing only.
    Limitations
        No unit registry, conversion, dimensional analysis, scientific
        validation, UQ, or Rust conformance is established.
    """

    assert_metadata_type_error("length_unit", value, "geometry length unit")


def test_empty_length_unit_is_rejected() -> None:
    """SV-G-019: reject empty length-unit metadata.

    Evidence ID
        ``SV-G-019``.
    Requirement
        The correctly typed field is nonempty.
    Method
        Pass exactly ``""``.
    Oracle
        The approved nonempty-string invariant.
    Acceptance
        Exactly ``ValueError`` identifies geometry length unit and emptiness.
    Interpretation
        Passing verifies the field-specific value boundary.
    Limitations
        No unit interpretation, scientific validation, UQ, or Rust conformance is
        established.
    """

    with pytest.raises(ValueError) as exc_info:
        construct_with(length_unit="")
    assert "geometry length unit" in str(exc_info.value)
    assert "empty" in str(exc_info.value)
