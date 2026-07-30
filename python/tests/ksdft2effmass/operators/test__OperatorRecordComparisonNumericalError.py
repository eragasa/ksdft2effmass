"""Object tests for structured operator-record comparison numerical errors."""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import OperatorRecordComparisonNumericalError


def test_error_retains_structured_reason() -> None:
    error = OperatorRecordComparisonNumericalError("nonfinite_residual")

    assert error.reason == "nonfinite_residual"
    assert "nonfinite_residual" in str(error)


@pytest.mark.parametrize("reason", [1, object()])
def test_reason_must_be_string(reason: Any) -> None:
    with pytest.raises(TypeError, match="string"):
        OperatorRecordComparisonNumericalError(cast(Any, reason))


def test_reason_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="empty"):
        OperatorRecordComparisonNumericalError("")
