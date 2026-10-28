"""Tests for direct Fourier-locality result admission."""

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityConfiguration,
    Periodic1DFourierLocalityEvaluationResult,
    Periodic1DFourierLocalityMeshResult,
    Periodic1DFourierLocalityRangeResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DFourierLocalityResult:
    """Establish direct wire and strict coefficient/threshold correlation."""

    @staticmethod
    def configuration() -> Periodic1DFourierLocalityConfiguration:
        return Periodic1DFourierLocalityConfiguration(
            parent_identity=(
                "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
            ),
            onsite_numerators=(
                (-120, 6, 0, 0),
                (6, -35, 0, 0),
                (0, 0, 100, 4),
                (0, 0, 4, 175),
            ),
            positive_hopping_numerators=(
                (15, 0, 12, 0),
                (0, -10, 0, 10),
                (0, 0, 5, 0),
                (0, 0, 0, -4),
            ),
            coefficient_denominator=100,
            construction_mesh_sizes=(4, 8),
            production_construction_size=8,
            evaluation_size=3,
            evaluation_shift_numerator=1,
            evaluation_shift_denominator=3,
            maximum_ranges=(0,),
            sampled_gap_threshold=0.25,
            energy_absolute_tolerance=1.0e-12,
            relative_tolerance=1.0e-12,
            squared_energy_absolute_tolerance=1.0e-12,
            dimensionless_absolute_tolerance=1.0e-12,
            refinement_tolerance=1.0e-10,
            application_threshold=1.0e-8,
        )

    @classmethod
    def result(
        cls,
        *,
        actual_total_error: float = 0.0,
        stored_total_error: float | None = None,
    ) -> Periodic1DFourierLocalityCalculationResult:
        configuration = cls.configuration()
        unit = Unitless()
        evaluation_coordinates = VectorQuantity(
            np.asarray(
                configuration.evaluation_reduced_momenta(),
                dtype=np.float64,
            ),
            unit,
        )
        evaluation = Periodic1DFourierLocalityEvaluationResult(
            evaluation_coordinates,
            VectorQuantity(np.zeros(3, dtype=np.float64), unit),
            VectorQuantity(np.ones(3, dtype=np.float64), unit),
        )
        retained_total_error = (
            actual_total_error if stored_total_error is None else stored_total_error
        )
        candidate_energy = 0.0 if actual_total_error == 0.0 else -actual_total_error
        meshes: list[Periodic1DFourierLocalityMeshResult] = []
        for size in configuration.construction_mesh_sizes:
            construction_coordinates = VectorQuantity(
                np.asarray(
                    [-0.5 + index / size for index in range(size)],
                    dtype=np.float64,
                ),
                unit,
            )
            complete_coefficients = np.zeros(size, dtype=np.complex128)
            complete_coefficients[size // 2] = candidate_energy
            construction_candidate = VectorQuantity(
                np.full(size, candidate_energy, dtype=np.float64),
                unit,
            )
            evaluation_candidate = VectorQuantity(
                np.full(3, candidate_energy, dtype=np.float64),
                unit,
            )
            range_result = Periodic1DFourierLocalityRangeResult(
                maximum_range=0,
                mediated_coefficients=ComplexVectorQuantity(
                    np.asarray([candidate_energy], dtype=np.complex128),
                    unit,
                ),
                direct_coefficients=ComplexVectorQuantity(
                    np.asarray([candidate_energy], dtype=np.complex128),
                    unit,
                ),
                mediated_construction_candidate=construction_candidate,
                mediated_evaluation_candidate=evaluation_candidate,
                direct_construction_candidate=construction_candidate,
                direct_evaluation_candidate=evaluation_candidate,
                truncation_maximum_error=ScalarQuantity(0.0, unit),
                truncation_rms_error=ScalarQuantity(0.0, unit),
                mediated_total_maximum_error=ScalarQuantity(
                    retained_total_error,
                    unit,
                ),
                mediated_total_rms_error=ScalarQuantity(
                    actual_total_error,
                    unit,
                ),
                direct_total_maximum_error=ScalarQuantity(
                    retained_total_error,
                    unit,
                ),
                direct_total_rms_error=ScalarQuantity(actual_total_error, unit),
                omitted_coefficient_l2_norm=ScalarQuantity(0.0, unit),
                parseval_observed_squared_residual=ScalarQuantity(
                    actual_total_error**2,
                    unit,
                ),
                parseval_expected_squared_residual=ScalarQuantity(0.0, unit),
                parseval_absolute_residual=ScalarQuantity(
                    actual_total_error**2,
                    unit,
                ),
                direct_design_rank=1,
                direct_design_condition_number=1.0,
                direct_training_l2_residual=ScalarQuantity(
                    float(np.sqrt(size) * actual_total_error),
                    unit,
                ),
                direct_training_maximum_residual=ScalarQuantity(
                    actual_total_error,
                    unit,
                ),
                coefficient_l2_defect=ScalarQuantity(0.0, unit),
                sampled_l2_defect=ScalarQuantity(0.0, unit),
                sampled_maximum_defect=ScalarQuantity(0.0, unit),
                bandwidth=ScalarQuantity(0.0, unit),
                zone_center_curvature=ScalarQuantity(0.0, unit),
                maximum_imaginary_residual=ScalarQuantity(0.0, unit),
            )
            passes = actual_total_error <= configuration.application_threshold
            meshes.append(
                Periodic1DFourierLocalityMeshResult(
                    construction_size=size,
                    construction_reduced_momenta=construction_coordinates,
                    lowest_energies=VectorQuantity(
                        np.zeros(size, dtype=np.float64),
                        unit,
                    ),
                    adjacent_energies=VectorQuantity(
                        np.ones(size, dtype=np.float64),
                        unit,
                    ),
                    complete_coefficients=ComplexVectorQuantity(
                        complete_coefficients,
                        unit,
                    ),
                    reconstructed_construction=construction_candidate,
                    complete_evaluation_candidate=evaluation_candidate,
                    reconstruction_maximum_error=ScalarQuantity(
                        actual_total_error,
                        unit,
                    ),
                    hermiticity_maximum_error=ScalarQuantity(0.0, unit),
                    interpolation_maximum_error=ScalarQuantity(
                        actual_total_error,
                        unit,
                    ),
                    interpolation_rms_error=ScalarQuantity(
                        actual_total_error,
                        unit,
                    ),
                    ranges=(range_result,),
                    nondominated_mask=(True,),
                    near_tie_mask=(False,),
                    first_joint_pass=0 if passes else None,
                    sustained_after_first_pass=passes,
                )
            )
        channel_names = configuration.refinement_channel_names()
        return Periodic1DFourierLocalityCalculationResult(
            calculation_family="periodic1d-rank1-fourier-locality",
            configuration=configuration,
            evaluation=evaluation,
            meshes=tuple(meshes),
            refinement_channel_names=channel_names,
            normalized_refinement_changes=MatrixQuantity(
                np.zeros((1, len(channel_names)), dtype=np.float64),
                unit,
            ),
            refinement_coarse_first_passes=(meshes[0].first_joint_pass,),
            refinement_fine_first_passes=(meshes[1].first_joint_pass,),
            minimum_sampled_gap=ScalarQuantity(1.0, unit),
            gap_minimizing_role="construction",
            gap_minimizing_index=0,
            gap_minimizing_reduced_momentum=ScalarQuantity(-0.5, unit),
        )

    def test__json__round_trips_canonical_bytes(self) -> None:
        subject = self.result()

        reconstructed = Periodic1DFourierLocalityCalculationResult.from_json(
            subject.to_json()
        )

        assert reconstructed.to_json() == subject.to_json()

    def test__init__rejects_semantically_wrong_refinement_channel_names(self) -> None:
        subject = self.result()
        wrong_names = tuple(
            f"wrong-{index}" for index in range(len(subject.refinement_channel_names))
        )

        with pytest.raises(ValueError, match="semantic inventory"):
            replace(subject, refinement_channel_names=wrong_names)

    def test__init__rejects_malformed_quantity_before_magnitude_access(self) -> None:
        range_result = self.result().meshes[0].ranges[0]

        with pytest.raises(TypeError, match="mediated_coefficients"):
            replace(
                range_result,
                mediated_coefficients="wrong",  # type: ignore[arg-type]
            )

    def test__init__rejects_complete_coefficient_candidate_mismatch(self) -> None:
        subject = self.result()
        mesh = subject.meshes[0]
        coefficients = mesh.complete_coefficients.magnitude.copy()
        coefficients[mesh.construction_size // 2] = 1.0
        malformed_mesh = replace(
            mesh,
            complete_coefficients=ComplexVectorQuantity(
                coefficients,
                mesh.complete_coefficients.unit,
            ),
        )

        with pytest.raises(ValueError, match="complete coefficients"):
            replace(subject, meshes=(malformed_mesh, subject.meshes[1]))

    def test__init__rejects_mediated_coefficient_mismatch(self) -> None:
        subject = self.result()
        mesh = subject.meshes[0]
        range_result = mesh.ranges[0]
        malformed_range = replace(
            range_result,
            mediated_coefficients=ComplexVectorQuantity(
                np.asarray([1.0], dtype=np.complex128),
                range_result.mediated_coefficients.unit,
            ),
        )
        malformed_mesh = replace(mesh, ranges=(malformed_range,))

        with pytest.raises(ValueError, match="mediated coefficients"):
            replace(subject, meshes=(malformed_mesh, subject.meshes[1]))

    def test__init__rejects_direct_coefficient_candidate_mismatch(self) -> None:
        subject = self.result()
        mesh = subject.meshes[0]
        range_result = mesh.ranges[0]
        malformed_range = replace(
            range_result,
            direct_coefficients=ComplexVectorQuantity(
                np.asarray([1.0], dtype=np.complex128),
                range_result.direct_coefficients.unit,
            ),
        )
        malformed_mesh = replace(mesh, ranges=(malformed_range,))

        with pytest.raises(ValueError, match="direct construction candidate"):
            replace(subject, meshes=(malformed_mesh, subject.meshes[1]))

    def test__init__rejects_meshes_outside_configuration_order(self) -> None:
        subject = self.result()

        with pytest.raises(ValueError, match="configured inventory"):
            replace(subject, meshes=tuple(reversed(subject.meshes)))

    def test__init__fails_closed_when_errors_straddle_threshold(self) -> None:
        with pytest.raises(ValueError, match="reverses its threshold disposition"):
            self.result(
                actual_total_error=1.00005e-8,
                stored_total_error=9.9995e-9,
            )
