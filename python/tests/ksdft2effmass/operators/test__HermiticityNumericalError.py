"""Object tests for structured Hermiticity numerical errors."""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import HermiticityNumericalError


def test_error_retains_structured_reason() -> None:
    error = HermiticityNumericalError("nonfinite_residual")

    assert error.reason == "nonfinite_residual"
    assert "nonfinite_residual" in str(error)


@pytest.mark.parametrize("reason", [1, object()])
def test_reason_must_be_string(reason: Any) -> None:
    with pytest.raises(TypeError, match="string"):
        HermiticityNumericalError(cast(Any, reason))


def test_reason_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="empty"):
        HermiticityNumericalError("")
