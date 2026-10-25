"""Software verification of reusable relative-error convergence analysis."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceAnalyzer,
    RelativeErrorConvergenceResult,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

pytestmark = pytest.mark.software_verification
SUT = RelativeErrorConvergenceAnalyzer


class TestRelativeErrorConvergenceAnalyzer:
    """Own multi-series relative errors and adjacent refinement orders."""

    def test_execute__quadratic_series__returns_typed_reversible_result(self) -> None:
        spacings = VectorQuantity(np.asarray([0.5, 0.25, 0.125]), Unitless())
        references = MatrixQuantity(np.ones((3, 2)), Unitless())
        approximations = MatrixQuantity(
            1.0
            + np.column_stack(
                (
                    spacings.magnitude**2,
                    2.0 * spacings.magnitude**2,
                )
            ),
            Unitless(),
        )

        result = SUT().execute(
            spacings=spacings,
            approximations=approximations,
            references=references,
            order_columns=(0, 1),
        )

        assert np.allclose(
            result.relative_errors.magnitude,
            approximations.magnitude - 1.0,
            rtol=0.0,
            atol=1.0e-15,
        )
        assert np.allclose(
            result.observed_orders.magnitude,
            2.0,
            rtol=0.0,
            atol=1.0e-14,
        )
        codec = TypedJsonValueCodec()
        decoded = codec.deserialize_bytes(codec.serialize_bytes(result))
        assert isinstance(decoded, dict)
        reconstructed = RelativeErrorConvergenceResult.from_dict(decoded)
        assert np.array_equal(
            reconstructed.relative_errors.magnitude,
            result.relative_errors.magnitude,
        )

    def test_result__nondecreasing_spacings__rejects_direct_construction(self) -> None:
        with pytest.raises(ValueError, match="strictly decreasing"):
            RelativeErrorConvergenceResult(
                spacings=VectorQuantity(np.asarray([0.25, 0.5]), Unitless()),
                relative_errors=MatrixQuantity(
                    np.asarray([[0.25], [0.125]]), Unitless()
                ),
                order_columns=(0,),
                observed_orders=MatrixQuantity(np.asarray([[1.0]]), Unitless()),
            )

    def test_result__zero_selected_error__rejects_direct_construction(self) -> None:
        with pytest.raises(ValueError, match="selected relative-error series"):
            RelativeErrorConvergenceResult(
                spacings=VectorQuantity(np.asarray([0.5, 0.25]), Unitless()),
                relative_errors=MatrixQuantity(np.asarray([[0.25], [0.0]]), Unitless()),
                order_columns=(0,),
                observed_orders=MatrixQuantity(np.asarray([[1.0]]), Unitless()),
            )

    def test_result__inconsistent_observed_orders__rejects_direct_construction(
        self,
    ) -> None:
        with pytest.raises(ValueError, match="must agree"):
            RelativeErrorConvergenceResult(
                spacings=VectorQuantity(np.asarray([0.5, 0.25]), Unitless()),
                relative_errors=MatrixQuantity(
                    np.asarray([[0.25], [0.0625]]), Unitless()
                ),
                order_columns=(0,),
                observed_orders=MatrixQuantity(np.asarray([[1.0]]), Unitless()),
            )

    def test_from_dict__nonmapping__rejects_before_field_access(self) -> None:
        with pytest.raises(TypeError, match="must be a mapping"):
            RelativeErrorConvergenceResult.from_dict([])  # type: ignore[arg-type]
