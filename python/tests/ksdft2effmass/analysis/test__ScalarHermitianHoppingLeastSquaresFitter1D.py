"""Tests for the explicit scalar Hermitian hopping fit."""

import numpy as np
import pytest
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.hopping_fits import (
    ScalarHermitianHoppingLeastSquaresFitter1D,
)
from ksdft2effmass.solidstate import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorSamples1D,
)


class TestScalarHermitianHoppingLeastSquaresFitter1D:
    """Establish rank-one fitting in one real Hermitian parameterization."""

    def test__execute__recovers_conjugate_scalar_hoppings(self) -> None:
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        mesh = CenteredUniformReciprocalMesh1D(period, 8)
        positive_hopping = 0.2 + 0.1j
        values = (
            0.5
            + positive_hopping * np.exp(2j * np.pi * mesh.coordinates.magnitude)
            + positive_hopping.conjugate()
            * np.exp(-2j * np.pi * mesh.coordinates.magnitude)
        )
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            period,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[value]], dtype=np.complex128),
                    unit,
                )
                for value in values
            ),
        )

        result = ScalarHermitianHoppingLeastSquaresFitter1D().execute(
            source,
            1,
            VectorQuantity(np.ones(8, dtype=np.float64), unit),
        )

        coefficients = tuple(
            block.magnitude[0, 0] for block in result.fitted_model.hopping_blocks
        )
        assert result.representatives == (-1, 0, 1)
        assert coefficients[0] == pytest.approx(positive_hopping.conjugate())
        assert coefficients[1] == pytest.approx(0.5)
        assert coefficients[2] == pytest.approx(positive_hopping)
        assert coefficients[0] == coefficients[2].conjugate()
        assert result.design_rank == 3
        assert result.is_identified
        assert result.training_maximum_frobenius_residual < 1.0e-14

    def test__execute__rejects_nonreal_scalar_source(self) -> None:
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        coordinates = VectorQuantity(
            np.asarray([-0.5, 0.0], dtype=np.float64),
            unit,
        )
        source = ReciprocalOperatorSamples1D(
            coordinates,
            period,
            (
                ComplexMatrixQuantity(
                    np.asarray([[1.0j]], dtype=np.complex128),
                    unit,
                ),
                ComplexMatrixQuantity(
                    np.asarray([[0.0]], dtype=np.complex128),
                    unit,
                ),
            ),
        )

        with pytest.raises(ValueError, match="exactly real"):
            ScalarHermitianHoppingLeastSquaresFitter1D().execute(
                source,
                0,
                VectorQuantity(np.ones(2, dtype=np.float64), unit),
            )
