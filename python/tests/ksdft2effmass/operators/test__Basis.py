"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from typing import Any

import pytest

from ksdft2effmass.operators import Basis


def test_public_import_constructs_basis_with_tuple_ordering() -> None:
    basis = Basis("canonical", "orthonormal test basis", ("a", "b"), True)

    assert basis.identifier == "canonical"
    assert basis.kind == "orthonormal test basis"
    assert basis.ordering == ("a", "b")
    assert basis.orthonormal is True


def test_runtime_sequence_ordering_is_canonicalized_to_tuple() -> None:
    ordering: Any = ["a", "b"]
    basis = Basis("canonical", "orthonormal test basis", ordering, True)

    assert basis.ordering == ("a", "b")


def test_ordering_rejects_bare_string() -> None:
    with pytest.raises(TypeError, match="not a string"):
        Basis("basis", "orbital", "sp", True)  # type: ignore[arg-type]


@pytest.mark.parametrize("ordering", [(), []])
def test_ordering_must_be_nonempty(ordering: Any) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        Basis("bad", "orthonormal test basis", ordering, True)


def test_ordering_labels_must_be_unique() -> None:
    with pytest.raises(ValueError, match="unique"):
        Basis("bad", "orthonormal test basis", ("a", "a"), True)


@pytest.mark.parametrize("label", ["", 1, None])
def test_ordering_labels_must_be_nonempty_strings(label: Any) -> None:
    error_type = ValueError if label == "" else TypeError
    with pytest.raises(error_type):
        Basis("bad", "orthonormal test basis", ("a", label), True)


@pytest.mark.parametrize("orthonormal", [1, 0, "true", None])
def test_orthonormal_flag_must_be_exact_python_bool(orthonormal: Any) -> None:
    with pytest.raises(TypeError, match="Python bool"):
        Basis("bad", "orthonormal test basis", ("a",), orthonormal)


@pytest.mark.parametrize(
    "field, value",
    [("identifier", ""), ("kind", "")],
)
def test_string_fields_must_be_nonempty(field: str, value: str) -> None:
    kwargs: dict[str, Any] = {
        "identifier": "basis",
        "kind": "orthonormal test basis",
        "ordering": ("a",),
        "orthonormal": True,
    }
    kwargs[field] = value

    with pytest.raises(ValueError, match="must not be empty"):
        Basis(**kwargs)
