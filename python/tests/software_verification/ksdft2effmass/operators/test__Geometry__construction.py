r"""Software verification of public ``Geometry`` construction.

Object and evidence class
-------------------------
``Geometry`` is a frozen DataObject storing finite row-lattice geometry metadata.
This facet owns construction, accepted scalar/sequence canonicalization,
defensive ownership, exact metadata and row representation, and serialization
exclusion. The approved architecture and Sphinx Geometry contract are the oracle.

Boundary and interpretation
---------------------------
Passing ``SV-G-001`` through ``SV-G-006`` establishes the documented Python
construction contract on synthetic metadata. Failure may indicate an
implementation regression, contract/documentation mismatch, or evidence defect.
The tests perform no DFT, Wannier, experimental, crystallographic, impurity, unit-
conversion, structure-relaxation, scientific-validation, or UQ calculation. Rust
conformance is not established.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import Geometry

pytestmark = pytest.mark.software_verification

VALID_CELL = ((2.0, 0.0, 0.0), (0.5, 3.0, 0.0), (0.0, 0.25, 4.0))


def make_geometry(
    cell: tuple[tuple[float, float, float], ...] = VALID_CELL,
    *,
    system: str = "Synthetic Si:P fixture",
    boundary_conditions: str = "Finite; open (test)",
    coordinate_convention: str = "Cartesian row vectors + signs",
    length_unit: str = "Synthetic length [L]",
) -> Geometry:
    """Construct synthetic Geometry without pre-construction coercion.

    Evidence ID
        Supporting helper for ``SV-G-001`` and ``SV-G-004`` through
        ``SV-G-006``; it owns no separate evidence identifier.
    Requirement
        Inputs pass unchanged to the public constructor; no ``np.asarray``,
        ``float``, or ``tuple`` coercion is performed here.
    Method
        Use explicit synthetic row-lattice and metadata defaults.
    Oracle
        The approved public Geometry contract defines the five stored fields.
    Acceptance
        The caller receives the public constructor result.
    Interpretation
        The helper isolates construction while preserving caller input identity.
    Limitations
        Metadata use synthetic length unit ``Synthetic length [L]`` and Cartesian
        row-vector convention. No DFT, Wannier, experimental, crystallographic,
        or impurity calculation produced the fixture; it establishes no
        scientific validity, scientific validation, UQ, or Rust conformance.
    """

    return Geometry(
        system=system,
        cell=cell,
        boundary_conditions=boundary_conditions,
        coordinate_convention=coordinate_convention,
        length_unit=length_unit,
    )


def test_public_construction_maps_exact_stored_fields() -> None:
    """SV-G-001: map all five public constructor roles to stored state.

    Evidence ID
        ``SV-G-001``.
    Requirement
        Public construction stores exactly ``system``, ``cell``,
        ``boundary_conditions``, ``coordinate_convention``, and ``length_unit``.
    Method
        Import from the supported package and compare every public stored field.
    Oracle
        The approved five-field Geometry model and explicit fixture values.
    Acceptance
        Every field equals its independently selected input exactly.
    Interpretation
        Passing verifies public construction without source-location assertions.
    Limitations
        It does not establish physical realism, serialization, scientific
        validation, UQ, or Rust conformance.
    """

    geometry = make_geometry()

    assert geometry.system == "Synthetic Si:P fixture"
    assert geometry.cell == VALID_CELL
    assert geometry.boundary_conditions == "Finite; open (test)"
    assert geometry.coordinate_convention == "Cartesian row vectors + signs"
    assert geometry.length_unit == "Synthetic length [L]"


@pytest.mark.parametrize(
    "cell",
    [
        pytest.param(((1, 0, 0), (0, 2, 0), (0, 0, 3)), id="SV-G-002-python-int-tuple"),
        pytest.param(
            [[1.5, 0.0, 0.0], [0.0, 2.5, 0.0], [0.0, 0.0, 3.5]],
            id="SV-G-002-python-float-list",
        ),
        pytest.param(
            (
                [np.int32(1), np.int64(0), np.int32(0)],
                [np.int64(0), np.int32(2), np.int64(0)],
                [np.int32(0), np.int64(0), np.int32(3)],
            ),
            id="SV-G-002-numpy-integer-mixed-rows",
        ),
        pytest.param(
            [
                (np.float32(1.25), np.float64(0.0), np.float32(0.0)),
                (np.float64(0.0), np.float32(2.25), np.float64(0.0)),
                (np.float32(0.0), np.float64(0.0), np.float32(3.25)),
            ],
            id="SV-G-002-numpy-floating-mixed-rows",
        ),
    ],
)
def test_approved_nested_sequences_and_scalars_are_canonicalized(
    cell: list[list[float]]
    | list[tuple[np.floating, np.floating, np.floating]]
    | tuple[tuple[int, int, int], ...]
    | tuple[list[np.integer], ...],
) -> None:
    """SV-G-002: canonicalize approved containers/scalars in Geometry itself.

    Evidence ID
        ``SV-G-002`` with stable scalar/container-family parameter IDs.
    Requirement
        Tuple/list nested sequences and Python/NumPy integer/floating scalars are
        accepted and stored as nested built-in tuples of exact built-in floats.
    Method
        Pass raw parameter values directly to ``Geometry`` without helper
        coercion, then recursively inspect stored container and scalar types.
    Oracle
        The approved constructor admission and canonical storage contract.
    Acceptance
        Outer and inner containers have exact type ``tuple`` and every component
        has exact type ``float`` while numerical values are preserved.
    Interpretation
        Passing establishes constructor-owned canonicalization, not broad NumPy
        coercion.
    Limitations
        Scalar examples are representative; no scientific validation, UQ, unit
        interpretation, or Rust conformance is established.
    """

    geometry = Geometry("synthetic", cell, "open", "row Cartesian", "test-L")

    assert type(geometry.cell) is tuple
    assert all(type(row) is tuple for row in geometry.cell)
    assert all(type(value) is float for row in geometry.cell for value in row)
    assert geometry.cell == tuple(tuple(float(value) for value in row) for row in cell)


def test_caller_owned_mutable_cell_is_defensively_copied() -> None:
    """SV-G-003: prevent later inner and outer list mutation from changing state.

    Evidence ID
        ``SV-G-003``.
    Requirement
        Geometry owns an immutable defensive copy of caller-provided sequences.
    Method
        Construct from nested lists, mutate one inner row and append an outer row.
    Oracle
        The original identity cell is the independently recorded expected value.
    Acceptance
        Stored state remains the original nested tuple of floats.
    Interpretation
        Passing verifies ordinary public operational immutability and ownership.
    Limitations
        It does not claim protection against unsupported interpreter internals,
        scientific validation, UQ, or Rust conformance.
    """

    caller_cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    geometry = Geometry("synthetic", caller_cell, "open", "row Cartesian", "test-L")

    caller_cell[0][0] = 9
    caller_cell.append([7, 8, 9])

    assert geometry.cell == ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    assert type(geometry.cell) is tuple
    assert all(type(row) is tuple for row in geometry.cell)


def test_metadata_strings_are_preserved_exactly() -> None:
    """SV-G-004: preserve spelling, case, spaces, and punctuation.

    Evidence ID
        ``SV-G-004``.
    Requirement
        Geometry treats all four metadata strings as explicit uninterpreted text.
    Method
        Construct with mixed case, leading/trailing spaces, and punctuation.
    Oracle
        Exact input literals are the expected stored values.
    Acceptance
        Every metadata field compares exactly equal to its input literal.
    Interpretation
        Passing excludes trimming, case folding, normalization, and vocabulary
        lookup from construction.
    Limitations
        It does not establish that any label is a recognized physical convention,
        scientific validation, UQ, or Rust conformance.
    """

    geometry = make_geometry(
        system="  Si:P / TEST!  ",
        boundary_conditions="Open + Periodic? (Case-Sensitive)",
        coordinate_convention=" Fractional? No: ROW-Cartesian! ",
        length_unit=" Angstrom-like [TEST] ",
    )

    assert geometry.system == "  Si:P / TEST!  "
    assert geometry.boundary_conditions == "Open + Periodic? (Case-Sensitive)"
    assert geometry.coordinate_convention == " Fractional? No: ROW-Cartesian! "
    assert geometry.length_unit == " Angstrom-like [TEST] "


def test_nonorthogonal_left_handed_row_representation_is_preserved() -> None:
    """SV-G-005: preserve valid row order, orientation, and component signs.

    Evidence ID
        ``SV-G-005``.
    Requirement
        Geometry does not impose orthogonality or positive handedness and does not
        reorder row vectors or alter signs.
    Method
        Construct a lower-triangular skew cell with diagonal product ``-24``.
    Oracle
        Nonzero diagonal product proves independence analytically; the negative
        product proves left handedness without calling NumPy linear algebra.
    Acceptance
        Stored nested floats exactly preserve the selected rows and signs.
    Interpretation
        Passing establishes representation fidelity only.
    Limitations
        Admission does not claim physical realism, crystallographic validity,
        scientific validation, UQ, or Rust conformance.
    """

    cell = ((2, 0, 0), (1, 3, 0), (-1, 2, -4))
    geometry = Geometry("synthetic", cell, "open", "row Cartesian", "test-L")

    assert geometry.cell == ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (-1.0, 2.0, -4.0))


def test_geometry_exposes_no_standalone_serialization_api() -> None:
    """SV-G-006: keep nested wire representation with the record serializer.

    Evidence ID
        ``SV-G-006``.
    Requirement
        Geometry has no standalone serialize/deserialize or dict/JSON API.
    Method
        Inspect only the six explicitly prohibited public attribute names.
    Oracle
        Serialization ownership belongs to ``OperatorRecordJsonSerializer``.
    Acceptance
        None of the names is present on a valid Geometry instance.
    Interpretation
        Passing verifies the DataObject/ActionObject serialization boundary.
    Limitations
        It does not test nested record serialization, scientific validation, UQ,
        or Rust conformance.
    """

    geometry = make_geometry()

    for name in (
        "serialize",
        "deserialize",
        "to_json",
        "from_json",
        "to_dict",
        "from_dict",
    ):
        assert not hasattr(geometry, name)
