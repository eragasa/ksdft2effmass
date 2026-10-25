"""Software verification for retained model-class fit records."""

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.analysis.operators import RetainedModelClassFitResult

pytestmark = pytest.mark.software_verification
SUT = RetainedModelClassFitResult


class TestRetainedModelClassFitResult:
    """Own software evidence for the immutable analysis result."""

    def test_constructor__valid_values__retains_typed_quantities(self) -> None:
        """A named fit retains its model, residual, and norm."""
        unit = Unitless()
        fit = MatrixQuantity(np.eye(2), unit)
        residual = MatrixQuantity(np.zeros((2, 2)), unit)
        norm = ScalarQuantity(0.0, unit)

        result = SUT("real_symmetric", fit, residual, norm)

        assert result.name == "real_symmetric"
        assert result.best_fit is fit
        assert result.unexplained_residual is residual
        assert result.unexplained_frobenius_norm is norm

    def test_constructor__empty_name__raises_type_error(self) -> None:
        """Every fit result requires a nonempty model-class name."""
        unit = Unitless()

        with pytest.raises(TypeError, match="name must be a nonempty string"):
            SUT(
                "",
                MatrixQuantity(np.eye(1), unit),
                MatrixQuantity(np.zeros((1, 1)), unit),
                ScalarQuantity(0.0, unit),
            )
