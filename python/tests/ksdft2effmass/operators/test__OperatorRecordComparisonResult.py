"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from dataclasses import FrozenInstanceError
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult


def test_public_import_constructs_comparison_result() -> None:
    result = OperatorRecordComparisonResult(
        "reference", "candidate", 2, "eV", 1.0, 4.0, 3.0
    )

    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.matrix_dimension == 2
    assert result.energy_unit == "eV"
    assert result.maximum_absolute_residual == 1.0
    assert result.frobenius_residual == 4.0
    assert result.spectral_residual == 3.0


def test_comparison_result_canonicalizes_numpy_integer_and_float_scalars() -> None:
    result = OperatorRecordComparisonResult(
        "reference",
        "candidate",
        cast(Any, np.int64(2)),
        "eV",
        np.float64(1.0),
        np.float64(4.0),
        np.float64(3.0),
    )

    assert result.matrix_dimension == 2
    assert isinstance(result.matrix_dimension, int)
    assert result.maximum_absolute_residual == 1.0
    assert result.frobenius_residual == 4.0
    assert result.spectral_residual == 3.0


def test_comparison_result_is_immutable() -> None:
    result = OperatorRecordComparisonResult(
        "reference", "candidate", 2, "eV", 1.0, 4.0, 3.0
    )

    with pytest.raises(FrozenInstanceError):
        result.maximum_absolute_residual = 0.0  # type: ignore[misc]


@pytest.mark.parametrize("identifier", ["", 1, object()])
def test_comparison_result_requires_nonempty_identifiers(identifier: Any) -> None:
    expected_error = ValueError if identifier == "" else TypeError

    with pytest.raises(expected_error, match="identifier"):
        OperatorRecordComparisonResult(identifier, "candidate", 2, "eV", 1.0, 4.0, 3.0)
    with pytest.raises(expected_error, match="identifier"):
        OperatorRecordComparisonResult("reference", identifier, 2, "eV", 1.0, 4.0, 3.0)


@pytest.mark.parametrize("energy_unit", ["", 1, object()])
def test_comparison_result_requires_nonempty_energy_unit(energy_unit: Any) -> None:
    expected_error = ValueError if energy_unit == "" else TypeError

    with pytest.raises(expected_error, match="energy unit"):
        OperatorRecordComparisonResult(
            "reference", "candidate", 2, energy_unit, 1.0, 4.0, 3.0
        )


@pytest.mark.parametrize("matrix_dimension", [0, -1, True, 2.0, "2"])
def test_comparison_result_requires_positive_integer_matrix_dimension(
    matrix_dimension: Any,
) -> None:
    expected_error = ValueError if matrix_dimension in (0, -1) else TypeError

    with pytest.raises(expected_error, match="matrix_dimension"):
        OperatorRecordComparisonResult(
            "reference", "candidate", matrix_dimension, "eV", 1.0, 4.0, 3.0
        )


@pytest.mark.parametrize(
    "field_name, values",
    [
        ("maximum_absolute_residual", [-1.0, np.nan, np.inf, True, "1.0", 1.0 + 0.0j]),
        ("frobenius_residual", [-1.0, np.nan, np.inf, True, "1.0", 1.0 + 0.0j]),
        ("spectral_residual", [-1.0, np.nan, np.inf, True, "1.0", 1.0 + 0.0j]),
    ],
)
def test_comparison_result_requires_finite_nonnegative_real_metrics(
    field_name: str, values: list[Any]
) -> None:
    kwargs = {
        "maximum_absolute_residual": 1.0,
        "frobenius_residual": 4.0,
        "spectral_residual": 3.0,
    }
    for value in values:
        kwargs[field_name] = value
        expected_error = (
            TypeError if isinstance(value, bool | str | complex) else ValueError
        )
        with pytest.raises(expected_error, match=field_name):
            OperatorRecordComparisonResult(
                "reference",
                "candidate",
                2,
                "eV",
                kwargs["maximum_absolute_residual"],
                kwargs["frobenius_residual"],
                kwargs["spectral_residual"],
            )


@pytest.mark.parametrize(
    "maximum, frobenius, spectral, message",
    [
        (4.0, 5.0, 3.0, "maximum_absolute_residual"),
        (1.0, 2.0, 3.0, "spectral_residual"),
    ],
)
def test_comparison_result_rejects_violated_metric_inequalities(
    maximum: float, frobenius: float, spectral: float, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        OperatorRecordComparisonResult(
            "reference", "candidate", 2, "eV", maximum, frobenius, spectral
        )


def test_comparison_result_has_no_json_serialization_api() -> None:
    result = OperatorRecordComparisonResult(
        "reference", "candidate", 2, "eV", 1.0, 4.0, 3.0
    )

    assert not hasattr(result, "to_json")
    assert not hasattr(result, "to_dict")
    assert not hasattr(result, "serialize")
    assert not hasattr(OperatorRecordComparisonResult, "from_json")
    assert not hasattr(OperatorRecordComparisonResult, "from_dict")
    assert not hasattr(OperatorRecordComparisonResult, "deserialize")
