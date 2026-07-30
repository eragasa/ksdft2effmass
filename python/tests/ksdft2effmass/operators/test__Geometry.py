"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import Geometry

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))


def make_geometry(cell: Any = VALID_CELL) -> Geometry:
    return Geometry(
        system="synthetic",
        cell=cell,
        boundary_conditions="finite synthetic",
        coordinate_convention="cartesian row lattice vectors",
        length_unit="angstrom",
    )


def test_public_import_constructs_geometry() -> None:
    geometry = make_geometry()

    assert geometry.system == "synthetic"
    assert geometry.cell == VALID_CELL
    assert geometry.boundary_conditions == "finite synthetic"
    assert geometry.coordinate_convention == "cartesian row lattice vectors"
    assert geometry.length_unit == "angstrom"


def test_runtime_lists_are_canonicalized_to_tuple_of_float_rows() -> None:
    geometry = make_geometry([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    assert geometry.cell == ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


@pytest.mark.parametrize(
    "cell, message",
    [
        (((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)), "three three-component"),
        (((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)), "three three-component"),
        (((1.0, 0.0, 0.0), (0.0, np.nan, 0.0), (0.0, 0.0, 1.0)), "finite"),
        (((1.0, 0.0, 0.0), (0.0, np.inf, 0.0), (0.0, 0.0, 1.0)), "finite"),
        (((1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 0.0, 1.0)), "independent"),
        (((1.0, 0.0, 0.0), (True, 1.0, 0.0), (0.0, 0.0, 1.0)), "numeric"),
        (((1.0, 0.0, 0.0), ("bad", 1.0, 0.0), (0.0, 0.0, 1.0)), "numeric"),
        (((1.0, 0.0, 0.0), ("1.0", 1.0, 0.0), (0.0, 0.0, 1.0)), "numeric"),
    ],
)
def test_rejects_malformed_nonfinite_and_rank_deficient_cells(
    cell: Any, message: str
) -> None:
    expected_error = TypeError if message == "numeric" else ValueError

    with pytest.raises(expected_error, match=message):
        make_geometry(cell)


def test_rejects_cells_below_documented_linear_independence_threshold() -> None:
    scale = Geometry.LINEAR_INDEPENDENCE_RTOL
    nearly_dependent_cell = ((1.0, 0.0, 0.0), (0.0, scale / 2.0, 0.0), (0.0, 0.0, 1.0))

    with pytest.raises(ValueError, match="independent"):
        make_geometry(nearly_dependent_cell)


@pytest.mark.parametrize(
    "field",
    ["system", "boundary_conditions", "coordinate_convention", "length_unit"],
)
def test_metadata_strings_must_be_nonempty(field: str) -> None:
    kwargs: dict[str, Any] = {
        "system": "synthetic",
        "cell": VALID_CELL,
        "boundary_conditions": "finite synthetic",
        "coordinate_convention": "cartesian row lattice vectors",
        "length_unit": "angstrom",
    }
    kwargs[field] = ""

    with pytest.raises(ValueError, match="must not be empty"):
        Geometry(**kwargs)
