"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import StateSpace


def test_public_import_constructs_state_space() -> None:
    state_space = StateSpace("two-level", "finite synthetic", 2)

    assert state_space.identifier == "two-level"
    assert state_space.kind == "finite synthetic"
    assert state_space.dimension == 2


def test_numpy_integral_dimension_is_canonicalized_to_python_int() -> None:
    state_space = StateSpace("two-level", "finite synthetic", np.int64(2))

    assert state_space.dimension == 2
    assert isinstance(state_space.dimension, int)


@pytest.mark.parametrize("dimension", [True, False, 2.0, np.float64(2.0), "2"])
def test_dimension_must_be_integer_not_boolean(dimension: Any) -> None:
    with pytest.raises(TypeError, match="positive integer"):
        StateSpace("bad", "finite synthetic", dimension)


@pytest.mark.parametrize("dimension", [0, -1, np.int64(-2)])
def test_dimension_must_be_positive(dimension: Any) -> None:
    with pytest.raises(ValueError, match="positive"):
        StateSpace("bad", "finite synthetic", dimension)


@pytest.mark.parametrize(
    "field, value",
    [("identifier", ""), ("kind", "")],
)
def test_string_fields_must_be_nonempty(field: str, value: str) -> None:
    kwargs: dict[str, Any] = {
        "identifier": "state-space",
        "kind": "finite synthetic",
        "dimension": 1,
    }
    kwargs[field] = value

    with pytest.raises(ValueError, match="must not be empty"):
        StateSpace(**kwargs)


@pytest.mark.parametrize(
    "field, value",
    [("identifier", 1), ("kind", None)],
)
def test_string_fields_must_be_strings(field: str, value: Any) -> None:
    kwargs: dict[str, Any] = {
        "identifier": "state-space",
        "kind": "finite synthetic",
        "dimension": 1,
    }
    kwargs[field] = value

    with pytest.raises(TypeError, match="must be a string"):
        StateSpace(**kwargs)
