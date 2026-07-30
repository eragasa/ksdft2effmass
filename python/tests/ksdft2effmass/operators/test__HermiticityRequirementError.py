"""Object tests for structured Hermiticity requirement errors."""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import HermiticityRequirementError, HermiticityResult


def test_error_retains_failed_hermiticity_result() -> None:
    result = HermiticityResult(1.0, 0.0, "eV")
    error = HermiticityRequirementError(result)

    assert error.result is result
    assert "not Hermitian" in str(error)


def test_error_requires_result_object() -> None:
    with pytest.raises(TypeError, match="HermiticityResult"):
        HermiticityRequirementError(cast(Any, object()))
