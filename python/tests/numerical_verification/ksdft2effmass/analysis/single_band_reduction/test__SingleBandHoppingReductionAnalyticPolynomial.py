"""Numerical verification for one analytic single-band Fourier polynomial."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionRequest1D,
    SingleBandHoppingReductionTolerances1D,
    SingleBandHoppingReductionWorkflow1D,
)
from ksdft2effmass.solidstate import CenteredUniformReciprocalMesh1D

pytestmark = pytest.mark.numerical_verification


class TestSingleBandHoppingReductionWorkflow1D:
    """Verify the Workflow against an independently stated Fourier polynomial."""

    def test_execute__recovers_known_complex_hopping_coefficients(self) -> None:
        """The complete transform and range-one routes recover analytic coefficients."""
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        mesh = CenteredUniformReciprocalMesh1D(period, 8)
        training_coordinates = mesh.coordinates.magnitude
        evaluation_coordinates = (
            np.linspace(
                -0.5,
                0.5,
                17,
                endpoint=False,
                dtype=np.float64,
            )
            + 1.0 / 9.0 / 17.0
        )

        def values(coordinates: np.ndarray) -> np.ndarray:
            return (
                1.0
                + 0.4 * np.cos(2.0 * np.pi * coordinates)
                + 0.3 * np.sin(2.0 * np.pi * coordinates)
            )

        training_target = BandSpectrumSamples1D(
            mesh.coordinates,
            period,
            MatrixQuantity(values(training_coordinates)[:, None], unit),
        )
        evaluation_target = BandSpectrumSamples1D(
            VectorQuantity(evaluation_coordinates, unit),
            period,
            MatrixQuantity(values(evaluation_coordinates)[:, None], unit),
        )
        tolerances = SingleBandHoppingReductionTolerances1D(
            coordinate_absolute=ScalarQuantity(1.0e-14, unit),
            reconstruction_absolute=ScalarQuantity(1.0e-12, unit),
            hermiticity_absolute=ScalarQuantity(1.0e-12, unit),
            parseval_absolute=ScalarQuantity(1.0e-12, unit),
            imaginary_absolute=ScalarQuantity(1.0e-12, unit),
        )
        request = SingleBandHoppingReductionRequest1D(
            training_target=training_target,
            evaluation_target=evaluation_target,
            transform_mesh=mesh,
            hopping_ranges=(0, 1),
            fitting_weights=VectorQuantity(np.ones(8, dtype=np.float64), unit),
            tolerances=tolerances,
        )

        result = SingleBandHoppingReductionWorkflow1D().execute(request)

        complete = result.complete_transform.hopping_model
        coefficients = {
            representative: block.magnitude[0, 0]
            for representative, block in zip(
                complete.representatives,
                complete.hopping_blocks,
                strict=True,
            )
        }
        assert coefficients[0] == pytest.approx(1.0, abs=1.0e-15)
        assert coefficients[-1] == pytest.approx(0.2 + 0.15j, abs=1.0e-15)
        assert coefficients[1] == pytest.approx(0.2 - 0.15j, abs=1.0e-15)
        for representative, coefficient in coefficients.items():
            if abs(representative) > 1:
                assert coefficient == pytest.approx(0.0, abs=1.0e-15)

        range_one = result.range_study[1]
        assert range_one.evaluation_error.maximum_absolute_error.magnitude < 1.0e-14
        assert range_one.route_comparison.coefficient_l2_frobenius_defect.magnitude < (
            1.0e-14
        )
        assert range_one.parseval.passes
