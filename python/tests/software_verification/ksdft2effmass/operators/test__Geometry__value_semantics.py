r"""Software verification of ``Geometry``.

Facet and represented meaning

-----------------------------
This class-owned module owns the value semantics facet. Object and evidence class
-------------------------
This facet owns frozen/slotted public state and exact structural equality for the
five stored Geometry fields. It deliberately specifies no hash contract and no
approximate geometry comparison.

Interpretation and exclusions
-----------------------------
Passing ``SV-G-020`` through ``SV-G-022`` establishes Python software value
semantics on synthetic metadata. Failure may indicate implementation regression,
contract/documentation mismatch, or evidence defect. No DFT, Wannier,
experimental, crystallographic, impurity, scientific-validation, or UQ
calculation is performed. Rust conformance is not established.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``Geometry``; collaborators only construct inputs or expose
public outcomes. Accepted public contracts, literal expected values, Python language
semantics, and assigned schema or fixture artifacts provide the oracles. No runtime
warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import Geometry

pytestmark = pytest.mark.software_verification

SUT = Geometry

EQUALITY_FIELDS = (
    "identifier",
    "cell",
    "boundary_conditions",
    "coordinate_convention",
    "length_unit",
)


def make_geometry(
    *,
    system: str = "synthetic",
    cell: tuple[tuple[float, float, float], ...] = (
        (2.0, 0.0, 0.0),
        (0.5, 3.0, 0.0),
        (0.0, 0.25, 4.0),
    ),
    boundary_conditions: str = "open",
    coordinate_convention: str = "row Cartesian",
    length_unit: str = "test-L",
) -> Geometry:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: No coercion, tuple conversion, or metadata normalization occurs here.

    Method: Forward explicit typed values directly to the public constructor.

    Oracle: The approved five-field exact-value contract.

    Acceptance: The caller receives a public Geometry instance.

    Interpretation: The helper makes one-field equality variations explicit.

    Limitations: Fixtures use synthetic ``test-L`` units and ``row Cartesian`` metadata.
    No DFT,
    Wannier, experimental, crystallographic, or impurity calculation produced them; no
    scientific validity, scientific validation, UQ, or Rust conformance is established.
    """

    return Geometry(
        system,
        cell,
        boundary_conditions,
        coordinate_convention,
        length_unit,
    )


def mutate_nested_cell(geometry: Geometry) -> None:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Nested stored tuples reject component assignment.

    Method: Execute direct public item assignment; the type-ignore is limited to the
    intentional
    runtime immutability probe and performs no coercion.

    Oracle: Exact nested built-in tuple storage is immutable under item assignment.

    Acceptance: Python raises its exact tuple-assignment ``TypeError``.

    Interpretation: The helper exercises ordinary public mutation, not invariant bypass.

    Limitations: Synthetic metadata establish no DFT, Wannier, experimental,
    crystallographic,
    impurity, scientific-validation, UQ, or Rust result.
    """

    geometry.cell[0][0] = 9.0  # type: ignore[index]


def test_field__frozen_slotted_state_rejects_public_mutation__is_exact() -> None:
    r"""Evidence ID: SV-G-020

    Requirement: Dataclass fields and dynamic attributes cannot be assigned, nested cell
    components
    cannot be mutated, and no per-instance ``__dict__`` exists.

    Method: Exercise ordinary ``setattr`` and tuple item assignment on a valid object.

    Oracle: Frozen dataclass assignment raises ``FrozenInstanceError`` and tuple item
    assignment
    raises ``TypeError`` under the public storage contract.

    Acceptance: Both field/dynamic assignment raise exactly ``FrozenInstanceError``;
    nested
    assignment raises exactly ``TypeError``; ``__dict__`` is absent.

    Interpretation: Passing establishes operational immutability through ordinary public
    APIs.

    Limitations: No hash behavior or unsupported invariant bypass is asserted;
    scientific validation,
    UQ, and Rust conformance are not established.
    """

    geometry = make_geometry()

    with pytest.raises(FrozenInstanceError):
        geometry.system = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        geometry.extra = "dynamic"  # type: ignore[attr-defined]
    with pytest.raises(TypeError):
        mutate_nested_cell(geometry)
    assert not hasattr(geometry, "__dict__")


@pytest.mark.parametrize(
    "changed",
    [
        pytest.param(make_geometry(system="different"), id="system"),
        pytest.param(
            make_geometry(cell=((2.0, 0.0, 0.0), (0.5, 3.5, 0.0), (0.0, 0.25, 4.0))),
            id="sv_g_021_cell",
        ),
        pytest.param(
            make_geometry(boundary_conditions="periodic"), id="boundary_conditions"
        ),
        pytest.param(
            make_geometry(coordinate_convention="fractional row"),
            id="coordinate_convention",
        ),
        pytest.param(make_geometry(length_unit="other-L"), id="length_unit"),
    ],
)
def test_method__eq__exact_structural_equality_uses_every_stored_field(
    changed: Geometry,
) -> None:
    r"""Evidence ID: SV-G-021

    Requirement: Equality is exact structural equality across all five stored fields.

    Method: Compare equal independently constructed objects and one-field variants.

    Oracle: Dataclass exact value semantics and independently selected variant values.

    Acceptance: Equal construction compares equal in both directions; each variant
    compares unequal
    in both directions.

    Interpretation: Passing establishes every field participates in exact equality.

    Limitations: It does not imply physical equivalence, approximate comparison,
    scientific
    validation, UQ, hashing, or Rust conformance.
    """

    reference = make_geometry()
    equal = make_geometry()

    assert reference == equal
    assert equal == reference
    assert reference != changed
    assert changed != reference


@pytest.mark.parametrize(
    "changed_cell",
    [
        pytest.param(
            ((0.5, 3.0, 0.0), (2.0, 0.0, 0.0), (0.0, 0.25, 4.0)),
            id="sv_g_022_row_permutation",
        ),
        pytest.param(
            ((2.0, 0.0, 0.0), (0.5, 3.0, 0.0), (0.0, 0.5, 4.0)),
            id="sv_g_022_component_change",
        ),
        pytest.param(
            ((-2.0, 0.0, 0.0), (0.5, 3.0, 0.0), (0.0, 0.25, 4.0)),
            id="sv_g_022_sign_change",
        ),
    ],
)
def test_method__eq__cell_equality_is_row_order_and_component_sensitive(
    changed_cell: tuple[tuple[float, float, float], ...],
) -> None:
    r"""Evidence ID: SV-G-022

    Requirement: Row permutation, component value, and sign changes alter exact value.

    Method: Compare otherwise identical valid cells differing in one listed way.

    Oracle: Stored row-lattice coordinates are ordering-sensitive represented data.

    Acceptance: Every variant compares unequal; an unchanged copy compares equal.

    Interpretation: Passing excludes approximate comparison from ``Geometry.__eq__``.

    Limitations: Inequality does not establish physical inequivalence, scientific
    invalidity,
    scientific validation, UQ, or Rust conformance.
    """

    reference = make_geometry()

    assert reference == make_geometry()
    assert reference != make_geometry(cell=changed_cell)
