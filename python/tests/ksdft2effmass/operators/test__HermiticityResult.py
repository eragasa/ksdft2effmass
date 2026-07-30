"""Object tests for the unit-bearing ``HermiticityResult`` ResultObject.

The module verifies constructor typing, scalar canonicalization, immutability,
and the derived software-verification predicate.  It makes no scientific
validation claim about any Hamiltonian.
"""

from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import HermiticityResult


def make_result(
    residual: Any = 0.0, tolerance: Any = 1.0e-12, unit: Any = "eV"
) -> HermiticityResult:
    """Return a unit-bearing Hermiticity result fixture."""

    return HermiticityResult(residual=residual, tolerance=tolerance, energy_unit=unit)


def test_public_import_constructs_hermiticity_result() -> None:
    result = make_result()

    assert result.residual == 0.0
    assert result.tolerance == 1.0e-12
    assert result.energy_unit == "eV"
    assert result.is_hermitian


@pytest.mark.parametrize(
    "residual, tolerance, expected",
    [(0.0, 0.0, True), (1.0e-12, 1.0e-12, True), (2.0e-12, 1.0e-12, False)],
)
def test_is_hermitian_is_derived_from_residual_and_tolerance(
    residual: float, tolerance: float, expected: bool
) -> None:
    assert make_result(residual, tolerance).is_hermitian is expected


@pytest.mark.parametrize("value", [True, False, "0.0", 0.0 + 0.0j])
def test_residual_must_be_real_not_boolean_string_or_complex(value: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        make_result(residual=value)


def test_residual_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        make_result(residual=-1.0)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_residual_must_be_finite(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        make_result(residual=value)


@pytest.mark.parametrize("value", [True, False, "1e-12", 0.0 + 0.0j])
def test_tolerance_must_be_real_not_boolean_string_or_complex(value: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        make_result(tolerance=value)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_tolerance_must_be_finite(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        make_result(tolerance=value)


def test_tolerance_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        make_result(tolerance=-1.0)


@pytest.mark.parametrize("unit", [1, b"eV", object()])
def test_energy_unit_must_be_string(unit: Any) -> None:
    with pytest.raises(TypeError, match="string"):
        make_result(unit=unit)


def test_energy_unit_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="empty"):
        make_result(unit="")


def test_result_canonicalizes_numpy_scalars() -> None:
    result = make_result(np.float64(0.0), np.float64(1.0e-12), "eV")

    assert type(result.residual) is float
    assert type(result.tolerance) is float


def test_result_is_immutable() -> None:
    result = make_result()

    with pytest.raises(AttributeError):
        result.residual = 1.0  # type: ignore[misc]
