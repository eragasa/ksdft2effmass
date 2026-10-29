"""Software verification for retained real-symmetric model-class fitting."""

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    Unitless,
)

from ksdft2effmass.analysis.operators import (
    RetainedModelClassFitRequest,
    RetainedModelClassFitter,
)

pytestmark = pytest.mark.software_verification
SUT = RetainedModelClassFitter


class TestRetainedModelClassFitter:
    """Own software evidence for the source-neutral fitting tool."""

    def test_method__execute__fits_declared_nested_model_classes(self) -> None:
        """The fitter returns the four declared least-Frobenius projections."""
        target = MatrixQuantity(
            np.array(
                [
                    [1.0, 2.0, 3.0],
                    [2.0, 4.0, 5.0],
                    [3.0, 5.0, 7.0],
                ]
            ),
            Unitless(),
        )

        request = RetainedModelClassFitRequest(target)
        fitter = SUT(request)

        results = fitter.execute()

        assert fitter.request is request
        assert tuple(result.name for result in results) == (
            "scalar",
            "diagonal",
            "tridiagonal",
            "real_symmetric",
        )
        np.testing.assert_allclose(results[0].best_fit.magnitude, 4.0 * np.eye(3))
        np.testing.assert_allclose(
            results[1].best_fit.magnitude, np.diag([1.0, 4.0, 7.0])
        )
        np.testing.assert_allclose(
            results[2].best_fit.magnitude,
            np.array([[1.0, 2.0, 0.0], [2.0, 4.0, 5.0], [0.0, 5.0, 7.0]]),
        )
        np.testing.assert_allclose(results[3].best_fit.magnitude, target.magnitude)
        assert results[3].unexplained_frobenius_norm.magnitude == 0.0

    def test_method__execute__rejects_nonsquare_target(self) -> None:
        """The declared real-symmetric model classes require a square target."""
        target = MatrixQuantity(np.ones((2, 3)), Unitless())

        with pytest.raises(ValueError, match="target must be square"):
            RetainedModelClassFitRequest(target)
