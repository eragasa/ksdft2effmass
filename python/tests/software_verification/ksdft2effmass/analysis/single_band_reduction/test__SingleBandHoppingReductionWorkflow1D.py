"""Software verification for reusable one-dimensional single-band reduction."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
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

pytestmark = pytest.mark.software_verification


class TestSingleBandHoppingReductionWorkflow1D:
    """Establish model-independent request, reduction, and validation behavior."""

    @staticmethod
    def target(
        coordinates: np.ndarray,
        reciprocal_period: ScalarQuantity,
        values: np.ndarray,
    ) -> BandSpectrumSamples1D:
        """Construct one supplied scalar band without a parent-model contract."""
        return BandSpectrumSamples1D(
            VectorQuantity(coordinates, reciprocal_period.unit),
            reciprocal_period,
            MatrixQuantity(values[:, None], Unitless()),
        )

    @staticmethod
    def tolerances() -> SingleBandHoppingReductionTolerances1D:
        """Return strict dimensionless numerical-consistency tolerances."""
        unit = Unitless()
        return SingleBandHoppingReductionTolerances1D(
            coordinate_absolute=ScalarQuantity(1.0e-14, unit),
            reconstruction_absolute=ScalarQuantity(1.0e-12, unit),
            hermiticity_absolute=ScalarQuantity(1.0e-12, unit),
            parseval_absolute=ScalarQuantity(1.0e-12, unit),
            imaginary_absolute=ScalarQuantity(1.0e-12, unit),
        )

    def request(
        self,
        values: np.ndarray,
        evaluation_values: np.ndarray,
        weights: np.ndarray,
    ) -> SingleBandHoppingReductionRequest1D:
        """Construct a request over supplied training and evaluation samples."""
        period = ScalarQuantity(1.0, Unitless())
        mesh = CenteredUniformReciprocalMesh1D(period, values.size)
        evaluation_coordinates = (
            np.linspace(
                -0.5,
                0.5,
                evaluation_values.size,
                endpoint=False,
                dtype=np.float64,
            )
            + 1.0 / (values.size + 1) / evaluation_values.size
        )
        return SingleBandHoppingReductionRequest1D(
            training_target=self.target(
                mesh.coordinates.magnitude,
                period,
                values,
            ),
            evaluation_target=self.target(
                evaluation_coordinates,
                period,
                evaluation_values,
            ),
            transform_mesh=mesh,
            hopping_ranges=(0, 1, 2),
            fitting_weights=VectorQuantity(weights, Unitless()),
            tolerances=self.tolerances(),
        )

    def test_execute__reduces_distinct_supplied_bands_without_a_parent_model(
        self,
    ) -> None:
        """One Workflow consumes unrelated bands through the same sample contract."""
        mesh_coordinates = np.linspace(-0.5, 0.5, 8, endpoint=False, dtype=np.float64)
        evaluation_coordinates = (
            np.linspace(-0.5, 0.5, 13, endpoint=False, dtype=np.float64)
            + 1.0 / 9.0 / 13.0
        )
        datasets = (
            (
                1.2 + 0.4 * np.cos(2.0 * np.pi * mesh_coordinates),
                1.2 + 0.4 * np.cos(2.0 * np.pi * evaluation_coordinates),
                np.ones(8, dtype=np.float64),
                1,
            ),
            (
                0.7
                - 0.25 * np.cos(2.0 * np.pi * mesh_coordinates)
                + 0.08 * np.cos(4.0 * np.pi * mesh_coordinates),
                0.7
                - 0.25 * np.cos(2.0 * np.pi * evaluation_coordinates)
                + 0.08 * np.cos(4.0 * np.pi * evaluation_coordinates),
                np.linspace(0.5, 1.5, 8, dtype=np.float64),
                2,
            ),
        )

        for training, evaluation, weights, exact_range in datasets:
            request = self.request(training, evaluation, weights)
            result = SingleBandHoppingReductionWorkflow1D().execute(request)

            assert result.request is request
            assert result.complete_transform.reconstruction_passes
            assert result.hopping_hermiticity.passes
            assert tuple(item.maximum_range for item in result.range_study) == (0, 1, 2)
            assert all(
                item.direct_fit.weights is request.fitting_weights
                for item in result.range_study
            )
            assert all(item.parseval.passes for item in result.range_study)
            exact = result.range_study[exact_range]
            assert exact.evaluation_error.maximum_absolute_error.magnitude < 1.0e-12
            assert exact.band_shape.passes

    def test_execute__retains_weighted_direct_route_distinct_from_truncation(
        self,
    ) -> None:
        """Caller-supplied weights may change the fit without changing truncation."""
        coordinates = np.linspace(-0.5, 0.5, 8, endpoint=False, dtype=np.float64)
        evaluation = np.linspace(-0.5, 0.5, 13, endpoint=False, dtype=np.float64)
        training_values = (
            1.0
            + 0.3 * np.cos(2.0 * np.pi * coordinates)
            + 0.2 * np.cos(4.0 * np.pi * coordinates)
        )
        evaluation_values = (
            1.0
            + 0.3 * np.cos(2.0 * np.pi * evaluation)
            + 0.2 * np.cos(4.0 * np.pi * evaluation)
        )
        request = self.request(
            training_values,
            evaluation_values,
            np.linspace(0.25, 2.0, 8, dtype=np.float64),
        )

        result = SingleBandHoppingReductionWorkflow1D().execute(request)

        range_one = result.range_study[1]
        assert (
            range_one.route_comparison.coefficient_l2_frobenius_defect.magnitude
            > 1.0e-6
        )
        assert range_one.direct_fit.is_identified

    def test_execute__preserves_explicit_physical_units(self) -> None:
        """The Workflow preserves explicit coordinate and energy dimensions."""
        reciprocal_unit = PhysicalUnit("1 / nanometer")
        energy_unit = PhysicalUnit("electron_volt")
        squared_energy_unit = PhysicalUnit("(electron_volt) ** 2")
        period = ScalarQuantity(2.0, reciprocal_unit)
        mesh = CenteredUniformReciprocalMesh1D(period, 8)
        normalized_training = mesh.coordinates.magnitude / period.magnitude
        evaluation_coordinates = (
            np.linspace(-1.0, 1.0, 11, endpoint=False, dtype=np.float64)
            + 1.0 / 9.0 / 11.0
        )
        normalized_evaluation = evaluation_coordinates / period.magnitude
        training = 0.8 + 0.2 * np.cos(2.0 * np.pi * normalized_training)
        evaluation = 0.8 + 0.2 * np.cos(2.0 * np.pi * normalized_evaluation)
        request = SingleBandHoppingReductionRequest1D(
            training_target=BandSpectrumSamples1D(
                mesh.coordinates,
                period,
                MatrixQuantity(training[:, None], energy_unit),
            ),
            evaluation_target=BandSpectrumSamples1D(
                VectorQuantity(evaluation_coordinates, reciprocal_unit),
                period,
                MatrixQuantity(evaluation[:, None], energy_unit),
            ),
            transform_mesh=mesh,
            hopping_ranges=(0, 1),
            fitting_weights=VectorQuantity(np.ones(8, dtype=np.float64), Unitless()),
            tolerances=SingleBandHoppingReductionTolerances1D(
                coordinate_absolute=ScalarQuantity(1.0e-14, reciprocal_unit),
                reconstruction_absolute=ScalarQuantity(1.0e-12, energy_unit),
                hermiticity_absolute=ScalarQuantity(1.0e-12, energy_unit),
                parseval_absolute=ScalarQuantity(1.0e-12, squared_energy_unit),
                imaginary_absolute=ScalarQuantity(1.0e-12, energy_unit),
            ),
        )

        result = SingleBandHoppingReductionWorkflow1D().execute(request)

        assert result.complete_transform.hopping_model.hopping_blocks[0].unit == (
            energy_unit
        )
        assert result.range_study[1].evaluation_error.maximum_absolute_error.unit == (
            energy_unit
        )
        assert (
            result.range_study[1].evaluation_error.maximum_absolute_error.magnitude
            < 1.0e-12
        )

    def test_request__rejects_multiple_bands(self) -> None:
        """The reusable Workflow cannot silently select a band for the caller."""
        period = ScalarQuantity(1.0, Unitless())
        mesh = CenteredUniformReciprocalMesh1D(period, 8)
        multiple = BandSpectrumSamples1D(
            mesh.coordinates,
            period,
            MatrixQuantity(
                np.column_stack(
                    (
                        np.zeros(8, dtype=np.float64),
                        np.ones(8, dtype=np.float64),
                    )
                ),
                Unitless(),
            ),
        )
        single = self.target(
            mesh.coordinates.magnitude,
            period,
            np.zeros(8, dtype=np.float64),
        )

        with pytest.raises(ValueError, match="exactly one band"):
            SingleBandHoppingReductionRequest1D(
                training_target=multiple,
                evaluation_target=single,
                transform_mesh=mesh,
                hopping_ranges=(0, 1),
                fitting_weights=VectorQuantity(
                    np.ones(8, dtype=np.float64), Unitless()
                ),
                tolerances=self.tolerances(),
            )

    def test_request__rejects_boolean_range_control(self) -> None:
        """A Boolean cannot masquerade as an exact hopping range."""
        values = np.ones(8, dtype=np.float64)
        request = self.request(values, np.ones(13, dtype=np.float64), values)

        with pytest.raises(TypeError, match="built-in integers"):
            SingleBandHoppingReductionRequest1D(
                training_target=request.training_target,
                evaluation_target=request.evaluation_target,
                transform_mesh=request.transform_mesh,
                hopping_ranges=(False,),
                fitting_weights=request.fitting_weights,
                tolerances=request.tolerances,
            )
