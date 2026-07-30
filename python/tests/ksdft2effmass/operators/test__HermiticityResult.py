from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import HermiticityResult


def test_public_import_constructs_hermiticity_result() -> None:
    result = HermiticityResult(residual=0.0, tolerance=1.0e-12)

    assert result.residual == 0.0
    assert result.tolerance == 1.0e-12
    assert result.is_hermitian


@pytest.mark.parametrize(
    "residual, tolerance, expected",
    [(0.0, 0.0, True), (1.0e-12, 1.0e-12, True), (2.0e-12, 1.0e-12, False)],
)
def test_is_hermitian_is_derived_from_residual_and_tolerance(
    residual: float, tolerance: float, expected: bool
) -> None:
    assert HermiticityResult(residual, tolerance).is_hermitian is expected


@pytest.mark.parametrize("value", [True, False, "0.0", 0.0 + 0.0j])
def test_residual_must_be_real_not_boolean_string_or_complex(value: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        HermiticityResult(value, 0.0)


def test_residual_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        HermiticityResult(residual=-1.0, tolerance=0.0)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_residual_must_be_finite(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        HermiticityResult(value, 0.0)


@pytest.mark.parametrize("value", [True, False, "1e-12", 0.0 + 0.0j])
def test_tolerance_must_be_real_not_boolean_string_or_complex(value: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        HermiticityResult(0.0, value)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_tolerance_must_be_finite(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        HermiticityResult(0.0, value)


def test_tolerance_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        HermiticityResult(0.0, -1.0)


def test_result_is_immutable() -> None:
    result = HermiticityResult(0.0, 1.0e-12)

    with pytest.raises(AttributeError):
        result.residual = 1.0  # type: ignore[misc]
